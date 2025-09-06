"""
YSense AI Attribution Infrastructure
Copyright 2025 Alton Lee Wei Bin
Licensed under Apache License 2.0

This file demonstrates the core attribution engine implementation
establishing prior art for AI content attribution systems.
"""

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, asdict


class ContributionType(Enum):
    """Types of contributions in the system"""
    HUMAN = "human"
    AI = "ai"
    HYBRID = "hybrid"


class ConsentTier(Enum):
    """Consent tiers based on Z Protocol"""
    PUBLIC = "public"
    PERSONAL = "personal"
    CULTURAL = "cultural"
    SACRED = "sacred"
    THERAPEUTIC = "therapeutic"


@dataclass
class AttributionRecord:
    """Data structure for attribution records"""
    contributor_id: str
    contribution_type: ContributionType
    content_hash: str
    timestamp: str
    verification_status: str
    consent_level: ConsentTier
    metadata: Dict[str, Any]
    blockchain_hash: Optional[str] = None
    parent_hash: Optional[str] = None
    attribution_score: float = 0.0


class AttributionEngine:
    """
    Core engine for tracking AI and human contributions.
    Implements novel attribution scoring and blockchain verification.
    """
    
    def __init__(self):
        self.attribution_chain: List[AttributionRecord] = []
        self.contributor_registry: Dict[str, Dict] = {}
        self.verification_queue: List[str] = []
        self.consensus_threshold = 0.95
        
    def generate_content_hash(self, content: Any) -> str:
        """
        Generate cryptographic hash of content
        
        Args:
            content: Content to hash (string, dict, or bytes)
            
        Returns:
            SHA-256 hash of content
        """
        if isinstance(content, dict):
            content = json.dumps(content, sort_keys=True)
        elif not isinstance(content, bytes):
            content = str(content).encode('utf-8')
            
        return hashlib.sha256(content).hexdigest()
    
    def calculate_attribution_weight(self, 
                                    contribution_type: ContributionType,
                                    content: Any,
                                    metadata: Dict) -> float:
        """
        Calculate attribution weight using novel scoring algorithm
        
        Args:
            contribution_type: Type of contribution
            content: The actual content
            metadata: Additional metadata about contribution
            
        Returns:
            Attribution weight score between 0 and 1
        """
        base_weights = {
            ContributionType.HUMAN: 1.0,
            ContributionType.AI: 0.8,
            ContributionType.HYBRID: 0.9
        }
        
        weight = base_weights[contribution_type]
        
        # Adjust based on content complexity
        if metadata.get('complexity_score', 0) > 0.7:
            weight *= 1.1
            
        # Adjust based on originality
        if metadata.get('originality_score', 0) > 0.8:
            weight *= 1.2
            
        # Adjust based on verification status
        if metadata.get('verified', False):
            weight *= 1.05
            
        return min(weight, 1.0)  # Cap at 1.0
    
    def get_consent_level(self, contributor_id: str) -> ConsentTier:
        """
        Retrieve consent level for a contributor
        
        Args:
            contributor_id: Unique identifier for contributor
            
        Returns:
            Consent tier for the contributor
        """
        contributor = self.contributor_registry.get(contributor_id, {})
        return contributor.get('consent_tier', ConsentTier.PERSONAL)
    
    def extract_metadata(self, content: Any) -> Dict:
        """
        Extract metadata from content using AI analysis
        
        Args:
            content: Content to analyze
            
        Returns:
            Dictionary of extracted metadata
        """
        metadata = {
            'content_length': len(str(content)),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'content_type': type(content).__name__,
            'extraction_version': '1.0.0'
        }
        
        # Simulate complexity analysis
        metadata['complexity_score'] = min(len(str(content)) / 1000, 1.0)
        
        # Simulate originality analysis
        metadata['originality_score'] = 0.85  # Would use ML model in production
        
        return metadata
    
    def write_to_blockchain(self, record: AttributionRecord) -> str:
        """
        Write attribution record to blockchain
        
        Args:
            record: Attribution record to write
            
        Returns:
            Blockchain transaction hash
        """
        # Get previous block hash for chain integrity
        previous_hash = self.attribution_chain[-1].blockchain_hash if self.attribution_chain else "0"
        
        # Create block data
        block_data = {
            'previous_hash': previous_hash,
            'timestamp': record.timestamp,
            'record': asdict(record),
            'nonce': 0
        }
        
        # Simulate proof of work (simplified)
        while True:
            block_string = json.dumps(block_data, sort_keys=True)
            block_hash = hashlib.sha256(block_string.encode()).hexdigest()
            
            # Simple difficulty: hash must start with "00"
            if block_hash.startswith("00"):
                return block_hash
                
            block_data['nonce'] += 1
    
    def record_contribution(self,
                          contributor_id: str,
                          content: Any,
                          contribution_type: ContributionType,
                          metadata: Optional[Dict] = None) -> AttributionRecord:
        """
        Record a contribution with full attribution metadata
        
        Args:
            contributor_id: Unique identifier for contributor
            content: The actual contribution content
            contribution_type: Type of contribution (human/ai/hybrid)
            metadata: Optional additional metadata
            
        Returns:
            Complete attribution record with blockchain hash
        """
        # Register contributor if new
        if contributor_id not in self.contributor_registry:
            self.register_contributor(contributor_id)
        
        # Generate timestamp
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Extract and merge metadata
        extracted_metadata = self.extract_metadata(content)
        if metadata:
            extracted_metadata.update(metadata)
        
        # Calculate attribution score
        attribution_score = self.calculate_attribution_weight(
            contribution_type, content, extracted_metadata
        )
        
        # Create attribution record
        record = AttributionRecord(
            contributor_id=contributor_id,
            contribution_type=contribution_type,
            content_hash=self.generate_content_hash(content),
            timestamp=timestamp,
            verification_status='pending',
            consent_level=self.get_consent_level(contributor_id),
            metadata=extracted_metadata,
            attribution_score=attribution_score
        )
        
        # Write to blockchain
        blockchain_hash = self.write_to_blockchain(record)
        record.blockchain_hash = blockchain_hash
        
        # Add to chain
        self.attribution_chain.append(record)
        
        # Queue for verification
        self.verification_queue.append(blockchain_hash)
        
        return record
    
    def register_contributor(self,
                           contributor_id: str,
                           contributor_type: ContributionType = ContributionType.HUMAN,
                           consent_tier: ConsentTier = ConsentTier.PERSONAL) -> Dict:
        """
        Register a new contributor in the system
        
        Args:
            contributor_id: Unique identifier for contributor
            contributor_type: Type of contributor
            consent_tier: Initial consent tier
            
        Returns:
            Contributor registration record
        """
        registration = {
            'contributor_id': contributor_id,
            'contributor_type': contributor_type,
            'consent_tier': consent_tier,
            'registration_date': datetime.now(timezone.utc).isoformat(),
            'status': 'active',
            'contribution_count': 0,
            'total_attribution_score': 0.0
        }
        
        self.contributor_registry[contributor_id] = registration
        return registration
    
    def verify_chain_integrity(self) -> Tuple[bool, Optional[str]]:
        """
        Verify the integrity of the attribution chain
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.attribution_chain:
            return True, None
            
        for i, record in enumerate(self.attribution_chain):
            if i == 0:
                continue
                
            # Verify link to previous record
            previous_record = self.attribution_chain[i - 1]
            if record.parent_hash != previous_record.blockchain_hash:
                return False, f"Chain broken at index {i}"
                
            # Verify record hash
            record_data = {
                'contributor_id': record.contributor_id,
                'content_hash': record.content_hash,
                'timestamp': record.timestamp
            }
            
            calculated_hash = self.generate_content_hash(record_data)
            if calculated_hash != record.content_hash:
                return False, f"Invalid hash at index {i}"
                
        return True, None
    
    def get_attribution_summary(self, contributor_id: Optional[str] = None) -> Dict:
        """
        Get attribution summary for a contributor or entire system
        
        Args:
            contributor_id: Optional contributor ID to filter by
            
        Returns:
            Attribution summary statistics
        """
        if contributor_id:
            records = [r for r in self.attribution_chain 
                      if r.contributor_id == contributor_id]
        else:
            records = self.attribution_chain
            
        if not records:
            return {'total_contributions': 0}
            
        summary = {
            'total_contributions': len(records),
            'human_contributions': len([r for r in records 
                                       if r.contribution_type == ContributionType.HUMAN]),
            'ai_contributions': len([r for r in records 
                                   if r.contribution_type == ContributionType.AI]),
            'hybrid_contributions': len([r for r in records 
                                        if r.contribution_type == ContributionType.HYBRID]),
            'average_attribution_score': sum(r.attribution_score for r in records) / len(records),
            'verified_contributions': len([r for r in records 
                                         if r.verification_status == 'verified']),
            'consent_distribution': {}
        }
        
        # Calculate consent distribution
        for tier in ConsentTier:
            count = len([r for r in records if r.consent_level == tier])
            if count > 0:
                summary['consent_distribution'][tier.value] = count
                
        return summary
    
    def export_attribution_proof(self, 
                                contribution_hash: str,
                                format: str = 'json') -> str:
        """
        Export proof of attribution for legal/verification purposes
        
        Args:
            contribution_hash: Hash of the contribution
            format: Export format (json, xml, etc.)
            
        Returns:
            Formatted attribution proof
        """
        # Find the record
        record = None
        for r in self.attribution_chain:
            if r.content_hash == contribution_hash or r.blockchain_hash == contribution_hash:
                record = r
                break
                
        if not record:
            raise ValueError(f"No record found for hash: {contribution_hash}")
            
        proof = {
            'attribution_proof': {
                'version': '1.0',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'record': asdict(record),
                'chain_position': self.attribution_chain.index(record),
                'chain_length': len(self.attribution_chain),
                'verification': {
                    'chain_integrity': self.verify_chain_integrity()[0],
                    'blockchain_hash': record.blockchain_hash,
                    'content_hash': record.content_hash
                }
            }
        }
        
        if format == 'json':
            return json.dumps(proof, indent=2)
        else:
            raise NotImplementedError(f"Format {format} not yet supported")


# Example usage and testing
if __name__ == "__main__":
    # Initialize attribution engine
    engine = AttributionEngine()
    
    # Register contributors
    engine.register_contributor(
        "human_001",
        ContributionType.HUMAN,
        ConsentTier.PUBLIC
    )
    
    engine.register_contributor(
        "ai_claude",
        ContributionType.AI,
        ConsentTier.PUBLIC
    )
    
    # Record human contribution
    human_contribution = {
        'text': 'Walking on the beach at sunset in Kelantan...',
        'image': 'beach_sunset.jpg',
        'metadata': {
            'location': 'Kelantan, Malaysia',
            'date': '2013-07-15'
        }
    }
    
    human_record = engine.record_contribution(
        contributor_id="human_001",
        content=human_contribution,
        contribution_type=ContributionType.HUMAN,
        metadata={'source': 'perception_toolkit', 'layer': 'narrative'}
    )
    
    print(f"Human contribution recorded: {human_record.blockchain_hash}")
    
    # Record AI contribution
    ai_contribution = {
        'analysis': 'This memory contains deep emotional resonance...',
        'extracted_themes': ['nostalgia', 'connection', 'nature'],
        'vibe_distillation': ['golden', 'infinite', 'peaceful']
    }
    
    ai_record = engine.record_contribution(
        contributor_id="ai_claude",
        content=ai_contribution,
        contribution_type=ContributionType.AI,
        metadata={'model': 'claude-3', 'confidence': 0.92}
    )
    
    print(f"AI contribution recorded: {ai_record.blockchain_hash}")
    
    # Record hybrid contribution
    hybrid_contribution = {
        'human_memory': human_contribution,
        'ai_enhancement': ai_contribution,
        'synthesis': 'A moment of transcendent beauty captured and understood'
    }
    
    hybrid_record = engine.record_contribution(
        contributor_id="human_001",
        content=hybrid_contribution,
        contribution_type=ContributionType.HYBRID,
        metadata={'collaboration_type': 'human_ai_synthesis'}
    )
    
    print(f"Hybrid contribution recorded: {hybrid_record.blockchain_hash}")
    
    # Verify chain integrity
    is_valid, error = engine.verify_chain_integrity()
    print(f"\nChain integrity: {'Valid' if is_valid else f'Invalid - {error}'}")
    
    # Get attribution summary
    summary = engine.get_attribution_summary()
    print(f"\nAttribution Summary:")
    print(json.dumps(summary, indent=2))
    
    # Export attribution proof
    proof = engine.export_attribution_proof(human_record.blockchain_hash)
    print(f"\nAttribution Proof for human contribution:")
    print(proof)
