"""
YSenseAI v4.5-Beta: Complete Application
5-Layer Perception + AI Distillation + Z-Protocol + Attribution + Quality Metrics
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
from agents.qwen_integration_v45 import QWENClient
from attribution.attribution_engine import AttributionEngine
from attribution.quality_metrics import QualityMetricsCalculator

# Page configuration
st.set_page_config(
    page_title="YSenseAI v4.5-Beta | 慧觉™",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (same as before, keeping it concise)
st.markdown(f"""
<style>
    .stApp {{ background-color: {UI_CONFIG['colors']['background']}; }}
    .ysense-header {{ display: flex; justify-content: space-between; padding: 1.5rem 0; }}
    .essence-display {{ text-align: center; padding: 2rem; background: white; 
                       border: 2px solid #1e293b; border-radius: 1.5rem; margin: 2rem 0; }}
    .essence-words {{ font-family: Georgia, serif; font-size: 2.5rem; font-weight: bold; }}
    .metric-card {{ background: white; padding: 1.5rem; border-radius: 1rem; 
                   border: 1px solid #e2e8f0; margin-bottom: 1rem; }}
    .quality-badge {{ display: inline-block; padding: 0.5rem 1rem; border-radius: 9999px;
                     font-weight: 600; font-size: 0.875rem; }}
    .grade-a {{ background: #d1fae5; color: #065f46; }}
    .grade-b {{ background: #dbeafe; color: #1e40af; }}
    .grade-c {{ background: #fef3c7; color: #92400e; }}
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
if 'quality_scores' not in st.session_state:
    st.session_state.quality_scores = {}
if 'attribution_data' not in st.session_state:
    st.session_state.attribution_data = None
if 'all_submissions' not in st.session_state:
    st.session_state.all_submissions = []

# Initialize components
@st.cache_resource
def get_components():
    """Initialize all components (cached)"""
    claude = AnthropicClient()
    qwen = QWENClient()
    attribution_engine = AttributionEngine()
    quality_calculator = QualityMetricsCalculator()
    return claude, qwen, attribution_engine, quality_calculator

claude_client, qwen_client, attribution_engine, quality_calculator = get_components()

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🪶 YSenseAI v4.5-Beta")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        ["✨ New Wisdom", "📊 Dashboard", "📚 My Submissions", "ℹ️ About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("**Z-Protocol Active** 🛡️")
    st.caption(f"Total Submissions: {len(st.session_state.all_submissions)}")
    
    if st.session_state.all_submissions:
        total_quality = sum(s.get('quality_scores', {}).get('overall', 0) 
                           for s in st.session_state.all_submissions)
        avg_quality = total_quality / len(st.session_state.all_submissions)
        st.caption(f"Avg Quality: {avg_quality:.2f}")

# Header
def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# 🪶 YSenseAI")
        st.caption("The Wisdom Protocol | 慧觉™")
    with col2:
        st.markdown("**v4.5-Beta**")
        st.caption("Z-Protocol v2.0")

# Main content router
if menu == "✨ New Wisdom":
    if st.session_state.step == 'story':
        render_header()
        
        st.markdown("## What is the story only you know?")
        st.markdown("A fleeting moment, a cultural memory, or a quiet realization. Share it raw. **Y will find the wisdom inside.**")
        
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
                st.success(f"✨ Ready ({len(story)} characters)")
            else:
                st.info("⏳ Waiting for input...")
        
        with col2:
            if st.button("🧠 Begin Perception", type="primary", disabled=len(story) < 30):
                st.session_state.step = 'layers'
                st.session_state.current_layer = 0
                st.rerun()
    
    elif st.session_state.step == 'layers':
        render_header()
        
        layer = PERCEPTION_LAYERS[st.session_state.current_layer]
        
        st.markdown(f"### {layer['icon']} {layer['title']}")
        st.markdown(f"*{layer['question']}*")
        
        response = st.text_area(
            "Your Response",
            value=st.session_state.layer_responses.get(layer['id'], ''),
            height=180,
            placeholder=layer['placeholder'],
            label_visibility="collapsed"
        )
        
        st.session_state.layer_responses[layer['id']] = response
        
        st.caption(f"💡 {layer['description']}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.current_layer > 0:
                if st.button("← Previous"):
                    st.session_state.current_layer -= 1
                    st.rerun()
        
        with col2:
            st.info(f"Layer {st.session_state.current_layer + 1} of {len(PERCEPTION_LAYERS)}")
        
        with col3:
            if st.session_state.current_layer < len(PERCEPTION_LAYERS) - 1:
                if st.button("Next →", type="primary", disabled=len(response) < 20):
                    st.session_state.current_layer += 1
                    st.rerun()
            else:
                if st.button("Process ✨", type="primary", disabled=len(response) < 20):
                    st.session_state.step = 'processing'
                    st.rerun()
    
    elif st.session_state.step == 'processing':
        render_header()
        
        st.markdown("## Y is perceiving...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = ["Dissolving context...", "Sensing body...", "Finding spark...", 
                 "Listening to time...", "Calculating quality...", "Minting wisdom..."]
        
        for i, stage in enumerate(stages):
            status_text.markdown(f"**{stage}**")
            progress_bar.progress((i + 1) / len(stages))
            time.sleep(0.6)
        
        # AI Distillation
        try:
            combined = "\n\n".join([f"{l['title']}: {st.session_state.layer_responses.get(l['id'], '')}" 
                                   for l in PERCEPTION_LAYERS])
            
            if not claude_client.use_fallback:
                prompt = f"Extract exactly 3 words that capture the essence:\n\n{combined}\n\nReturn only 3 words."
                essence_text = claude_client.generate_response(prompt)
                words = [w.strip().strip('.').strip() for w in essence_text.replace(',', '.').split('.') if w.strip()]
                st.session_state.distilled_essence = words[:3] if len(words) >= 3 else ["Wisdom", "Insight", "Truth"]
            else:
                st.session_state.distilled_essence = ["Wisdom", "Insight", "Truth"]
            
            # Calculate quality metrics
            st.session_state.quality_scores = quality_calculator.calculate_all_metrics(
                st.session_state.raw_story,
                st.session_state.layer_responses,
                st.session_state.distilled_essence
            )
            
            st.session_state.step = 'review'
            time.sleep(0.5)
            st.rerun()
            
        except Exception as e:
            st.error(f"Processing error: {e}")
            st.session_state.distilled_essence = ["Wisdom", "Insight", "Truth"]
            st.session_state.quality_scores = {}
            time.sleep(2)
            st.rerun()
    
    elif st.session_state.step == 'review':
        render_header()
        
        st.markdown("## Perception Map")
        
        # Display essence
        essence_text = ". ".join(st.session_state.distilled_essence) + "."
        st.markdown(f"""
        <div class="essence-display">
            <div class="essence-words">{essence_text}</div>
            <div style="color: #94a3b8; font-size: 0.875rem; margin-top: 0.5rem;">The Vibe Signature</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quality scores
        if st.session_state.quality_scores:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Quality Metrics")
                for metric, score in st.session_state.quality_scores.items():
                    if metric != "overall":
                        st.progress(score, text=f"{metric.replace('_', ' ').title()}: {score:.2f}")
            
            with col2:
                overall = st.session_state.quality_scores.get('overall', 0)
                grade = quality_calculator.get_quality_grade(overall)
                
                st.markdown("### 🎯 Overall Quality")
                st.metric("Score", f"{overall:.3f}", f"Grade: {grade.split('(')[0].strip()}")
                
                recommendations = quality_calculator.get_recommendations(st.session_state.quality_scores)
                st.markdown("**Recommendations:**")
                for rec in recommendations:
                    st.caption(rec)
        
        # Layers
        st.markdown("### 📝 Your Layers")
        for layer in PERCEPTION_LAYERS:
            with st.expander(f"{layer['icon']} {layer['title']}"):
                st.write(st.session_state.layer_responses.get(layer['id'], ''))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ Edit Layers"):
                st.session_state.step = 'layers'
                st.session_state.current_layer = 0
                st.rerun()
        
        with col2:
            if st.button("Proceed to Consent →", type="primary"):
                st.session_state.step = 'consent'
                st.rerun()
    
    elif st.session_state.step == 'consent':
        render_header()
        
        st.markdown("## Z-Protocol Classification")
        st.markdown("Choose how your wisdom will be shared and protected.")
        
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
                st.success(f"✓ Protection: {tier['protection_level']}")
        
        st.markdown("---")
        
        if st.button("🔒 Sign & Mint Wisdom Asset", type="primary", use_container_width=True):
            st.session_state.step = 'minting'
            st.rerun()
    
    elif st.session_state.step == 'minting':
        render_header()
        
        st.markdown("## Minting Wisdom Asset...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = ["Hashing content...", "Assigning DID...", "Signing asset...", "Storing attribution..."]
        
        for i, stage in enumerate(stages):
            status_text.text(stage)
            progress_bar.progress((i + 1) / len(stages))
            time.sleep(0.4)
        
        # Create attribution
        try:
            user_id = f"user_{int(time.time())}"
            
            attribution_data = attribution_engine.create_wisdom_asset(
                user_id=user_id,
                raw_story=st.session_state.raw_story,
                layer_responses=st.session_state.layer_responses,
                distilled_essence=st.session_state.distilled_essence,
                consent_tier=st.session_state.selected_tier,
                quality_scores=st.session_state.quality_scores
            )
            
            st.session_state.attribution_data = attribution_data
            st.session_state.all_submissions.append(attribution_data)
            
            st.session_state.step = 'complete'
            time.sleep(0.5)
            st.rerun()
            
        except Exception as e:
            st.error(f"Minting error: {e}")
            time.sleep(2)
            st.rerun()
    
    elif st.session_state.step == 'complete':
        render_header()
        
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
                <div style="color: #94a3b8; font-size: 0.875rem; margin-top: 0.5rem;">Your Vibe Signature</div>
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
            if st.button("✨ Submit Another", type="primary", use_container_width=True):
                st.session_state.step = 'story'
                st.session_state.raw_story = ''
                st.session_state.current_layer = 0
                st.session_state.layer_responses = {}
                st.session_state.distilled_essence = []
                st.session_state.selected_tier = 'tier1'
                st.session_state.attribution_data = None
                st.rerun()

elif menu == "📊 Dashboard":
    render_header()
    
    st.markdown("## Platform Dashboard")
    
    if not st.session_state.all_submissions:
        st.info("No submissions yet. Create your first wisdom!")
    else:
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Submissions", len(st.session_state.all_submissions))
        
        with col2:
            training_ready = sum(1 for s in st.session_state.all_submissions if s.get('training_ready'))
            st.metric("Training Ready", training_ready)
        
        with col3:
            avg_quality = sum(s.get('quality_scores', {}).get('overall', 0) 
                            for s in st.session_state.all_submissions) / len(st.session_state.all_submissions)
            st.metric("Avg Quality", f"{avg_quality:.2f}")
        
        with col4:
            # Mock revenue
            mock_revenue = len(st.session_state.all_submissions) * 5.0
            st.metric("Est. Revenue", f"€{mock_revenue:.2f}")
        
        # Leaderboard
        st.markdown("### 🏆 Quality Leaderboard")
        sorted_submissions = sorted(st.session_state.all_submissions, 
                                   key=lambda x: x.get('quality_scores', {}).get('overall', 0), 
                                   reverse=True)
        
        for i, submission in enumerate(sorted_submissions[:5]):
            essence = ". ".join(submission.get('distilled_essence', []))
            quality = submission.get('quality_scores', {}).get('overall', 0)
            grade = quality_calculator.get_quality_grade(quality)
            
            st.markdown(f"**#{i+1}** {essence} - Score: {quality:.2f} ({grade.split('(')[0].strip()})")

elif menu == "📚 My Submissions":
    render_header()
    
    st.markdown("## My Submissions")
    
    if not st.session_state.all_submissions:
        st.info("No submissions yet.")
    else:
        for submission in reversed(st.session_state.all_submissions):
            with st.expander(f"{'. '.join(submission['distilled_essence'])} - {submission['asset_id'][:12]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Created:** {submission['created_at']}")
                    st.markdown(f"**Tier:** {submission['consent_tier']}")
                    st.markdown(f"**Revenue Share:** {submission['revenue_share']}")
                with col2:
                    quality = submission.get('quality_scores', {}).get('overall', 0)
                    st.markdown(f"**Quality:** {quality:.2f}")
                    st.markdown(f"**Training Ready:** {'✅' if submission['training_ready'] else '⏳'}")
                
                if st.button(f"View Full Details", key=submission['asset_id']):
                    st.json(submission)

elif menu == "ℹ️ About":
    render_header()
    
    st.markdown("## About YSenseAI v4.5-Beta")
    
    st.markdown("""
    ### The Wisdom Protocol
    
    YSenseAI is building the future of AI training data - **structured wisdom** that captures:
    
    - **5-Layer Perception**: Narrative, Somatic, Attention, Synesthetic, Temporal
    - **AI Distillation**: 3-word essence extraction
    - **Z-Protocol Consent**: 3-tier revenue sharing (15-30%)
    - **Cryptographic Attribution**: DID + fingerprinting
    - **Quality Optimization**: 6 training metrics
    - **Training-Ready Export**: Alpaca/ShareGPT format
    
    ### Core Pillars
    
    ✅ **Consent** - You choose how your wisdom is shared  
    ✅ **Transparency** - Full attribution proof visible  
    ✅ **Revenue Compensation** - Fair revenue sharing  
    ✅ **Attribution** - Cryptographic ownership  
    ✅ **Quality Data** - Training-optimized format  
    ✅ **Wisdom Data** - Cultural & emotional richness  
    🔄 **Decentralize** - IPFS/Arweave (Phase 2)  
    🔄 **Blockchain** - Smart contracts (Phase 2)  
    
    ### Vision
    
    📜 Consent → 🙏 Wisdom Data → 🧐 Attribution → 🔗 Decentralize → 👩‍🔬 Fine-tuning → 🤖 Iteration → 🔄 Loop
    
    **Target**: €15,000 Q1 2026 revenue through ethical AI training data marketplace.
    """)

if __name__ == "__main__":
    pass
