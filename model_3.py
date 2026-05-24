import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import joblib
import os
import numpy as np

# Define the file path
excel_file_path = "customer_full_backup.xlsx"

# Define the features lists based on the user's requirements for Model 3
FSI_COLS = [
    "debt_to_income_ratio", "credit_utilization_ratio", "emi_payment_delay_count",
    "late_credit_card_payment_count", "minimum_due_paid_flag"
]

CRI_COLS = [
    "credit_utilization_3m_avg", "credit_utilization_6m_avg", "total_revolving_bal",
    "credit_card_limit", "loan_default_risk_score"
]

TPI_COLS = [
    "monthly_transaction_value", "monthly_transaction_count", "cash_withdrawal_count",
    "total_trans_amt", "total_trans_count", "balance_decline_percentage",
    "avg_quarterly_balance", "upi_transaction_count", "debit_card_transaction_count",
    "net_banking_transaction_count"
]

DMI_COLS = [
    "digital_transaction_ratio", "mobile_banking_active_flag", "paperless_statement_enabled",
    "total_digital_logins", "mobile_app_login_count", "website_login_count"
]

CEI_COLS = [
    "branch_visit_count", "call_center_interaction_count", "relationship_manager_interaction_count",
    "email_open_rate", "service_request_count"
]

PBI_COLS = [
    "number_of_products", "savings_account_flag", "current_account_flag", "credit_card_flag",
    "personal_loan_flag", "home_loan_flag", "auto_loan_flag", "fixed_deposit_flag",
    "investment_product_flag", "insurance_product_flag", "demat_account_flag", "loyalty_program_member"
]

FRI_COLS = [
    "failed_login_count", "last_login_days", "account_inactive_days", "total_complaints",
    "unresolved_complaint_count", "escalation_count"
]

# Combine all raw features
raw_features = FSI_COLS + CRI_COLS + TPI_COLS + DMI_COLS + CEI_COLS + PBI_COLS + FRI_COLS

def derive_scores(df):
    """
    Derives the calculated scores requested by the user.
    Since exact business logic wasn't provided, we use reasonable mathematical aggregations
    (like sum or mean of normalized variables where appropriate) to create these scores.
    """
    df_derived = df.copy()
    
    # Simple derivation using z-scores of existing columns so they scale correctly
    def safe_zscore_sum(cols):
        valid_cols = [c for c in cols if c in df_derived.columns]
        if not valid_cols:
            return np.zeros(len(df_derived))
        # Impute missing values with median before computing zscore
        temp = df_derived[valid_cols].fillna(df_derived[valid_cols].median())
        # Z-score standardization
        z_scores = (temp - temp.mean()) / temp.std(ddof=0).replace(0, 1)
        return z_scores.sum(axis=1)

    # 1. digital_maturity_score
    df_derived["digital_maturity_score"] = safe_zscore_sum(DMI_COLS)
    
    # 2. multi_channel_engagement_score
    df_derived["multi_channel_engagement_score"] = safe_zscore_sum(CEI_COLS)
    
    # 3. bank_engagement_depth_score
    # We'll use the Product Based Index (PBI_COLS) to represent depth of relationship
    df_derived["bank_engagement_depth_score"] = safe_zscore_sum(PBI_COLS)
    
    # 4. digital_friction_score
    df_derived["digital_friction_score"] = safe_zscore_sum(FRI_COLS)
    
    return df_derived

def main():
    if not os.path.exists(excel_file_path):
        print(f"Error: Could not find the Excel file at {excel_file_path}")
        return

    print("Loading data from Excel...")
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        print(f"Data loaded successfully. Total shape: {df.shape}")
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return

    # Check for missing raw features
    available_features = [feat for feat in raw_features if feat in df.columns]
    missing_features = [feat for feat in raw_features if feat not in df.columns]
    
    if missing_features:
        print("\nWarning: The following requested features were not found in the Excel file:")
        for feat in missing_features:
            print(f" - {feat}")
            
    # Derive the requested features
    print("\nDeriving calculated scores (digital_maturity_score, etc.)...")
    df = derive_scores(df)

    # Add the newly derived columns to the list of features to train on
    derived_cols = [
        "digital_maturity_score", "multi_channel_engagement_score", 
        "bank_engagement_depth_score", "digital_friction_score"
    ]
    
    # Final feature set for modeling
    model_features = available_features + derived_cols
    
    print(f"\nProceeding with {len(model_features)} total features (including {len(derived_cols)} derived scores) for Model 3.")
    
    # Extract the feature subset
    X = df[model_features]

    print("\nPreprocessing data...")
    # Impute missing values
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Train Model 3
    n_clusters = 5 
    print(f"\nTraining K-Means clustering model (k={n_clusters}) for Model 3...")
    
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    model.fit(X_scaled)
    
    # Add cluster labels
    df['model_3_segment'] = model.labels_
    
    print("\nModel trained successfully!")
    
    # Display cluster sizes
    print("\nModel 3 Segments Distribution:")
    print(df['model_3_segment'].value_counts().sort_index())
    
    # Save artifacts
    print("\nSaving model 3 artifacts...")
    joblib.dump(model, 'customer_segmentation_model_3.pkl')
    joblib.dump(imputer, 'imputer_model_3.pkl')
    joblib.dump(scaler, 'scaler_model_3.pkl')
    
    # Save the clustered data
    output_file = "customer_segmented_data_model_3.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved segmented data for Model 3 to {output_file}")
    
    print("\nDone. The intelligent Model 3 is ready.")

if __name__ == "__main__":
    main()
