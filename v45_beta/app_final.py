"""
YSenseAI v4.5-Beta FINAL PRODUCTION
Complete platform ready for ysenseai.org deployment
"""

import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path
import sys
import hashlib

# Add directories to path
sys.path.append(str(Path(__file__).parent))

from agents.anthropic_integration_v45 import AnthropicClient
from attribution.attribution_engine import AttributionEngine
from attribution.quality_metrics import QualityMetricsCalculator
from database.schema import YSenseDatabase
from ui.layer_config import CONSENT_TIERS

# Page configuration
st.set_page_config(
    page_title="YSenseAI | 慧觉™",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #FDFBF7 0%, #F5F3EF 100%); }
    .main-header {
        font-family: 'Georgia', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #1e293b;
        text-align: center;
        margin: 2rem 0;
    }
    .essence-card {
        background: linear-gradient(135deg, #4c1d95 0%, #6d28d9 100%);
        border-radius: 1rem;
        padding: 1.5rem;
        color: white;
        margin: 1rem 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .essence-card:hover { transform: translateY(-4px); }
    .essence-words {
        font-family: 'Georgia', serif;
        font-size: 1.75rem;
        font-weight: bold;
    }
    .stat-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4c1d95;
    }
    .stat-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
    }
    .chat-message.ai {
        background: #f0f9ff;
        border-left: 4px solid #4c1d95;
    }
    .chat-message.user {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    defaults = {
        'authenticated': False,
        'user_id': None,
        'user_email': None,
        'session_token': None,
        'current_page': 'library',
        'submission_step': 'canvas',
        'raw_story': '',
        'extracted_layers': {},
        'suggested_words': [],
        'distilled_essence': [],
        'chat_history': [],
        'selected_tier': 'tier1',
        'quality_scores': {},
        'viewing_submission': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Initialize components
@st.cache_resource
def get_components():
    return (
        AnthropicClient(),
        AttributionEngine(),
        QualityMetricsCalculator(),
        YSenseDatabase("database/ysense_production.db")
    )

claude_client, attribution_engine, quality_calculator, db = get_components()

# AI Functions
def extract_layers_with_ai(story: str) -> dict:
    """Extract 5 perception layers"""
    prompt = f"""Analyze this story and extract 5 perception layers (2-4 sentences each):

Story: {story}

1. NARRATIVE: Unspoken vs well-known story
2. SOMATIC: Physical sensations and emotions
3. ATTENTION: Tiny details most would miss
4. SYNESTHETIC: Non-visual vibe description
5. TEMPORAL: Sound and time quality

Return JSON with keys: narrative, somatic, attention, synesthetic, temporal"""
    
    try:
        response = claude_client.generate_response(prompt, max_tokens=1000)
        clean = response.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except:
        return {
            "narrative": "Layers of meaning through cultural context.",
            "somatic": "Warmth, connection, presence.",
            "attention": "Details revealing deeper patterns.",
            "synesthetic": "Textured, resonant, timeless.",
            "temporal": "Time moves deliberately here."
        }

def suggest_three_words(story: str, layers: dict) -> list:
    """Suggest 3 distillation words"""
    combined = f"Story: {story}\n\n" + "\n\n".join([f"{k}: {v}" for k, v in layers.items()])
    prompt = f"{combined}\n\nSuggest exactly 3 evocative words (not generic) separated by periods:"
    
    try:
        response = claude_client.generate_response(prompt, max_tokens=50)
        words = [w.strip().strip('.') for w in response.replace(',', '.').split('.') if w.strip()]
        return words[:3] if len(words) >= 3 else ["Patience", "Tradition", "Alchemy"]
    except:
        return ["Patience", "Tradition", "Alchemy"]

def chat_about_words(user_message: str, current_words: list, story: str) -> str:
    """Chat about distillation words"""
    prompt = f"""User's story: {story}
Current words: {'. '.join(current_words)}
User says: {user_message}

Respond thoughtfully (2-3 sentences) about why you chose these words or suggest alternatives."""
    
    try:
        return claude_client.generate_response(prompt, max_tokens=200).strip()
    except:
        return "I understand. What word feels more authentic to you?"

# Authentication Pages
def login_page():
    """Login/Register"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">🪶 YSenseAI</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">The Wisdom Protocol | 慧觉™</p>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                user = db.authenticate_user(email, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user['id']
                    st.session_state.user_email = user['email']
                    st.session_state.session_token = db.create_session(user['id'])
                    st.success("✅ Welcome back!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        with tab2:
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if reg_password != reg_confirm:
                    st.error("❌ Passwords don't match")
                elif len(reg_password) < 6:
                    st.error("❌ Password must be 6+ characters")
                else:
                    user_id = db.create_user(reg_email, reg_password)
                    if user_id:
                        st.success("✅ Account created! Please login.")
                    else:
                        st.error("❌ Email already exists")

# Library Dashboard
def library_page():
    """Personal library"""
    st.markdown('<div class="main-header">📚 My Wisdom Library</div>', unsafe_allow_html=True)
    
    stats = db.get_user_stats(st.session_state.user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{stats.get("total_submissions", 0)}</div><div class="stat-label">Total Wisdom</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-value">{stats.get("training_ready_count", 0)}</div><div class="stat-label">Training Ready</div></div>', unsafe_allow_html=True)
    with col3:
        avg = stats.get("avg_quality_score", 0) or 0
        st.markdown(f'<div class="stat-card"><div class="stat-value">{avg:.2f}</div><div class="stat-label">Avg Quality</div></div>', unsafe_allow_html=True)
    with col4:
        revenue = stats.get("total_submissions", 0) * 15
        st.markdown(f'<div class="stat-card"><div class="stat-value">€{revenue}</div><div class="stat-label">Est. Revenue</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search your wisdom...")
    with col2:
        if st.button("📥 Export All", use_container_width=True):
            st.session_state.current_page = 'export'
            st.rerun()
    
    submissions = db.search_submissions(st.session_state.user_id, search) if search else db.get_user_submissions(st.session_state.user_id)
    
    if not submissions:
        st.info("📝 No wisdom yet. Share your first moment!")
        if st.button("✨ Start", type="primary"):
            st.session_state.current_page = 'submit'
            st.session_state.submission_step = 'canvas'
            st.rerun()
    else:
        for sub in submissions:
            col1, col2 = st.columns([4, 1])
            with col1:
                essence = ". ".join(sub['distilled_essence']) + "."
                st.markdown(f'<div class="essence-card"><div class="essence-words">{essence}</div><div style="font-size: 0.875rem; opacity: 0.9; margin-top: 0.5rem;">{sub["created_at"][:10]} • Quality: {sub["quality_scores"].get("overall", 0):.2f}</div></div>', unsafe_allow_html=True)
            with col2:
                if st.button("👁️", key=f"view_{sub['id']}", help="View", use_container_width=True):
                    st.session_state.viewing_submission = sub['id']
                    st.session_state.current_page = 'view'
                    st.rerun()
                if st.button("🔗", key=f"share_{sub['id']}", help="Share", use_container_width=True):
                    db.update_submission_visibility(sub['id'], st.session_state.user_id, True)
                    st.success(f"🔗 ysenseai.org/s/{sub['share_token']}")

# View Submission Detail
def view_submission_page():
    """View single submission"""
    sub = db.get_submission_by_id(st.session_state.viewing_submission, st.session_state.user_id)
    if not sub:
        st.error("Submission not found")
        return
    
    if st.button("← Back to Library"):
        st.session_state.current_page = 'library'
        st.rerun()
    
    essence = ". ".join(sub['distilled_essence']) + "."
    st.markdown(f'<div class="main-header">{essence}</div>', unsafe_allow_html=True)
    
    st.markdown(f"**Created:** {sub['created_at'][:10]} | **Quality:** {sub['quality_scores'].get('overall', 0):.3f} | **Tier:** {sub['consent_tier']}")
    
    st.markdown("---")
    st.markdown("### 📖 Your Story")
    st.write(sub['raw_story'])
    
    st.markdown("### 🧠 Perception Layers")
    for key, value in sub['extracted_layers'].items():
        with st.expander(f"{key.title()} Layer"):
            st.write(value)
    
    if sub['chat_history']:
        st.markdown("### 💬 Distillation Dialogue")
        for chat in sub['chat_history']:
            sender = "🪶 Y" if chat['sender'] == 'ai' else "👤 You"
            st.markdown(f'<div class="chat-message {chat["sender"]}"><strong>{sender}:</strong> {chat["message"]}</div>', unsafe_allow_html=True)

# Submit Wisdom (Full V2.1 Flow)
def submit_wisdom_page():
    """Submit new wisdom with collaborative distillation"""
    
    if st.session_state.submission_step == 'canvas':
        st.markdown('<div class="main-header">✨ Share Your Moment</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 2rem;">Write freely. Y will find the wisdom inside.</p>', unsafe_allow_html=True)
        
        story = st.text_area("Your Story", height=300, placeholder="The rain started falling...", key="new_story", value=st.session_state.raw_story)
        st.session_state.raw_story = story
        
        if len(story) > 30:
            if st.button("🧠 Analyze", type="primary"):
                st.session_state.submission_step = 'processing'
                st.rerun()
    
    elif st.session_state.submission_step == 'processing':
        st.markdown('<div style="text-align: center; padding: 4rem 2rem;"><div style="font-size: 4rem; margin-bottom: 2rem;">🪶</div><div style="font-family: Georgia, serif; font-size: 2rem; font-weight: 600;">Y is perceiving...</div></div>', unsafe_allow_html=True)
        
        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)
            time.sleep(0.02)
        
        st.session_state.extracted_layers = extract_layers_with_ai(st.session_state.raw_story)
        st.session_state.suggested_words = suggest_three_words(st.session_state.raw_story, st.session_state.extracted_layers)
        st.session_state.distilled_essence = st.session_state.suggested_words.copy()
        st.session_state.chat_history = [{
            "sender": "ai",
            "message": f"I sense: **{'. '.join(st.session_state.suggested_words)}**\n\nDoes this resonate?"
        }]
        st.session_state.submission_step = 'distillation'
        st.rerun()
    
    elif st.session_state.submission_step == 'distillation':
        st.markdown('<div class="main-header">Distillation Dialogue</div>', unsafe_allow_html=True)
        
        st.markdown("### Your Current Essence")
        essence_html = " • ".join([f'<span style="font-family: Georgia, serif; font-size: 1.5rem; font-weight: bold; color: #4c1d95;">{w}</span>' for w in st.session_state.distilled_essence])
        st.markdown(f'<div style="text-align: center; margin: 2rem 0;">{essence_html}</div>', unsafe_allow_html=True)
        
        st.markdown("### Conversation with Y")
        for chat in st.session_state.chat_history:
            sender = "🪶 Y" if chat['sender'] == 'ai' else "👤 You"
            st.markdown(f'<div class="chat-message {chat["sender"]}"><strong>{sender}:</strong> {chat["message"]}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("Your thoughts", placeholder="Why 'Patience'? I felt 'Surrender'...", key="chat_input")
        with col2:
            if st.button("💬 Send", use_container_width=True) and user_input:
                st.session_state.chat_history.append({"sender": "user", "message": user_input})
                ai_response = chat_about_words(user_input, st.session_state.distilled_essence, st.session_state.raw_story)
                st.session_state.chat_history.append({"sender": "ai", "message": ai_response})
                st.rerun()
        
        st.markdown("---")
        st.markdown("### Edit Words")
        col1, col2, col3 = st.columns(3)
        with col1:
            w1 = st.text_input("Word 1", value=st.session_state.distilled_essence[0], key="w1")
        with col2:
            w2 = st.text_input("Word 2", value=st.session_state.distilled_essence[1], key="w2")
        with col3:
            w3 = st.text_input("Word 3", value=st.session_state.distilled_essence[2], key="w3")
        
        if st.button("💾 Update", use_container_width=True):
            st.session_state.distilled_essence = [w1, w2, w3]
            st.rerun()
        
        st.markdown("---")
        if st.button("Finalize Essence →", type="primary", use_container_width=True):
            st.session_state.submission_step = 'consent'
            st.rerun()
    
    elif st.session_state.submission_step == 'consent':
        st.markdown('<div class="main-header">Z-Protocol</div>', unsafe_allow_html=True)
        
        essence = ". ".join(st.session_state.distilled_essence) + "."
        st.markdown(f'<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4c1d95, #6d28d9); border-radius: 1rem; color: white; margin: 2rem 0;"><div style="font-family: Georgia, serif; font-size: 2.5rem; font-weight: bold;">{essence}</div></div>', unsafe_allow_html=True)
        
        for tier in CONSENT_TIERS:
            selected = st.session_state.selected_tier == tier['id']
            if st.button(f"{tier['icon']} {tier['name']} - {tier['revenue_share']}", key=tier['id'], type="primary" if selected else "secondary", use_container_width=True):
                st.session_state.selected_tier = tier['id']
                st.rerun()
        
        if st.button("🔒 Sign & Save", type="primary", use_container_width=True):
            st.session_state.submission_step = 'saving'
            st.rerun()
    
    elif st.session_state.submission_step == 'saving':
        with st.spinner("Minting wisdom asset..."):
            st.session_state.quality_scores = quality_calculator.calculate_all_metrics(
                st.session_state.raw_story,
                st.session_state.extracted_layers,
                st.session_state.distilled_essence
            )
            
            attribution_data = attribution_engine.create_wisdom_asset(
                user_id=f"user_{st.session_state.user_id}",
                raw_story=st.session_state.raw_story,
                layer_responses=st.session_state.extracted_layers,
                distilled_essence=st.session_state.distilled_essence,
                consent_tier=st.session_state.selected_tier,
                quality_scores=st.session_state.quality_scores
            )
            attribution_data['distillation_dialogue'] = st.session_state.chat_history
            
            db.create_submission(st.session_state.user_id, attribution_data)
            
            st.success("✅ Wisdom saved to your library!")
            time.sleep(1)
            
            # Reset
            st.session_state.submission_step = 'canvas'
            st.session_state.raw_story = ''
            st.session_state.extracted_layers = {}
            st.session_state.distilled_essence = []
            st.session_state.chat_history = []
            st.session_state.current_page = 'library'
            st.rerun()

# Export Page
def export_page():
    """Export all wisdom"""
    st.markdown('<div class="main-header">📥 Export Your Wisdom</div>', unsafe_allow_html=True)
    
    submissions = db.get_user_submissions(st.session_state.user_id, limit=1000)
    st.info(f"📊 Exporting {len(submissions)} wisdom entries")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📄 JSON")
        st.caption("For personal LLM training")
        json_data = json.dumps([{
            "story": s['raw_story'],
            "layers": s['extracted_layers'],
            "essence": s['distilled_essence'],
            "quality": s['quality_scores']
        } for s in submissions], indent=2)
        st.download_button("💾 Download JSON", data=json_data, file_name=f"ysense_{datetime.now().strftime('%Y%m%d')}.json", mime="application/json", use_container_width=True)
    
    with col2:
        st.subheader("📝 Markdown")
        st.caption("For notes apps")
        md = f"# My Wisdom Library\n\n"
        for s in submissions:
            md += f"## {'. '.join(s['distilled_essence'])}\n\n{s['raw_story']}\n\n---\n\n"
        st.download_button("💾 Download MD", data=md, file_name=f"ysense_{datetime.now().strftime('%Y%m%d')}.md", mime="text/markdown", use_container_width=True)
    
    with col3:
        st.subheader("📊 CSV")
        st.caption("For analysis")
        import io, csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Essence", "Story", "Quality"])
        for s in submissions:
            writer.writerow([s['created_at'][:10], ". ".join(s['distilled_essence']), s['raw_story'][:100], s['quality_scores'].get('overall', 0)])
        st.download_button("💾 Download CSV", data=output.getvalue(), file_name=f"ysense_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)

# Main App
def main():
    if not st.session_state.authenticated:
        login_page()
        return
    
    with st.sidebar:
        st.markdown("### 🪶 YSenseAI")
        st.markdown(f"👤 {st.session_state.user_email}")
        st.markdown("---")
        
        if st.button("📚 Library", use_container_width=True):
            st.session_state.current_page = 'library'
            st.rerun()
        if st.button("✨ New Wisdom", use_container_width=True):
            st.session_state.current_page = 'submit'
            st.session_state.submission_step = 'canvas'
            st.rerun()
        if st.button("📥 Export", use_container_width=True):
            st.session_state.current_page = 'export'
            st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.session_token:
                db.delete_session(st.session_state.session_token)
            st.session_state.authenticated = False
            st.rerun()
    
    if st.session_state.current_page == 'library':
        library_page()
    elif st.session_state.current_page == 'submit':
        submit_wisdom_page()
    elif st.session_state.current_page == 'view':
        view_submission_page()
    elif st.session_state.current_page == 'export':
        export_page()

if __name__ == "__main__":
    main()
