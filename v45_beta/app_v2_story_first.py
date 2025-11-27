"""
YSenseAI v4.5-Beta V2: Story-First AI-Native UX
User writes freely, AI extracts 5 layers automatically
"""

import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add directories to path
sys.path.append(str(Path(__file__).parent / "agents"))
sys.path.append(str(Path(__file__).parent / "ui"))
sys.path.append(str(Path(__file__).parent / "attribution"))

from ui.layer_config import PERCEPTION_LAYERS, CONSENT_TIERS, UI_CONFIG
from agents.anthropic_integration_v45 import AnthropicClient
from attribution.attribution_engine import AttributionEngine
from attribution.quality_metrics import QualityMetricsCalculator

# Page configuration
st.set_page_config(
    page_title="YSenseAI | 慧觉™",
    page_icon="🪶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for story-first design
st.markdown("""
<style>
    /* Global */
    .stApp {
        background: linear-gradient(135deg, #FDFBF7 0%, #F5F3EF 100%);
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Story Canvas */
    .story-canvas {
        background: white;
        border-radius: 1.5rem;
        padding: 3rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        margin: 2rem 0;
    }
    
    .story-title {
        font-family: 'Georgia', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .story-subtitle {
        font-size: 1.125rem;
        color: #64748b;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Processing Animation */
    .processing-container {
        text-align: center;
        padding: 4rem 2rem;
    }
    
    .processing-icon {
        font-size: 4rem;
        margin-bottom: 2rem;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .processing-title {
        font-family: 'Georgia', serif;
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .processing-step {
        font-size: 1rem;
        color: #4c1d95;
        font-weight: 500;
        margin: 0.5rem 0;
        padding: 0.75rem 1.5rem;
        background: #f0f9ff;
        border-radius: 9999px;
        display: inline-block;
    }
    
    /* Perception Layer Card */
    .layer-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    
    .layer-card:hover {
        border-color: #4c1d95;
        box-shadow: 0 4px 12px rgba(76, 29, 149, 0.1);
    }
    
    .layer-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .layer-icon {
        font-size: 1.75rem;
    }
    
    .layer-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .layer-content {
        color: #475569;
        line-height: 1.7;
        font-size: 1rem;
    }
    
    /* Essence Display */
    .essence-display {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%);
        border-radius: 1.5rem;
        margin: 2rem 0;
        color: white;
    }
    
    .essence-words {
        font-family: 'Georgia', serif;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        letter-spacing: 0.05em;
    }
    
    .essence-subtitle {
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 9999px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'canvas'
if 'raw_story' not in st.session_state:
    st.session_state.raw_story = ''
if 'extracted_layers' not in st.session_state:
    st.session_state.extracted_layers = {}
if 'distilled_essence' not in st.session_state:
    st.session_state.distilled_essence = []
if 'selected_tier' not in st.session_state:
    st.session_state.selected_tier = 'tier1'
if 'quality_scores' not in st.session_state:
    st.session_state.quality_scores = {}
if 'attribution_data' not in st.session_state:
    st.session_state.attribution_data = None

# Initialize components
@st.cache_resource
def get_components():
    claude = AnthropicClient()
    attribution_engine = AttributionEngine()
    quality_calculator = QualityMetricsCalculator()
    return claude, attribution_engine, quality_calculator

claude_client, attribution_engine, quality_calculator = get_components()

# AI Layer Extraction Function
def extract_layers_with_ai(story: str) -> dict:
    """
    Use Claude to automatically extract all 5 perception layers from the story
    """
    
    prompt = f"""You are Y, the wisdom extraction agent for YSenseAI. Your task is to analyze a story and extract insights across 5 perception layers.

Story:
{story}

Extract the following 5 layers. Be specific, poetic, and insightful. Each layer should be 2-4 sentences.

1. NARRATIVE LAYER: What is the unspoken story vs. the well-known story? What cultural or personal narrative is hidden beneath the surface?

2. SOMATIC LAYER: What physical sensations and emotions does this moment evoke? Describe the body's experience - temperature, tension, textures, smells, tastes.

3. ATTENTION LAYER: What is one tiny detail that most people would miss? What micro-observation reveals deeper truth?

4. SYNESTHETIC LAYER: Describe the "vibe" using non-visual sensory words. If this moment had a texture, temperature, or sound quality, what would it be?

5. TEMPORAL LAYER: If this moment had a sound, what would it be? How does time feel here - does it rush, crawl, or stand still?

Return ONLY a JSON object with these exact keys: "narrative", "somatic", "attention", "synesthetic", "temporal"

Example format:
{{
  "narrative": "The unspoken story is...",
  "somatic": "The body feels...",
  "attention": "The tiny detail is...",
  "synesthetic": "The vibe is...",
  "temporal": "The sound would be..."
}}
"""
    
    try:
        response = claude_client.generate_response(prompt, max_tokens=1000)
        
        # Try to parse JSON from response
        # Sometimes Claude wraps JSON in markdown code blocks
        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        
        layers = json.loads(response_clean.strip())
        
        # Validate all keys exist
        required_keys = ["narrative", "somatic", "attention", "synesthetic", "temporal"]
        if all(key in layers for key in required_keys):
            return layers
        else:
            raise ValueError("Missing required keys in AI response")
            
    except Exception as e:
        print(f"AI extraction error: {e}")
        # Fallback layers
        return {
            "narrative": f"This story reveals layers of meaning that unfold through careful observation and cultural context.",
            "somatic": f"The body experiences this moment through sensations of warmth, connection, and presence.",
            "attention": f"The small detail that stands out is the way elements interact in unexpected ways.",
            "synesthetic": f"The vibe feels textured, layered, and resonant - like velvet worn smooth by time.",
            "temporal": f"Time moves like honey here - slow, thick, deliberate, transforming the ordinary into the sacred."
        }

# Step 1: Story Canvas
def render_story_canvas():
    st.markdown("""
    <div class="story-canvas">
        <div class="story-title">Share your moment.</div>
        <div class="story-subtitle">
            A fleeting experience, a cultural memory, or a quiet realization. 
            Write freely. <strong>Y will find the wisdom inside.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    story = st.text_area(
        "Your Story",
        value=st.session_state.raw_story,
        height=300,
        placeholder="The rain started falling on the day my grandmother taught me to cook rendang...",
        label_visibility="collapsed",
        key="story_input"
    )
    
    st.session_state.raw_story = story
    
    # Character count and status
    char_count = len(story)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if char_count > 100:
            st.success(f"✨ Ready to analyze ({char_count} characters)")
        elif char_count > 30:
            st.info(f"⏳ Keep writing... ({char_count} characters)")
        else:
            st.caption("💡 Share at least 30 characters to begin")
    
    with col2:
        if st.button("🧠 Analyze", type="primary", disabled=char_count < 30, use_container_width=True):
            st.session_state.step = 'processing'
            st.rerun()

# Step 2: AI Processing
def render_processing():
    st.markdown("""
    <div class="processing-container">
        <div class="processing-icon">🪶</div>
        <div class="processing-title">Y is perceiving...</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Processing steps
    steps = [
        ("Reading your story...", 0.15),
        ("Identifying narrative layers...", 0.30),
        ("Sensing somatic markers...", 0.45),
        ("Finding hidden details...", 0.60),
        ("Capturing synesthetic qualities...", 0.75),
        ("Listening to temporal rhythms...", 0.90),
        ("Distilling essence...", 1.0)
    ]
    
    progress_bar = st.progress(0)
    status_container = st.empty()
    
    for step_text, progress in steps:
        status_container.markdown(f'<div class="processing-step">{step_text}</div>', unsafe_allow_html=True)
        progress_bar.progress(progress)
        time.sleep(0.8)
    
    # Extract layers with AI
    try:
        st.session_state.extracted_layers = extract_layers_with_ai(st.session_state.raw_story)
        
        # Extract essence
        combined = "\n\n".join([f"{k.title()}: {v}" for k, v in st.session_state.extracted_layers.items()])
        essence_prompt = f"Extract exactly 3 words that capture the essence:\n\n{combined}\n\nReturn only 3 words separated by periods."
        
        essence_text = claude_client.generate_response(essence_prompt, max_tokens=50)
        words = [w.strip().strip('.').strip() for w in essence_text.replace(',', '.').split('.') if w.strip()]
        st.session_state.distilled_essence = words[:3] if len(words) >= 3 else ["Wisdom", "Insight", "Truth"]
        
        # Calculate quality
        st.session_state.quality_scores = quality_calculator.calculate_all_metrics(
            st.session_state.raw_story,
            st.session_state.extracted_layers,
            st.session_state.distilled_essence
        )
        
    except Exception as e:
        st.error(f"Processing error: {e}")
        st.session_state.extracted_layers = {}
        st.session_state.distilled_essence = ["Wisdom", "Insight", "Truth"]
    
    st.session_state.step = 'review'
    time.sleep(0.5)
    st.rerun()

# Step 3: Perception Map Review
def render_perception_map():
    st.markdown('<div class="story-title" style="text-align: center; margin-bottom: 2rem;">Perception Map</div>', unsafe_allow_html=True)
    
    # Display essence
    essence_text = ". ".join(st.session_state.distilled_essence) + "."
    st.markdown(f"""
    <div class="essence-display">
        <div class="essence-words">{essence_text}</div>
        <div class="essence-subtitle">The Vibe Signature</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display extracted layers with edit capability
    st.markdown("### 📝 AI-Extracted Layers")
    st.caption("Review what Y found in your story. Edit if needed.")
    
    layer_info = [
        ("narrative", "📖", "Narrative Layer"),
        ("somatic", "❤️", "Somatic Layer"),
        ("attention", "👁️", "Attention Layer"),
        ("synesthetic", "✨", "Synesthetic Layer"),
        ("temporal", "🎵", "Temporal Layer")
    ]
    
    edited_layers = {}
    
    for layer_id, icon, title in layer_info:
        with st.expander(f"{icon} {title}", expanded=True):
            content = st.session_state.extracted_layers.get(layer_id, "")
            edited_content = st.text_area(
                f"Edit {title}",
                value=content,
                height=100,
                key=f"edit_{layer_id}",
                label_visibility="collapsed"
            )
            edited_layers[layer_id] = edited_content
    
    # Update session state with edits
    st.session_state.extracted_layers = edited_layers
    
    # Quality scores
    if st.session_state.quality_scores:
        with st.expander("📊 Quality Metrics"):
            col1, col2 = st.columns(2)
            
            with col1:
                overall = st.session_state.quality_scores.get('overall', 0)
                grade = quality_calculator.get_quality_grade(overall)
                st.metric("Overall Score", f"{overall:.3f}", f"Grade: {grade.split('(')[0].strip()}")
            
            with col2:
                for metric, score in st.session_state.quality_scores.items():
                    if metric != "overall":
                        st.caption(f"{metric.replace('_', ' ').title()}: {score:.2f}")
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← Back to Story", use_container_width=True):
            st.session_state.step = 'canvas'
            st.rerun()
    
    with col2:
        if st.button("🔄 Re-analyze", use_container_width=True):
            st.session_state.step = 'processing'
            st.rerun()
    
    with col3:
        if st.button("Sign Protocol →", type="primary", use_container_width=True):
            st.session_state.step = 'consent'
            st.rerun()

# Step 4: Z-Protocol Consent
def render_consent():
    st.markdown('<div class="story-title" style="text-align: center; margin-bottom: 1rem;">Z-Protocol</div>', unsafe_allow_html=True)
    st.markdown('<div class="story-subtitle" style="text-align: center; margin-bottom: 2rem;">Choose how your wisdom will be shared and protected.</div>', unsafe_allow_html=True)
    
    essence_text = ". ".join(st.session_state.distilled_essence) + "."
    st.info(f"✨ Your essence: **{essence_text}**")
    
    # Tier selection
    for tier in CONSENT_TIERS:
        is_selected = st.session_state.selected_tier == tier['id']
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(
                f"{tier['icon']} {tier['name']} - {tier['description']}",
                key=f"tier_{tier['id']}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.selected_tier = tier['id']
                st.rerun()
        
        with col2:
            st.markdown(f"**{tier['revenue_share']}**")
        
        if is_selected:
            st.success(f"✓ {tier['protection_level']}")
    
    st.markdown("---")
    
    if st.button("🔒 Sign & Mint", type="primary", use_container_width=True):
        st.session_state.step = 'minting'
        st.rerun()

# Step 5: Minting
def render_minting():
    st.markdown("""
    <div class="processing-container">
        <div class="processing-icon">🔒</div>
        <div class="processing-title">Minting Wisdom Asset...</div>
    </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = ["Hashing content...", "Assigning DID...", "Signing asset...", "Storing attribution..."]
    
    for i, stage in enumerate(stages):
        status_text.markdown(f'<div class="processing-step">{stage}</div>', unsafe_allow_html=True)
        progress_bar.progress((i + 1) / len(stages))
        time.sleep(0.5)
    
    # Create attribution
    try:
        user_id = f"user_{int(time.time())}"
        
        attribution_data = attribution_engine.create_wisdom_asset(
            user_id=user_id,
            raw_story=st.session_state.raw_story,
            layer_responses=st.session_state.extracted_layers,
            distilled_essence=st.session_state.distilled_essence,
            consent_tier=st.session_state.selected_tier,
            quality_scores=st.session_state.quality_scores
        )
        
        st.session_state.attribution_data = attribution_data
        st.session_state.step = 'complete'
        time.sleep(0.5)
        st.rerun()
        
    except Exception as e:
        st.error(f"Minting error: {e}")
        time.sleep(2)
        st.rerun()

# Step 6: Complete
def render_complete():
    st.success("✅ Wisdom Asset Minted Successfully!")
    
    if st.session_state.attribution_data:
        data = st.session_state.attribution_data
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Asset ID", data['asset_id'][:16] + "...")
        with col2:
            st.metric("Revenue Share", data['revenue_share'])
        with col3:
            st.metric("Training Ready", "✅" if data['training_ready'] else "⏳")
        
        essence_text = ". ".join(data['distilled_essence']) + "."
        st.markdown(f"""
        <div class="essence-display">
            <div class="essence-words">{essence_text}</div>
            <div class="essence-subtitle">Your Vibe Signature</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 View Attribution Proof"):
            st.json({
                "asset_id": data['asset_id'],
                "author_did": data['author_did'],
                "fingerprint": data['fingerprint'],
                "signature": data['signature'],
                "consent_tier": data['consent_tier'],
                "created_at": data['created_at']
            })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download JSON", use_container_width=True):
            st.download_button(
                "Download",
                data=json.dumps(st.session_state.attribution_data, indent=2),
                file_name=f"{st.session_state.attribution_data['asset_id']}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("✨ Share Another", type="primary", use_container_width=True):
            st.session_state.step = 'canvas'
            st.session_state.raw_story = ''
            st.session_state.extracted_layers = {}
            st.session_state.distilled_essence = []
            st.session_state.selected_tier = 'tier1'
            st.session_state.attribution_data = None
            st.rerun()

# Main App Router
def main():
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; padding: 2rem 0;"><h1 style="font-family: Georgia, serif; font-size: 2.5rem; margin: 0;">🪶 YSenseAI</h1><p style="color: #64748b; margin: 0.5rem 0 0 0;">The Wisdom Protocol | 慧觉™</p></div>', unsafe_allow_html=True)
    
    # Route to appropriate step
    if st.session_state.step == 'canvas':
        render_story_canvas()
    elif st.session_state.step == 'processing':
        render_processing()
    elif st.session_state.step == 'review':
        render_perception_map()
    elif st.session_state.step == 'consent':
        render_consent()
    elif st.session_state.step == 'minting':
        render_minting()
    elif st.session_state.step == 'complete':
        render_complete()

if __name__ == "__main__":
    main()
