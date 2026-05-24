import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import joblib
import os

# Define the file path
excel_file_path = "customer_full_backup.xlsx"

# Competitive pressure feature sets
competitive_pressure_features = {
    "competitive_pressure_signal": [
        "competitor_bank_offer_awareness",
        "campaign_received_count",
        "campaign_response_count",
        "cross_sell_offer_count",
        "upsell_offer_count",
        "last_campaign_response_days",
        "discount_or_fee_waiver_received",
        "referral_count",
        "loyalty_program_member"
    ],
    "market_churn_pressure_index": [
        "competitor_bank_offer_awareness",
        "campaign_response_count",
        "last_campaign_response_days",
        "satisfaction_score",
        "nps_score",
        "customer_feedback_sentiment"
    ],
    "retention_offer_sensitivity": [
        "discount_or_fee_waiver_received",
        "campaign_received_count",
        "campaign_response_count",
        "cross_sell_offer_count",
        "upsell_offer_count"
    ],
    "external_pull_risk_score": [
        "competitor_bank_offer_awareness",
        "last_campaign_response_days",
        "digital_transaction_ratio",
        "credit_utilization_ratio",
        "satisfaction_score"
    ]
}

def main():
    if not os.path.exists(excel_file_path):
        print(f"Error: Could not find the Excel file at {excel_file_path}")
        return

    print("Loading data from Excel...")
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
        print(f"Data loaded successfully. Total shape: {df.shape}\n")
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return

    # Check columns in dataframe
    all_requested_features = set()
    for feature_name, cols in competitive_pressure_features.items():
        print(f"\nChecking: {feature_name}")
        
        missing = [c for c in cols if c not in df.columns]
        all_requested_features.update(cols)
        
        if len(missing) == 0:
            print("[PASS] All keywords present")
        else:
            print("[FAIL] Missing columns:")
            for c in missing:
                print(" -", c)
                
    all_requested_features = list(all_requested_features)
    
    print("\n-------------------------------------------")

    available_features = [feat for feat in all_requested_features if feat in df.columns]
    
    if not available_features:
        print("Error: None of the requested features were found in the dataset.")
        return

    print(f"\nProceeding with {len(available_features)} available features for Model 6 (Final).")
    
    # Extract the feature subset
    X = df[available_features]

    # Identify numeric and categorical columns
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category', 'bool', 'datetime64']).columns.tolist()
    
    print(f"Numeric features ({len(numeric_features)}): {numeric_features}")
    print(f"Categorical features ({len(categorical_features)}): {categorical_features}")

    # Explicitly cast categorical columns to string
    if categorical_features:
        X = X.copy()
        X[categorical_features] = X[categorical_features].astype(str)

    print("\nPreprocessing data...")
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    X_processed = preprocessor.fit_transform(X)
    print(f"Data processed shape: {X_processed.shape}")

    # Build the K-Means clustering model
    n_clusters = 5 
    print(f"\nTraining K-Means clustering model (k={n_clusters}) for Model 6...")
    
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    model.fit(X_processed)
    
    df['model_6_final_segment'] = model.labels_
    
    print("\nModel 6 trained successfully!")
    print("\nModel 6 Segments Distribution:")
    print(df['model_6_final_segment'].value_counts().sort_index())
    
    print("\nSaving model 6 artifacts...")
    joblib.dump(model, 'customer_segmentation_model_6.pkl')
    joblib.dump(preprocessor, 'preprocessor_model_6.pkl')
    
    output_file = "customer_segmented_data_model_6_final.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved segmented data for Model 6 to {output_file}")
    
    print("\nDone. The final intelligent Model 6 is ready.")

if __name__ == "__main__":
    main()
