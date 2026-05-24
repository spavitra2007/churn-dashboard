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

# Define the features list for Model 4 (Life Stage Profile)
features = [
    "age", "age_group", "marital_status", "dependent_count", "tenure_months",
    "tenure_bin", "relationship_type", "customer_segment", "annual_income",
    "income_band", "income_category", "occupation_type", "education_level",
    "number_of_products", "loyalty_program_member"
]

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

    # Filter only the columns that exist in the dataframe
    available_features = [feat for feat in features if feat in df.columns]
    missing_features = [feat for feat in features if feat not in df.columns]
    
    if missing_features:
        print("\nWarning: The following requested features were not found in the Excel file:")
        for feat in missing_features:
            print(f" - {feat}")
    
    if not available_features:
        print("Error: None of the requested features were found in the dataset.")
        return

    print(f"\nProceeding with {len(available_features)} available features for Model 4.")
    
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
    
    # Preprocessing pipelines for both numeric and categorical data
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        # handle_unknown='ignore' ensures robustness if new categories appear later
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
    print(f"Data processed shape after One-Hot Encoding: {X_processed.shape}")

    # Build the K-Means clustering model
    n_clusters = 5 
    print(f"\nTraining K-Means clustering model (k={n_clusters}) for Model 4 (Life Stage Profile)...")
    
    model = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    model.fit(X_processed)
    
    # Add cluster labels to the original dataframe
    df['model_4_life_stage_segment'] = model.labels_
    
    print("\nModel trained successfully!")
    
    # Display cluster sizes
    print("\nModel 4 Segments Distribution:")
    print(df['model_4_life_stage_segment'].value_counts().sort_index())
    
    # Save the model and the preprocessor (which contains imputer, scaler, and one-hot encoder)
    print("\nSaving model 4 artifacts...")
    joblib.dump(model, 'customer_segmentation_model_4.pkl')
    joblib.dump(preprocessor, 'preprocessor_model_4.pkl')
    
    # Save the clustered data
    output_file = "customer_segmented_data_model_4.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSaved segmented data for Model 4 to {output_file}")
    
    print("\nDone. The intelligent Model 4 (Life Stage Profile) is ready.")

if __name__ == "__main__":
    main()
