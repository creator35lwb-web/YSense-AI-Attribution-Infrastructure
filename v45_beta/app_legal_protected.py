"""
YSenseAI™ Platform v4.5-Beta - Legally Protected Production Version
Z-Protocol v2.0 Compliant | GDPR Compliant | Beta Program

Features:
- Complete Z-Protocol v2.0 integration
- Privacy Policy & Terms of Service
- Registration consent flow
- Cookie consent banner
- Beta disclaimers
- Founder liability protection
"""

import streamlit as st
import hashlib
import json
import uuid
from datetime import datetime
from pathlib import Path

# Import consent engine
import sys
sys.path.append(str(Path(__file__).parent / "consent"))

# Import attribution and quality
sys.path.append(str(Path(__file__).parent / "attribution"))
from attribution_engine import AttributionEngine
from quality_metrics import QualityMetricsCalculator

# Import database
sys.path.append(str(Path(__file__).parent / "database"))
from schema import Database

# Import agents
sys.path.append(str(Path(__file__).parent / "agents"))
from anthropic_integration_v45 import AnthropicAgent
from qwen_integration_v45 import QwenAgent

# Import UI config
sys.path.append(str(Path(__file__).parent / "ui"))
from layer_config import LAYER_PROMPTS, Z_PROTOCOL_TIERS

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="YSenseAI™ v4.5-Beta | Ethical AI Training Data",
    page_icon="🪶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    /* Beta Badge */
    .beta-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-left: 10px;
    }
    
    /* Warning Box */
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 20px 0;
        border-radius: 4px;
    }
    
    /* Consent Checkbox */
    .consent-item {
        background: #f8f9fa;
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
        border-left: 3px solid #667eea;
    }
    
    /* Legal Link */
    .legal-link {
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
    }
    
    .legal-link:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INITIALIZE ====================
db = Database()
attribution_engine = AttributionEngine()
quality_calculator = QualityMetricsCalculator()
claude_agent = AnthropicAgent()
qwen_agent = QwenAgent()

# ==================== SESSION STATE ====================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'cookie_consent' not in st.session_state:
    st.session_state.cookie_consent = False
if 'beta_acknowledged' not in st.session_state:
    st.session_state.beta_acknowledged = False

# ==================== LEGAL PAGES ====================
def show_privacy_policy():
    """Display Privacy Policy"""
    st.title("🔒 Privacy Policy")
    
    privacy_path = Path(__file__).parent / "legal" / "privacy_policy.md"
    if privacy_path.exists():
        with open(privacy_path, 'r') as f:
            st.markdown(f.read())
    else:
        st.error("Privacy Policy not found. Please contact privacy@ysenseai.org")

def show_terms_of_service():
    """Display Terms of Service"""
    st.title("📜 Terms of Service")
    
    terms_path = Path(__file__).parent / "legal" / "terms_of_service.md"
    if terms_path.exists():
        with open(terms_path, 'r') as f:
            st.markdown(f.read())
    else:
        st.error("Terms of Service not found. Please contact legal@ysenseai.org")

def show_beta_disclaimer():
    """Display Beta Program Disclaimer"""
    st.markdown("""
    <div class="warning-box">
        <h3>⚠️ BETA PROGRAM DISCLAIMER</h3>
        <p><strong>YSenseAI v4.5-Beta is an experimental testing platform.</strong></p>
        
        <p><strong>By using this platform, you acknowledge:</strong></p>
        <ul>
            <li>This is a <strong>BETA PRODUCT</strong> under active development</li>
            <li>Features are provided "AS IS" and "AS AVAILABLE"</li>
            <li>The platform may contain bugs or incomplete features</li>
            <li>Service may be interrupted without notice</li>
            <li>You use this platform <strong>AT YOUR OWN RISK</strong></li>
        </ul>
        
        <p><strong>We make NO WARRANTIES regarding:</strong></p>
        <ul>
            <li>Platform availability or uptime</li>
            <li>Data accuracy or completeness</li>
            <li>Fitness for any particular purpose</li>
        </ul>
        
        <p><strong>Participation is VOLUNTARY. You may exit at any time.</strong></p>
    </div>
    """, unsafe_allow_html=True)

