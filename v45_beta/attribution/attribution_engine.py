"""
YSenseAI v4.5-Beta: Attribution Engine
Cryptographic attribution with blockchain-ready structure
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class AttributionEngine:
    """
    Core attribution engine for YSenseAI
    Implements cryptographic signing and DID assignment
    Blockchain-ready structure for future decentralization
    """
    
    def __init__(self, app_id: str = "YSenseAI-v45-beta"):
        self.app_id = app_id
        self.version = "1.0.0"
    
    def create_wisdom_asset(self, 
                           user_id: str,
                           raw_story: str,
                           layer_responses: Dict[str, str],
                           distilled_essence: List[str],
                           consent_tier: str,
                           quality_scores: Optional[Dict[str, float]] = None) -> Dict:
        """
        Create a complete wisdom asset with attribution
        
        Args:
            user_id: User identifier
            raw_story: Original story text
            layer_responses: 5-layer perception responses
            distilled_essence: 3-word essence
            consent_tier: Z-Protocol tier (tier1, tier3, tier4)
            quality_scores: Training quality metrics
        
        Returns:
            Complete attributed wisdom asset
        """
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        # 1. Create training-ready format
        training_format = self._create_training_format(
            raw_story, layer_responses, distilled_essence
        )
        
        # 2. Generate content hash (fingerprint)
        content_hash = self._generate_content_hash(training_format)
        
        # 3. Create asset ID
        asset_id = f"ysense-{content_hash[:12]}"
        
        # 4. Generate DID (Decentralized Identifier)
        author_did = self._generate_did(user_id)
        
        # 5. Create attribution record
        attribution_record = {
            # Asset Identity
            "asset_id": asset_id,
            "asset_type": "wisdom_cot_v1",
            "version": self.version,
            
            # Attribution
            "author_did": author_did,
            "fingerprint": content_hash,
            "signature": self._generate_signature(content_hash, author_did),
            
            # Legal & Consent
            "license": "YSense-Commercial-v1",
            "consent_tier": consent_tier,
            "revenue_share": self._get_revenue_share(consent_tier),
            
            # Timestamps
            "created_at": timestamp,
            "minted_at": timestamp,
            
            # Content
            "raw_story": raw_story,
            "layers": layer_responses,
            "distilled_essence": distilled_essence,
            
            # Training Format
            "training_format": training_format,
            
            # Quality Metrics
            "quality_scores": quality_scores or {},
            "training_ready": self._is_training_ready(quality_scores),
            
            # Metadata
            "metadata": {
                "app_id": self.app_id,
                "platform_version": "4.5-beta",
                "z_protocol_version": "2.0",
                "blockchain_ready": True,
                "ipfs_ready": True
            }
        }
        
        return attribution_record
    
    def _create_training_format(self, 
                                raw_story: str,
                                layer_responses: Dict[str, str],
                                distilled_essence: List[str]) -> Dict:
        """
        Create Alpaca/ShareGPT compatible training format
        """
        
        # Build chain of thought from layers
        chain_of_thought = []
        layer_names = ["narrative", "somatic", "attention", "synesthetic", "temporal"]
        layer_titles = [
            "Narrative Layer (Story vs Legend)",
            "Somatic Layer (Body & Emotion)",
            "Attention Layer (Tiny Detail)",
            "Synesthetic Layer (Non-visual Vibe)",
            "Temporal Layer (Sound of Time)"
        ]
        
        for name, title in zip(layer_names, layer_titles):
            if name in layer_responses and layer_responses[name]:
                chain_of_thought.append(f"{title}: {layer_responses[name]}")
        
        # Create instruction
        instruction = "Extract wisdom from this moment using the 5-layer perception toolkit."
        
        # Create output with reasoning
        output = {
            "chain_of_thought": chain_of_thought,
            "distilled_essence": distilled_essence,
            "wisdom_conclusion": self._generate_conclusion(layer_responses, distilled_essence)
        }
        
        return {
            "instruction": instruction,
            "input": raw_story,
            "output": output
        }
    
    def _generate_conclusion(self, 
                            layer_responses: Dict[str, str],
                            distilled_essence: List[str]) -> str:
        """
        Generate wisdom conclusion from layers
        """
        essence_text = ", ".join(distilled_essence)
        return f"The essence of this wisdom is: {essence_text}. " \
               f"It reveals truth through multiple layers of perception."
    
    def _generate_content_hash(self, training_format: Dict) -> str:
        """
        Generate SHA-256 hash of content for fingerprinting
        """
        content_string = json.dumps(training_format, sort_keys=True)
        return hashlib.sha256(content_string.encode()).hexdigest()
    
    def _generate_did(self, user_id: str) -> str:
        """
        Generate Decentralized Identifier (DID)
        Format: did:ysense:{user_id_hash}
        """
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()[:16]
        return f"did:ysense:{user_hash}"
    
    def _generate_signature(self, content_hash: str, author_did: str) -> str:
        """
        Generate cryptographic signature
        In production, this would use actual private key signing
        """
        signature_input = f"{content_hash}:{author_did}:{self.app_id}"
        signature = hashlib.sha256(signature_input.encode()).hexdigest()
        return f"sig:ysense:{signature[:32]}"
    
    def _get_revenue_share(self, consent_tier: str) -> str:
        """
        Get revenue share percentage for consent tier
        """
        revenue_shares = {
            "tier1": "15%",
            "tier3": "25%",
            "tier4": "30%"
        }
        return revenue_shares.get(consent_tier, "15%")
    
    def _is_training_ready(self, quality_scores: Optional[Dict[str, float]]) -> bool:
        """
        Determine if wisdom asset is ready for AI training
        """
        if not quality_scores:
            return False
        
        # Check if all scores meet minimum thresholds
        thresholds = {
            "context_efficiency": 0.60,
            "reasoning_depth": 0.70,
            "cultural_specificity": 0.60,
            "emotional_richness": 0.65,
            "attention_density": 0.60,
            "compression_quality": 0.70
        }
        
        for metric, threshold in thresholds.items():
            if quality_scores.get(metric, 0) < threshold:
                return False
        
        return True
    
    def verify_attribution(self, attribution_record: Dict) -> Dict:
        """
        Verify attribution integrity
        
        Returns:
            Verification result with status and details
        """
        try:
            # Recalculate content hash
            training_format = attribution_record.get("training_format", {})
            calculated_hash = self._generate_content_hash(training_format)
            
            # Compare with stored fingerprint
            stored_hash = attribution_record.get("fingerprint", "")
            
            is_valid = calculated_hash == stored_hash
            
            return {
                "valid": is_valid,
                "asset_id": attribution_record.get("asset_id"),
                "author_did": attribution_record.get("author_did"),
                "fingerprint_match": is_valid,
                "message": "Attribution verified successfully" if is_valid else "WARNING: Content has been tampered",
                "verified_at": datetime.utcnow().isoformat() + "Z"
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "message": "Verification failed"
            }
    
    def export_for_training(self, attribution_records: List[Dict]) -> str:
        """
        Export wisdom assets in JSONL format for AI training
        
        Args:
            attribution_records: List of attributed wisdom assets
        
        Returns:
            JSONL string ready for training
        """
        jsonl_lines = []
        
        for record in attribution_records:
            # Only export training-ready assets
            if not record.get("training_ready", False):
                continue
            
            # Extract training format
            training_format = record.get("training_format", {})
            
            # Add metadata for attribution tracking
            training_entry = {
                **training_format,
                "asset_id": record.get("asset_id"),
                "author_did": record.get("author_did"),
                "consent_tier": record.get("consent_tier"),
                "quality_score": record.get("quality_scores", {}).get("overall", 0.0)
            }
            
            jsonl_lines.append(json.dumps(training_entry))
        
        return "\n".join(jsonl_lines)
    
    def calculate_revenue_distribution(self, 
                                      attribution_records: List[Dict],
                                      total_revenue: float) -> Dict:
        """
        Calculate revenue distribution based on consent tiers
        
        Args:
            attribution_records: List of attributed wisdom assets
            total_revenue: Total revenue to distribute
        
        Returns:
            Revenue distribution by contributor
        """
        distribution = {}
        
        # Group by author
        author_contributions = {}
        for record in attribution_records:
            author_did = record.get("author_did")
            consent_tier = record.get("consent_tier")
            
            if author_did not in author_contributions:
                author_contributions[author_did] = []
            
            author_contributions[author_did].append({
                "asset_id": record.get("asset_id"),
                "consent_tier": consent_tier,
                "revenue_share": record.get("revenue_share")
            })
        
        # Calculate distribution
        total_contributions = len(attribution_records)
        
        for author_did, contributions in author_contributions.items():
            author_revenue = 0
            
            for contrib in contributions:
                # Parse revenue share percentage
                share_pct = float(contrib["revenue_share"].rstrip("%")) / 100
                
                # Calculate per-contribution revenue
                per_contribution = total_revenue / total_contributions
                author_revenue += per_contribution * share_pct
            
            distribution[author_did] = {
                "total_revenue": round(author_revenue, 2),
                "contributions": len(contributions),
                "assets": [c["asset_id"] for c in contributions]
            }
        
        return distribution


# Test the attribution engine
def test_attribution_engine():
    """Test attribution engine functionality"""
    
    print("🔒 Testing YSenseAI Attribution Engine")
    print("=" * 60)
    
    engine = AttributionEngine()
    
    # Test data
    test_wisdom = {
        "user_id": "user_test_001",
        "raw_story": "A grandmother teaches patience through cooking rendang",
        "layer_responses": {
            "narrative": "The unspoken story is about generational knowledge transfer",
            "somatic": "The body feels warmth, connection, reverence",
            "attention": "The way the paste darkens like memories deepening",
            "synesthetic": "Patience. Tradition. Alchemy.",
            "temporal": "A low, steady hum - like time itself cooking"
        },
        "distilled_essence": ["Patience", "Tradition", "Alchemy"],
        "consent_tier": "tier3",
        "quality_scores": {
            "context_efficiency": 0.85,
            "reasoning_depth": 0.90,
            "cultural_specificity": 0.92,
            "emotional_richness": 0.88,
            "attention_density": 0.87,
            "compression_quality": 0.91,
            "overall": 0.89
        }
    }
    
    # Create wisdom asset
    print("\n📝 Creating wisdom asset...")
    asset = engine.create_wisdom_asset(**test_wisdom)
    
    print(f"✅ Asset ID: {asset['asset_id']}")
    print(f"✅ Author DID: {asset['author_did']}")
    print(f"✅ Fingerprint: {asset['fingerprint'][:32]}...")
    print(f"✅ Signature: {asset['signature'][:32]}...")
    print(f"✅ Revenue Share: {asset['revenue_share']}")
    print(f"✅ Training Ready: {asset['training_ready']}")
    
    # Verify attribution
    print("\n🔍 Verifying attribution...")
    verification = engine.verify_attribution(asset)
    print(f"✅ Valid: {verification['valid']}")
    print(f"✅ Message: {verification['message']}")
    
    # Export for training
    print("\n📤 Exporting for training...")
    jsonl = engine.export_for_training([asset])
    print(f"✅ JSONL length: {len(jsonl)} characters")
    
    # Calculate revenue distribution
    print("\n💰 Calculating revenue distribution...")
    distribution = engine.calculate_revenue_distribution([asset], 1000.0)
    print(f"✅ Distribution: {json.dumps(distribution, indent=2)}")
    
    print("\n🎉 Attribution Engine Test Complete!")


if __name__ == "__main__":
    test_attribution_engine()
