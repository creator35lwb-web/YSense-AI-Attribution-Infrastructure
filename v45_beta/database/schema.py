"""
YSenseAI v4.5-Beta: Database Schema
SQLite database for data vault, users, and submissions
"""

import sqlite3
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict
import json


# Password hashing: salted scrypt (stdlib, no extra dependency).
# Legacy rows created before this change hold a bare SHA-256 hex digest;
# they still verify and are transparently upgraded on next login.
_SCRYPT_N, _SCRYPT_R, _SCRYPT_P = 2 ** 14, 8, 1


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P
    )
    return f"scrypt${_SCRYPT_N}${_SCRYPT_R}${_SCRYPT_P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    if stored.startswith("scrypt$"):
        try:
            _, n, r, p, salt_hex, digest_hex = stored.split("$")
            digest = hashlib.scrypt(
                password.encode("utf-8"),
                salt=bytes.fromhex(salt_hex),
                n=int(n), r=int(r), p=int(p),
            )
            return hmac.compare_digest(digest.hex(), digest_hex)
        except (ValueError, TypeError):
            return False
    # Legacy unsalted SHA-256
    legacy = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy, stored)


class YSenseDatabase:
    """
    Main database class for YSenseAI platform
    """
    
    def __init__(self, db_path: str = "database/ysense_production.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            username TEXT,
            created_at TEXT NOT NULL,
            last_login TEXT,
            is_active BOOLEAN DEFAULT 1
        )
        """)
        
        # Submissions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            asset_id TEXT UNIQUE NOT NULL,
            author_did TEXT NOT NULL,
            raw_story TEXT NOT NULL,
            extracted_layers TEXT NOT NULL,
            distilled_essence TEXT NOT NULL,
            chat_history TEXT,
            consent_tier TEXT NOT NULL,
            revenue_share TEXT NOT NULL,
            quality_scores TEXT NOT NULL,
            fingerprint TEXT NOT NULL,
            signature TEXT NOT NULL,
            training_ready BOOLEAN DEFAULT 0,
            is_public BOOLEAN DEFAULT 0,
            share_token TEXT UNIQUE,
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Sessions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Analytics table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            event_data TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        
        # Consent records (Z-Protocol audit trail: one row per grant or revocation)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            consent_type TEXT NOT NULL,
            granted BOOLEAN NOT NULL,
            document_version TEXT,
            metadata TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_consents_user_id ON consents(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_submissions_user_id ON submissions(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_submissions_created_at ON submissions(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(session_token)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)")
        
        conn.commit()

    # User Management

    def create_user(self, email: str, password: str, username: str = None) -> Optional[int]:
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO users (email, password_hash, username, created_at)
            VALUES (?, ?, ?, ?)
            """, (email, hash_password(password), username, datetime.utcnow().isoformat()))

            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None  # User already exists

    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, email, username, created_at, password_hash
        FROM users
        WHERE email = ? AND is_active = 1
        """, (email,))

        row = cursor.fetchone()
        if row and verify_password(password, row['password_hash']):
            now = datetime.utcnow().isoformat()
            if not row['password_hash'].startswith("scrypt$"):
                # Upgrade legacy unsalted hash in place
                cursor.execute("UPDATE users SET password_hash = ?, last_login = ? WHERE id = ?",
                               (hash_password(password), now, row['id']))
            else:
                cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, row['id']))
            conn.commit()

            user = dict(row)
            user.pop('password_hash', None)
            return user
        return None

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email (no password hash returned)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, email, username, created_at, last_login
        FROM users WHERE email = ? AND is_active = 1
        """, (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def delete_user(self, user_id: int) -> Dict:
        """Delete a user and everything they own (GDPR / PDPA erasure).

        Consent rows are kept but anonymised (user_id set to 0) so the
        audit trail can show that consent existed and was withdrawn.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        counts = {}
        for table in ("submissions", "sessions", "analytics"):
            cursor.execute(f"DELETE FROM {table} WHERE user_id = ?", (user_id,))
            counts[table] = cursor.rowcount
        cursor.execute("""
        INSERT INTO consents (user_id, consent_type, granted, document_version, metadata, created_at)
        VALUES (?, 'account_deletion', 1, NULL, NULL, ?)
        """, (user_id, datetime.utcnow().isoformat()))
        cursor.execute("UPDATE consents SET user_id = 0 WHERE user_id = ?", (user_id,))
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        counts["users"] = cursor.rowcount
        conn.commit()
        return counts

    # Consent Management

    def record_consent(self, user_id: int, consent_type: str, granted: bool,
                       document_version: str = None, metadata: Dict = None) -> int:
        """Append a consent grant or revocation to the audit trail"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO consents (user_id, consent_type, granted, document_version, metadata, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, consent_type, bool(granted), document_version,
              json.dumps(metadata) if metadata else None, datetime.utcnow().isoformat()))
        conn.commit()
        return cursor.lastrowid

    def get_user_consents(self, user_id: int) -> List[Dict]:
        """Full consent history for a user, newest first"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, consent_type, granted, document_version, metadata, created_at
        FROM consents WHERE user_id = ? ORDER BY created_at DESC, id DESC
        """, (user_id,))
        rows = []
        for row in cursor.fetchall():
            item = dict(row)
            item['granted'] = bool(item['granted'])
            item['metadata'] = json.loads(item['metadata']) if item['metadata'] else {}
            rows.append(item)
        return rows

    def has_consent(self, user_id: int, consent_type: str) -> bool:
        """True if the most recent record of this type is a grant"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT granted FROM consents WHERE user_id = ? AND consent_type = ?
        ORDER BY created_at DESC, id DESC LIMIT 1
        """, (user_id, consent_type))
        row = cursor.fetchone()
        return bool(row['granted']) if row else False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, email, username, created_at, last_login
        FROM users
        WHERE id = ? AND is_active = 1
        """, (user_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    # Session Management
    
    def create_session(self, user_id: int, expires_hours: int = 24) -> str:
        """Create new session token"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO sessions (user_id, session_token, expires_at, created_at)
        VALUES (?, ?, ?, ?)
        """, (user_id, session_token, expires_at.isoformat(), datetime.utcnow().isoformat()))
        
        conn.commit()
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[int]:
        """Validate session and return user_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT user_id, expires_at
        FROM sessions
        WHERE session_token = ?
        """, (session_token,))
        
        row = cursor.fetchone()
        if row:
            expires_at = datetime.fromisoformat(row['expires_at'])
            if expires_at > datetime.utcnow():
                return row['user_id']
        return None
    
    def delete_session(self, session_token: str):
        """Delete session (logout)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM sessions WHERE session_token = ?", (session_token,))
        conn.commit()
    
    # Submission Management
    
    def create_submission(self, user_id: int, attribution_data: Dict) -> int:
        """Create new wisdom submission"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate share token
        share_token = secrets.token_urlsafe(16)

        # AttributionEngine.create_wisdom_asset() emits "layers"; older callers
        # passed "layer_responses". Accept both so the save path cannot KeyError.
        layers = attribution_data.get('layer_responses', attribution_data.get('layers', {}))

        cursor.execute("""
        INSERT INTO submissions (
            user_id, asset_id, author_did, raw_story, extracted_layers,
            distilled_essence, chat_history, consent_tier, revenue_share,
            quality_scores, fingerprint, signature, training_ready,
            is_public, share_token, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            attribution_data['asset_id'],
            attribution_data['author_did'],
            attribution_data['raw_story'],
            json.dumps(layers),
            json.dumps(attribution_data['distilled_essence']),
            json.dumps(attribution_data.get('distillation_dialogue', [])),
            attribution_data['consent_tier'],
            attribution_data['revenue_share'],
            json.dumps(attribution_data['quality_scores']),
            attribution_data['fingerprint'],
            attribution_data['signature'],
            attribution_data['training_ready'],
            False,  # is_public
            share_token,
            attribution_data['created_at']
        ))
        
        conn.commit()
        return cursor.lastrowid
    
    def get_user_submissions(self, user_id: int, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all submissions for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM submissions
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
        """, (user_id, limit, offset))
        
        rows = cursor.fetchall()
        submissions = []
        
        for row in rows:
            submission = dict(row)
            # Parse JSON fields
            submission['extracted_layers'] = json.loads(submission['extracted_layers'])
            submission['distilled_essence'] = json.loads(submission['distilled_essence'])
            submission['chat_history'] = json.loads(submission['chat_history']) if submission['chat_history'] else []
            submission['quality_scores'] = json.loads(submission['quality_scores'])
            submissions.append(submission)
        
        return submissions
    
    def get_submission_by_id(self, submission_id: int, user_id: int = None) -> Optional[Dict]:
        """Get single submission by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("SELECT * FROM submissions WHERE id = ? AND user_id = ?", (submission_id, user_id))
        else:
            cursor.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,))
        
        row = cursor.fetchone()
        if row:
            submission = dict(row)
            submission['extracted_layers'] = json.loads(submission['extracted_layers'])
            submission['distilled_essence'] = json.loads(submission['distilled_essence'])
            submission['chat_history'] = json.loads(submission['chat_history']) if submission['chat_history'] else []
            submission['quality_scores'] = json.loads(submission['quality_scores'])
            return submission
        return None
    
    def get_submission_by_share_token(self, share_token: str) -> Optional[Dict]:
        """Get submission by public share token"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM submissions
        WHERE share_token = ? AND is_public = 1
        """, (share_token,))
        
        row = cursor.fetchone()
        if row:
            submission = dict(row)
            submission['extracted_layers'] = json.loads(submission['extracted_layers'])
            submission['distilled_essence'] = json.loads(submission['distilled_essence'])
            submission['chat_history'] = json.loads(submission['chat_history']) if submission['chat_history'] else []
            submission['quality_scores'] = json.loads(submission['quality_scores'])
            return submission
        return None
    
    def update_submission_visibility(self, submission_id: int, user_id: int, is_public: bool):
        """Update submission public/private status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        UPDATE submissions
        SET is_public = ?, updated_at = ?
        WHERE id = ? AND user_id = ?
        """, (is_public, datetime.utcnow().isoformat(), submission_id, user_id))
        
        conn.commit()
    
    def delete_submission(self, submission_id: int, user_id: int):
        """Delete submission"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        DELETE FROM submissions
        WHERE id = ? AND user_id = ?
        """, (submission_id, user_id))
        
        conn.commit()
    
    def search_submissions(self, user_id: int, query: str) -> List[Dict]:
        """Search submissions by content"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        search_pattern = f"%{query}%"
        cursor.execute("""
        SELECT * FROM submissions
        WHERE user_id = ? AND (
            raw_story LIKE ? OR
            extracted_layers LIKE ? OR
            distilled_essence LIKE ?
        )
        ORDER BY created_at DESC
        """, (user_id, search_pattern, search_pattern, search_pattern))
        
        rows = cursor.fetchall()
        submissions = []
        
        for row in rows:
            submission = dict(row)
            submission['extracted_layers'] = json.loads(submission['extracted_layers'])
            submission['distilled_essence'] = json.loads(submission['distilled_essence'])
            submission['chat_history'] = json.loads(submission['chat_history']) if submission['chat_history'] else []
            submission['quality_scores'] = json.loads(submission['quality_scores'])
            submissions.append(submission)
        
        return submissions
    
    # Analytics
    
    def get_user_stats(self, user_id: int) -> Dict:
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            COUNT(*) as total_submissions,
            SUM(CASE WHEN training_ready = 1 THEN 1 ELSE 0 END) as training_ready_count,
            AVG(json_extract(quality_scores, '$.overall')) as avg_quality_score
        FROM submissions
        WHERE user_id = ?
        """, (user_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else {}
    
    def log_event(self, user_id: int, event_type: str, event_data: Dict = None):
        """Log analytics event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO analytics (user_id, event_type, event_data, created_at)
        VALUES (?, ?, ?, ?)
        """, (user_id, event_type, json.dumps(event_data) if event_data else None, datetime.utcnow().isoformat()))
        
        conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


