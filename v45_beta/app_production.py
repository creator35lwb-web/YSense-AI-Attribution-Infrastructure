"""
YSenseAI v4.5-Beta PRODUCTION
Complete platform with auth, library, export, and sharing
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
sys.path.append(str(Path(__file__).parent / "database"))

from ui.layer_config import CONSENT_TIERS
from agents.anthropic_integration_v45 import AnthropicClient
from attribution.attribution_engine import AttributionEngine
from attribution.quality_metrics import QualityMetricsCalculator
from database.schema import YSenseDatabase

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
    .stApp {
        background: linear-gradient(135deg, #FDFBF7 0%, #F5F3EF 100%);
    }
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
        padding: 2rem;
        color: white;
        margin: 1rem 0;
    }
    .essence-words {
        font-family: 'Georgia', serif;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
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
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'session_token' not in st.session_state:
    st.session_state.session_token = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'library'
if 'submission_step' not in st.session_state:
    st.session_state.submission_step = 'canvas'

# Initialize components
@st.cache_resource
def get_components():
    claude = AnthropicClient()
    attribution_engine = AttributionEngine()
    quality_calculator = QualityMetricsCalculator()
    db = YSenseDatabase("database/ysense_production.db")
    return claude, attribution_engine, quality_calculator, db

claude_client, attribution_engine, quality_calculator, db = get_components()

# Authentication Functions
def login_page():
    """Login/Register page"""
    st.markdown('<div class="main-header">🪶 YSenseAI</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #64748b; margin-bottom: 3rem;">The Wisdom Protocol | 慧觉™</p>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Welcome Back")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            user = db.authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user['id']
                st.session_state.user_email = user['email']
                st.session_state.session_token = db.create_session(user['id'])
                st.success("✅ Login successful!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    
    with tab2:
        st.subheader("Create Account")
        reg_email = st.text_input("Email", key="reg_email")
        reg_username = st.text_input("Username (optional)", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
        
        if st.button("Register", type="primary", use_container_width=True):
            if reg_password != reg_password_confirm:
                st.error("❌ Passwords don't match")
            elif len(reg_password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                user_id = db.create_user(reg_email, reg_password, reg_username)
                if user_id:
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Email already exists")

# Library Dashboard
def library_page():
    """Personal library dashboard"""
    st.markdown(f'<div class="main-header">📚 My Wisdom Library</div>', unsafe_allow_html=True)
    
    # Stats
    stats = db.get_user_stats(st.session_state.user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('total_submissions', 0)}</div>
            <div class="stat-label">Total Wisdom</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats.get('training_ready_count', 0)}</div>
            <div class="stat-label">Training Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_score = stats.get('avg_quality_score', 0) or 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{avg_score:.2f}</div>
            <div class="stat-label">Avg Quality</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">€{stats.get('total_submissions', 0) * 15:.0f}</div>
            <div class="stat-label">Est. Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("🔍 Search your wisdom", placeholder="Search by content, essence, or layers...")
    with col2:
        if st.button("📥 Export All", use_container_width=True):
            st.session_state.current_page = 'export'
            st.rerun()
    
    # Get submissions
    if search_query:
        submissions = db.search_submissions(st.session_state.user_id, search_query)
    else:
        submissions = db.get_user_submissions(st.session_state.user_id)
    
    if not submissions:
        st.info("📝 No wisdom yet. Start by sharing your first moment!")
        if st.button("✨ Share Wisdom", type="primary"):
            st.session_state.current_page = 'submit'
            st.rerun()
    else:
        # Display submissions
        for submission in submissions:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    essence_text = ". ".join(submission['distilled_essence']) + "."
                    st.markdown(f"""
                    <div class="essence-card">
                        <div class="essence-words">{essence_text}</div>
                        <div style="font-size: 0.875rem; opacity: 0.9;">{submission['created_at'][:10]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Details"):
                        st.markdown(f"**Story:** {submission['raw_story'][:200]}...")
                        st.markdown(f"**Quality Score:** {submission['quality_scores'].get('overall', 0):.3f}")
                        st.markdown(f"**Consent Tier:** {submission['consent_tier']}")
                        st.markdown(f"**Training Ready:** {'✅' if submission['training_ready'] else '⏳'}")
                
                with col2:
                    if st.button("📄 View", key=f"view_{submission['id']}", use_container_width=True):
                        st.session_state.viewing_submission = submission['id']
                        st.session_state.current_page = 'view'
                        st.rerun()
                    
                    if st.button("📤 Share", key=f"share_{submission['id']}", use_container_width=True):
                        db.update_submission_visibility(submission['id'], st.session_state.user_id, True)
                        share_url = f"https://ysenseai.org/share/{submission['share_token']}"
                        st.success(f"🔗 {share_url}")
                    
                    if st.button("🗑️ Delete", key=f"delete_{submission['id']}", use_container_width=True):
                        db.delete_submission(submission['id'], st.session_state.user_id)
                        st.rerun()
                
                st.markdown("---")

# Submission Flow (simplified from V2.1)
def submit_wisdom_page():
    """Submit new wisdom"""
    st.markdown('<div class="main-header">✨ Share Your Wisdom</div>', unsafe_allow_html=True)
    
    # Story input
    story = st.text_area(
        "Your Story",
        height=300,
        placeholder="Share a moment, memory, or realization...",
        key="new_story"
    )
    
    if len(story) > 30 and st.button("🧠 Analyze", type="primary"):
        with st.spinner("Y is perceiving..."):
            # Extract layers
            from app_v2_1_collaborative import extract_layers_with_ai, suggest_three_words
            
            layers = extract_layers_with_ai(story)
            words = suggest_three_words(story, layers)
            
            # Calculate quality
            quality_scores = quality_calculator.calculate_all_metrics(story, layers, words)
            
            # Create attribution
            attribution_data = attribution_engine.create_wisdom_asset(
                user_id=f"user_{st.session_state.user_id}",
                raw_story=story,
                layer_responses=layers,
                distilled_essence=words,
                consent_tier="tier1",
                quality_scores=quality_scores
            )
            
            # Save to database
            db.create_submission(st.session_state.user_id, attribution_data)
            
            st.success("✅ Wisdom saved to your library!")
            time.sleep(1)
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
        if st.button("Download JSON", use_container_width=True):
            json_data = json.dumps([{
                "story": s['raw_story'],
                "layers": s['extracted_layers'],
                "essence": s['distilled_essence'],
                "quality": s['quality_scores']
            } for s in submissions], indent=2)
            
            st.download_button(
                "💾 Save JSON",
                data=json_data,
                file_name=f"ysense_wisdom_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    
    with col2:
        st.subheader("📝 Markdown")
        st.caption("For notes apps")
        if st.button("Download MD", use_container_width=True):
            md_content = f"# My Wisdom Library\n\n"
            for s in submissions:
                essence = ". ".join(s['distilled_essence'])
                md_content += f"## {essence}\n\n"
                md_content += f"**Date:** {s['created_at'][:10]}\n\n"
                md_content += f"{s['raw_story']}\n\n"
                md_content += "---\n\n"
            
            st.download_button(
                "💾 Save MD",
                data=md_content,
                file_name=f"ysense_wisdom_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )
    
    with col3:
        st.subheader("📊 CSV")
        st.caption("For analysis")
        if st.button("Download CSV", use_container_width=True):
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Date", "Essence", "Story", "Quality", "Training Ready"])
            
            for s in submissions:
                writer.writerow([
                    s['created_at'][:10],
                    ". ".join(s['distilled_essence']),
                    s['raw_story'][:100],
                    s['quality_scores'].get('overall', 0),
                    "Yes" if s['training_ready'] else "No"
                ])
            
            st.download_button(
                "💾 Save CSV",
                data=output.getvalue(),
                file_name=f"ysense_wisdom_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Main App
def main():
    # Check authentication
    if not st.session_state.authenticated:
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🪶 YSenseAI")
        st.markdown(f"👤 {st.session_state.user_email}")
        st.markdown("---")
        
        if st.button("📚 Library", use_container_width=True):
            st.session_state.current_page = 'library'
            st.rerun()
        
        if st.button("✨ New Wisdom", use_container_width=True):
            st.session_state.current_page = 'submit'
            st.rerun()
        
        if st.button("📥 Export", use_container_width=True):
            st.session_state.current_page = 'export'
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.session_token:
                db.delete_session(st.session_state.session_token)
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.session_token = None
            st.rerun()
    
    # Route to pages
    if st.session_state.current_page == 'library':
        library_page()
    elif st.session_state.current_page == 'submit':
        submit_wisdom_page()
    elif st.session_state.current_page == 'export':
        export_page()

if __name__ == "__main__":
    main()
