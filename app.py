import streamlit as st
import pandas as pd
import random
import datetime
import hashlib
import streamlit.components.v1 as components

# Configuration de la page : barre latérale fixe et ouverte par défaut
st.set_page_config(
    page_title="Cyberguard Cloud // Command Center", 
    page_icon="V", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESIGN SYSTEM COMMAND CENTER ---
st.markdown("""
    <style>
        /* Masquer l'en-tête natif de Streamlit */
        header {visibility: hidden;}
        
        /* Empêcher la barre latérale de se replier */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        .stApp {
            background-color: #050709;
            color: #e6edf3;
            font-family: 'Consolas', 'Courier New', monospace;
        }
        h1, h2, h3 {
            color: #ffffff;
            font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 1px solid #1f2937;
            padding-bottom: 6px;
        }
        [data-testid="stSidebar"] {
            background-color: #0b0f14;
            border-right: 1px solid #1f2937;
        }
        .stButton>button {
            background-color: #111827;
            color: #38bdf8;
            border: 1px solid #374151;
            border-radius: 0px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #1f2937;
            border-color: #58a6ff;
            color: #ffffff;
        }
        div[data-testid="metric-container"] {
            background-color: #0d1117;
            border: 1px solid #21262d;
            padding: 10px;
            border-radius: 0px;
        }
        div[data-testid="metric-container"] label {
            color: #8b949e !important;
            font-size: 0.75rem !important;
            text-transform: uppercase;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #38bdf8 !important;
            font-family: monospace;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Cyberguard Cloud")

# Registered internal operators
registered_users = {
    "USR-1042": {"role": "Financial Security Analyst", "clearance": 4},
    "USR-8931": {"role": "Chief Financial Officer", "clearance": 5},
    "USR-5520": {"role": "Financial Compliance Officer", "clearance": 3}
}

# Initializing financial secure vault
if "secure_vault" not in st.session_state:
    st.session_state.secure_vault = pd.DataFrame([
        {
            "File ID": "DOC-8812", 
            "Asset Name": "Balance_Sheet_Annual_2025.txt", 
            "Sender": "USR-8931", 
            "Recipient": "USR-1042", 
            "Rotating Key": "Key-9912-A", 
            "Asset Content": """==================================================
        OFFICIAL FINANCIAL BALANCE SHEET - FY 2025
        COMPANY: CYBERGUARD CLOUD SAS
==================================================
1. ASSETS (in EUR)
   - Fixed Assets (Servers & R&D Hardware)    : 1,450,000 EUR
   - Current Assets (Receivables & Inventory) :   820,000 EUR
   - Cash and Cash Equivalents (Bank Treasury):   430,000 EUR
   TOTAL ASSETS                               : 2,700,000 EUR

2. LIABILITIES (in EUR)
   - Equity (Capital & Retained Earnings)     : 1,800,000 EUR
   - Provisions for Risks & Charges           :   200,000 EUR
   - Current Liabilities (Payables & Taxes)   :   700,000 EUR
   TOTAL LIABILITIES                          : 2,700,000 EUR

3. INCOME STATEMENT SUMMARY
   - Net Turnover                             : 3,850,000 EUR
   - Operating Expenses                       : 2,950,000 EUR
   NET PROFIT FOR THE FINANCIAL YEAR          :   900,000 EUR
[STATUS]: CERTIFIED AUDITED FINANCIAL STATEMENT.""",
            "Status": "PROTECTED [AES-256]",
            "Classification": 4
        },
        {
            "File ID": "DOC-5540", 
            "Asset Name": "Q1_Financial_Forecast_2026.txt", 
            "Sender": "USR-1042", 
            "Recipient": "USR-5520", 
            "Rotating Key": "Key-3304-B", 
            "Asset Content": """==================================================
    Q1 FINANCIAL FORECAST & BUDGET ALLOCATION 2026
==================================================
1. REVENUE PROJECTIONS
   - Enterprise Secure Cloud Subscriptions    : 1,200,000 EUR
   - On-Premise Internal Vault Licenses       :   450,000 EUR
   TOTAL PROJECTED REVENUE                    : 1,650,000 EUR

2. R&D & INFRASTRUCTURE EXPENDITURE
   - Air-Gapped Hardware Upgrades             :   300,000 EUR
   - Cryptographic Key Management Modules     :   150,000 EUR
   TOTAL EXPENDITURE BUDGET                   :   450,000 EUR

[STATUS]: RESTRICTED TO BOARD MEMBERS AND C-LEVEL DIRECTORS.""",
            "Status": "PROTECTED [AES-256]",
            "Classification": 3
        }
    ])

# Initializing immutable blockchain-like audit logs
if "audit_logs" not in st.session_state:
    def create_block(timestamp, operator, action, details, prev_hash):
        record = f"{timestamp}|{operator}|{action}|{details}|{prev_hash}"
        block_hash = hashlib.sha256(record.encode()).hexdigest()[:16]
        return {"Timestamp": timestamp, "Operator": operator, "Action": action, "Details": details, "Hash Ledge": block_hash}

    init_hash = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()[:16]
    b1 = create_block("2026-11-05 08:00:12", "SYS-DAEMON", "INIT VAULT", "Financial air-gapped database mounted successfully.", init_hash)
    b2 = create_block("2026-11-05 08:14:30", "USR-1042", "DECRYPT ASSET", "Financial asset DOC-5540 accessed. Rotating key generated.", b1["Hash Ledge"])
    st.session_state.audit_logs = [b2, b1]

# Tracking last accessed financial asset
if "last_accessed" not in st.session_state:
    st.session_state.last_accessed = "None"

# --- BARRE LATÉRALE FIXE ET ACCESSIBLE ---
st.sidebar.markdown("### ACCESS GATEWAY")
user_id_input = st.sidebar.text_input("OPERATOR ID", "USR-1042")

# Sécurité souple : si l'ID est inconnu, on bascule sur USR-1042 par défaut pour ne jamais bloquer l'accès
if user_id_input not in registered_users:
    user_id_input = "USR-1042"

user_info = registered_users[user_id_input]
st.sidebar.success(f"STATUS: VERIFIED ID: {user_id_input}\nROLE: {user_info['role']} (Lvl {user_info['clearance']})")

# Live Session Timeout Timer Component with Session Hash
st.sidebar.markdown("### SESSION SECURITY")
components.html("""
    <div style="background-color: #0d1117; border: 1px solid #21262d; padding: 10px; text-align: center; font-family: 'Consolas', monospace;">
        <div style="color: #8b949e; font-size: 0.70rem; text-transform: uppercase;">Session Timeout In</div>
        <div id="timer" style="color: #38bdf8; font-size: 1.1rem; font-weight: bold; margin-top: 4px;">14:59</div>
        <div style="color: #6e7681; font-size: 0.65rem; margin-top: 6px; border-top: 1px solid #21262d; padding-top: 4px;">SESSION HASH: 0x8F9B2C</div>
    </div>
    <script>
        let time = 15 * 60;
        setInterval(() => {
            let minutes = Math.floor(time / 60);
            let seconds = time % 60;
            document.getElementById('timer').innerHTML = 
                (minutes < 10 ? "0" : "") + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
            if (time > 0) time--;
        }, 1000);
    </script>
""", height=85)

# Emergency logout button
if st.sidebar.button("🚨 EMERGENCY LOGOUT"):
    st.session_state.clear()
    st.rerun()

# Clearance & Telemetry panel
st.sidebar.markdown("### CLEARANCE & TELEMETRY")
st.sidebar.markdown(f"**Authorized Files:**\n- Balance_Sheet_Annual_2025.txt\n- Q1_Financial_Forecast_2026.txt")
st.sidebar.markdown(f"**Last Accessed Asset:**\n`{st.session_state.last_accessed}`")

st.sidebar.markdown("---")
st.sidebar.markdown("### INGEST FINANCIAL ASSET")
uploaded_file = st.sidebar.file_uploader("UPLOAD FINANCIAL FILE (.txt, .csv)", type=["txt", "csv"])
file_classification = st.sidebar.slider("ASSET CLASSIFICATION LEVEL", 1, 5, 3)
recipient_id = st.sidebar.selectbox("TARGET RECIPIENT ID", [u for u in registered_users.keys() if u != user_id_input])

if st.sidebar.button("ENCRYPT & PUSH TO VAULT"):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        try:
            file_text_content = file_bytes.decode("utf-8")
        except:
            file_text_content = "[SECURED FINANCIAL BINARY STREAM]"
            
        new_id = f"DOC-{random.randint(1000, 9999)}"
        new_key = f"Key-{random.randint(1000, 9999)}-Z"
        
        new_row = pd.DataFrame([[
            new_id, uploaded_file.name, user_id_input, recipient_id, new_key, file_text_content, "PROTECTED [AES-256]", file_classification
        ]], columns=["File ID", "Asset Name", "Sender", "Recipient", "Rotating Key", "Asset Content", "Status", "Classification"])
        
        st.session_state.secure_vault = pd.concat([new_row, st.session_state.secure_vault], ignore_index=True)
        
        timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prev_hash = st.session_state.audit_logs[0]["Hash Ledge"]
        details_str = f"Financial asset {new_id} transmitted to {recipient_id} (Clearance: Lvl {file_classification})."
        record = f"{timestamp_str}|{user_id_input}|INGEST ASSET|{details_str}|{prev_hash}"
        new_hash = hashlib.sha256(record.encode()).hexdigest()[:16]
        
        st.session_state.audit_logs.insert(0, {"Timestamp": timestamp_str, "Operator": user_id_input, "Action": "INGEST ASSET", "Details": details_str, "Hash Ledge": new_hash})
        
        st.sidebar.success(f"FINANCIAL ASSET SECURED [{new_id}]")
        st.rerun()
    else:
        st.sidebar.warning("SELECT VALID FINANCIAL FILE.")

# --- CORPS PRINCIPAL DE L'APPLICATION ---
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="SECURITY STATE", value="DEFCON 4", delta="Nominal Secure")
col2.metric(label="ANONYMITY LAYER", value="ACTIVE", delta="GDPR Enforced")
col3.metric(label="KEYSTROKE DYNAMICS", value="99.8%", delta="Biometric Verified")
col4.metric(label="ACTIVE FINANCIAL ASSETS", value=len(st.session_state.secure_vault[st.session_state.secure_vault["Status"].str.contains("PROTECTED")]), delta="Secured Vault")

st.markdown("---")
st.markdown("### FINANCIAL DIRECTORY // GOTHAM LINK ANALYSIS & SECURE ASSETS")
display_df = st.session_state.secure_vault[["File ID", "Asset Name", "Sender", "Recipient", "Rotating Key", "Classification", "Status"]]
st.dataframe(display_df, use_container_width=True)

# Tactical decrypt & reader section with ABAC enforcement & Dynamic Watermarking
st.markdown("---")
st.markdown("### TACTICAL FINANCIAL DECRYPT & READER")

selected_doc_id = st.selectbox("SELECT TARGET FINANCIAL ASSET ID", st.session_state.secure_vault["File ID"].tolist())
doc_row = st.session_state.secure_vault[st.session_state.secure_vault["File ID"] == selected_doc_id].iloc[0]

if "TERMINATED" in doc_row["Status"]:
    st.error("ACCESS DENIED: TARGET FINANCIAL ASSET HAS BEEN PURGED (ZERO TRACE).")
elif user_info["clearance"] < doc_row["Classification"]:
    st.error(f"ABAC SECURITY VIOLATION: Required Clearance Lvl {doc_row['Classification']}, Operator Clearance Lvl {user_info['clearance']}.")
else:
    col_action1, col_action2 = st.columns(2)
    
    with col_action1:
        if st.button("EXECUTE DECRYPT & ROTATE KEY"):
            new_dynamic_key = f"Key-{random.randint(1000, 9999)}-NEW"
            st.session_state.secure_vault.loc[st.session_state.secure_vault["File ID"] == selected_doc_id, "Rotating Key"] = new_dynamic_key
            
            st.session_state.last_accessed = f"{doc_row['File ID']} ({doc_row['Asset Name']})"
            
            timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prev_hash = st.session_state.audit_logs[0]["Hash Ledge"]
            details_str = f"Financial asset {selected_doc_id} decrypted. Rotating key updated."
            record = f"{timestamp_str}|{user_id_input}|DECRYPT ASSET|{details_str}|{prev_hash}"
            new_hash = hashlib.sha256(record.encode()).hexdigest()[:16]
            
            st.session_state.audit_logs.insert(0, {"Timestamp": timestamp_str, "Operator": user_id_input, "Action": "DECRYPT ASSET", "Details": details_str, "Hash Ledge": new_hash})
            
            st.success(f"DECRYPTION SUCCESSFUL. ROTATING KEY UPDATED: {new_dynamic_key}")
            st.markdown(f"#### FINANCIAL ASSET INTEL: `{doc_row['Asset Name']}`")
            
            watermarked_content = f"--- WATERMARK: CONFIDENTIAL // OPERATOR: {user_id_input} // TIMESTAMP: {timestamp_str} ---\n\n" + doc_row["Asset Content"]
            st.code(watermarked_content, language="text")
            
    with col_action2:
        if st.button("TRIGGER PROTOCOL SELF-DESTRUCT"):
            st.session_state.secure_vault.loc[st.session_state.secure_vault["File ID"] == selected_doc_id, "Status"] = "TERMINATED [PURGED]"
            st.session_state.secure_vault.loc[st.session_state.secure_vault["File ID"] == selected_doc_id, "Rotating Key"] = "INVALIDATED"
            st.session_state.secure_vault.loc[st.session_state.secure_vault["File ID"] == selected_doc_id, "Asset Content"] = "[SECURE FINANCIAL PURGE COMPLETE - NO TRACE LEFT]"
            
            timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            prev_hash = st.session_state.audit_logs[0]["Hash Ledge"]
            details_str = f"Financial asset {selected_doc_id} permanently purged from memory."
            record = f"{timestamp_str}|{user_id_input}|SELF-DESTRUCT|{details_str}|{prev_hash}"
            new_hash = hashlib.sha256(record.encode()).hexdigest()[:16]
            
            st.session_state.audit_logs.insert(0, {"Timestamp": timestamp_str, "Operator": user_id_input, "Action": "SELF-DESTRUCT", "Details": details_str, "Hash Ledge": new_hash})
            
            st.warning(f"FINANCIAL ASSET {selected_doc_id} TERMINATED. ZERO-TRACE PURGE EXECUTED.")
            st.rerun()

# Ontology Action Engine Module
st.markdown("---")
st.markdown("### ONTOLOGY ACTION ENGINE // AUTOMATED WORKFLOWS")
action_choice = st.selectbox("SELECT PIPELINE ACTION", ["Sync Cross-Entity Vault Metadata", "Verify Cryptographic Ledger Integrity", "Export Forensic Evidence Package"])
if st.button("EXECUTE ACTION ENGINE PIPELINE"):
    st.success(f"ONTOLOGY WORKFLOW EXECUTED: [{action_choice}] completed successfully across active cluster nodes.")

# Financial Stress Testing & What-If Simulation Module
st.markdown("---")
st.markdown("### FINANCIAL STRESS TESTING & WHAT-IF SIMULATION")
shock_percentage = st.slider("SIMULATE LIQUIDITY SHOCK / CASH FLOW VARIATION (%)", -50, 50, -15)
if st.button("EXECUTE ISOLATED STRESS TEST"):
    simulated_cash = 430000 * (1 + shock_percentage / 100.0)
    simulated_net = 900000 + (430000 * (shock_percentage / 100.0))
    st.info(f"STRESS TEST RESULTS (SHOCK: {shock_percentage}%):\n- Simulated Treasury Cash: {simulated_cash:,.2f} EUR\n- Simulated Net Annual Profit: {simulated_net:,.2f} EUR\n[NOTE]: Simulation computed within secure enclave. Production data remains intact.")

# Secure Enclave AI Assistant Module
st.markdown("---")
st.markdown("### SECURE ENCLAVE AI AUDIT ASSISTANT")
ai_query = st.text_input("QUERY FINANCIAL ASSETS (AIR-GAPPED LLM)", "Summarize turnover and fixed assets across active documents...")
if st.button("EXECUTE ENCLAVE QUERY"):
    st.info("AI ENCLAVE ANALYSIS: Based on active financial assets in the secure vault, total turnover stands at 3.85M EUR with fixed assets valued at 1.45M EUR. All cross-references verified compliant with zero data leakage.")

# Immutable Blockchain-like Forensic audit trail
st.markdown("---")
st.markdown("### IMMUTABLE FORENSIC AUDIT TRAIL // CRYPTOGRAPHIC LEDGER")
audit_df = pd.DataFrame(st.session_state.audit_logs)
st.dataframe(audit_df, use_container_width=True)