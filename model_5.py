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

# ─────────────────────────────────────────
# CEI — Channel Engagement Index
# ─────────────────────────────────────────
CEI_COLS = [
    "branch_visit_count",
    "relationship_manager_interaction_count",
    "email_open_rate",
]

# ─────────────────────────────────────────
# CSI — Complaint & Service Index
# ─────────────────────────────────────────
CSI_COLS = [
    "unresolved_complaint_count",
    "total_complaints",
    "complaint_resolution_time",
    "escalation_count",
    "service_request_count",
    "call_center_interaction_count",
]

# ─────────────────────────────────────────
# CLI — Customer Loyalty Index
# ─────────────────────────────────────────
CLI_COLS = [
    "loyalty_program_member",
    "referral_count",
    "tenure_months",
    "number_of_products",
    "campaign_response_count",
]

# ─────────────────────────────────────────
# NPI — NPS & Sentiment Index
# ─────────────────────────────────────────
NPI_COLS = [
    "nps_score",
    "satisfaction_score",
    "customer_feedback_sentiment",
    "app_rating_given",
]

all_requested_features = CEI_COLS + CSI_COLS + CLI_COLS + NPI_COLS

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

    # ─────────────────────────────────────────
    # VERIFY Features
    # ─────────────────────────────────────────
    print("Verifying feature existence in dataset:")
    for name, cols in [("CEI", CEI_COLS), ("CSI", CSI_COLS),
                       ("CLI", CLI_COLS), ("NPI", NPI_COLS)]:
        missing = [c for c in cols if c not in df.columns]
        present = [c for c in cols if c in df.columns]
        status  = "[PASS]" if not missing else "[FAIL]"
        print(f"{status} {name} -> Present: {len(present)}/{len(cols)}", end="")
        if missing:
            print(f"  Missing: {missing}")
        else:
            print()
    
    print("\n-------------------------------------------")

    available_features = [feat for feat in all_requested_features if feat in df.columns]
    
    if not available_features:
        print("Error: None of the requested features were found in the dataset.")
        return

    print(f"\nProceeding with {len(available_features)} available features for Model 5.")
    
    # Extract the feature subset
    X = df[available_features]

    # Identify numeric and categorical columns
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category', 'bool', 'datetime64']).columns.tolist()
    
    print(f"Numeric features ({len(numeric_features)}): {numeric_features}")
    print(f"Categorical features ({len(categorical_features)}): {categorical_features}")

    # Explicitly cast categorical columns to string to avoid OneHotEncoder type errors
    if categorical_features:
        X = X.copy()
        X[categorical_features] = X[categorical_features].astype(str)

    print("\nPreprocessing data (Handling both numeric and categorical features)...")
    
    # Preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Fit and transform the data
    X_processed = preprocessor.fit_transform(X)
    print(f"Data processed shape: {X_processed.shape}")

    # Build the K-Means clustering model
    n_clusters = 5 
    print(f"\nTraining K-Means clustering model (k={n_clusters}) for Model 5...")
    
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    model.fit(X_processed)
    
    # Add cluster labels
    df['model_5_segment'] = model.labels_
    
    print("\nModel 5 trained successfully!")
    
    # Display cluster sizes
    print("\nModel 5 Segments Distribution:")
    print(df['model_5_segment'].value_counts().sort_index())
    
    # Save artifacts
    print("\nSaving model 5 artifacts...")
    joblib.dump(model, 'customer_segmentation_model_5.pkl')
    joblib.dump(preprocessor, 'preprocessor_model_5.pkl')
    
    # Save the clustered data
    output_file = "customer_segmented_data_model_5.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved segmented data for Model 5 to {output_file}")
    
    print("\nDone. The intelligent Model 5 is ready.")

if __name__ == "__main__":
    main()
