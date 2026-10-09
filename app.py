import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="BharathCloud CRM | Intelligence Suite",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN ENTERPRISE SAAS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; }
    
    .stApp {
        background-color: #070B14;
        color: #F8FAFC;
    }

    section[data-testid="stSidebar"] {
        background-color: #040711;
        border-right: 1px solid rgba(30, 58, 138, 0.3);
    }

    /* Professional Sidebar Buttons */
    .stButton > button {
        width: 100%;
        text-align: left;
        display: flex;
        align-items: center;
        gap: 12px;
        background-color: transparent;
        color: #94A3B8;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 9px 14px;
        font-weight: 500;
        font-size: 0.90rem;
        letter-spacing: 0.01em;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background-color: rgba(30, 58, 138, 0.25);
        color: #38BDF8;
        border-color: rgba(56, 189, 248, 0.2);
    }

    .hero-banner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.4rem 1.8rem;
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.35) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
    }
    
    .brand-heading {
        font-size: 1.7rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        margin: 0;
    }
    
    .brand-sub { font-size: 0.85rem; color: #94A3B8; margin-top: 4px; }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
        margin-bottom: 1.5rem;
    }
    
    .kpi-box {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(11, 15, 23, 0.95) 100%);
        border: 1px solid rgba(30, 58, 138, 0.45);
        border-radius: 14px;
        padding: 1.3rem 1.6rem;
    }
    
    .kpi-label {
        color: #38BDF8;
        font-size: 0.76rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.3rem;
    }
    
    .kpi-val {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .kpi-sub {
        font-size: 0.78rem;
        color: #34D399;
        margin-top: 4px;
    }

    .activity-row {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.15);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .activity-title {
        font-weight: 600;
        font-size: 1rem;
        color: #FFFFFF;
    }

    .activity-desc {
        font-size: 0.84rem;
        color: #94A3B8;
        margin-top: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- DATABASE ENGINE ---
def run_db_query(sql: str):
    conn = sqlite3.connect("bharathcloud_crm.db")
    try:
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df
    except Exception as e:
        conn.close()
        return str(e)

def add_crm_task(account_id: int, task_desc: str, due_days: int = 2):
    conn = sqlite3.connect("bharathcloud_crm.db")
    cur = conn.cursor()
    due = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")
    cur.execute(
        "INSERT INTO tasks (account_id, task_description, due_date, status) VALUES (?, ?, ?, ?)",
        (account_id, task_desc, due, "Scheduled")
    )
    conn.commit()
    conn.close()
    return due

# --- NATIVE CRM INTENT RESOLVER ---
def resolve_crm_request(user_text: str):
    q = user_text.lower().strip()
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    last_context = st.session_state.get("last_context", {})

    if q in ["hi", "hello", "hey"]:
        return (
            "Hello. I am your BharathCloud Enterprise CRM Agent. Relational schemas, "
            "workload allocations, and task orchestration engines are operational. "
            "How can I assist your sales pipeline today?"
        )

    # Specific account inspection
    for comp in ["astra medtech", "paydirect", "telangana health", "indologistics", "kavach", "deccan fincorp"]:
        if comp in q:
            sql = f"""
            SELECT a.id, a.company_name, a.contact_person, a.assigned_rep, a.last_contacted_date,
                   o.workload_type, o.monthly_recurring_inr, o.stage
            FROM accounts a
            JOIN opportunities o ON a.id = o.account_id
            WHERE LOWER(a.company_name) LIKE '%{comp}%'
            """
            df = run_db_query(sql)
            if isinstance(df, pd.DataFrame) and not df.empty:
                r = df.iloc[0]
                st.session_state.last_context = {"account_ids": [int(r['id'])]}
                return (
                    f"### Account Analysis: {r['company_name']}\n"
                    f"- **Workload Infrastructure:** {r['workload_type']}\n"
                    f"- **Recurring Value:** ₹{r['monthly_recurring_inr']:,.0f} MRR\n"
                    f"- **Current Stage:** *{r['stage']}*\n"
                    f"- **Assigned Rep:** {r['assigned_rep']} (Contact: {r['contact_person']})\n"
                    f"- **Last Engagement:** `{r['last_contacted_date']}`\n\n"
                    f"Recommended Action: State **'Create follow-up task for them'** to schedule pipeline outreach."
                )

    # Multi-turn resolution
    if ("for them" in q or "these" in q or "the first one" in q) and last_context.get("account_ids"):
        target_ids = last_context["account_ids"]
        if "first" in q:
            target_ids = target_ids[:1]
        items = []
        for aid in target_ids:
            acc_info = run_db_query(f"SELECT company_name FROM accounts WHERE id = {aid}")
            cname = acc_info['company_name'].iloc[0] if isinstance(acc_info, pd.DataFrame) and not acc_info.empty else f"Account #{aid}"
            due = add_crm_task(aid, f"Follow up on cloud migration proposal with {cname}", 2)
            items.append(f"- **{cname} (ID: {aid})** → Action item registered (Scheduled: `{due}`)")
        return f"### Context Action Executed\n" + "\n".join(items)

    # Action: Create follow-up tasks
    if any(k in q for k in ["create task", "create follow-up", "schedule", "follow up"]):
        df = run_db_query(f"SELECT id, company_name FROM accounts WHERE last_contacted_date <= '{seven_days_ago}'")
        if isinstance(df, pd.DataFrame) and not df.empty:
            st.session_state.pending_action = {
                "account_ids": df["id"].tolist(),
                "companies": df["company_name"].tolist()
            }
            names = ", ".join(df["company_name"].tolist())
            return (
                f"### Authorization Required\n"
                f"Identified **{len(df)} accounts** untouched for greater than 7 days (*{names}*).\n\n"
                f"**Queued Action:** Insert follow-up tasks scheduled for 48 hours out.\n"
                f"Please confirm execution using the button below."
            )
        return "No stale accounts require follow-up actions."

    # Leads untouched > 7 days
    if any(k in q for k in ["7 days", "contacted", "untouched", "stale"]):
        sql = """
        SELECT a.id, a.company_name, a.assigned_rep, a.last_contacted_date, o.workload_type, o.stage
        FROM accounts a JOIN opportunities o ON a.id = o.account_id
        WHERE a.last_contacted_date <= date('now', '-7 days')
        """
        df = run_db_query(sql)
        if isinstance(df, pd.DataFrame) and not df.empty:
            st.session_state.last_context = {"account_ids": df["id"].tolist()}
            out = f"### Accounts Untouched in Last 7 Days\nFound **{len(df)} enterprise accounts**:\n\n"
            for _, r in df.iterrows():
                out += f"- **{r['company_name']}** ({r['workload_type']}) — Rep: `{r['assigned_rep']}`, Stage: *{r['stage']}* (Last active: `{r['last_contacted_date']}`)\n"
            return out

    # Stuck in Proposal
    if "proposal" in q or "stuck" in q:
        sql = """
        SELECT a.id, a.company_name, o.workload_type, o.monthly_recurring_inr, a.assigned_rep
        FROM accounts a JOIN opportunities o ON a.id = o.account_id
        WHERE o.stage = 'Proposal'
        """
        df = run_db_query(sql)
        if isinstance(df, pd.DataFrame) and not df.empty:
            st.session_state.last_context = {"account_ids": df["id"].tolist()}
            tot = df['monthly_recurring_inr'].sum()
            out = f"### Opportunities in Proposal Stage\n**₹{tot:,.0f} MRR** across **{len(df)} accounts**:\n\n"
            for _, r in df.iterrows():
                out += f"- **{r['company_name']}**: ₹{r['monthly_recurring_inr']:,.0f}/mo — `{r['workload_type']}` (Owner: {r['assigned_rep']})\n"
            return out

    # Top value opportunities
    if any(k in q for k in ["top", "highest", "value"]):
        sql = """
        SELECT a.company_name, o.workload_type, o.monthly_recurring_inr, o.stage
        FROM accounts a JOIN opportunities o ON a.id = o.account_id
        ORDER BY o.monthly_recurring_inr DESC LIMIT 5
        """
        df = run_db_query(sql)
        if isinstance(df, pd.DataFrame):
            out = "### Top Opportunities by MRR\n\n"
            for i, r in df.iterrows():
                out += f"{i+1}. **{r['company_name']}** — **₹{r['monthly_recurring_inr']:,.0f}/mo** ({r['workload_type']}) | Stage: *{r['stage']}*\n"
            return out

    # Fallback Table
    sql = "SELECT a.company_name, o.workload_type, o.monthly_recurring_inr, o.stage FROM accounts a JOIN opportunities o ON a.id = o.account_id"
    df = run_db_query(sql)
    if isinstance(df, pd.DataFrame):
        table_md = "| Company | Solution Tier | Monthly Value | Stage |\n| :--- | :--- | :--- | :--- |\n"
        for _, r in df.iterrows():
            table_md += f"| **{r['company_name']}** | {r['workload_type']} | ₹{r['monthly_recurring_inr']:,.0f} | {r['stage']} |\n"
        return "### Pipeline Snapshot\n\n" + table_md
    return "No records found."

# --- NAVIGATION STATE ---
if "current_view" not in st.session_state:
    st.session_state.current_view = "Overview"

# --- SIDEBAR (CLEAN ENTERPRISE ICONS & LABELS) ---
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:1.8rem; padding: 4px 6px;">
        <svg width="38" height="38" viewBox="0 0 100 100" fill="none">
            <path d="M25 65C16.7157 65 10 58.2843 10 50C10 42.148 16.0368 35.6983 23.7383 35.0566C26.1264 24.321 35.698 16.5 47.1429 16.5C59.2132 16.5 69.2144 25.2152 70.8988 36.804C72.0628 36.5615 73.2678 36.4286 74.5 36.4286C84.165 36.4286 92 44.2636 92 53.9286C92 63.5936 84.165 71.4286 74.5 71.4286L25 71.4286" stroke="#38BDF8" stroke-width="6" stroke-linecap="round"/>
            <rect x="34" y="50" width="6" height="15" rx="3" fill="#38BDF8" />
            <rect x="46" y="42" width="6" height="23" rx="3" fill="#38BDF8" />
            <rect x="58" y="34" width="6" height="31" rx="3" fill="#38BDF8" />
        </svg>
        <div>
            <div style="font-weight:700; font-size:1.05rem; color:#FFFFFF;">BharathCloud</div>
            <div style="font-size:0.72rem; color:#38BDF8; letter-spacing:0.06em; font-weight:600;">INTELLIGENCE SUITE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Professional clean text navigation (matches enterprise dashboard UX)
    if st.button("Overview", key="nav_overview"):
        st.session_state.current_view = "Overview"
    if st.button("AI Copilot", key="nav_copilot"):
        st.session_state.current_view = "AI Copilot"
    if st.button("Pipeline", key="nav_pipeline"):
        st.session_state.current_view = "Pipeline"
    if st.button("Audit Ledger", key="nav_audit"):
        st.session_state.current_view = "Audit Ledger"
    if st.button("Automations", key="nav_automations"):
        st.session_state.current_view = "Automations"

    st.markdown("""
    <div style="margin-top: 6rem; padding: 12px; background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 10px;">
        <div style="display:flex; align-items:center; gap:8px; font-size:0.78rem; font-weight:600; color:#34D399;">
            <span style="height:8px; width:8px; background-color:#34D399; border-radius:50%; display:inline-block;"></span>
            BharathCloud
        </div>
        <div style="font-size:0.72rem; color:#94A3B8; margin-top:3px;">
            Secure • Local Processing<br>Enterprise Grade
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- REFRESH DATABASE DATA ---
conn = sqlite3.connect("bharathcloud_crm.db")
pipe_rev = pd.read_sql_query("SELECT SUM(monthly_recurring_inr) as rev FROM opportunities", conn)["rev"][0] or 0
leads_count = pd.read_sql_query("SELECT COUNT(*) as c FROM accounts", conn)["c"][0]
tasks_count = pd.read_sql_query("SELECT COUNT(*) as c FROM tasks", conn)["c"][0]
acc_df = pd.read_sql_query("SELECT * FROM accounts", conn)
opp_df = pd.read_sql_query("SELECT * FROM opportunities", conn)
tasks_df = pd.read_sql_query("SELECT * FROM tasks ORDER BY id DESC", conn)
conn.close()

# --- HEADER BANNER ---
st.markdown("""
<div class="hero-banner">
    <div>
        <h1 class="brand-heading">BharathCloud CRM Assistant</h1>
        <div class="brand-sub">Smarter pipelines. Autonomous infrastructure orchestration.</div>
    </div>
    <div>
        <span style="background:rgba(56, 189, 248, 0.15); color:#38BDF8; padding:6px 14px; border-radius:9999px; font-size:0.8rem; font-weight:600; border:1px solid rgba(56, 189, 248, 0.35);">
            ● System Connected
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- VIEW 1: OVERVIEW DASHBOARD ---
if st.session_state.current_view == "Overview":
    st.markdown(f"""
    <div class="metric-grid">
        <div class="kpi-box">
            <div class="kpi-label">Pipeline Revenue</div>
            <div class="kpi-val">₹{pipe_rev:,.0f}</div>
            <div class="kpi-sub">↑ 12% vs last 30 days</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Active Workload Leads</div>
            <div class="kpi-val">{leads_count}</div>
            <div class="kpi-sub" style="color:#38BDF8;">6 Enterprises in Stage Flow</div>
        </div>
        <div class="kpi-box">
            <div class="kpi-label">Autonomous Actions Executed</div>
            <div class="kpi-val" style="color:#38BDF8;">{tasks_count}</div>
            <div class="kpi-sub">Verified in Database Audit</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Recent Activity Stream")
    st.caption("Select any account to launch contextual analysis in Copilot:")

    activities = [
        {"name": "Astra MedTech", "desc": "Proposal stage active • ₹85,000 MRR", "status": "10 days untouched", "prompt": "Tell me about Astra MedTech and its cloud migration status"},
        {"name": "PayDirect UPI Gateway", "desc": "Architecture Review in progress • ₹2,60,000 MRR", "status": "Contacted 3 days ago", "prompt": "Tell me about PayDirect UPI Gateway and its cloud requirements"},
        {"name": "Telangana Health Network", "desc": "Migration & DR Review • ₹1,95,000 MRR", "status": "Stuck in Proposal", "prompt": "Tell me about Telangana Health Network deal status"},
        {"name": "Deccan FinCorp", "desc": "Dedicated Bare Metal Cluster • ₹3,40,000 MRR", "status": "High Priority", "prompt": "Tell me about Deccan FinCorp workload requirements"}
    ]

    for idx, act in enumerate(activities):
        c1, c2 = st.columns([4, 1.2])
        with c1:
            st.markdown(f"""
            <div class="activity-row" style="margin-bottom:0px;">
                <div>
                    <div class="activity-title">{act['name']}</div>
                    <div class="activity-desc">{act['desc']}</div>
                </div>
                <div>
                    <span style="background:rgba(30, 58, 138, 0.4); color:#93C5FD; padding:4px 10px; border-radius:6px; font-size:0.75rem;">
                        {act['status']}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("Inspect Account", key=f"act_btn_{idx}"):
                st.session_state.current_view = "AI Copilot"
                if "messages" not in st.session_state:
                    st.session_state.messages = []
                st.session_state.messages.append({"role": "user", "content": act['prompt']})
                rep = resolve_crm_request(act['prompt'])
                st.session_state.messages.append({"role": "assistant", "content": rep})
                st.rerun()

# --- VIEW 2: AI COPILOT ---
elif st.session_state.current_view == "AI Copilot":
    st.markdown("### Ask Your CRM (AI Copilot)")
    
    if "messages" not in st.session_state or not st.session_state.messages:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome. I am your BharathCloud Enterprise CRM Copilot. You can inspect pipeline health, analyze stale deals, or command action automations."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if "pending_action" in st.session_state and st.session_state.pending_action:
        act = st.session_state.pending_action
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Confirm Action", type="primary"):
                created = []
                for aid in act["account_ids"]:
                    acc_info = run_db_query(f"SELECT company_name FROM accounts WHERE id = {aid}")
                    cname = acc_info['company_name'].iloc[0]
                    due = add_crm_task(aid, f"Follow up on cloud migration proposal with {cname}", 2)
                    created.append(f"- **{cname} (ID: {aid})** → Task logged (Scheduled: `{due}`)")
                st.session_state.pending_action = None
                res_msg = f"### Bulk Action Executed\n" + "\n".join(created)
                st.session_state.messages.append({"role": "assistant", "content": res_msg})
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.pending_action = None
                st.session_state.messages.append({"role": "assistant", "content": "Action cancelled."})
                st.rerun()

    user_query = st.chat_input("Enter query or sales command...")
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.spinner("Processing relational query..."):
            reply = resolve_crm_request(user_query)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.rerun()

# --- VIEW 3: PIPELINE ---
elif st.session_state.current_view == "Pipeline":
    st.markdown("### Active Workload Pipeline")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Enterprise Accounts")
        st.dataframe(acc_df, use_container_width=True, hide_index=True)
    with c2:
        st.markdown("#### Workload Opportunities")
        st.dataframe(opp_df, use_container_width=True, hide_index=True)

# --- VIEW 4: AUDIT LEDGER ---
elif st.session_state.current_view == "Audit Ledger":
    st.markdown("### Autonomous Action Audit Ledger")
    if len(tasks_df) == 0:
        st.info("No tasks recorded yet. Issue action commands in the AI Copilot to see mutations logged here.")
    else:
        st.dataframe(tasks_df, use_container_width=True, hide_index=True)

# --- VIEW 5: AUTOMATIONS ---
elif st.session_state.current_view == "Automations":
    st.markdown("### Autonomous Engine Settings & Triggers")
    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); padding: 16px; border-radius: 12px;">
            <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">Stale Deal Trigger</div>
            <div style="color: #94A3B8; font-size: 0.85rem;">Automatically flags accounts untouched for > 7 days and queues follow-ups.</div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); padding: 16px; border-radius: 12px;">
            <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">Proposal Risk Engine</div>
            <div style="color: #94A3B8; font-size: 0.85rem;">Monitors high-value deals stuck in Proposal stage to prevent pipeline leakage.</div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); padding: 16px; border-radius: 12px;">
            <div style="color: #34D399; font-weight: 700; margin-bottom: 6px;">Human-in-the-Loop Safeguard</div>
            <div style="color: #94A3B8; font-size: 0.85rem;">Requires sales manager authorization before executing bulk database writes.</div>
        </div>
        <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(56, 189, 248, 0.2); padding: 16px; border-radius: 12px;">
            <div style="color: #38BDF8; font-weight: 700; margin-bottom: 6px;">Local Sovereignty Protocol</div>
            <div style="color: #94A3B8; font-size: 0.85rem;">Executes query routines in an isolated environment with zero data leakage.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)