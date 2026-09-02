import streamlit as st
import plotly.express as px
from text_to_sql import generate_sql, run_query

# Page setup
st.set_page_config(page_title="TaskFlow Analytics Assistant", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stTextInput input {
        border-radius: 10px;
        border: 1.5px solid #2D2D3D;
        background-color: #1A1A26;
        padding: 14px 18px;
        font-size: 16px;
        color: #E5E7EB;
    }
    .stTextInput input:focus {
        border-color: #818CF8;
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3);
    }
    div[data-testid="stExpander"] {
        border-radius: 12px;
        border: 1px solid #2D2D3D;
        background-color: #1A1A26;
    }
    .stButton button {
        border-radius: 10px;
        background-color: #1A1A26;
        color: #E5E7EB;
        font-weight: 500;
        border: 1px solid #2D2D3D;
        transition: all 0.2s;
    }
    .stButton button:hover {
        border-color: #818CF8;
        color: #818CF8;
        transform: translateY(-1px);
    }
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }
    code {
        color: #A78BFA !important;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }
    .kpi-card {
        background-color: #1A1A26;
        border: 1px solid #2D2D3D;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        text-align: left;
        transition: all 0.2s;
    }
    .kpi-card:hover {
        border-color: #818CF8;
    }
    .kpi-label {
        color: #9CA3AF;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        color: #818CF8;
        font-size: 1.6rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown("### 📊 TaskFlow")
    st.caption("AI Analytics Assistant")
    st.divider()
    st.markdown("**About this project**")
    st.write("Ask natural language questions about SaaS metrics — churn, MRR, usage, and support data — and get instant SQL-backed answers.")
    st.divider()
    st.markdown("**Tech stack**")
    st.write("Groq (Llama) · DuckDB · Streamlit · Plotly")
    st.divider()
    st.markdown("**Built by** Your Name")
    st.markdown("[GitHub](#) · [LinkedIn](#)")

# Header banner (only ONE copy of this block)
st.markdown("""
    <div style="background: linear-gradient(135deg, #6366F1 0%, #A78BFA 100%);
                padding: 2.5rem; border-radius: 20px; margin-bottom: 1.5rem;
                box-shadow: 0 10px 40px rgba(99, 102, 241, 0.25);">
        <h1 style="color: white; margin: 0; font-size: 2.3rem; font-weight: 800;">📊 TaskFlow Analytics Assistant</h1>
        <p style="color: #E0E7FF; margin-top: 0.6rem; font-size: 1.1rem;">
            Ask questions about our SaaS data in plain English — powered by AI
        </p>
    </div>
""", unsafe_allow_html=True)

# KPI summary cards
kpi_df = run_query("""
    SELECT
        (SELECT COUNT(*) FROM users) AS total_users,
        (SELECT ROUND(SUM(mrr)) FROM subscriptions WHERE status = 'active') AS total_mrr,
        (SELECT ROUND(100.0 * SUM(CASE WHEN status='churned' THEN 1 ELSE 0 END) / COUNT(*), 1) FROM subscriptions) AS churn_rate,
        (SELECT COUNT(*) FROM support_tickets) AS total_tickets
""")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Users</div><div class="kpi-value">{int(kpi_df.total_users[0]):,}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total MRR</div><div class="kpi-value">${int(kpi_df.total_mrr[0]):,}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Churn Rate</div><div class="kpi-value">{kpi_df.churn_rate[0]}%</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Support Tickets</div><div class="kpi-value">{int(kpi_df.total_tickets[0]):,}</div></div>', unsafe_allow_html=True)

st.write("")

# Quick-question chips
st.markdown("**Try a quick question:**")
example_questions = [
    ("Churn by plan tier", "What is the churn rate by plan tier?"),
    ("Total MRR", "What is our total MRR?"),
    ("Top support issues", "What are the top 5 issue types in support tickets?"),
    ("Users by country", "How many users are there by country?"),
]
cols = st.columns(len(example_questions))
clicked_question = None
for i, (label, full_q) in enumerate(example_questions):
    if cols[i].button(label, use_container_width=True):
        clicked_question = full_q

with st.expander("💡 More example questions"):
    st.markdown("""
    **Revenue & Growth**
    - What is the average MRR per country?
    - How many users signed up each month?

    **Usage & Engagement**
    - Which plan tier has the most active users?
    - How many users have never logged in?

    **Support & Satisfaction**
    - What is the average resolution time by issue type?
    - What is the average satisfaction score by plan tier?

    **Customer Segments**
    - Which country has the most Enterprise customers?
    - Which plan tier has the highest churn among small companies?
    """)

# Input box (pre-filled if a chip was clicked)
question = st.text_input(
    "Ask a question about the data:",
    value=clicked_question if clicked_question else "",
    placeholder="e.g. What is the churn rate by plan tier?"
)

if question:
    with st.spinner("Thinking..."):
        try:
            sql = generate_sql(question)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            df = run_query(sql)
            st.subheader("Results")

            if df.empty:
                st.warning("No results found for this question.")
            else:
                st.dataframe(df, use_container_width=True)

                numeric_cols = df.select_dtypes(include="number").columns.tolist()
                non_numeric_cols = df.select_dtypes(exclude="number").columns.tolist()

                if len(numeric_cols) >= 1 and len(non_numeric_cols) >= 1 and len(df) <= 50:
                    x_col = non_numeric_cols[0]
                    y_col = numeric_cols[0]
                    fig = px.bar(
                        df, x=x_col, y=y_col, title=f"{y_col} by {x_col}",
                        color_discrete_sequence=["#818CF8"]
                    )
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font_color="#E5E7EB"
                    )
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.info("Try rephrasing your question, or check that your database and API key are set up correctly.")