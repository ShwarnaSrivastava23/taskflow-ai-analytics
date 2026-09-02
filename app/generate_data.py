import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)
np.random.seed(42)

# -------------------------
# 1. USERS TABLE
# -------------------------
NUM_USERS = 800
plan_tiers = ["Free", "Starter", "Pro", "Enterprise"]
countries = ["USA", "India", "UK", "Germany", "Canada", "Australia"]

users = []
for i in range(NUM_USERS):
    signup_date = fake.date_between(start_date="-2y", end_date="today")
    users.append({
        "user_id": i + 1,
        "company_name": fake.company(),
        "signup_date": signup_date,
        "plan_tier": random.choices(plan_tiers, weights=[40, 30, 20, 10])[0],
        "company_size": random.choice(["1-10", "11-50", "51-200", "201-500", "500+"]),
        "country": random.choice(countries)
    })

users_df = pd.DataFrame(users)

# -------------------------
# 2. USAGE EVENTS TABLE
# -------------------------
event_types = ["login", "task_created", "report_generated", "file_uploaded", "comment_added"]
usage_events = []
event_id = 1

for user in users:
    # Users on higher plans tend to be more active (realistic pattern)
    activity_level = {"Free": 5, "Starter": 15, "Pro": 30, "Enterprise": 50}[user["plan_tier"]]
    num_events = np.random.poisson(activity_level)

    for _ in range(num_events):
        days_since_signup = (datetime.today().date() - user["signup_date"]).days
        if days_since_signup <= 0:
            continue
        event_date = user["signup_date"] + timedelta(days=random.randint(0, days_since_signup))
        usage_events.append({
            "event_id": event_id,
            "user_id": user["user_id"],
            "event_type": random.choice(event_types),
            "event_date": event_date
        })
        event_id += 1

usage_df = pd.DataFrame(usage_events)

# -------------------------
# 3. SUBSCRIPTIONS TABLE (with churn logic)
# -------------------------
plan_prices = {"Free": 0, "Starter": 15, "Pro": 49, "Enterprise": 199}
subscriptions = []

for user in users:
    user_events = usage_df[usage_df["user_id"] == user["user_id"]]
    num_user_events = len(user_events)

    # Low usage = higher churn chance (realistic pattern for later insights)
    churn_probability = 0.4 if num_user_events < 5 else 0.1
    is_churned = random.random() < churn_probability

    mrr = plan_prices[user["plan_tier"]]
    status = "churned" if is_churned else "active"
    churn_date = None
    if is_churned:
        days_since_signup = (datetime.today().date() - user["signup_date"]).days
        if days_since_signup > 30:
            churn_date = user["signup_date"] + timedelta(days=random.randint(30, days_since_signup))

    subscriptions.append({
        "user_id": user["user_id"],
        "plan_tier": user["plan_tier"],
        "mrr": mrr,
        "status": status,
        "churn_date": churn_date
    })

subs_df = pd.DataFrame(subscriptions)

# -------------------------
# 4. SUPPORT TICKETS TABLE
# -------------------------
issue_types = ["billing", "bug", "feature_request", "how_to", "performance"]
tickets = []
ticket_id = 1

for user in users:
    num_tickets = np.random.poisson(1.5)
    for _ in range(num_tickets):
        days_since_signup = (datetime.today().date() - user["signup_date"]).days
        if days_since_signup <= 0:
            continue
        created_date = user["signup_date"] + timedelta(days=random.randint(0, days_since_signup))
        resolution_hours = round(np.random.exponential(24), 1)
        tickets.append({
            "ticket_id": ticket_id,
            "user_id": user["user_id"],
            "issue_type": random.choice(issue_types),
            "created_date": created_date,
            "resolution_hours": resolution_hours,
            "satisfaction_score": random.choice([1, 2, 3, 4, 5, None])  # some missing on purpose
        })
        ticket_id += 1

tickets_df = pd.DataFrame(tickets)

# -------------------------
# SAVE TO CSV
# -------------------------
users_df.to_csv("data/users.csv", index=False)
usage_df.to_csv("data/usage_events.csv", index=False)
subs_df.to_csv("data/subscriptions.csv", index=False)
tickets_df.to_csv("data/support_tickets.csv", index=False)

print("✅ Data generated successfully!")
print(f"Users: {len(users_df)}")
print(f"Usage events: {len(usage_df)}")
print(f"Subscriptions: {len(subs_df)}")
print(f"Support tickets: {len(tickets_df)}")