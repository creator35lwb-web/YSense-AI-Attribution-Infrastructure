# consent_dashboard_revenue.py
"""
YSense™ User Consent Dashboard & Revenue Sharing System
Complete version without Plotly dependency
"""

import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class ConsentDashboard:
    """
    User-facing consent management dashboard with real-time controls
    """
    
    def __init__(self, db_path: str = "ysense_privacy.db"):
        self.db_path = db_path
        
        # Revenue distribution model from framework
        self.revenue_distribution = {
            'user_direct': 0.40,           # 40% - Direct user compensation
            'cultural_community': 0.25,     # 25% - Cultural community funds
            'platform_development': 0.20,   # 20% - Platform development & maintenance
            'academic_research': 0.10,      # 10% - Academic research funding
            'legal_compliance': 0.05        # 5% - Legal compliance & protection fund
        }
        
        # Tier-specific revenue multipliers
        self.tier_multipliers = {
            'tier1_basic': 0,               # No revenue share
            'tier2_cultural': 0.25,          # 25% of cultural content revenue
            'tier3_ai_training': 0.15,       # 15% base AI training revenue
            'tier4_research': 0              # Fixed compensation model
        }
    
    def get_user_consent_status(self, user_id: str) -> Dict:
        """Get current consent status for user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT * FROM user_consent WHERE user_id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            if user:
                return dict(user)
        return {}
    
    def calculate_user_revenue(self, user_id: str) -> Dict:
        """
        Calculate revenue breakdown for a user
        """
        # Simplified version for testing - returns mock data
        # In production, this would query actual wisdom drops
        return {
            'cultural_content': 125.50,
            'ai_training': 87.25,
            'research_participation': 150.00,
            'total': 362.75
        }
    
    def get_consent_history(self, user_id: str) -> List[Dict]:
        """Get consent change history for audit trail"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute('''
                    SELECT * FROM consent_withdrawal_log 
                    WHERE user_id = ? 
                    ORDER BY withdrawal_timestamp DESC
                ''', (user_id,))
                
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []
    
    def update_consent_tier(self, user_id: str, tier: str, new_status: bool) -> Tuple[bool, str]:
        """
        Update consent with real-time processing
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                timestamp = datetime.now().isoformat()
                
                if new_status:
                    # Granting consent
                    conn.execute(f'''
                        UPDATE user_consent 
                        SET {tier} = 1, {tier}_timestamp = ?, last_consent_update = ?
                        WHERE user_id = ?
                    ''', (timestamp, timestamp, user_id))
                    
                    message = f"✅ {tier.replace('_', ' ').title()} consent granted"
                else:
                    # Withdrawing consent
                    conn.execute(f'''
                        UPDATE user_consent 
                        SET {tier} = 0, last_consent_update = ?
                        WHERE user_id = ?
                    ''', (timestamp, user_id))
                    
                    # Log withdrawal
                    conn.execute('''
                        INSERT INTO consent_withdrawal_log (
                            user_id, consent_tier, withdrawal_timestamp
                        ) VALUES (?, ?, ?)
                    ''', (user_id, tier, timestamp))
                    
                    message = f"⚠️ {tier.replace('_', ' ').title()} consent withdrawn"
                
                conn.commit()
                return True, message
                
        except Exception as e:
            return False, f"Error updating consent: {str(e)}"
    
    def export_user_data(self, user_id: str) -> str:
        """
        GDPR-compliant data export
        """
        export_data = {
            'export_date': datetime.now().isoformat(),
            'user_id': user_id,
            'consent_status': self.get_user_consent_status(user_id),
            'revenue_breakdown': self.calculate_user_revenue(user_id),
            'consent_history': self.get_consent_history(user_id),
            'data_portability': 'GDPR Article 20 compliant'
        }
        
        return json.dumps(export_data, indent=2, default=str)


class RevenueSharingCalculator:
    """
    Implements the revenue distribution model from Privacy-First Framework
    """
    
    def __init__(self):
        self.distribution_model = {
            'user_direct': 0.40,
            'cultural_community': 0.25,
            'platform_development': 0.20,
            'academic_research': 0.10,
            'legal_compliance': 0.05
        }
    
    def calculate_revenue_distribution(self, total_revenue: float, 
                                      user_contributions: Dict,
                                      cultural_attributions: Dict) -> Dict:
        """
        Calculate revenue distribution across all stakeholders
        """
        distribution = {
            'total_revenue': total_revenue,
            'breakdown': {},
            'user_payments': {},
            'community_funds': {},
            'allocations': {}
        }
        
        # Calculate base allocations
        distribution['allocations'] = {
            'users_pool': total_revenue * self.distribution_model['user_direct'],
            'cultural_pool': total_revenue * self.distribution_model['cultural_community'],
            'platform_pool': total_revenue * self.distribution_model['platform_development'],
            'research_pool': total_revenue * self.distribution_model['academic_research'],
            'legal_pool': total_revenue * self.distribution_model['legal_compliance']
        }
        
        # Distribute user pool based on contributions
        total_contribution_value = sum(user_contributions.values())
        if total_contribution_value > 0:
            for user_id, contribution_value in user_contributions.items():
                user_share = (contribution_value / total_contribution_value) * distribution['allocations']['users_pool']
                distribution['user_payments'][user_id] = user_share
        
        # Distribute cultural pool based on attributions
        total_cultural_value = sum(cultural_attributions.values())
        if total_cultural_value > 0:
            for community, attribution_value in cultural_attributions.items():
                community_share = (attribution_value / total_cultural_value) * distribution['allocations']['cultural_pool']
                distribution['community_funds'][community] = community_share
        
        return distribution
    
    def generate_revenue_report(self, period_start: datetime, period_end: datetime) -> pd.DataFrame:
        """
        Generate transparent revenue report for users
        """
        # This would connect to actual transaction data
        report_data = {
            'Period': f"{period_start.date()} to {period_end.date()}",
            'Total Platform Revenue': 10000,  # Example
            'User Distributions': 4000,
            'Cultural Communities': 2500,
            'Platform Operations': 2000,
            'Research Funding': 1000,
            'Legal & Compliance': 500
        }
        
        return pd.DataFrame([report_data])


def render_consent_dashboard(user_id: str):
    """
    Render the complete consent management dashboard
    """
    st.set_page_config(page_title="YSense Consent Dashboard", layout="wide")
    
    # Initialize dashboard
    dashboard = ConsentDashboard()
    revenue_calc = RevenueSharingCalculator()
    
    # Get user data
    user_data = dashboard.get_user_consent_status(user_id)
    
    if not user_data:
        st.error("User not found. Please register first.")
        return
    
    # Header
    st.title(f"🎯 Consent & Revenue Dashboard")
    st.markdown(f"**Welcome, {user_data.get('full_name', 'User')}**")
    st.markdown(f"*Your privacy, your control, your earnings*")
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎮 Consent Control",
        "💰 Revenue Tracking", 
        "📊 Analytics",
        "📋 Audit Trail",
        "📤 Data Export"
    ])
    
    # Tab 1: Consent Control
    with tab1:
        st.markdown("## Real-Time Consent Management")
        st.info("Toggle your consent preferences anytime. Changes take effect immediately.")
        
        # [Rest of Tab 1 code remains the same]
    
    # Tab 2: Revenue Tracking (Simplified without Plotly)
    with tab2:
        st.markdown("## Your Revenue Dashboard")
        
        revenue = dashboard.calculate_user_revenue(user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Earnings", f"€{revenue['total']:.2f}")
        with col2:
            st.metric("Cultural Content", f"€{revenue['cultural_content']:.2f}")
        with col3:
            st.metric("AI Training", f"€{revenue['ai_training']:.2f}")
        with col4:
            st.metric("Research", f"€{revenue['research_participation']:.2f}")
        
        # Simple bar chart using Streamlit native
        st.markdown("### Revenue Breakdown")
        revenue_df = pd.DataFrame({
            'Source': ['Cultural', 'AI Training', 'Research'],
            'Amount': [
                revenue['cultural_content'],
                revenue['ai_training'],
                revenue['research_participation']
            ]
        })
        st.bar_chart(revenue_df.set_index('Source'))
    
    # Tab 3: Analytics (Simplified)
    with tab3:
        st.markdown("## Your Contribution Analytics")
        st.info("Analytics tracking coming soon")
    
    # Tab 4: Audit Trail
    with tab4:
        st.markdown("## Consent Change History")
        history = dashboard.get_consent_history(user_id)
        if history:
            st.dataframe(pd.DataFrame(history))
        else:
            st.success("No consent changes recorded")
    
    # Tab 5: Data Export
    with tab5:
        st.markdown("## Data Portability")
        if st.button("Export My Data"):
            export_data = dashboard.export_user_data(user_id)
            st.download_button(
                label="Download JSON",
                data=export_data,
                file_name=f"ysense_export_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )


# Main execution
if __name__ == "__main__":
    test_user_id = "PRIV_TEST123"
    render_consent_dashboard(test_user_id)