import pandas as pd
import os

print("Creating Master Clustered CSV...")

# Load the original data to preserve everything
base_df = pd.read_excel("customer_full_backup.xlsx", engine='openpyxl')
print(f"Loaded original data: {base_df.shape}")

# Define the models and their respective segment column names
model_files = [
    ("customer_segmented_data.csv", "customer_segment"),
    ("customer_segmented_data_model_2.csv", "model_2_segment"),
    ("customer_segmented_data_model_3.csv", "model_3_segment"),
    ("customer_segmented_data_model_4.csv", "model_4_life_stage_segment"),
    ("customer_segmented_data_model_5.csv", "model_5_segment"),
    ("customer_segmented_data_model_6_final.csv", "model_6_final_segment")
]

# For model 3, we also derived 4 new scores, let's grab them too
derived_scores_model_3 = [
    "digital_maturity_score", 
    "multi_channel_engagement_score", 
    "bank_engagement_depth_score", 
    "digital_friction_score"
]

# Extract the cluster columns and add them to the base dataframe
for file_name, col_name in model_files:
    if os.path.exists(file_name):
        temp_df = pd.read_csv(file_name)
        base_df[col_name] = temp_df[col_name]
        
        # If it's model 3, also bring over the derived scores
        if file_name == "customer_segmented_data_model_3.csv":
            for score in derived_scores_model_3:
                if score in temp_df.columns:
                    base_df[score] = temp_df[score]
                    
        print(f" -> Added {col_name} from {file_name}")
    else:
        print(f" Warning: {file_name} not found.")

output_file = "master_customer_segmented_data.xlsx"
base_df.to_excel(output_file, index=False)
print(f"\nMaster clustered data saved as an Excel file to: {output_file}")
print(f"Final shape: {base_df.shape}")
