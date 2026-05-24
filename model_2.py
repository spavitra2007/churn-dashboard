import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import joblib
import os

# Define the file path
excel_file_path = "customer_full_backup.xlsx"

# Define the features lists based on the user's requirements for Model 2
fsi_features = [
    "debt_to_income_ratio", "credit_utilization_ratio", "emi_payment_delay_count",
    "late_credit_card_payment_count", "loan_outstanding_amount", "emi_amount",
    "avg_monthly_balance", "minimum_due_paid_flag"
]

cri_features = [
    "credit_utilization_3m_avg", "credit_utilization_6m_avg", "total_revolving_bal",
    "credit_card_limit", "loan_default_risk_score"
]

tpi_features = [
    "monthly_transaction_value", "monthly_transaction_count", "cash_withdrawal_count",
    "total_trans_amt", "total_trans_count", "balance_decline_percentage",
    "avg_quarterly_balance", "upi_transaction_count", "debit_card_transaction_count",
    "net_banking_transaction_count"
]

eri_features = [
    "last_login_days", "account_inactive_days", "mobile_app_login_count",
    "website_login_count", "satisfaction_score", "nps_score",
    "unresolved_complaint_count", "escalation_count", "complaint_resolution_time",
    "total_complaints"
]

# Combine all features for model 2
all_features = fsi_features + cri_features + tpi_features + eri_features

def main():
    if not os.path.exists(excel_file_path):
        print(f"Error: Could not find the Excel file at {excel_file_path}")
        return

    print("Loading data from Excel...")
    try:
        # Load the excel file
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        print(f"Data loaded successfully. Total shape: {df.shape}")
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return

    # Filter only the columns that exist in the dataframe
    available_features = [feat for feat in all_features if feat in df.columns]
    missing_features = [feat for feat in all_features if feat not in df.columns]
    
    if missing_features:
        print("\nWarning: The following requested features were not found in the Excel file:")
        for feat in missing_features:
            print(f" - {feat}")
    
    if not available_features:
        print("Error: None of the requested features were found in the dataset.")
        return

    print(f"\nProceeding with {len(available_features)} available features for Model 2.")
    
    # Extract the feature subset
    X = df[available_features]

    print("\nPreprocessing data...")
    # 1. Impute missing values (using median)
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    # 2. Scale features (standardization)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # We will build another K-Means clustering model for Model 2
    n_clusters = 5 
    print(f"\nTraining K-Means clustering model (k={n_clusters}) for Model 2...")
    
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    model.fit(X_scaled)
    
    # Add cluster labels to the original dataframe
    df['model_2_segment'] = model.labels_
    
    print("\nModel trained successfully!")
    
    # Display cluster sizes
    print("\nModel 2 Segments Distribution:")
    print(df['model_2_segment'].value_counts().sort_index())
    
    # Save the model and preprocessors
    print("\nSaving model 2 artifacts...")
    joblib.dump(model, 'customer_segmentation_model_2.pkl')
    joblib.dump(imputer, 'imputer_model_2.pkl')
    joblib.dump(scaler, 'scaler_model_2.pkl')
    
    # Save the clustered data back to a new CSV
    output_file = "customer_segmented_data_model_2.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved segmented data for Model 2 to {output_file}")
    
    print("\nDone. The intelligent Model 2 is ready.")

if __name__ == "__main__":
    main()
