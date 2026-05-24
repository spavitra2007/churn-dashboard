import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans
import joblib
import os

# Define the file path
excel_file_path = "customer_full_backup.xlsx"

# Define the features lists based on the user's requirements
tbs_features = [
    "monthly_transaction_count", "monthly_transaction_value", "total_trans_amt",
    "total_trans_count", "upi_transaction_count", "debit_card_transaction_count",
    "net_banking_transaction_count", "cash_withdrawal_count", "avg_monthly_balance",
    "current_balance", "balance_decline_percentage", "digital_txn_ratio"
]

es_features = [
    "mobile_app_login_count", "website_login_count", "last_login_days",
    "account_inactive_days", "email_open_rate", "call_center_interaction_count",
    "relationship_manager_interaction_count", "branch_visit_count", "service_request_count",
    "digital_engagement_index"
]

eaps_features = [
    "competitor_bank_offer_awareness", "customer_feedback_sentiment", "satisfaction_score",
    "nps_score", "total_complaints", "unresolved_complaint_count", "escalation_count",
    "complaint_resolution_time", "late_credit_card_payment_count", "emi_payment_delay_count"
]

# Combine all features for the model
all_features = tbs_features + es_features + eaps_features

def main():
    if not os.path.exists(excel_file_path):
        print(f"Error: Could not find the Excel file at {excel_file_path}")
        return

    print("Loading data from Excel...")
    try:
        # Load the excel file
        # Using engine='openpyxl' is recommended for .xlsx files
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        print(f"Data loaded successfully. Total shape: {df.shape}")
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return

    # Filter only the columns that exist in the dataframe to avoid KeyError
    available_features = [feat for feat in all_features if feat in df.columns]
    missing_features = [feat for feat in all_features if feat not in df.columns]
    
    if missing_features:
        print("\nWarning: The following requested features were not found in the Excel file:")
        for feat in missing_features:
            print(f" - {feat}")
    
    if not available_features:
        print("Error: None of the requested features were found in the dataset.")
        return

    print(f"\nProceeding with {len(available_features)} available features.")
    
    # Extract the feature subset
    X = df[available_features]

    print("\nPreprocessing data...")
    # 1. Impute missing values (using median for robustness to outliers)
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)

    # 2. Scale features (standardization)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Since no target variable was specified, we will build an unsupervised clustering model 
    # to segment the customers based on these behavioral metrics. K-Means is a good start.
    n_clusters = 5 # Arbitrary number of clusters for segmentation
    print(f"\nTraining K-Means clustering model (k={n_clusters}) for customer segmentation...")
    
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    model.fit(X_scaled)
    
    # Add cluster labels to the original dataframe
    df['customer_segment'] = model.labels_
    
    print("\nModel trained successfully!")
    
    # Display cluster sizes
    print("\nCustomer Segments Distribution:")
    print(df['customer_segment'].value_counts().sort_index())
    
    # Save the model and preprocessors for future use
    print("\nSaving model artifacts...")
    joblib.dump(model, 'customer_segmentation_model_1.pkl')
    joblib.dump(imputer, 'imputer.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    
    # Optionally, save the clustered data back to a new Excel/CSV
    output_file = "customer_segmented_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved segmented data to {output_file}")
    
    print("\nDone. The intelligent model 1 is ready.")

if __name__ == "__main__":
    main()
