import os
import duckdb
from groq import Groq
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Describe our database schema so the LLM knows what it's working with
SCHEMA = """
Table: users
- user_id (integer, primary key)
- company_name (text)
- signup_date (date)
- plan_tier (text: 'Free', 'Starter', 'Pro', 'Enterprise')
- company_size (text)
- country (text)

Table: usage_events
- event_id (integer, primary key)
- user_id (integer, foreign key -> users.user_id)
- event_type (text: 'login', 'task_created', 'report_generated', 'file_uploaded', 'comment_added')
- event_date (date)

Table: subscriptions
- user_id (integer, foreign key -> users.user_id)
- plan_tier (text)
- mrr (float, monthly recurring revenue in USD)
- status (text: 'active' or 'churned')
- churn_date (date, nullable)

Table: support_tickets
- ticket_id (integer, primary key)
- user_id (integer, foreign key -> users.user_id)
- issue_type (text)
- created_date (date)
- resolution_hours (float)
- satisfaction_score (integer 1-5, nullable)
"""

def generate_sql(question: str) -> str:
    """Takes a natural language question and returns a SQL query."""

    system_prompt = f"""You are a SQL expert. Given a database schema and a question, write a single valid DuckDB SQL query that answers it.

Schema:
{SCHEMA}

Rules:
- Return ONLY the SQL query, no explanation, no markdown code fences, no extra text.
- Use only SELECT statements — never write/modify data.
- Use table joins where needed via user_id.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    # Safety cleanup: remove markdown fences if the model adds them anyway
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


# Keywords that should never appear in a query we run
FORBIDDEN_KEYWORDS = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "REPLACE"]

def is_safe_query(sql: str) -> bool:
    """Checks that the SQL is read-only (SELECT statements only)."""
    sql_upper = sql.upper()

    # Must start with SELECT (ignoring leading whitespace/newlines)
    if not sql_upper.strip().startswith("SELECT"):
        return False

    # Must not contain any dangerous keywords anywhere in the query
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in sql_upper:
            return False

    return True


def run_query(sql: str):
    """Runs the SQL against our DuckDB database and returns a DataFrame. Blocks unsafe queries."""
    if not is_safe_query(sql):
        raise ValueError("This query was blocked for safety reasons — only SELECT statements are allowed.")

    con = duckdb.connect("data/taskflow.duckdb")
    result = con.execute(sql).fetchdf()
    con.close()
    return result


# -------------------------
# Quick test
# -------------------------
if __name__ == "__main__":
    question = "What is the churn rate by plan tier?"
    print(f"❓ Question: {question}\n")

    sql = generate_sql(question)
    print(f"🧠 Generated SQL:\n{sql}\n")

    df = run_query(sql)
    print("📊 Result:")
    print(df)