import duckdb

# Connect to (or create) a persistent DuckDB database file
con = duckdb.connect("data/taskflow.duckdb")

# Load each CSV directly into a table in the database
con.execute("""
    CREATE OR REPLACE TABLE users AS
    SELECT * FROM read_csv_auto('data/users.csv')
""")

con.execute("""
    CREATE OR REPLACE TABLE usage_events AS
    SELECT * FROM read_csv_auto('data/usage_events.csv')
""")

con.execute("""
    CREATE OR REPLACE TABLE subscriptions AS
    SELECT * FROM read_csv_auto('data/subscriptions.csv')
""")

con.execute("""
    CREATE OR REPLACE TABLE support_tickets AS
    SELECT * FROM read_csv_auto('data/support_tickets.csv')
""")

# Quick sanity check: print row counts for each table
tables = ["users", "usage_events", "subscriptions", "support_tickets"]
print("✅ Database created at data/taskflow.duckdb\n")
for t in tables:
    count = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {count} rows")

# Try one real query as a test — top 5 countries by number of users
print("\n📊 Sample query — Users by country:")
result = con.execute("""
    SELECT country, COUNT(*) as user_count
    FROM users
    GROUP BY country
    ORDER BY user_count DESC
""").fetchdf()
print(result)

con.close()