import pandas as pd
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

excel_file_path = "customer_full_backup.xlsx"

def main():
    print("Loading data for Recommendation Engine (Next Best Product)...")
    if not os.path.exists(excel_file_path):
        print("Error: File not found.")
        return
        
    df = pd.read_excel(excel_file_path, engine='openpyxl')
    
    # Isolate product flags to see what products customers own
    product_cols = [
        "savings_account_flag", "current_account_flag", "credit_card_flag",
        "personal_loan_flag", "home_loan_flag", "auto_loan_flag",
        "fixed_deposit_flag", "investment_product_flag", "insurance_product_flag",
        "demat_account_flag"
    ]
    
    # Verify columns exist
    available_products = [p for p in product_cols if p in df.columns]
    if not available_products:
        print("No product flag columns found to build recommendations.")
        return
        
    print(f"Found {len(available_products)} products in portfolio.")
    
    # Customer-Product Matrix
    user_item_matrix = df[available_products].fillna(0)
    
    # Calculate Product-to-Product Similarity Matrix (Item-Based Collaborative Filtering)
    # This answers: "Customers who have Product A also tend to have Product B"
    print("\nCalculating Product Similarity Matrix...")
    item_similarity = cosine_similarity(user_item_matrix.T)
    item_sim_df = pd.DataFrame(item_similarity, index=available_products, columns=available_products)
    
    print("\nTop 3 Highly Correlated Products:")
    # Get top correlations excluding self (1.0)
    corr_stack = item_sim_df.unstack().reset_index()
    corr_stack.columns = ['Product A', 'Product B', 'Similarity']
    corr_stack = corr_stack[corr_stack['Product A'] != corr_stack['Product B']]
    top_corrs = corr_stack.sort_values(by='Similarity', ascending=False).drop_duplicates(subset=['Similarity']).head(3)
    for _, row in top_corrs.iterrows():
        print(f" -> {row['Product A']} & {row['Product B']} (Score: {row['Similarity']:.2f})")

    # Generate "Next Best Product" recommendation for every customer
    print("\nGenerating 'Next Best Product' recommendations for all customers...")
    
    # Dot product of user_item_matrix and item_similarity gives us a propensity score 
    # for every product for every user based on what they already own
    propensity_scores = user_item_matrix.dot(item_sim_df)
    
    # Set score to 0 for products the customer ALREADY owns (we don't want to recommend what they have)
    propensity_scores = propensity_scores.where(user_item_matrix == 0, -1)
    
    # Find the column name with the highest propensity score for each row
    df['recommended_next_product'] = propensity_scores.idxmax(axis=1)
    
    # Save results
    output_file = "customer_product_recommendations.csv"
    
    cols_to_save = ['customer_id'] if 'customer_id' in df.columns else []
    cols_to_save += available_products + ['recommended_next_product']
    
    df[cols_to_save].to_csv(output_file, index=False)
    
    print(f"\n====================================")
    print(f"[PASS] RECOMMENDATION ENGINE COMPLETE")
    print(f"====================================")
    print(f"Recommendations saved to: {output_file}")
    
    print("\nMost Recommended Products (Overall):")
    print(df['recommended_next_product'].value_counts().head(5))

if __name__ == "__main__":
    main()
