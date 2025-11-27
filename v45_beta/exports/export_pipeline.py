"""
YSenseAI v4.5-Beta: Export Pipeline
Generate training-ready datasets for AI labs
"""

import json
import csv
from datetime import datetime
from typing import List, Dict
from pathlib import Path

class ExportPipeline:
    """
    Export wisdom assets in various formats for AI training
    """
    
    def __init__(self, output_dir: str = "exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_jsonl(self, 
                     submissions: List[Dict],
                     filename: str = None,
                     training_ready_only: bool = True) -> str:
        """
        Export in JSONL format (Alpaca/ShareGPT compatible)
        
        Args:
            submissions: List of wisdom submissions
            filename: Output filename (auto-generated if None)
            training_ready_only: Only export training-ready submissions
        
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ysense_wisdom_{timestamp}.jsonl"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for submission in submissions:
                # Filter by training readiness
                if training_ready_only and not submission.get('training_ready', False):
                    continue
                
                # Extract training format
                training_format = submission.get('training_format', {})
                
                # Add metadata for attribution
                entry = {
                    "instruction": training_format.get('instruction', ''),
                    "input": training_format.get('input', ''),
                    "output": training_format.get('output', {}),
                    "metadata": {
                        "asset_id": submission.get('asset_id'),
                        "author_did": submission.get('author_did'),
                        "consent_tier": submission.get('consent_tier'),
                        "revenue_share": submission.get('revenue_share'),
                        "quality_score": submission.get('quality_scores', {}).get('overall', 0),
                        "created_at": submission.get('created_at'),
                        "fingerprint": submission.get('fingerprint')
                    }
                }
                
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        return str(output_path)
    
    def export_alpaca_format(self, 
                            submissions: List[Dict],
                            filename: str = None) -> str:
        """
        Export in Alpaca instruction format
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ysense_alpaca_{timestamp}.json"
        
        output_path = self.output_dir / filename
        
        alpaca_data = []
        
        for submission in submissions:
            if not submission.get('training_ready', False):
                continue
            
            training_format = submission.get('training_format', {})
            output = training_format.get('output', {})
            
            # Flatten output for Alpaca format
            cot_text = "\n".join(output.get('chain_of_thought', []))
            essence_text = ", ".join(output.get('distilled_essence', []))
            conclusion = output.get('wisdom_conclusion', '')
            
            full_output = f"{cot_text}\n\nEssence: {essence_text}\n\n{conclusion}"
            
            alpaca_entry = {
                "instruction": training_format.get('instruction', ''),
                "input": training_format.get('input', ''),
                "output": full_output,
                "asset_id": submission.get('asset_id')
            }
            
            alpaca_data.append(alpaca_entry)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(alpaca_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def export_sharegpt_format(self, 
                               submissions: List[Dict],
                               filename: str = None) -> str:
        """
        Export in ShareGPT conversation format
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ysense_sharegpt_{timestamp}.json"
        
        output_path = self.output_dir / filename
        
        sharegpt_data = []
        
        for submission in submissions:
            if not submission.get('training_ready', False):
                continue
            
            training_format = submission.get('training_format', {})
            output = training_format.get('output', {})
            
            # Build conversation
            conversations = [
                {
                    "from": "human",
                    "value": f"{training_format.get('instruction', '')}\n\n{training_format.get('input', '')}"
                },
                {
                    "from": "gpt",
                    "value": json.dumps(output, indent=2, ensure_ascii=False)
                }
            ]
            
            sharegpt_entry = {
                "conversations": conversations,
                "asset_id": submission.get('asset_id'),
                "quality_score": submission.get('quality_scores', {}).get('overall', 0)
            }
            
            sharegpt_data.append(sharegpt_entry)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sharegpt_data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def export_csv_metadata(self, 
                           submissions: List[Dict],
                           filename: str = None) -> str:
        """
        Export metadata in CSV format for analysis
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ysense_metadata_{timestamp}.csv"
        
        output_path = self.output_dir / filename
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'asset_id', 'author_did', 'consent_tier', 'revenue_share',
                'quality_score', 'training_ready', 'created_at',
                'context_efficiency', 'reasoning_depth', 'cultural_specificity',
                'emotional_richness', 'attention_density', 'compression_quality',
                'essence_word_1', 'essence_word_2', 'essence_word_3'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for submission in submissions:
                quality_scores = submission.get('quality_scores', {})
                essence = submission.get('distilled_essence', ['', '', ''])
                
                row = {
                    'asset_id': submission.get('asset_id', ''),
                    'author_did': submission.get('author_did', ''),
                    'consent_tier': submission.get('consent_tier', ''),
                    'revenue_share': submission.get('revenue_share', ''),
                    'quality_score': quality_scores.get('overall', 0),
                    'training_ready': submission.get('training_ready', False),
                    'created_at': submission.get('created_at', ''),
                    'context_efficiency': quality_scores.get('context_efficiency', 0),
                    'reasoning_depth': quality_scores.get('reasoning_depth', 0),
                    'cultural_specificity': quality_scores.get('cultural_specificity', 0),
                    'emotional_richness': quality_scores.get('emotional_richness', 0),
                    'attention_density': quality_scores.get('attention_density', 0),
                    'compression_quality': quality_scores.get('compression_quality', 0),
                    'essence_word_1': essence[0] if len(essence) > 0 else '',
                    'essence_word_2': essence[1] if len(essence) > 1 else '',
                    'essence_word_3': essence[2] if len(essence) > 2 else ''
                }
                
                writer.writerow(row)
        
        return str(output_path)
    
    def export_full_archive(self, 
                           submissions: List[Dict],
                           filename: str = None) -> str:
        """
        Export complete archive with all data
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"ysense_full_archive_{timestamp}.json"
        
        output_path = self.output_dir / filename
        
        archive = {
            "export_metadata": {
                "platform": "YSenseAI",
                "version": "4.5-beta",
                "exported_at": datetime.utcnow().isoformat() + "Z",
                "total_submissions": len(submissions),
                "training_ready": sum(1 for s in submissions if s.get('training_ready', False))
            },
            "submissions": submissions
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(archive, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def generate_dataset_card(self, 
                             submissions: List[Dict],
                             filename: str = None) -> str:
        """
        Generate HuggingFace-style dataset card
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"DATASET_CARD_{timestamp}.md"
        
        output_path = self.output_dir / filename
        
        # Calculate statistics
        total = len(submissions)
        training_ready = sum(1 for s in submissions if s.get('training_ready', False))
        avg_quality = sum(s.get('quality_scores', {}).get('overall', 0) for s in submissions) / total if total > 0 else 0
        
        # Count by tier
        tier_counts = {}
        for s in submissions:
            tier = s.get('consent_tier', 'unknown')
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
        
        card_content = f"""# YSenseAI Wisdom Dataset v4.5-Beta

## Dataset Description

This dataset contains structured wisdom extracted through the YSenseAI 5-layer perception toolkit. Each entry represents culturally-rich, emotionally-aware reasoning chains optimized for AI training.

### Dataset Summary

- **Total Entries**: {total}
- **Training-Ready**: {training_ready}
- **Average Quality Score**: {avg_quality:.3f}
- **Format**: Alpaca/ShareGPT compatible
- **License**: YSense-Commercial-v1

### Consent Tiers

{chr(10).join([f"- **{tier}**: {count} entries" for tier, count in tier_counts.items()])}

## Dataset Structure

Each entry contains:

- **instruction**: Task description
- **input**: Raw story/moment
- **output**: 
  - chain_of_thought: 5-layer perception analysis
  - distilled_essence: 3-word vibe signature
  - wisdom_conclusion: Final insight
- **metadata**: Attribution, quality scores, consent tier

## Quality Metrics

All entries are evaluated on 6 training optimization signals:

1. **Context Efficiency** (300-800 tokens optimal)
2. **Reasoning Depth** (5 explicit steps)
3. **Cultural Specificity** (>70% unique markers)
4. **Emotional Richness** (>15 descriptors per 100 words)
5. **Attention Density** (3+ concrete details per layer)
6. **Compression Quality** (>80% essence preservation)

## Attribution & Ethics

- **Z-Protocol v2.0**: All contributions are cryptographically attributed
- **Revenue Sharing**: 15-30% based on consent tier
- **DID System**: Decentralized identifiers for all contributors
- **Fingerprinting**: SHA-256 content hashing for integrity

## Use Cases

- Fine-tuning LLMs for cultural awareness
- Training models on structured reasoning
- Enhancing emotional intelligence in AI
- Cross-cultural knowledge transfer

## Citation

```
@dataset{{ysenseai_wisdom_v45_beta,
  title={{YSenseAI Wisdom Dataset v4.5-Beta}},
  author={{YSenseAI Platform}},
  year={{2025}},
  url={{https://ysenseai.org}},
  license={{YSense-Commercial-v1}}
}}
```

## Contact

For licensing, partnerships, or questions:
- Website: https://ysenseai.org
- Platform: YSenseAI v4.5-Beta
- Z-Protocol: v2.0

---

*Generated on {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(card_content)
        
        return str(output_path)


# Test the export pipeline
def test_export_pipeline():
    """Test export pipeline functionality"""
    
    print("📤 Testing YSenseAI Export Pipeline")
    print("=" * 60)
    
    pipeline = ExportPipeline(output_dir="test_exports")
    
    # Mock submissions
    test_submissions = [
        {
            "asset_id": "ysense-test001",
            "author_did": "did:ysense:test001",
            "consent_tier": "tier3",
            "revenue_share": "25%",
            "training_ready": True,
            "created_at": "2025-11-27T00:00:00Z",
            "fingerprint": "abc123...",
            "distilled_essence": ["Patience", "Tradition", "Alchemy"],
            "quality_scores": {
                "context_efficiency": 0.85,
                "reasoning_depth": 0.90,
                "cultural_specificity": 0.92,
                "emotional_richness": 0.88,
                "attention_density": 0.87,
                "compression_quality": 0.91,
                "overall": 0.89
            },
            "training_format": {
                "instruction": "Extract wisdom using 5-layer perception",
                "input": "A grandmother teaches patience through cooking rendang",
                "output": {
                    "chain_of_thought": [
                        "Narrative: Generational knowledge transfer",
                        "Somatic: Warmth, reverence, connection",
                        "Attention: Paste darkening like memories",
                        "Synesthetic: Patient, Earthy, Sacred",
                        "Temporal: Time itself cooking"
                    ],
                    "distilled_essence": ["Patience", "Tradition", "Alchemy"],
                    "wisdom_conclusion": "True mastery requires slowness"
                }
            }
        }
    ]
    
    # Test exports
    print("\n📝 Exporting JSONL...")
    jsonl_path = pipeline.export_jsonl(test_submissions)
    print(f"✅ Exported: {jsonl_path}")
    
    print("\n📝 Exporting Alpaca format...")
    alpaca_path = pipeline.export_alpaca_format(test_submissions)
    print(f"✅ Exported: {alpaca_path}")
    
    print("\n📝 Exporting ShareGPT format...")
    sharegpt_path = pipeline.export_sharegpt_format(test_submissions)
    print(f"✅ Exported: {sharegpt_path}")
    
    print("\n📝 Exporting CSV metadata...")
    csv_path = pipeline.export_csv_metadata(test_submissions)
    print(f"✅ Exported: {csv_path}")
    
    print("\n📝 Exporting full archive...")
    archive_path = pipeline.export_full_archive(test_submissions)
    print(f"✅ Exported: {archive_path}")
    
    print("\n📝 Generating dataset card...")
    card_path = pipeline.generate_dataset_card(test_submissions)
    print(f"✅ Generated: {card_path}")
    
    print("\n🎉 Export Pipeline Test Complete!")


if __name__ == "__main__":
    test_export_pipeline()
