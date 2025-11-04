# YSense™ Five-Layer Perception Toolkit™ - AI Backend

**Version:** 1.0
**Author:** Alton (with AI collaboration)
**Date:** November 2025

## Overview

This is the **AI backend implementation** of the YSense™ Five-Layer Perception Toolkit™, which transforms human experiences into **15+ structured data points** for AI training. The toolkit processes user stories through five distinct perceptual layers to capture the multi-dimensional richness of human wisdom.

## What This Does

The Five-Layer Perception Toolkit™ solves a critical problem in AI development: **how to capture and structure human wisdom in a way that AI systems can learn from**.

Traditional AI training data is flat and one-dimensional (just text, images, etc.). This toolkit captures:

1. **Narrative Layer** - Unspoken stories and meaning
2. **Somatic Layer** - Physical sensations and emotional states
3. **Attention Layer** - Overlooked details and significance
4. **Synesthetic Layer** - Cross-modal "vibe" descriptions
5. **Temporal-Auditory Layer** - Sound and rhythm of moments

Each experience generates **15+ structured data points** that provide rich, multi-dimensional training data for AI models.

## Architecture

```
User Story + 3-Word Resonance
         ↓
Five-Layer Perception Toolkit
         ↓
    [AI Processing]
         ↓
Layer 1: Narrative (context, emotion, meaning)
Layer 2: Somatic (physical_sensation, emotional_state, embodied_memory)
Layer 3: Attention (focus_point, peripheral_awareness, significance)
Layer 4: Synesthetic (cross_modal_perception, atmosphere, essence)
Layer 5: Temporal-Auditory (temporal_quality, rhythmic_pattern, auditory_imagination)
         ↓
Composite Analysis (themes, attribution_score)
         ↓
    Wisdom Drop JSON
         ↓
[Blockchain Attribution Engine]
```

## Installation

### Prerequisites

- Python 3.11+
- OpenAI API access (API key in environment variable `OPENAI_API_KEY`)

### Setup

```bash
# Install dependencies
pip3 install openai

# Set environment variable (already configured in this sandbox)
export OPENAI_API_KEY="your-api-key"
```

## Usage

### Basic Example

```python
from perception_toolkit import FiveLayerPerceptionToolkit, ConsentTier

# Initialize toolkit
toolkit = FiveLayerPerceptionToolkit(model="gpt-4.1-mini")

# Process a user's experience
perception_data = toolkit.process_experience(
    story="Your personal story here...",
    primary_vibe_word="Connection",
    primary_vibe_description="This word resonates because...",
    secondary_resonance_word="Peace",
    secondary_resonance_description="This connects to...",
    tertiary_essence_word="Home",
    tertiary_essence_description="It reveals...",
    contributor_id="user123",
    consent_tier=ConsentTier.PUBLIC
)

# Save wisdom drop
toolkit.save_wisdom_drop(perception_data)
```

### Creating Founder's Wisdom Drops

```bash
# Run the script to create example wisdom drops from founder's story
python3 create_founder_wisdom_drops.py
```

This generates 3 wisdom drops from the founder's Substack article "An Echo in the Black Box: Finding Trust in the Age of AI".

## Output Format

Each wisdom drop is saved as a JSON file with the following structure:

```json
{
  "wisdom_drop_id": "WD-20251103195812",
  "timestamp": "2025-11-03T19:58:19.848931Z",
  "contributor_id": "alton",
  "consent_tier": "public",
  "original_input": {
    "story": "...",
    "primary_vibe_word": "Trust",
    "primary_vibe_description": "...",
    "secondary_resonance_word": "Discovery",
    "secondary_resonance_description": "...",
    "tertiary_essence_word": "Synthesis",
    "tertiary_essence_description": "..."
  },
  "five_layer_analysis": {
    "narrative": {
      "context": "...",
      "emotion": "...",
      "meaning": "..."
    },
    "somatic": {
      "physical_sensation": "...",
      "emotional_state": "...",
      "embodied_memory": "..."
    },
    "attention": {
      "focus_point": "...",
      "peripheral_awareness": "...",
      "significance": "..."
    },
    "synesthetic": {
      "cross_modal_perception": ["Trust", "Discovery", "Synthesis"],
      "atmosphere": "...",
      "essence": "..."
    },
    "temporal_auditory": {
      "temporal_quality": "...",
      "rhythmic_pattern": "...",
      "auditory_imagination": "..."
    }
  },
  "composite_analysis": {
    "themes": ["Trust and Doubt", "Human-AI Collaboration", ...],
    "attribution_score": 1.0
  }
}
```

## Data Points Generated

Each wisdom drop contains **17 structured data points**:

### Original Input (7 data points)
1. story
2. primary_vibe_word
3. primary_vibe_description
4. secondary_resonance_word
5. secondary_resonance_description
6. tertiary_essence_word
7. tertiary_essence_description

