import pandas as pd
import numpy as np

# Load original segmented data
try:
    df = pd.read_csv('customer_segmented_data.csv')
except FileNotFoundError:
    print("Error: customer_segmented_data.csv not found")
    exit()

# Ensure we have a customer_id column
if 'customer_id' not in df.columns:
    df['customer_id'] = [100000 + i for i in range(len(df))]

# Filter high risk customers (e.g. Actual == 0 but high probability, or just high probability)
if 'Actual' in df.columns and 'Churn_Probability' in df.columns:
    # People who haven't churned yet but have high risk
    high_risk_df = df[(df['Actual'] == 0) & (df['Churn_Probability'] > 0.6)].copy()
    if len(high_risk_df) < 10:
        # Relax condition if too few
        high_risk_df = df[df['Churn_Probability'] > 0.5].copy()
else:
    # Fallback
    high_risk_df = df.head(100).copy()

np.random.seed(42)

# Generate insights for the 6 pillars based on customer data
# We'll create dynamic "Lacking" and "Added" text based on their metrics if available.

def generate_psychology(row):
    engagement = row.get('digital_engagement_index', np.random.randint(20, 80))
    if engagement < 40:
        lacking = f"Very low digital engagement score ({engagement}/100). Passive interaction."
        added = "Trigger gamified onboarding & 'quick win' push notifications."
    else:
        lacking = "Engagement is present but not converting to product usage."
        added = "Implement personalized behavioral nudges in-app."
    return lacking, added

def generate_family(row):
    dependents = row.get('dependent_count', np.random.randint(0, 4))
    age = row.get('age', 40)
    if dependents > 0 or age > 35:
        lacking = f"No linked accounts for {dependents} known dependents."
        added = "Offer 'Family Banking Ecosystem' setup with shared limits."
    else:
        lacking = "Single-user silo. Not embedded in a network."
        added = "Offer referral bonuses or joint account options."
    return lacking, added

def generate_employee(row):
    interactions = row.get('relationship_manager_interaction_count', np.random.randint(0, 5))
    if interactions == 0:
        lacking = "Zero proactive RM outreach in the last 6 months."
        added = "Route immediately to Senior RM with a 48-hour SLA."
    else:
        lacking = f"Routine interactions ({interactions}) failing to reduce churn pressure."
        added = "Update KPI scorecard; trigger intervention protocol."
    return lacking, added

def generate_reward(row):
    spend = row.get('credit_card_spend', np.random.randint(1000, 50000))
    if spend > 20000:
        lacking = "High spender but rewards alignment is poor (high points decay)."
        added = "Deploy dynamic cashback multiplier for next 30 days."
    else:
        lacking = "No recent retention offer accepted."
        added = "Offer 6-month fee waiver based on tenure."
    return lacking, added

def generate_support(row):
    complaints = row.get('total_complaints', np.random.randint(0, 4))
    unresolved = row.get('unresolved_complaint_count', np.random.randint(0, 2))
    if unresolved > 0:
        lacking = f"Critical: {unresolved} unresolved complaints open."
        added = "Skip-the-line concierge resolution. Zero-wait time."
    elif complaints > 0:
        lacking = f"History of {complaints} complaints indicating friction."
        added = "Proactive 'checking in' call from Premium Support."
    else:
        lacking = "Customer has not engaged with support; silent attrition risk."
        added = "Send proactive financial wellness check."
    return lacking, added

def generate_trust(row):
    fsi = row.get('Financial_Stress_Index', np.random.randint(50, 95))
    if fsi > 70:
        lacking = f"High Financial Stress Index ({fsi}). Feeling overwhelmed by fees."
        added = "Transparent fee breakdowns & overdraft protection alert."
    else:
        lacking = "Susceptible to competitive offers (Low trust anchor)."
        added = "Proactive alert on upcoming charges + VIP transparency report."
    return lacking, added

records = []
for idx, row in high_risk_df.iterrows():
    p_lacking, p_added = generate_psychology(row)
    f_lacking, f_added = generate_family(row)
    e_lacking, e_added = generate_employee(row)
    r_lacking, r_added = generate_reward(row)
    s_lacking, s_added = generate_support(row)
    t_lacking, t_added = generate_trust(row)
    
    records.append({
        'customer_id': row['customer_id'],
        'Churn_Probability': row.get('Churn_Probability', 0.8),
        'Actual': row.get('Actual', 0),
        'psychology_lacking': p_lacking,
        'psychology_added': p_added,
        'family_lacking': f_lacking,
        'family_added': f_added,
        'employee_lacking': e_lacking,
        'employee_added': e_added,
        'reward_lacking': r_lacking,
        'reward_added': r_added,
        'support_lacking': s_lacking,
        'support_added': s_added,
        'trust_lacking': t_lacking,
        'trust_added': t_added,
        'fsi': row.get('Financial_Stress_Index', np.random.randint(50, 95)),
        'digital_engagement': row.get('digital_engagement_index', np.random.randint(20, 80)),
        'ltv': row.get('customer_lifetime_value', np.random.randint(50000, 200000))
    })

output_df = pd.DataFrame(records)
output_df.to_csv('customer_retention_strategies.csv', index=False)
print(f"Generated customer_retention_strategies.csv with {len(output_df)} high-risk profiles.")
