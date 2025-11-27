"""
YSenseAI v4.5-Beta V2.1: Story-First with Collaborative Distillation
User writes freely, AI extracts layers, then collaborative dialogue on 3 words
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

# Custom CSS (same as V2 plus chat styles)
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
    
    /* Chat Interface */
    .chat-container {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 0.75rem;
    }
    
    .chat-message.ai {
        background: #f0f9ff;
        border-left: 4px solid #4c1d95;
    }
    
    .chat-message.user {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
    
    .chat-sender {
        font-weight: 600;
        font-size: 0.875rem;
        margin-bottom: 0.5rem;
        color: #1e293b;
    }
    
    .chat-content {
        color: #475569;
        line-height: 1.6;
    }
    
    /* Word Chips */
    .word-chip {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        margin: 0.25rem;
        background: white;
        border: 2px solid #4c1d95;
        border-radius: 9999px;
        font-family: 'Georgia', serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #4c1d95;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .word-chip:hover {
        background: #4c1d95;
        color: white;
        transform: scale(1.05);
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
if 'suggested_words' not in st.session_state:
    st.session_state.suggested_words = []
if 'distilled_essence' not in st.session_state:
    st.session_state.distilled_essence = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
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
    """Use Claude to automatically extract all 5 perception layers"""
    
    prompt = f"""You are Y, the wisdom extraction agent for YSenseAI. Analyze this story and extract insights across 5 perception layers.

Story:
{story}

Extract these 5 layers. Be specific, poetic, and insightful. Each layer should be 2-4 sentences.

1. NARRATIVE LAYER: What is the unspoken story vs. the well-known story? What cultural or personal narrative is hidden beneath the surface?

2. SOMATIC LAYER: What physical sensations and emotions does this moment evoke? Describe the body's experience - temperature, tension, textures, smells, tastes.

3. ATTENTION LAYER: What is one tiny detail that most people would miss? What micro-observation reveals deeper truth?

4. SYNESTHETIC LAYER: Describe the "vibe" using non-visual sensory words. If this moment had a texture, temperature, or sound quality, what would it be?

5. TEMPORAL LAYER: If this moment had a sound, what would it be? How does time feel here - does it rush, crawl, or stand still?

Return ONLY a JSON object with these exact keys: "narrative", "somatic", "attention", "synesthetic", "temporal"
"""
    
    try:
        response = claude_client.generate_response(prompt, max_tokens=1000)
        response_clean = response.strip()
        if response_clean.startswith("```json"):
            response_clean = response_clean[7:]
        if response_clean.startswith("```"):
            response_clean = response_clean[3:]
        if response_clean.endswith("```"):
            response_clean = response_clean[:-3]
        
        layers = json.loads(response_clean.strip())
        
        required_keys = ["narrative", "somatic", "attention", "synesthetic", "temporal"]
        if all(key in layers for key in required_keys):
            return layers
        else:
            raise ValueError("Missing required keys")
            
    except Exception as e:
        print(f"AI extraction error: {e}")
        return {
            "narrative": f"This story reveals layers of meaning through cultural context and personal experience.",
            "somatic": f"The body experiences warmth, connection, and presence in this moment.",
            "attention": f"Small details interact in unexpected ways, revealing deeper patterns.",
            "synesthetic": f"The vibe feels textured and resonant - like velvet worn smooth by time.",
            "temporal": f"Time moves deliberately here, transforming the ordinary into the sacred."
        }

# AI Word Suggestion Function
def suggest_three_words(story: str, layers: dict) -> list:
    """Use Claude to suggest 3 distillation words"""
    
    combined = f"Story: {story}\n\n" + "\n\n".join([f"{k.title()}: {v}" for k, v in layers.items()])
    
    prompt = f"""You are Y, the wisdom distillation agent. Based on this story and its perception layers, suggest exactly 3 words that capture the essence.

{combined}

Requirements:
- Choose words that resonate emotionally and culturally
- Each word should be a single noun, verb, or adjective
- Words should work together to create a "vibe signature"
- Avoid generic words like "wisdom", "insight", "knowledge"
- Choose specific, evocative words

Return ONLY 3 words separated by periods, like: "Patience. Tradition. Alchemy."
"""
    
    try:
        response = claude_client.generate_response(prompt, max_tokens=50)
        words = [w.strip().strip('.').strip() for w in response.replace(',', '.').split('.') if w.strip()]
        return words[:3] if len(words) >= 3 else ["Patience", "Tradition", "Alchemy"]
    except Exception as e:
        print(f"Word suggestion error: {e}")
        return ["Patience", "Tradition", "Alchemy"]

# AI Conversation Function
def chat_about_words(user_message: str, current_words: list, story: str, layers: dict) -> str:
    """Have a conversation with user about the 3 words"""
    
    context = f"""You are Y, helping a user refine their 3-word essence distillation.

Story: {story}

Current 3 words: {'. '.join(current_words)}

User's question/feedback: {user_message}

Respond thoughtfully:
- If they ask why you chose a word, explain the reasoning
- If they suggest a different word, validate their insight and explain how it fits
- If they're unsure, offer 2-3 alternative words with brief explanations
- Keep responses concise (2-3 sentences)
- Be encouraging and collaborative