### Five-Layer Analysis (15 data points)
8. narrative.context
9. narrative.emotion
10. narrative.meaning
11. somatic.physical_sensation
12. somatic.emotional_state
13. somatic.embodied_memory
14. attention.focus_point
15. attention.peripheral_awareness
16. attention.significance
17. synesthetic.cross_modal_perception (3 words)
18. synesthetic.atmosphere
19. synesthetic.essence
20. temporal_auditory.temporal_quality
21. temporal_auditory.rhythmic_pattern
22. temporal_auditory.auditory_imagination

### Composite Analysis (2+ data points)
23. composite_themes (3-5 themes)
24. attribution_score

**Total: 24+ structured data points per wisdom drop**

## Integration with YSense Platform

This backend can be integrated with the YSense™ platform frontend (ysenseai.org) in several ways:

### 1. REST API Integration

Create a FastAPI or Flask wrapper:

```python
from fastapi import FastAPI
from perception_toolkit import FiveLayerPerceptionToolkit

app = FastAPI()
toolkit = FiveLayerPerceptionToolkit()

@app.post("/api/v1/process-experience")
async def process_experience(request: ExperienceRequest):
    perception_data = toolkit.process_experience(
        story=request.story,
        primary_vibe_word=request.primary_vibe_word,
        # ... other parameters
    )
    return perception_data
```

### 2. Streamlit Integration

For the current Streamlit prototype:

```python
import streamlit as st
from perception_toolkit import FiveLayerPerceptionToolkit

toolkit = FiveLayerPerceptionToolkit()

if st.button("Process Experience"):
    with st.spinner("Processing through Five Layers..."):
        perception_data = toolkit.process_experience(
            story=story_input,
            primary_vibe_word=primary_word,
            # ... other inputs
        )
    st.success("Wisdom Drop Created!")
    st.json(toolkit._perception_data_to_dict(perception_data))
```

### 3. Database Storage

The wisdom drops can be stored in PostgreSQL with JSONB columns (as specified in the API documentation):

```sql
CREATE TABLE perception_data (
    wisdom_drop_id VARCHAR(50) PRIMARY KEY,
    contributor_id VARCHAR(100),
    timestamp TIMESTAMP,
    consent_tier VARCHAR(20),
    original_input JSONB,
    five_layer_analysis JSONB,
    composite_analysis JSONB,
    attribution_score FLOAT
);
```

## Z Protocol v2.0 Consent Tiers

The toolkit supports five consent tiers:

- **PUBLIC**: Shareable with attribution
- **PERSONAL**: Private, not for public use
- **CULTURAL**: Requires cultural context and sensitivity
- **SACRED**: Highly sensitive, restricted access
- **THERAPEUTIC**: For therapeutic purposes only

## Example Wisdom Drops

Three example wisdom drops from the founder's story are included in `./founder_wisdom_drops/`:

1. **WD-20251103195812** - The 20-Day Immersive Journey
   - Themes: Trust and Doubt, Human-AI Collaboration, Nostalgic Exploration

2. **WD-20251103195819** - The Vision/Iron Man Moment
   - Themes: Creative Breakthrough, Human-AI Synergy, Cinematic Achievement

3. **WD-20251103195827** - Living While Creating
   - Themes: Immersive Experience, Work-Life Balance, Technological Evolution

## Model Configuration

The toolkit supports multiple LLM models:

- `gpt-4.1-mini` (default) - Fast, cost-effective
- `gpt-4.1-nano` - Ultra-fast, basic analysis
- `gemini-2.5-flash` - Google's model

All models use the OpenAI-compatible API format.

## Performance

Processing time per wisdom drop:
- **gpt-4.1-mini**: ~5-8 seconds
- **gpt-4.1-nano**: ~3-5 seconds
- **gemini-2.5-flash**: ~4-6 seconds

## Next Steps

### For Development

1. **Create REST API wrapper** for production deployment
2. **Add database integration** for storing wisdom drops
3. **Implement blockchain attribution** using the attribution engine
4. **Add batch processing** for multiple wisdom drops
5. **Create admin dashboard** for reviewing wisdom drops

### For Academic Partnerships

1. **Generate 50-100 example wisdom drops** from diverse sources
2. **Create dataset documentation** for researchers
3. **Develop API access credentials** for academic partners
4. **Prepare research paper** demonstrating AI performance improvements

### For Q1 2026 Launch

1. **Integrate with production platform** (replace demo data)
2. **Set up revenue sharing** (50% to contributors)
3. **Launch beta program** with early adopters
4. **Onboard first academic partner** (€15K target)

## License

This implementation is part of the YSense™ defensive publication (DOI: 10.5281/zenodo.17072168) establishing prior art for AI attribution systems.

## Contact

**Founder:** Alton
**Substack:** https://ysense.substack.com
**Platform:** https://ysenseai.org

---

**慧觉™** - Illuminating the culture in everyday life and translating our feelings into a legacy of wisdom.
