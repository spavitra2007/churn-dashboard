# ChurnData Pro - Intelligent Banking Dashboard

This repository contains an end-to-end intelligent banking analytics system. It integrates predictive churn modeling with 6 behavioral AI clustering models to provide a real-time Streamlit dashboard with actionable, cross-indexed retention strategies, product recommendations, and deep financial diagnostics.

## Features

- **Analysis Dashboard:** Overview of total customers, outstanding revenue, churn rate, and demographic insights.
- **Recommendation System:** Deep dive into individual customer profiles with demographic and financial data, along with top product recommendations.
- **Feature Engineering Models:** Interactive metrics showcasing the results of 6 distinct AI models, including risk signals and life stage profiling.
- **Retention System:** A proactive, 6-pillar AI-powered retention playbook tailored for high-risk customer profiles.

## Data Files Used

The dashboard and models rely on the following datasets to generate insights. **For a full breakdown of the columns and data structures, see the [Predictions Data Dictionary](PREDICTIONS_DOCUMENTATION.md).**

### Main Application Datasets
- `customer_predictions.csv`: Contains the output of the supervised churn prediction model, including Churn Probability and Risk Segments.
- `customer_product_recommendations.csv`: Used for the Recommendation System to map customers to their next best product.
- `customer_retention_strategies.csv`: Contains the AI-generated strategies for the 6-pillar retention playbook (Psychology, Family, Employee Accountability, Rewards, Support, Trust).
- `Ultimate_Customer_Intelligence.xlsx`: Contains the consolidated insights and scores from all 6 behavioral feature engineering models.

### Intermediate & Model Outputs
- `customer_segmented_data.csv` (and `model_2` through `model_6_final`): Output data from the individual clustering and segmentation models.
- `master_customer_segmented_data.csv`: A unified dataset combining all intermediate segmented data for final model consumption.

## Running the Dashboard

1. Ensure you have the required dependencies installed (see `requirements.txt`).
2. Run the application using Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Open the provided localhost URL in your browser to interact with the dashboard.
