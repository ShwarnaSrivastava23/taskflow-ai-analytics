# 📊 TaskFlow Analytics Assistant

An AI-powered natural language analytics tool for SaaS business data. Ask questions in plain English — like *"What is the churn rate by plan tier?"* — and get back real, SQL-backed answers with auto-generated charts.

🔗 **Live demo:** [taskflow-ai-analytics-k98f95vpxkpscfftevxtut.streamlit.app](https://taskflow-ai-analytics-k98f95vpxkpscfftevxtut.streamlit.app/)

🔗 **GitHub repo:** [github.com/ShwarnaSrivastava23/taskflow-ai-analytics](https://github.com/ShwarnaSrivastava23/taskflow-ai-analytics)

---

## What it does

This project simulates a fictional SaaS company ("TaskFlow") and lets anyone query its business data conversationally instead of writing SQL by hand. Under the hood, an LLM converts each question into a real SQL query, runs it against a database, and renders the results as a table and chart.

**Example questions it can answer:**
- What is the churn rate by plan tier?
- What is our total MRR?
- What are the top 5 issue types in support tickets?
- Which country has the most Enterprise customers?
- Which plan tier has the highest churn among small companies?
- How many users signed up each month?
- What is the average satisfaction score by plan tier?

---

## How it works

```
User question
    ↓
LLM (Groq / Llama) converts question → SQL, using the database schema as context
    ↓
SQL is validated (read-only check — blocks DROP/DELETE/UPDATE/etc.)
    ↓
Query runs against DuckDB
    ↓
Results shown as a table + auto-generated chart (Plotly)
```

---

## Tech stack

- **Python** — core language
- **Groq API (Llama / GPT-OSS models)** — natural language → SQL generation
- **DuckDB** — lightweight, fast analytics database
- **Streamlit** — web app / UI framework
- **Plotly** — interactive charts
- **Faker** — synthetic data generation

---

## Dataset

Since real company data raises privacy/confidentiality concerns, I generated a realistic **synthetic SaaS dataset** (800 users, ~14,000 usage events, subscriptions, and support tickets) with intentional realistic patterns — for example, users with low product usage have a meaningfully higher churn probability, mirroring real-world SaaS behavior.

The dataset spans four related tables:
- **users** — signup date, plan tier, company size, country
- **subscriptions** — plan tier, MRR, active/churned status
- **usage_events** — logins, tasks created, reports generated, etc.
- **support_tickets** — issue type, resolution time, satisfaction score

---

## Safety guardrails

- All generated SQL is validated before execution — only `SELECT` statements are allowed; any query containing `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, or similar is blocked.
- The underlying LLM also has its own built-in safety behavior and will refuse to generate destructive queries in the first place — so the app has two independent layers of protection.

---

## Challenges faced (and how I solved them)

**1. Model deprecation mid-build**
My first choice of LLM (`llama-3.3-70b-versatile` on Groq) returned a 404 error — Groq had deprecated that model. I researched their current model lineup and switched to `openai/gpt-oss-120b`, which taught me to always verify model availability rather than trust cached documentation or tutorials.

**2. Silent `.gitignore` conflict**
When setting up Git, I discovered Python's `venv` module auto-generates its *own* `.gitignore` file inside the `venv/` folder. I had accidentally moved that auto-generated file (which ignores everything with a bare `*`) to my project root instead of my intended one — which made Git think the entire project was empty. Diagnosing this required comparing file contents directly rather than assuming the file was correct.

**3. Deployment failing on a clean environment**
The app worked perfectly locally but crashed on Streamlit Community Cloud with a `ModuleNotFoundError`. My local virtual environment had all packages installed, but I hadn't created a `requirements.txt` — so the cloud server had no way to know what to install. This reinforced the importance of explicit dependency declarations for reproducible deployments.

**4. Environment variables across local vs. cloud**
My API key worked locally via a `.env` file, but Streamlit Cloud uses its own secrets management system. I wrote a small fallback function that checks `st.secrets` first (for the deployed app) and falls back to `.env` locally, so the same codebase works in both environments without modification.

---

## Running it locally

```bash
git clone https://github.com/ShwarnaSrivastava23/taskflow-ai-analytics.git
cd taskflow-ai-analytics
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Create a `.env` file in the root with:
```
GROQ_API_KEY=your_key_here
```

Generate the data and run the app:
```bash
python app/generate_data.py
python app/load_db.py
streamlit run app/streamlit_app.py
```

---

## What I'd improve next

- Add a formal query evaluation suite to track SQL generation accuracy over a fixed test set of questions
- Support follow-up / conversational questions (multi-turn context)
- Add user authentication for a real multi-tenant scenario
- Cache repeated questions to reduce API calls

---

Built by **Shwarna Srivastava**