# Test database
def test_database():
    """Test database functionality"""
    print("🧪 Testing YSenseAI Database")
    print("=" * 60)
    
    # Initialize database
    db = YSenseDatabase("database/test_ysense.db")
    
    # Test user creation
    print("\n[1/5] Testing user creation...")
    user_id = db.create_user("test@ysenseai.org", "password123", "TestUser")
    if user_id:
        print(f"✅ User created: ID {user_id}")
    else:
        print("⚠️ User already exists")
        user_id = 1
    
    # Test authentication
    print("\n[2/5] Testing authentication...")
    user = db.authenticate_user("test@ysenseai.org", "password123")
    if user:
        print(f"✅ Authentication successful: {user['email']}")
    else:
        print("❌ Authentication failed")
    
    # Test session
    print("\n[3/5] Testing session management...")
    session_token = db.create_session(user_id)
    print(f"✅ Session created: {session_token[:16]}...")
    
    validated_user_id = db.validate_session(session_token)
    if validated_user_id == user_id:
        print(f"✅ Session validated for user {validated_user_id}")
    
    # Test submission
    print("\n[4/5] Testing submission creation...")
    mock_attribution = {
        "asset_id": "ysense-test001",
        "author_did": "did:ysense:test001",
        "raw_story": "Test story",
        "layer_responses": {"narrative": "test"},
        "distilled_essence": ["Test", "Words", "Here"],
        "distillation_dialogue": [],
        "consent_tier": "tier1",
        "revenue_share": "15%",
        "quality_scores": {"overall": 0.85},
        "fingerprint": "abc123",
        "signature": "sig123",
        "training_ready": True,
        "created_at": datetime.utcnow().isoformat()
    }
    
    submission_id = db.create_submission(user_id, mock_attribution)
    print(f"✅ Submission created: ID {submission_id}")
    
    # Test retrieval
    print("\n[5/5] Testing submission retrieval...")
    submissions = db.get_user_submissions(user_id)
    print(f"✅ Retrieved {len(submissions)} submissions")
    
    if submissions:
        print(f"   - Asset ID: {submissions[0]['asset_id']}")
        print(f"   - Essence: {'. '.join(submissions[0]['distilled_essence'])}")
    
    # Stats
    stats = db.get_user_stats(user_id)
    print(f"\n📊 User Stats:")
    print(f"   - Total: {stats.get('total_submissions', 0)}")
    print(f"   - Training Ready: {stats.get('training_ready_count', 0)}")
    print(f"   - Avg Quality: {stats.get('avg_quality_score', 0):.3f}")
    
    print("\n✅ Database test complete!")
    db.close()


if __name__ == "__main__":
    test_database()
