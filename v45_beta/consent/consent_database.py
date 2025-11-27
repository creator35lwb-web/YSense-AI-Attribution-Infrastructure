# src/consent_database.py
"""
YSense™ Platform v4.1 - Consent & ToS Database Schema
Z Protocol v2.0 Compliant - Privacy-First Architecture
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

class ConsentDatabase:
    """Manages consent and ToS acceptance database"""

    def __init__(self, db_path: str = "database/ysense_v41.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._initialize_consent_tables()

    def _initialize_consent_tables(self):
        """Create consent management tables"""

        with sqlite3.connect(self.db_path) as conn:
            # Terms of Service Acceptance Table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tos_acceptance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    tos_version TEXT NOT NULL,
                    z_protocol_version TEXT NOT NULL DEFAULT '2.0',
                    accepted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT,
                    user_agent TEXT,
                    crypto_signature TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')

            # Consent Records Table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS consent_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    consent_type TEXT NOT NULL,
                    granted BOOLEAN NOT NULL,
                    granted_at TIMESTAMP,
                    revoked_at TIMESTAMP,
                    wisdom_id TEXT,
                    content_tier TEXT,
                    revenue_share_percentage REAL,
                    metadata TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')

            # Content Tier Classification Table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS content_tiers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wisdom_id TEXT NOT NULL UNIQUE,
                    user_id TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    revenue_share REAL NOT NULL,
                    requires_community_approval BOOLEAN DEFAULT 0,
                    community_approved BOOLEAN DEFAULT 0,
                    ai_training_enabled BOOLEAN DEFAULT 0,
                    public_sharing_enabled BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops(id)
                )
            ''')

            # Data Deletion Requests Table (GDPR Compliance)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS deletion_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    deadline_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    status TEXT NOT NULL DEFAULT 'pending',
                    crypto_signature TEXT NOT NULL,
                    data_types TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')

            # Revenue Transparency Table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS revenue_transparency (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period TEXT NOT NULL,
                    total_revenue REAL NOT NULL DEFAULT 0,
                    total_contributors INTEGER NOT NULL DEFAULT 0,
                    public_tier_revenue REAL DEFAULT 0,
                    personal_tier_revenue REAL DEFAULT 0,
                    cultural_tier_revenue REAL DEFAULT 0,
                    sacred_tier_revenue REAL DEFAULT 0,
                    therapeutic_tier_revenue REAL DEFAULT 0,
                    community_fund_total REAL DEFAULT 0,
                    research_fund_total REAL DEFAULT 0,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # User Revenue Dashboard Table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_revenue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    wisdom_id TEXT NOT NULL,
                    period TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    revenue_earned REAL NOT NULL DEFAULT 0,
                    revenue_share_percentage REAL NOT NULL,
                    payout_status TEXT DEFAULT 'pending',
                    payout_date TIMESTAMP,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (wisdom_id) REFERENCES wisdom_drops(id)
                )
            ''')

            # Create indexes for performance
            conn.execute('CREATE INDEX IF NOT EXISTS idx_consent_user ON consent_records(user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_consent_type ON consent_records(consent_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_consent_wisdom ON consent_records(wisdom_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_tos_user ON tos_acceptance(user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_tier_wisdom ON content_tiers(wisdom_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_revenue_user ON user_revenue(user_id)')

            conn.commit()
            self.logger.info("Consent management tables initialized successfully")

    def record_tos_acceptance(
        self,
        user_id: str,
        tos_version: str,
        ip_address: str,
        user_agent: str,
        crypto_signature: str
    ) -> int:
        """Record Terms of Service acceptance"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO tos_acceptance (
                    user_id, tos_version, z_protocol_version,
                    ip_address, user_agent, crypto_signature
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, tos_version, '2.0', ip_address, user_agent, crypto_signature))

            conn.commit()
            return cursor.lastrowid

    def check_tos_acceptance(self, user_id: str, tos_version: str = "1.0.0") -> bool:
        """Check if user has accepted current ToS version"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT COUNT(*) FROM tos_acceptance
                WHERE user_id = ? AND tos_version = ?
            ''', (user_id, tos_version))

            count = cursor.fetchone()[0]
            return count > 0

    def record_consent(
        self,
        user_id: str,
        consent_type: str,
        granted: bool,
        wisdom_id: Optional[str] = None,
        content_tier: Optional[str] = None,
        revenue_share: Optional[float] = None,
        metadata: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> int:
        """Record a consent decision"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO consent_records (
                    user_id, consent_type, granted,
                    granted_at, revoked_at, wisdom_id, content_tier,
                    revenue_share_percentage, metadata,
                    ip_address, user_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                consent_type,
                granted,
                datetime.now() if granted else None,
                None if granted else datetime.now(),
                wisdom_id,
                content_tier,
                revenue_share,
                json.dumps(metadata or {}),
                ip_address,
                user_agent
            ))

            conn.commit()
            return cursor.lastrowid

    def get_user_consents(self, user_id: str) -> List[Dict]:
        """Get all consents for a user"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM consent_records
                WHERE user_id = ?
                ORDER BY granted_at DESC
            ''', (user_id,))

            return [dict(row) for row in cursor.fetchall()]

    def set_content_tier(
        self,
        wisdom_id: str,
        user_id: str,
        tier: str,
        revenue_share: float,
        ai_training: bool = False,
        public_sharing: bool = False,
        requires_community: bool = False
    ) -> int:
        """Set content tier for a wisdom submission"""

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO content_tiers (
                    wisdom_id, user_id, tier, revenue_share,
                    requires_community_approval, ai_training_enabled,
                    public_sharing_enabled
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (wisdom_id, user_id, tier, revenue_share,
                  requires_community, ai_training, public_sharing))

            conn.commit()
            return cursor.lastrowid

    def request_data_deletion(
        self,
        user_id: str,
        crypto_signature: str,
        data_types: List[str]
    ) -> int:
        """Request data deletion (72-hour GDPR compliance)"""

        deadline = datetime.now().timestamp() + (72 * 3600)  # 72 hours

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO deletion_requests (
                    user_id, deadline_at, crypto_signature, data_types
                ) VALUES (?, ?, ?, ?)
            ''', (user_id, datetime.fromtimestamp(deadline),
                  crypto_signature, json.dumps(data_types)))

            conn.commit()
            return cursor.lastrowid

    def update_revenue_transparency(
        self,
        period: str,
        tier_revenues: Dict[str, float],
        total_contributors: int
    ):
        """Update public revenue transparency data"""

        total_revenue = sum(tier_revenues.values())

        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO revenue_transparency (
                    period, total_revenue, total_contributors,
                    public_tier_revenue, personal_tier_revenue,
                    cultural_tier_revenue, sacred_tier_revenue,
                    therapeutic_tier_revenue
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                period,
                total_revenue,
                total_contributors,
                tier_revenues.get('public', 0),
                tier_revenues.get('personal', 0),
                tier_revenues.get('cultural', 0),
                tier_revenues.get('sacred', 0),
                tier_revenues.get('therapeutic', 0)
            ))

            conn.commit()

    def get_public_revenue_dashboard(self, period: Optional[str] = None) -> Dict:
        """Get public revenue transparency data"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            if period:
                cursor = conn.execute('''
                    SELECT * FROM revenue_transparency
                    WHERE period = ?
                ''', (period,))
            else:
                cursor = conn.execute('''
                    SELECT * FROM revenue_transparency
                    ORDER BY created_at DESC LIMIT 1
                ''')

            row = cursor.fetchone()

            if row:
                return dict(row)
            return {}

    def get_user_revenue_dashboard(self, user_id: str) -> Dict:
        """Get user-specific revenue dashboard"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row

            # Total earnings
            cursor = conn.execute('''
                SELECT SUM(revenue_earned) as total_earned,
                       COUNT(*) as total_submissions
                FROM user_revenue
                WHERE user_id = ?
            ''', (user_id,))

            totals = dict(cursor.fetchone())

            # By tier
            cursor = conn.execute('''
                SELECT tier, SUM(revenue_earned) as tier_revenue,
                       COUNT(*) as tier_count
                FROM user_revenue
                WHERE user_id = ?
                GROUP BY tier
            ''', (user_id,))

            by_tier = [dict(row) for row in cursor.fetchall()]

            # Recent earnings
            cursor = conn.execute('''
                SELECT * FROM user_revenue
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT 10
            ''', (user_id,))

            recent = [dict(row) for row in cursor.fetchall()]

            return {
                "total_earned": totals.get('total_earned', 0) or 0,
                "total_submissions": totals.get('total_submissions', 0) or 0,
                "by_tier": by_tier,
                "recent_earnings": recent
            }

# Global instance
consent_db = ConsentDatabase()