Your response:"""
    
    try:
        response = claude_client.generate_response(context, max_tokens=200)
        return response.strip()
    except Exception as e:
        return "I understand your perspective. What word feels more authentic to you?"

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
    
    # Extract layers and suggest words
    try:
        st.session_state.extracted_layers = extract_layers_with_ai(st.session_state.raw_story)
        st.session_state.suggested_words = suggest_three_words(st.session_state.raw_story, st.session_state.extracted_layers)
        st.session_state.distilled_essence = st.session_state.suggested_words.copy()
        
        # Initialize chat with AI's suggestion
        st.session_state.chat_history = [{
            "sender": "ai",
            "message": f"I sense the essence of your story as: **{'. '.join(st.session_state.suggested_words)}**\n\nDoes this resonate with you? Feel free to discuss or suggest changes."
        }]
        
    except Exception as e:
        st.error(f"Processing error: {e}")
        st.session_state.extracted_layers = {}
        st.session_state.suggested_words = ["Patience", "Tradition", "Alchemy"]
        st.session_state.distilled_essence = ["Patience", "Tradition", "Alchemy"]
    
    st.session_state.step = 'distillation'
    time.sleep(0.5)
    st.rerun()

# Step 3: Collaborative Distillation
def render_collaborative_distillation():
    st.markdown('<div class="story-title" style="text-align: center; margin-bottom: 1rem;">Distillation Dialogue</div>', unsafe_allow_html=True)
    st.markdown('<div class="story-subtitle" style="text-align: center; margin-bottom: 2rem;">Refine your 3-word essence through conversation with Y</div>', unsafe_allow_html=True)
    
    # Display current words
    st.markdown("### Your Current Essence")
    essence_html = " ".join([f'<span class="word-chip">{word}</span>' for word in st.session_state.distilled_essence])
    st.markdown(f'<div style="text-align: center; margin: 1rem 0;">{essence_html}</div>', unsafe_allow_html=True)
    
    # Chat history
    st.markdown("### Conversation with Y")
    chat_container = st.container()
    
    with chat_container:
        for chat in st.session_state.chat_history:
            sender_label = "🪶 Y (AI)" if chat['sender'] == 'ai' else "👤 You"
            st.markdown(f"""
            <div class="chat-message {chat['sender']}">
                <div class="chat-sender">{sender_label}</div>
                <div class="chat-content">{chat['message']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # User input
    st.markdown("### Your Thoughts")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask Y or suggest changes",
            placeholder="Why did you choose 'Patience'? I felt it was more about 'Surrender'...",
            key="user_chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("💬 Send", use_container_width=True)
    
    if send_button and user_input:
        # Add user message
        st.session_state.chat_history.append({
            "sender": "user",
            "message": user_input
        })
        
        # Get AI response
        ai_response = chat_about_words(
            user_input,
            st.session_state.distilled_essence,
            st.session_state.raw_story,
            st.session_state.extracted_layers
        )
        
        st.session_state.chat_history.append({
            "sender": "ai",
            "message": ai_response
        })
        
        st.rerun()
    
    # Manual word editing
    st.markdown("---")
    st.markdown("### Edit Words Directly")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        word1 = st.text_input("Word 1", value=st.session_state.distilled_essence[0] if len(st.session_state.distilled_essence) > 0 else "", key="word1")
    with col2:
        word2 = st.text_input("Word 2", value=st.session_state.distilled_essence[1] if len(st.session_state.distilled_essence) > 1 else "", key="word2")
    with col3:
        word3 = st.text_input("Word 3", value=st.session_state.distilled_essence[2] if len(st.session_state.distilled_essence) > 2 else "", key="word3")
    
    if st.button("💾 Update Words", use_container_width=True):
        st.session_state.distilled_essence = [word1, word2, word3]
        st.success("✅ Words updated!")
        time.sleep(0.5)
        st.rerun()
    
    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Back to Story", use_container_width=True):
            st.session_state.step = 'canvas'
            st.rerun()
    
    with col2:
        if st.button("Finalize Essence →", type="primary", use_container_width=True):
            # Calculate quality metrics
            st.session_state.quality_scores = quality_calculator.calculate_all_metrics(
                st.session_state.raw_story,
                st.session_state.extracted_layers,
                st.session_state.distilled_essence
            )
            st.session_state.step = 'consent'
            st.rerun()

# Step 4: Z-Protocol Consent
def render_consent():
    st.markdown('<div class="story-title" style="text-align: center; margin-bottom: 1rem;">Z-Protocol</div>', unsafe_allow_html=True)
    st.markdown('<div class="story-subtitle" style="text-align: center; margin-bottom: 2rem;">Choose how your wisdom will be shared and protected.</div>', unsafe_allow_html=True)
    
    essence_text = ". ".join(st.session_state.distilled_essence) + "."
    st.markdown(f"""
    <div class="essence-display">
        <div class="essence-words">{essence_text}</div>
        <div class="essence-subtitle">Your Finalized Essence</div>
    </div>
    """, unsafe_allow_html=True)
    
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
        
        # Add chat history to attribution
        attribution_data['distillation_dialogue'] = st.session_state.chat_history
        
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
        
        with st.expander("💬 View Distillation Dialogue"):
            for chat in st.session_state.chat_history:
                sender_label = "🪶 Y" if chat['sender'] == 'ai' else "👤 You"
                st.markdown(f"**{sender_label}**: {chat['message']}")
        
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
            st.session_state.suggested_words = []
            st.session_state.distilled_essence = []
            st.session_state.chat_history = []
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
    elif st.session_state.step == 'distillation':
        render_collaborative_distillation()
    elif st.session_state.step == 'consent':
        render_consent()
    elif st.session_state.step == 'minting':
        render_minting()
    elif st.session_state.step == 'complete':
        render_complete()

if __name__ == "__main__":
    main()
