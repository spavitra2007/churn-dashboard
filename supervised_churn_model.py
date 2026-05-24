import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report, accuracy_score
import joblib
import os

excel_file_path = "customer_full_backup.xlsx"

def main():
    print("Loading data for Supervised Model (Churn Prediction)...")
    if not os.path.exists(excel_file_path):
        print("Error: File not found.")
        return
        
    df = pd.read_excel(excel_file_path, engine='openpyxl')
    
    # Target variable
    target = 'churn'
    if target not in df.columns:
        print(f"Error: Target column '{target}' not found in data.")
        return

    print(f"Target variable '{target}' distribution:")
    print(df[target].value_counts(normalize=True))

    # Drop target and any obviously leaky columns
    X = df.drop(columns=[target, 'customer_id'], errors='ignore')
    y = df[target]

    # Convert y to numeric if it's string (e.g. 'Yes'/'No')
    if y.dtype == 'object' or y.dtype.name == 'category':
        y = y.map(lambda x: 1 if str(x).strip().lower() in ['yes', '1', 'true'] else 0)

    # Separate Numeric and Categorical Features
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    
    # Explicit cast for categoricals
    if categorical_features:
        X[categorical_features] = X[categorical_features].astype(str)

    # Preprocessing
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

    print("Splitting data into Training and Testing sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Create the complete pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1))
    ])

    print("Training Supervised Random Forest Classifier...")
    model_pipeline.fit(X_train, y_train)

    print("\nEvaluating Model on Test Data...")
    y_pred = model_pipeline.predict(X_test)
    y_prob = model_pipeline.predict_proba(X_test)[:, 1]

    auc_score = roc_auc_score(y_test, y_prob)
    acc_score = accuracy_score(y_test, y_pred)

    print(f"\n====================================")
    print(f"[PASS] MODEL PERFORMANCE METRICS")
    print(f"====================================")
    print(f"AUC Score: {auc_score:.4f} (This tells you how well it separates churners from non-churners!)")
    print(f"Accuracy:  {acc_score:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model_pipeline, 'supervised_churn_model.pkl')
    print("Model saved to 'supervised_churn_model.pkl'")

if __name__ == "__main__":
    main()
