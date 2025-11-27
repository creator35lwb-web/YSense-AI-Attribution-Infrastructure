"""
YSenseAI v4.5-Beta: Main Streamlit Application
5-Layer Perception Toolkit + AI Distillation + Z-Protocol Consent
"""

import streamlit as st
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
import sys

# Add agents directory to path
sys.path.append(str(Path(__file__).parent / "agents"))
sys.path.append(str(Path(__file__).parent / "ui"))

from ui.layer_config import PERCEPTION_LAYERS, CONSENT_TIERS, UI_CONFIG, TRAINING_FORMAT_TEMPLATE
from agents.anthropic_integration_v45 import YSenseOrchestrator as ClaudeOrchestrator
from agents.qwen_integration_v45 import YSenseOrchestrator as QwenOrchestrator

# Page configuration
st.set_page_config(
    page_title="YSenseAI v4.5-Beta | 慧觉™",
    page_icon="🪶",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown(f"""
<style>
    /* Global Styles */
    .stApp {{
        background-color: {UI_CONFIG['colors']['background']};
        font-family: {UI_CONFIG['fonts']['body']};
    }}
    
    /* Header */
    .ysense-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
    }}
    
    .ysense-logo {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .ysense-logo-icon {{
        background: {UI_CONFIG['colors']['text']};
        color: white;
        padding: 0.5rem;
        border-radius: 0.75rem;
        font-size: 1.25rem;
    }}
    
    .ysense-logo-text {{
        font-family: {UI_CONFIG['fonts']['heading']};
        font-size: 1.5rem;
        font-weight: bold;
        color: {UI_CONFIG['colors']['text']};
    }}
    
    .z-protocol-badge {{
        background: #d1fae5;
        color: #065f46;
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid #a7f3d0;
    }}
    
    /* Layer Cards */
    .layer-card {{
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    .layer-header {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
        color: {UI_CONFIG['colors']['primary']};
    }}
    
    .layer-icon {{
        font-size: 1.5rem;
    }}
    
    .layer-title {{
        font-size: 1.125rem;
        font-weight: bold;
    }}
    
    .layer-question {{
        font-family: {UI_CONFIG['fonts']['heading']};
        font-size: 1.25rem;
        font-style: italic;
        color: #64748b;
        margin-bottom: 1.5rem;
    }}
    
    /* Consent Tier Cards */
    .tier-card {{
        border: 2px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .tier-card:hover {{
        border-color: {UI_CONFIG['colors']['primary']};
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .tier-card-selected {{
        border-color: {UI_CONFIG['colors']['primary']};
        background: #f0f9ff;
    }}
    
    .tier-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }}
    
    .tier-name {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: bold;
        font-size: 1.125rem;
    }}
    
    .tier-revenue {{
        background: {UI_CONFIG['colors']['accent']};
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }}
    
    /* Processing Animation */
    .processing-container {{
        text-align: center;
        padding: 3rem 0;
    }}
    
    .processing-spinner {{
        width: 6rem;
        height: 6rem;
        margin: 0 auto 2rem;
        border: 4px solid #e0e7ff;
        border-top-color: {UI_CONFIG['colors']['primary']};
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    
    .processing-stage {{
        font-size: 1.125rem;
        color: {UI_CONFIG['colors']['primary']};
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    
    /* Essence Display */
    .essence-display {{
        text-align: center;
        padding: 2rem;
        background: white;
        border: 2px solid {UI_CONFIG['colors']['text']};
        border-radius: 1.5rem;
        margin: 2rem 0;
    }}
    
    .essence-words {{
        font-family: {UI_CONFIG['fonts']['heading']};
        font-size: 2.5rem;
        font-weight: bold;
        color: {UI_CONFIG['colors']['text']};
        margin-bottom: 0.5rem;
    }}
    
    .essence-subtitle {{
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'story'
if 'raw_story' not in st.session_state:
    st.session_state.raw_story = ''
if 'current_layer' not in st.session_state:
    st.session_state.current_layer = 0
if 'layer_responses' not in st.session_state:
    st.session_state.layer_responses = {}
if 'distilled_essence' not in st.session_state:
    st.session_state.distilled_essence = []
if 'selected_tier' not in st.session_state:
    st.session_state.selected_tier = 'tier1'
if 'attribution_data' not in st.session_state:
    st.session_state.attribution_data = None

# Initialize AI orchestrators
@st.cache_resource
def get_orchestrators():
    """Initialize AI orchestrators (cached)"""
    try:
        claude_orch = ClaudeOrchestrator()
        qwen_orch = QwenOrchestrator()
        return claude_orch, qwen_orch
    except Exception as e:
        st.error(f"Failed to initialize AI orchestrators: {e}")
        return None, None

claude_orchestrator, qwen_orchestrator = get_orchestrators()

# Header
def render_header():
    st.markdown("""
    <div class="ysense-header">
        <div class="ysense-logo">
            <div class="ysense-logo-icon">🪶</div>
            <div class="ysense-logo-text">YSense</div>
        </div>
        <div class="z-protocol-badge">
            🛡️ Z-Protocol Active
        </div>
    </div>
    """, unsafe_allow_html=True)

# Step 1: Story Input
def render_story_input():
    render_header()
    
    st.markdown("""
    <h1 style="font-family: Georgia, serif; font-size: 3rem; font-weight: bold; color: #1e293b; line-height: 1.2; margin-bottom: 1rem;">
        What is the story<br/>
        <span style="color: #94a3b8;">only you know?</span>
    </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="color: #64748b; margin-bottom: 2rem; font-size: 1.125rem; line-height: 1.6;">
        A fleeting moment, a cultural memory, or a quiet realization. 
        Share it raw. <strong style="color: #4c1d95;">Y will find the wisdom inside.</strong>
    </p>
    """, unsafe_allow_html=True)
    
    story = st.text_area(
        "Your Story",
        value=st.session_state.raw_story,
        height=250,
        placeholder="The rain started falling...",
        label_visibility="collapsed"
    )
    
    st.session_state.raw_story = story
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if len(story) > 30:
            st.success(f"✨ Ready to perceive ({len(story)} characters)")
        else:
            st.info("⏳ Waiting for input...")
    
    with col2:
        if st.button("🧠 Distill Wisdom", type="primary", disabled=len(story) < 30, use_container_width=True):
            st.session_state.step = 'layers'
            st.session_state.current_layer = 0
            st.rerun()

# Step 2: Layer-by-Layer Extraction
def render_layer_extraction():
    render_header()
    
    layer = PERCEPTION_LAYERS[st.session_state.current_layer]
    
    st.markdown(f"""
    <div class="layer-card">
        <div class="layer-header">
            <span class="layer-icon">{layer['icon']}</span>
            <span class="layer-title">{layer['title']}</span>
        </div>
        <div class="layer-question">"{layer['question']}"</div>
    </div>
    """, unsafe_allow_html=True)
    
    response = st.text_area(
        f"Your Response",
        value=st.session_state.layer_responses.get(layer['id'], ''),
        height=180,
        placeholder=layer['placeholder'],
        label_visibility="collapsed",
        key=f"layer_{layer['id']}"
    )
    
    st.session_state.layer_responses[layer['id']] = response
    
    st.caption(f"💡 {layer['description']} • Optimal: {layer['optimal_length']}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_layer > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_layer -= 1
                st.rerun()
    
    with col2:
        st.info(f"Layer {st.session_state.current_layer + 1} of {len(PERCEPTION_LAYERS)}")
    
    with col3:
        if st.session_state.current_layer < len(PERCEPTION_LAYERS) - 1:
            if st.button("Next →", type="primary", disabled=len(response) < 20, use_container_width=True):
                st.session_state.current_layer += 1
                st.rerun()
        else:
            if st.button("Process ✨", type="primary", disabled=len(response) < 20, use_container_width=True):
                st.session_state.step = 'processing'
                st.rerun()

# Step 3: AI Processing
def render_processing():
    render_header()
    
    st.markdown("""
    <div class="processing-container">
        <div class="processing-spinner"></div>
        <h2 style="font-family: Georgia, serif; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">
            Y is perceiving...
        </h2>
        <p style="color: #94a3b8; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em;">
            AI-Assisted Reflection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate processing stages
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = UI_CONFIG['animations']['processing_stages']
    
    for i, stage in enumerate(stages):
        status_text.markdown(f"<div class='processing-stage'>{stage}</div>", unsafe_allow_html=True)
        progress_bar.progress((i + 1) / len(stages))
        time.sleep(0.8)
    
    # Call AI to distill essence
    try:
        # Combine all layer responses
        combined_wisdom = "\n\n".join([
            f"{layer['title']}: {st.session_state.layer_responses.get(layer['id'], '')}"
            for layer in PERCEPTION_LAYERS
        ])
        
        # Use Claude (Y agent) to distill essence
        if claude_orchestrator:
            prompt = f"""Extract the core essence of this wisdom in exactly 3 words.

{combined_wisdom}

Return only 3 words separated by periods, like: "Patience. Tradition. Alchemy."
"""
            essence_text = claude_orchestrator.agents['y_strategy'].generate_response(
                "Extract 3-word essence from wisdom layers",
                {"wisdom": combined_wisdom}
            )
            
            # Parse essence (handle various formats)
            essence_words = [w.strip().strip('.').strip() for w in essence_text.split('.') if w.strip()]
            if len(essence_words) >= 3:
                st.session_state.distilled_essence = essence_words[:3]
            else:
                # Fallback
                st.session_state.distilled_essence = ["Wisdom", "Insight", "Truth"]
        else:
            # Fallback if AI not available
            st.session_state.distilled_essence = ["Wisdom", "Insight", "Truth"]
        
        st.session_state.step = 'review'
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Processing error: {e}")
        st.session_state.distilled_essence = ["Wisdom", "Insight", "Truth"]
        st.session_state.step = 'review'
        time.sleep(2)
        st.rerun()

# Step 4: Review Perception Map
def render_review():
    render_header()
    
    st.markdown("""
    <h2 style="font-family: Georgia, serif; font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">
        Perception Map
    </h2>
    <p style="color: #64748b; margin-bottom: 2rem;">
        Your story, seen through the 5 layers.
    </p>
    """, unsafe_allow_html=True)
    
    # Display essence
    essence_text = ". ".join(st.session_state.distilled_essence) + "."
    st.markdown(f"""
    <div class="essence-display">
        <div class="essence-words">{essence_text}</div>
        <div class="essence-subtitle">The Vibe Signature</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display all layers
    for layer in PERCEPTION_LAYERS:
        with st.expander(f"{layer['icon']} {layer['title']}", expanded=False):
            st.markdown(f"**{layer['question']}**")
            st.write(st.session_state.layer_responses.get(layer['id'], ''))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ Edit Layers", use_container_width=True):
            st.session_state.step = 'layers'
            st.session_state.current_layer = 0
            st.rerun()
    
    with col2:
        if st.button("Proceed to Consent →", type="primary", use_container_width=True):
            st.session_state.step = 'consent'
            st.rerun()

# Step 5: Z-Protocol Consent
def render_consent():
    render_header()
    
    st.markdown("""
    <h2 style="font-family: Georgia, serif; font-size: 2.5rem; font-weight: bold; margin-bottom: 0.5rem;">
        Z-Protocol Classification
    </h2>
    <p style="color: #64748b; margin-bottom: 2rem;">
        Choose how your wisdom will be shared and protected.
    </p>
    """, unsafe_allow_html=True)
    
    # Display essence reminder
    essence_text = ". ".join(st.session_state.distilled_essence) + "."
    st.info(f"✨ Your essence: **{essence_text}**")
    
    # Tier selection
    for tier in CONSENT_TIERS:
        is_selected = st.session_state.selected_tier == tier['id']
        
        if st.button(
            f"{tier['icon']} {tier['name']} ({tier['revenue_share']} revenue share)",
            key=tier['id'],
            use_container_width=True,
            type="primary" if is_selected else "secondary"
        ):
            st.session_state.selected_tier = tier['id']
            st.rerun()
        
        if is_selected:
            st.success(f"✓ {tier['description']}")
            st.caption(f"Protection: {tier['protection_level']} • Use cases: {tier['use_cases']}")
    
    st.markdown("---")
    
    if st.button("🔒 Cryptographically Sign & Mint", type="primary", use_container_width=True):
        st.session_state.step = 'minting'
        st.rerun()

# Step 6: Minting & Attribution
def render_minting():
    render_header()
    
    st.markdown("""
    <div class="processing-container">
        <div class="processing-spinner"></div>
        <h2 style="font-family: Georgia, serif; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">
            Minting Wisdom Asset...
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    stages = ["Hashing content...", "Assigning DID...", "Signing asset...", "Storing attribution..."]
    
    for i, stage in enumerate(stages):
        status_text.text(stage)
        progress_bar.progress((i + 1) / len(stages))
        time.sleep(0.5)
    
    # Create attribution data
    try:
        # Prepare training format
        combined_wisdom = {layer['id']: st.session_state.layer_responses.get(layer['id'], '') 
                          for layer in PERCEPTION_LAYERS}
        
        # Generate content hash
        content_string = json.dumps(combined_wisdom, sort_keys=True)
        content_hash = hashlib.sha256(content_string.encode()).hexdigest()
        asset_id = f"ysense-{content_hash[:12]}"
        
        # Create attribution record
        attribution_data = {
            "asset_id": asset_id,
            "fingerprint": content_hash,
            "author_did": f"did:ysense:user_{int(time.time())}",
            "license": "YSense-Commercial-v1",
            "consent_tier": st.session_state.selected_tier,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "distilled_essence": st.session_state.distilled_essence,
            "layers": combined_wisdom,
            "raw_story": st.session_state.raw_story
        }
        
        st.session_state.attribution_data = attribution_data
        
        # Save to database (placeholder)
        # TODO: Implement actual database storage
        
        st.session_state.step = 'complete'
        time.sleep(1)
        st.rerun()
        
    except Exception as e:
        st.error(f"Minting error: {e}")
        time.sleep(2)
        st.session_state.step = 'consent'
        st.rerun()

# Step 7: Complete
def render_complete():
    render_header()
    
    st.success("✅ Wisdom Asset Minted Successfully!")
    
    st.markdown("""
    <h2 style="font-family: Georgia, serif; font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;">
        Your Wisdom is Protected
    </h2>
    """, unsafe_allow_html=True)
    
    if st.session_state.attribution_data:
        data = st.session_state.attribution_data
        
        st.info(f"**Asset ID**: `{data['asset_id']}`")
        st.caption(f"Created: {data['created_at']}")
        
        essence_text = ". ".join(data['distilled_essence']) + "."
        st.markdown(f"""
        <div class="essence-display">
            <div class="essence-words">{essence_text}</div>
            <div class="essence-subtitle">Your Vibe Signature</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 View Attribution Proof"):
            st.json(data)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download JSON", use_container_width=True):
            st.download_button(
                "Download Attribution Data",
                data=json.dumps(st.session_state.attribution_data, indent=2),
                file_name=f"{st.session_state.attribution_data['asset_id']}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("✨ Submit Another Wisdom", type="primary", use_container_width=True):
            # Reset state
            st.session_state.step = 'story'
            st.session_state.raw_story = ''
            st.session_state.current_layer = 0
            st.session_state.layer_responses = {}
            st.session_state.distilled_essence = []
            st.session_state.selected_tier = 'tier1'
            st.session_state.attribution_data = None
            st.rerun()

# Main App Router
def main():
    if st.session_state.step == 'story':
        render_story_input()
    elif st.session_state.step == 'layers':
        render_layer_extraction()
    elif st.session_state.step == 'processing':
        render_processing()
    elif st.session_state.step == 'review':
        render_review()
    elif st.session_state.step == 'consent':
        render_consent()
    elif st.session_state.step == 'minting':
        render_minting()
    elif st.session_state.step == 'complete':
        render_complete()

if __name__ == "__main__":
    main()
