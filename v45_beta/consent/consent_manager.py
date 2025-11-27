# src/consent_manager.py
"""
YSense™ Platform v4.1 - Consent Management System
Z Protocol v2.0 Compliant - Privacy-First Architecture
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from sqlalchemy.orm import Session

from .database import ConsentRecord, User, WisdomSubmission
from .config import settings

class ConsentType(Enum):
    """Types of consent tracking"""
    ACCOUNT_CREATION = "account_creation"
    WISDOM_STORAGE = "wisdom_storage"
    AI_TRAINING = "ai_training"
    PUBLIC_SHARING = "public_sharing"
    CULTURAL_COMMUNITY = "cultural_community"
    REVENUE_SHARING = "revenue_sharing"
    RESEARCH_USE = "research_use"
    ANONYMIZED_ANALYTICS = "anonymized_analytics"

class ContentTier(Enum):
    """Z Protocol v2.0 Content Tiers"""
    PUBLIC = "public"  # 15% revenue
    PERSONAL = "personal"  # 20% revenue
    CULTURAL = "cultural"  # 25% + community fund
    SACRED = "sacred"  # 30% + community fund
    THERAPEUTIC = "therapeutic"  # 25% + research fund

TIER_REVENUE_SHARE = {
    ContentTier.PUBLIC: 0.15,
    ContentTier.PERSONAL: 0.20,
    ContentTier.CULTURAL: 0.25,
    ContentTier.SACRED: 0.30,
    ContentTier.THERAPEUTIC: 0.25
}

class ConsentManager:
    """Manages all user consent with Z Protocol v2.0 compliance"""

    def __init__(self, db: Session):
        self.db = db

    def create_consent_record(
        self,
        user_id: str,
        consent_type: ConsentType,
        granted: bool,
        metadata: Optional[Dict] = None
    ) -> ConsentRecord:
        """Create a new consent record with timestamp"""

        consent = ConsentRecord(
            user_id=user_id,
            consent_type=consent_type.value,
            granted=granted,
            granted_at=datetime.now() if granted else None,
            revoked_at=None if granted else datetime.now(),
            metadata=json.dumps(metadata or {}),
            ip_address=metadata.get("ip_address") if metadata else None,
            user_agent=metadata.get("user_agent") if metadata else None
        )

        self.db.add(consent)
        self.db.commit()
        self.db.refresh(consent)

        return consent

    def grant_consent(
        self,
        user_id: str,
        consent_type: ConsentType,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Grant a specific consent"""

        # Check if consent already exists
        existing = self.get_active_consent(user_id, consent_type)

        if existing and existing.granted:
            return {
                "status": "already_granted",
                "consent_id": existing.id,
                "granted_at": existing.granted_at.isoformat()
            }

        # Create new consent record
        consent = self.create_consent_record(
            user_id=user_id,
            consent_type=consent_type,
            granted=True,
            metadata=metadata
        )

        return {
            "status": "granted",
            "consent_id": consent.id,
            "granted_at": consent.granted_at.isoformat(),
            "type": consent_type.value
        }

    def revoke_consent(
        self,
        user_id: str,
        consent_type: ConsentType,
        reason: Optional[str] = None
    ) -> Dict:
        """Revoke a specific consent"""

        # Get active consent
        consent = self.get_active_consent(user_id, consent_type)

        if not consent or not consent.granted:
            return {
                "status": "not_found",
                "message": "No active consent to revoke"
            }

        # Update consent record
        consent.granted = False
        consent.revoked_at = datetime.now()

        if reason:
            metadata = json.loads(consent.metadata or "{}")
            metadata["revocation_reason"] = reason
            consent.metadata = json.dumps(metadata)

        self.db.commit()

        return {
            "status": "revoked",
            "consent_id": consent.id,
            "revoked_at": consent.revoked_at.isoformat(),
            "type": consent_type.value
        }

    def get_active_consent(
        self,
        user_id: str,
        consent_type: ConsentType
    ) -> Optional[ConsentRecord]:
        """Get the most recent active consent for a type"""

        return self.db.query(ConsentRecord).filter(
            ConsentRecord.user_id == user_id,
            ConsentRecord.consent_type == consent_type.value,
            ConsentRecord.granted == True
        ).order_by(ConsentRecord.granted_at.desc()).first()

    def get_all_user_consents(self, user_id: str) -> List[Dict]:
        """Get all consents for a user (for dashboard)"""

        consents = self.db.query(ConsentRecord).filter(
            ConsentRecord.user_id == user_id
        ).order_by(ConsentRecord.granted_at.desc()).all()

        return [
            {
                "id": c.id,
                "type": c.consent_type,
                "granted": c.granted,
                "granted_at": c.granted_at.isoformat() if c.granted_at else None,
                "revoked_at": c.revoked_at.isoformat() if c.revoked_at else None,
                "metadata": json.loads(c.metadata or "{}")
            }
            for c in consents
        ]

    def check_consent(
        self,
        user_id: str,
        consent_type: ConsentType
    ) -> bool:
        """Check if user has granted a specific consent"""

        consent = self.get_active_consent(user_id, consent_type)
        return consent is not None and consent.granted

    def register_wisdom_consent(
        self,
        user_id: str,
        wisdom_id: str,
        content_tier: ContentTier,
        ai_training: bool = False,
        public_sharing: bool = False,
        cultural_community: bool = False
    ) -> Dict:
        """Register complete consent for a wisdom submission"""

        consents_granted = []

        # Always require wisdom storage consent
        storage_consent = self.grant_consent(
            user_id=user_id,
            consent_type=ConsentType.WISDOM_STORAGE,
            metadata={
                "wisdom_id": wisdom_id,
                "content_tier": content_tier.value
            }
        )
        consents_granted.append(storage_consent)

        # AI Training consent (optional)
        if ai_training:
            ai_consent = self.grant_consent(
                user_id=user_id,
                consent_type=ConsentType.AI_TRAINING,
                metadata={
                    "wisdom_id": wisdom_id,
                    "content_tier": content_tier.value,
                    "revenue_share": TIER_REVENUE_SHARE[content_tier]
                }
            )
            consents_granted.append(ai_consent)

        # Public sharing consent (optional)
        if public_sharing:
            public_consent = self.grant_consent(
                user_id=user_id,
                consent_type=ConsentType.PUBLIC_SHARING,
                metadata={
                    "wisdom_id": wisdom_id,
                    "content_tier": content_tier.value
                }
            )
            consents_granted.append(public_consent)

        # Cultural community consent (for Cultural/Sacred tiers)
        if cultural_community and content_tier in [ContentTier.CULTURAL, ContentTier.SACRED]:
            cultural_consent = self.grant_consent(
                user_id=user_id,
                consent_type=ConsentType.CULTURAL_COMMUNITY,
                metadata={
                    "wisdom_id": wisdom_id,
                    "content_tier": content_tier.value,
                    "requires_community_approval": True
                }
            )
            consents_granted.append(cultural_consent)

        # Revenue sharing consent (always for AI training)
        if ai_training:
            revenue_consent = self.grant_consent(
                user_id=user_id,
                consent_type=ConsentType.REVENUE_SHARING,
                metadata={
                    "wisdom_id": wisdom_id,
                    "content_tier": content_tier.value,
                    "revenue_share_percentage": TIER_REVENUE_SHARE[content_tier] * 100
                }
            )
            consents_granted.append(revenue_consent)

        return {
            "status": "success",
            "wisdom_id": wisdom_id,
            "content_tier": content_tier.value,
            "consents_granted": consents_granted,
            "total_consents": len(consents_granted)
        }

    def get_wisdom_consents(self, wisdom_id: str) -> Dict:
        """Get all consents for a specific wisdom submission"""

        consents = self.db.query(ConsentRecord).filter(
            ConsentRecord.metadata.like(f'%"wisdom_id": "{wisdom_id}"%')
        ).all()

        return {
            "wisdom_id": wisdom_id,
            "consents": [
                {
                    "type": c.consent_type,
                    "granted": c.granted,
                    "granted_at": c.granted_at.isoformat() if c.granted_at else None
                }
                for c in consents
            ]
        }

    def export_user_consent_history(self, user_id: str) -> Dict:
        """Export complete consent history for GDPR compliance"""

        consents = self.get_all_user_consents(user_id)

        return {
            "user_id": user_id,
            "export_date": datetime.now().isoformat(),
            "total_consents": len(consents),
            "consents": consents,
            "z_protocol_version": "2.0",
            "compliance": ["GDPR", "Malaysia PDPA", "Singapore PDPA"]
        }

    def delete_user_consents(
        self,
        user_id: str,
        verification_signature: str
    ) -> Dict:
        """Delete all user consents (72-hour GDPR compliance)"""

        # Verify user signature (crypto key verification)
        # TODO: Implement crypto verification

        # Get all consents
        consents = self.db.query(ConsentRecord).filter(
            ConsentRecord.user_id == user_id
        ).all()

        consent_count = len(consents)

        # Mark for deletion (actual deletion happens in background job)
        for consent in consents:
            metadata = json.loads(consent.metadata or "{}")
            metadata["deletion_requested_at"] = datetime.now().isoformat()
            metadata["deletion_deadline"] = (
                datetime.now().timestamp() + (72 * 3600)  # 72 hours
            )
            consent.metadata = json.dumps(metadata)

        self.db.commit()

        return {
            "status": "deletion_scheduled",
            "user_id": user_id,
            "consents_to_delete": consent_count,
            "deletion_deadline": "72 hours",
            "deletion_completion_by": (
                datetime.now().timestamp() + (72 * 3600)
            )
        }

# Global consent manager instance
def get_consent_manager(db: Session) -> ConsentManager:
    """Get consent manager instance"""
    return ConsentManager(db)
