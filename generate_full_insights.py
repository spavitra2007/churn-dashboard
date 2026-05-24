import pandas as pd
import joblib
import os
import numpy as np

def main():
    print("Loading data and models...")
    # Load original full dataset
    df_full = pd.read_excel("customer_full_backup.xlsx", engine='openpyxl')
    
    # Load supervised model pipeline
    try:
        churn_model = joblib.load('supervised_churn_model.pkl')
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("Generating Churn Predictions for ALL 8,101 customers...")
    # Drop target and customer_id if present as the model expects
    X_full = df_full.drop(columns=['churn', 'customer_id'], errors='ignore')
    
    # Ensure categoricals are strings
    categorical_features = X_full.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    if categorical_features:
        X_full[categorical_features] = X_full[categorical_features].astype(str)

    # Predict probabilities
    churn_probs = churn_model.predict_proba(X_full)[:, 1]
    df_full['Churn_Probability'] = churn_probs
    df_full['Predicted_Churn'] = churn_model.predict(X_full)
    
    # Feature Engineering: Risk Segments
    conditions = [
        (df_full['Churn_Probability'] >= 0.7),
        (df_full['Churn_Probability'] >= 0.3) & (df_full['Churn_Probability'] < 0.7),
        (df_full['Churn_Probability'] < 0.3)
    ]
    choices = ['High Risk', 'Medium Risk', 'Low Risk']
    df_full['Risk_Segment'] = np.select(conditions, choices, default='Unknown')

    print("Loading 6 AI Clustering Models data...")
    if os.path.exists('master_customer_segmented_data.xlsx'):
        df_master = pd.read_excel('master_customer_segmented_data.xlsx', engine='openpyxl')
        # Extract just the cluster columns
        cluster_cols = [c for c in df_master.columns if 'segment' in c or 'score' in c]
        for col in cluster_cols:
            if col not in df_full.columns:
                df_full[col] = df_master[col]
    
    print("Loading Recommendation Engine data...")
    if os.path.exists('customer_product_recommendations.csv'):
        df_reco = pd.read_csv('customer_product_recommendations.csv')
        if 'recommended_next_product' in df_reco.columns:
            df_full['recommended_next_product'] = df_reco['recommended_next_product']

    # Save the ultimate dataset
    output_file = "Ultimate_Customer_Intelligence.xlsx"
    df_full.to_excel(output_file, index=False)
    print(f"\nSaved Ultimate Intelligence file to {output_file}")

    print("\n================================================")
    print("📊 1. PREDICTION INSIGHTS (FULL DATASET)")
    print("================================================")
    print(df_full['Risk_Segment'].value_counts())
    
    print("\n================================================")
    print("🧩 2. CROSS-ANALYSIS: CHURN RISK x AI SEGMENTS")
    print("================================================")
    if 'model_6_final_segment' in df_full.columns:
        print("Average Churn Probability by Model 6 (Competitive Pressure) Segment:")
        print(df_full.groupby('model_6_final_segment')['Churn_Probability'].mean().sort_values(ascending=False))
        
    print("\n================================================")
    print("💡 3. RECOMMENDATIONS FOR HIGH RISK CUSTOMERS")
    print("================================================")
    if 'recommended_next_product' in df_full.columns:
        high_risk_recos = df_full[df_full['Risk_Segment'] == 'High Risk']['recommended_next_product'].value_counts().head(3)
        print("Top 3 products to retain 'High Risk' customers:")
        print(high_risk_recos)

if __name__ == "__main__":
    main()