# ==================== COOKIE CONSENT ====================
def show_cookie_consent():
    """Display cookie consent banner"""
    if not st.session_state.cookie_consent:
        st.markdown("""
        <div class="warning-box">
            <h4>🍪 Cookie Notice</h4>
            <p>We use essential cookies for authentication and security. By using YSenseAI, you agree to our use of cookies as described in our Privacy Policy.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Accept Cookies"):
                st.session_state.cookie_consent = True
                st.rerun()
        with col2:
            st.markdown('[Learn more about our Privacy Policy](#privacy-policy)', unsafe_allow_html=True)

# ==================== REGISTRATION WITH CONSENT ====================
def show_registration():
    """Registration with comprehensive consent flow"""
    st.title("🪶 Join YSenseAI Beta Program")
    
    # Beta Disclaimer
    show_beta_disclaimer()
    
    st.markdown("---")
    
    # Registration Form
    st.subheader("Create Your Account")
    
    email = st.text_input("Email Address*", placeholder="your@email.com")
    password = st.text_input("Password*", type="password", placeholder="Minimum 8 characters")
    password_confirm = st.text_input("Confirm Password*", type="password")
    
    st.markdown("---")
    
    # Consent Section
    st.subheader("📋 Required Consents")
    
    st.markdown("""
    <div class="consent-item">
        <strong>To create an account, you must agree to the following:</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Consent 1: Privacy Policy
    consent_privacy = st.checkbox(
        "I have read and agree to the Privacy Policy",
        help="Required to create an account"
    )
    st.markdown('[📖 Read Privacy Policy](/?page=privacy)', unsafe_allow_html=True)
    
    # Consent 2: Terms of Service
    consent_terms = st.checkbox(
        "I have read and agree to the Terms of Service",
        help="Required to create an account"
    )
    st.markdown('[📜 Read Terms of Service](/?page=terms)', unsafe_allow_html=True)
    
    # Consent 3: Beta Acknowledgment
    consent_beta = st.checkbox(
        "I understand this is a BETA PROGRAM and I use it AT MY OWN RISK",
        help="Required to participate in beta"
    )
    
    # Consent 4: Age Verification
    consent_age = st.checkbox(
        "I am 18 years or older",
        help="You must be 18+ to use YSenseAI"
    )
    
    # Consent 5: Data Processing
    consent_data = st.checkbox(
        "I consent to YSenseAI processing my data as described in the Privacy Policy",
        help="Required for platform functionality"
    )
    
    st.markdown("---")
    
    # Optional Consents
    st.subheader("📊 Optional Consents")
    
    st.markdown("""
    <div class="consent-item">
        <strong>These are optional. You can change them later in your settings.</strong>
    </div>
    """, unsafe_allow_html=True)
    
    consent_community = st.checkbox(
        "I want to share my reflections within the YSense community",
        value=False,
        help="Optional: Share with other users"
    )
    
    consent_research = st.checkbox(
        "I want to participate in academic research (anonymized)",
        value=False,
        help="Optional: Help advance AI ethics research"
    )
    
    st.markdown("---")
    
    # Register Button
    if st.button("Create Account", type="primary", use_container_width=True):
        # Validation
        errors = []
        
        if not email or '@' not in email:
            errors.append("Please enter a valid email address")
        
        if not password or len(password) < 8:
            errors.append("Password must be at least 8 characters")
        
        if password != password_confirm:
            errors.append("Passwords do not match")
        
        if not all([consent_privacy, consent_terms, consent_beta, consent_age, consent_data]):
            errors.append("You must agree to all required consents to create an account")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Check if email exists
            if db.get_user_by_email(email):
                st.error("An account with this email already exists")
            else:
                # Create account
                user_id = db.create_user(
                    email=email,
                    password_hash=hashlib.sha256(password.encode()).hexdigest(),
                    username=email.split('@')[0]
                )
                
                # Record consents
                consent_metadata = {
                    "ip_address": "127.0.0.1",  # TODO: Get real IP
                    "user_agent": "Streamlit",
                    "timestamp": datetime.now().isoformat(),
                    "beta_program": True
                }
                
                # Required consents
                db.create_consent(user_id, "privacy_policy", True, consent_metadata)
                db.create_consent(user_id, "terms_of_service", True, consent_metadata)
                db.create_consent(user_id, "beta_acknowledgment", True, consent_metadata)
                db.create_consent(user_id, "age_verification", True, consent_metadata)
                db.create_consent(user_id, "data_processing", True, consent_metadata)
                
                # Optional consents
                if consent_community:
                    db.create_consent(user_id, "community_sharing", True, consent_metadata)
                if consent_research:
                    db.create_consent(user_id, "research_participation", True, consent_metadata)
                
                st.success("✅ Account created successfully! Please log in.")
                st.balloons()
                
                # Auto-login
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = email.split('@')[0]
                st.session_state.beta_acknowledged = True
                st.rerun()

# ==================== LOGIN ====================
def show_login():
    """Login page"""
    st.title("🪶 Welcome to YSenseAI")
    
    st.markdown('<span class="beta-badge">BETA</span>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Ethical AI Training Data Platform
    
    Build your personal wisdom library while contributing to ethical AI development.
    """)
    
    # Beta Notice
    st.info("🧪 **Beta Program**: This is an experimental testing platform. [Learn more](#beta-disclaimer)")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary", use_container_width=True):
            user = db.get_user_by_email(email)
            
            if user and user['password_hash'] == hashlib.sha256(password.encode()).hexdigest():
                st.session_state.logged_in = True
                st.session_state.user_id = user['id']
                st.session_state.username = user['username']
                st.session_state.beta_acknowledged = True
                st.success("✅ Logged in successfully!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")
    
    with tab2:
        show_registration()

# ==================== MAIN APP ====================
def main():
    """Main application"""
    
    # Cookie Consent (top of page)
    show_cookie_consent()
    
    # Check if user wants to view legal pages
    query_params = st.query_params
    page = query_params.get("page", None)
    
    if page == "privacy":
        show_privacy_policy()
        return
    elif page == "terms":
        show_terms_of_service()
        return
    
    # Authentication Check
    if not st.session_state.logged_in:
        show_login()
        return
    
    # Beta Acknowledgment (first login)
    if not st.session_state.beta_acknowledged:
        st.title("⚠️ Beta Program Acknowledgment")
        show_beta_disclaimer()
        
        if st.button("I Understand and Accept", type="primary"):
            st.session_state.beta_acknowledged = True
            st.rerun()
        
        if st.button("I Do Not Accept (Exit Beta)"):
            st.session_state.logged_in = False
            st.rerun()
        
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.markdown('<span class="beta-badge">BETA TESTER</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Home", "✨ Submit Wisdom", "📚 My Library", "⚙️ Settings", "ℹ️ About", "🔒 Privacy", "📜 Terms"]
        )
        
        st.markdown("---")
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    # Page Routing
    if page == "🏠 Home":
        show_home()
    elif page == "✨ Submit Wisdom":
        show_submit_wisdom()
    elif page == "📚 My Library":
        show_library()
    elif page == "⚙️ Settings":
        show_settings()
    elif page == "ℹ️ About":
        show_about()
    elif page == "🔒 Privacy":
        show_privacy_policy()
    elif page == "📜 Terms":
        show_terms_of_service()

def show_home():
    """Home page"""
    st.title("🪶 YSenseAI™ v4.5-Beta")
    st.markdown('<span class="beta-badge">BETA PROGRAM</span>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to Your Wisdom Sanctuary
    
    Build your personal knowledge library while contributing to ethical AI development.
    """)
    
    # Stats
    submissions = db.get_user_submissions(st.session_state.user_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Submissions", len(submissions))
    
    with col2:
        training_ready = sum(1 for s in submissions if s.get('quality_score', 0) > 0.7)
        st.metric("Training-Ready", training_ready)
    
    with col3:
        avg_quality = sum(s.get('quality_score', 0) for s in submissions) / len(submissions) if submissions else 0
        st.metric("Avg Quality", f"{avg_quality:.2f}")
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ Submit New Wisdom", use_container_width=True):
            st.session_state.page = "✨ Submit Wisdom"
            st.rerun()
    
    with col2:
        if st.button("📚 View My Library", use_container_width=True):
            st.session_state.page = "📚 My Library"
            st.rerun()

def show_submit_wisdom():
    """Wisdom submission with collaborative distillation"""
    st.title("✨ Share Your Wisdom")
    
    st.markdown("""
    Write freely about a moment, experience, or reflection. Our AI will help you explore its deeper layers.
    """)
    
    # Story Canvas
    story = st.text_area(
        "Your Story",
        placeholder="Share a moment that holds meaning for you...",
        height=200,
        help="Write freely. The AI will extract layers of perception from your story."
    )
    
    if st.button("Analyze Story", type="primary") and story:
        with st.spinner("🧠 AI is analyzing your story..."):
            # Extract 5 layers (using Claude)
            layers = claude_agent.extract_layers(story)
            
            # Suggest 3 words
            suggested_words = claude_agent.suggest_distillation(story, layers)
            
            st.session_state.current_story = story
            st.session_state.current_layers = layers
            st.session_state.suggested_words = suggested_words
            st.session_state.chat_history = []
        
        st.success("✅ Analysis complete!")
        st.rerun()
    
    # Show results if available
    if 'current_story' in st.session_state:
        st.markdown("---")
        
        # Show layers
        st.subheader("🌈 Perception Layers")
        
        for layer_name, content in st.session_state.current_layers.items():
            with st.expander(f"📍 {layer_name}"):
                st.write(content)
        
        st.markdown("---")
        
        # Collaborative Distillation
        st.subheader("💬 Collaborative Distillation")
        
        st.markdown(f"""
        **AI suggests**: {st.session_state.suggested_words}
        
        Chat with the AI to refine these words, or edit them directly below.
        """)
        
        # Chat interface
        user_message = st.text_input("Ask about the words or suggest alternatives...")
        
        if st.button("Send") and user_message:
            # Get AI response
            ai_response = claude_agent.discuss_distillation(
                st.session_state.current_story,
                st.session_state.suggested_words,
                user_message
            )
            
            st.session_state.chat_history.append({
                "user": user_message,
                "ai": ai_response
            })
            
            st.rerun()
        
        # Show chat history
        for msg in st.session_state.get('chat_history', []):
            st.markdown(f"**You**: {msg['user']}")
            st.markdown(f"**AI**: {msg['ai']}")
            st.markdown("---")
        
        # Final words
        final_words = st.text_input(
            "Final 3 Words",
            value=st.session_state.suggested_words,
            help="Edit these words based on your reflection"
        )
        
        # Z-Protocol Consent
        st.markdown("---")
        st.subheader("🛡️ Z-Protocol Consent")
        
        tier = st.selectbox(
            "Choose Content Tier",
            options=list(Z_PROTOCOL_TIERS.keys()),
            format_func=lambda x: f"{x} ({Z_PROTOCOL_TIERS[x]['revenue']}% revenue)",
            help="Select the sensitivity level of your content"
        )
        
        ai_training = st.checkbox(
            f"I consent to AI training use ({Z_PROTOCOL_TIERS[tier]['revenue']}% revenue share)",
            help="Optional: Allow your anonymized wisdom to be used for AI training"
        )
        
        if st.button("💾 Save Wisdom", type="primary"):
            # Calculate quality metrics
            quality = quality_calculator.calculate_quality(
                st.session_state.current_story,
                st.session_state.current_layers,
                final_words
            )
            
            # Create attribution
            attribution = attribution_engine.create_attribution(
                user_id=st.session_state.user_id,
                content=st.session_state.current_story,
                layers=st.session_state.current_layers,
                essence=final_words,
                tier=tier
            )
            
            # Save to database
            submission_id = db.create_submission(
                user_id=st.session_state.user_id,
                story=st.session_state.current_story,
                layers=st.session_state.current_layers,
                essence=final_words,
                tier=tier,
                quality_score=quality['overall_score'],
                attribution=attribution,
                ai_training_consent=ai_training
            )
            
            st.success("✅ Wisdom saved to your library!")
            st.balloons()
            
            # Clear session
            del st.session_state.current_story
            del st.session_state.current_layers
            del st.session_state.suggested_words
            
            st.rerun()

def show_library():
    """Personal library"""
    st.title("📚 My Wisdom Library")
    
    submissions = db.get_user_submissions(st.session_state.user_id)
    
    if not submissions:
        st.info("You haven't submitted any wisdom yet. Start by sharing a story!")
        return
    
    # Search
    search = st.text_input("🔍 Search your wisdom...")
    
    # Display submissions
    for sub in submissions:
        if search and search.lower() not in sub['story'].lower():
            continue
        
        with st.expander(f"🪶 {sub['essence']} - {sub['created_at'][:10]}"):
            st.markdown(f"**Story**: {sub['story']}")
            st.markdown(f"**Tier**: {sub['tier']}")
            st.markdown(f"**Quality Score**: {sub['quality_score']:.2f}")
            
            if st.button(f"Export JSON", key=f"export_{sub['id']}"):
                st.download_button(
                    "Download",
                    data=json.dumps(sub, indent=2),
                    file_name=f"wisdom_{sub['id']}.json",
                    mime="application/json"
                )

def show_settings():
    """Settings page"""
    st.title("⚙️ Settings")
    
    st.subheader("Account")
    st.write(f"Email: {st.session_state.username}@...")
    
    st.markdown("---")
    
    st.subheader("Consents")
    st.info("Manage your consent preferences here (coming soon)")
    
    st.markdown("---")
    
    st.subheader("Danger Zone")
    if st.button("Delete Account", type="secondary"):
        st.warning("This will permanently delete your account and all data within 72 hours.")
        if st.button("Confirm Deletion"):
            db.delete_user(st.session_state.user_id)
            st.session_state.logged_in = False
            st.success("Account deletion scheduled. You will receive a confirmation email.")
            st.rerun()

def show_about():
    """About page"""
    st.title("ℹ️ About YSenseAI")
    
    st.markdown("""
    ### Our Mission
    
    Protect human dignity, cultural heritage, and user sovereignty while enabling ethical AI advancement through authentic cultural bridge-building.
    
    ### Z-Protocol v2.0
    
    Our comprehensive ethical framework for AI attribution and cultural protection.
    
    ### Beta Program
    
    You're part of our early testing program. Thank you for helping us build the future of ethical AI training data!
    """)

# ==================== RUN ====================
if __name__ == "__main__":
    main()
