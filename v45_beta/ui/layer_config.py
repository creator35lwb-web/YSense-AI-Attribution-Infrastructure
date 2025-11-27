"""
YSenseAI v4.5-Beta: 5-Layer Perception Toolkit Configuration
Defines the structured prompts for wisdom extraction
"""

PERCEPTION_LAYERS = [
    {
        "id": "narrative",
        "title": "Narrative Layer",
        "icon": "📖",
        "question": "What is the unspoken story of this moment? And what is the well-known story?",
        "placeholder": "e.g., The locals say this tree houses spirits, but tourists just see shade...",
        "description": "The hidden narrative vs. the legend everyone knows",
        "training_value": "Context understanding, cultural nuance, implicit vs explicit meaning",
        "optimal_length": "100-200 words"
    },
    {
        "id": "somatic",
        "title": "Somatic Layer",
        "icon": "❤️",
        "question": "What does being in this moment make your body and emotions feel?",
        "placeholder": "e.g., My chest feels tight with nostalgia, the air smells like rain and earth...",
        "description": "Physical sensations and emotional states",
        "training_value": "Emotional intelligence, embodied cognition, sensory awareness",
        "optimal_length": "80-150 words"
    },
    {
        "id": "attention",
        "title": "Attention Layer",
        "icon": "👁️",
        "question": "What is one tiny detail here that most people would miss?",
        "placeholder": "e.g., The way the moss only grows on the north side of the brick...",
        "description": "The micro-observation that reveals truth",
        "training_value": "Observation skills, detail recognition, pattern detection",
        "optimal_length": "50-100 words"
    },
    {
        "id": "synesthetic",
        "title": "Synesthetic Layer",
        "icon": "✨",
        "question": "What are three non-visual words to describe the 'vibe' of this moment?",
        "placeholder": "e.g., Crunchy. Velvet. Hollow.",
        "description": "Cross-sensory description beyond sight",
        "training_value": "Cross-modal reasoning, abstract representation, synesthesia",
        "optimal_length": "30-80 words"
    },
    {
        "id": "temporal",
        "title": "Temporal-Auditory Layer",
        "icon": "🎵",
        "question": "If this moment had a sound, what would it be? How does time feel here?",
        "placeholder": "e.g., A low cello note held for eternity, time moves like honey...",
        "description": "The sonic and temporal quality",
        "training_value": "Temporal reasoning, auditory imagination, rhythm perception",
        "optimal_length": "50-100 words"
    }
]

# Z-Protocol Consent Tiers
CONSENT_TIERS = [
    {
        "id": "tier1",
        "name": "Public Commons",
        "icon": "🌍",
        "revenue_share": "15%",
        "description": "Contribute to general human wisdom. Your knowledge helps train AI for everyone.",
        "protection_level": "Attribution only",
        "use_cases": "General knowledge, basic reasoning, common wisdom",
        "distribution": "Wide distribution, public datasets",
        "color": "emerald"
    },
    {
        "id": "tier3",
        "name": "Cultural Heritage",
        "icon": "🏛️",
        "revenue_share": "25%",
        "description": "Traditional knowledge attributed to your community. Protected cultural context.",
        "protection_level": "Community consent required",
        "use_cases": "Cultural traditions, indigenous wisdom, regional knowledge",
        "distribution": "Restricted use, cultural sensitivity filters",
        "color": "indigo"
    },
    {
        "id": "tier4",
        "name": "Sacred / Private",
        "icon": "🔒",
        "revenue_share": "30%",
        "description": "Highly restricted access. Maximum protection and compensation.",
        "protection_level": "High encryption, limited distribution",
        "use_cases": "Personal insights, proprietary reasoning, sensitive knowledge",
        "distribution": "Minimal distribution, premium datasets only",
        "color": "amber"
    }
]

# Quality Metrics Configuration
QUALITY_METRICS = {
    "context_efficiency": {
        "name": "Context Efficiency",
        "description": "Optimal token count for training",
        "target_range": (300, 800),
        "weight": 0.15
    },
    "reasoning_depth": {
        "name": "Reasoning Depth",
        "description": "Number of explicit reasoning steps",
        "target_min": 5,
        "weight": 0.25
    },
    "cultural_specificity": {
        "name": "Cultural Specificity",
        "description": "Unique cultural markers vs generic content",
        "target_min": 0.70,
        "weight": 0.20
    },
    "emotional_richness": {
        "name": "Emotional Richness",
        "description": "Emotional descriptors per 100 words",
        "target_min": 15,
        "weight": 0.15
    },
    "attention_density": {
        "name": "Attention Density",
        "description": "Specific, verifiable details per layer",
        "target_min": 3,
        "weight": 0.15
    },
    "compression_quality": {
        "name": "Compression Quality",
        "description": "Information preserved in distillation",
        "target_min": 0.80,
        "weight": 0.10
    }
}

# UI Configuration
UI_CONFIG = {
    "colors": {
        "primary": "#4c1d95",  # Indigo
        "secondary": "#10b981",  # Emerald
        "accent": "#f59e0b",  # Amber
        "background": "#FDFBF7",  # Warm white
        "text": "#1e293b",  # Slate
        "error": "#ef4444",  # Red
        "success": "#10b981"  # Emerald
    },
    "fonts": {
        "heading": "Georgia, serif",
        "body": "Inter, system-ui, sans-serif",
        "code": "Fira Code, monospace"
    },
    "animations": {
        "processing_stages": [
            "Dissolving context...",
            "Sensing the body...",
            "Finding the spark...",
            "Listening to time...",
            "Minting wisdom..."
        ]
    }
}

# Training Format Template
TRAINING_FORMAT_TEMPLATE = {
    "asset_type": "wisdom_cot_v1",
    "asset_id": "",  # Generated: ysense-{hash_prefix}
    "author_did": "",  # Generated: did:ysense:{user_id}
    "fingerprint": "",  # SHA-256 hash
    "license": "YSense-Commercial-v1",
    "consent_tier": "",
    "created_at": "",  # ISO-8601 timestamp
    "training_format": {
        "instruction": "",
        "input": "",
        "output": {
            "chain_of_thought": [],
            "distilled_essence": [],
            "wisdom_conclusion": ""
        }
    },
    "metadata": {
        "category": "",
        "domain": "",
        "culture": "",
        "difficulty": "",
        "quality_score": 0.0,
        "training_signals": {}
    }
}
