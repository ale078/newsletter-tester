import streamlit as st
import pandas as pd
import json
from database import get_connection, create_tables, save_execution
from automator import run_test

# Initialize database schema
create_tables()

st.set_page_config(
    page_title="Newsletter Testing Automator",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Newsletter Testing Automator")
st.caption("Automated simulation of newsletter opens and article link clicks across Desktop and Mobile Web.")

menu = st.sidebar.radio("Navigation", ["Create Campaign", "Campaigns & Execution", "Reports & History"])

# ========================================================
# 1. CREATE CAMPAIGN
# ========================================================
if menu == "Create Campaign":
    st.subheader("➕ Create New Testing Campaign")
    
    with st.form("campaign_form", clear_on_submit=True):
        name = st.text_input("Campaign Name", placeholder="e.g. Tech Weekly Newsletter #42")
        newsletter_url = st.text_input("Newsletter URL (Web version / Tracking link)", placeholder="https://newsletter-service.com/p/...")
        
        st.write("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💻 Desktop Web")
            opens_desktop = st.number_input("Planned Desktop Opens", min_value=0, max_value=500, value=10, step=1)
            clicks_desktop = st.number_input("Planned Desktop Clicks", min_value=0, max_value=500, value=5, step=1)
            
        with col2:
            st.markdown("#### 📱 Mobile Web (iPhone)")
            opens_mobile = st.number_input("Planned Mobile Opens", min_value=0, max_value=500, value=10, step=1)
            clicks_mobile = st.number_input("Planned Mobile Clicks", min_value=0, max_value=500, value=5, step=1)
            
        st.write("---")
        daily = st.checkbox("Schedule daily automated execution", value=True)
        
        submitted = st.form_submit_button("💾 Save Campaign", use_container_width=True)
        
        if submitted:
            if not name.strip() or not newsletter_url.strip():
                st.error("Please provide both Campaign Name and Newsletter URL.")
            else:
                conn = get_connection()
                c = conn.cursor()
                c.execute("""
                    INSERT INTO campaigns (name, newsletter_url, opens_desktop, opens_mobile, clicks_desktop, clicks_mobile, daily)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name.strip(), newsletter_url.strip(), opens_desktop, opens_mobile, clicks_desktop, clicks_mobile, int(daily)))
                conn.commit()
                conn.close()
                st.success(f"Campaign '{name}' created successfully!")

# ========================================================
# 2. CAMPAIGNS & MANUAL EXECUTION
# ========================================================
elif menu == "Campaigns & Execution":
    st.subheader("📋 Registered Campaigns")
    
    conn = get_connection()
    df_campaigns = pd.read_sql("SELECT * FROM campaigns ORDER BY id DESC", conn)
    conn.close()
    
    if df_campaigns.empty:
        st.info("No campaigns found. Go to 'Create Campaign' to add one.")
    else:
        st.dataframe(df_campaigns, use_container_width=True)
        
        st.write("---")
        st.markdown("### 🚀 Run Campaign Now")
        
        campaign_options = {f"#{row['id']} - {row['name']}": row['id'] for _, row in df_campaigns.iterrows()}
        selected_label = st.selectbox("Select campaign to run:", list(campaign_options.keys()))
        selected_id = campaign_options[selected_label]
        
        selected_campaign = df_campaigns[df_campaigns['id'] == selected_id].iloc[0].to_dict()
        
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.info(f"**URL:** {selected_campaign.get('newsletter_url')}\n\n"
                    f"**Desktop:** {selected_campaign.get('opens_desktop')} opens | {selected_campaign.get('clicks_desktop')} clicks  \n"
                    f"**Mobile:** {selected_campaign.get('opens_mobile')} opens | {selected_campaign.get('clicks_mobile')} clicks")
        
        with col_c2:
            run_btn = st.button("▶️ Run Test Now", type="primary", use_container_width=True)

        if run_btn:
            if not selected_campaign.get("newsletter_url"):
                st.error("This campaign does not have a configured newsletter URL.")
            else:
                progress_container = st.empty()
                status_log = []

                def update_progress(msg):
                    status_log.append(msg)
                    progress_container.text_area("Live Execution Log:", "\n".join(status_log[-12:]), height=220)

                with st.spinner("Simulating opens and clicks via Playwright..."):
                    try:
                        results = run_test(selected_campaign, on_progress=update_progress)
                        save_execution(selected_campaign["id"], results)
                        st.success("Test completed and saved to execution history!")
                        
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Successful Opens", results["opens_success"])
                        m2.metric("Failed Opens", results["opens_fail"])
                        m3.metric("Successful Clicks", results["clicks_success"])
                        m4.metric("Failed Clicks", results["clicks_fail"])
                        
                        if results.get("article_links_found"):
                            with st.expander(f"Detected Article Links ({len(results['article_links_found'])})"):
                                for link in results["article_links_found"]:
                                    st.write(f"- [{link}]({link})")
                                    
                    except Exception as e:
                        st.error(f"Error during execution: {e}")

# ========================================================
# 3. REPORTS & RESULTS HISTORY
# ========================================================
elif menu == "Reports & History":
    st.subheader("📊 Execution Reports & History")
    
    conn = get_connection()
    query = """
    SELECT 
        e.id AS execution_id,
        c.name AS campaign_name,
        e.date,
        e.opens_success,
        e.opens_fail,
        e.clicks_success,
        e.clicks_fail,
        e.details
    FROM executions e
    LEFT JOIN campaigns c ON e.campaign_id = c.id
    ORDER BY e.id DESC
    """
    df_exec = pd.read_sql(query, conn)
    conn.close()
    
    if df_exec.empty:
        st.info("No campaign execution records found yet.")
    else:
        # Global Aggregated Metrics
        tot_opens_ok = df_exec["opens_success"].sum()
        tot_opens_fail = df_exec["opens_fail"].sum()
        tot_clicks_ok = df_exec["clicks_success"].sum()
        tot_clicks_fail = df_exec["clicks_fail"].sum()
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Successful Opens", int(tot_opens_ok))
        c2.metric("Total Failed Opens", int(tot_opens_fail), delta_color="inverse")
        c3.metric("Total Successful Clicks", int(tot_clicks_ok))
        c4.metric("Total Failed Clicks", int(tot_clicks_fail), delta_color="inverse")
        
        st.write("---")
        st.dataframe(df_exec.drop(columns=["details"], errors="ignore"), use_container_width=True)
        
        st.markdown("#### Execution Details")
        for _, row in df_exec.head(10).iterrows():
            with st.expander(f"Execution #{row['execution_id']} - {row['campaign_name']} ({row['date']})"):
                st.write(f"- **Successful Opens:** {row['opens_success']} | **Failed Opens:** {row['opens_fail']}")
                st.write(f"- **Successful Clicks:** {row['clicks_success']} | **Failed Clicks:** {row['clicks_fail']}")
                try:
                    details = json.loads(row["details"]) if row["details"] else []
                    if details:
                        st.write("**Details / Logged Errors:**")
                        for d in details:
                            st.text(f"• {d}")
                    else:
                        st.write("No errors reported.")
                except Exception:
                    st.text(row["details"])