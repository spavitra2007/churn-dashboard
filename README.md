# ChurnData Pro - Intelligent Banking Dashboard

🟢 **Live Application:** [View the Deployed Dashboard Here](https://spavitra2007-churn-dashboard-app-uiq9cg.streamlit.app/)

This repository contains an end-to-end intelligent banking analytics system. It integrates predictive churn modeling with 6 behavioral AI clustering models to provide a real-time Streamlit dashboard with actionable, cross-indexed retention strategies, product recommendations, and deep financial diagnostics.

## 🧠 The 6 Behavioral AI Models (Feature Engineering)

To understand customer behavior deeply, we engineered 6 distinct AI clustering models. Each model analyzes a different facet of the customer profile and generates its own predictive insights:

1. **Model 1 (Early Warning Signal):** Analyzes engagement across key touchpoints to detect drops in activity.
2. **Model 2 (Financial Stress Index):** Evaluates revenue, value, and debt to determine financial distress.
3. **Model 3 (Digital Maturity Score):** Assesses satisfaction and digital product adoption.
4. **Model 4 (Life Stage Profile):** Segments customers based on usage patterns and demographic life stages.
5. **Model 5 (Trust & Experience Gap):** Measures interactions with support and issue resolution.
6. **Model 6 (Competitive Pressure Signal):** Triangulates overall risk based on external competitive indicators.

*These 6 models output their individual predictions into files like `customer_segmented_data.csv` and `customer_segmented_data_model_2.csv` through `customer_segmented_data_model_6_final.csv`.*

## 🎯 Final Predictions & Core Dashboard CSVs

The final dashboard relies on the following generated datasets (For a full breakdown of the columns, see the [Predictions Data Dictionary](PREDICTIONS_DOCUMENTATION.md)):

- **Supervised Churn Predictions (`customer_predictions.csv`):** The final prediction model. Contains the core machine learning output, providing the `Churn_Probability` (exact AI confidence score) and `Risk_Segment` for every customer.
- **The Dashboard Intelligence Database (`Ultimate_Customer_Intelligence.csv`):** The master CSV dataset that powers the dashboard visualizations. It consolidates the insights and scores from all 6 behavioral feature engineering models into one optimized dataset.
- **Recommendation Engine (`customer_product_recommendations.csv`):** Maps customers to their predicted "Next Best Product" to increase retention and Lifetime Value (LTV).
- **Retention Playbook (`customer_retention_strategies.csv`):** Contains the AI-generated strategies for the 6-pillar retention playbook (Psychology, Family, Employee Accountability, Rewards, Support, Trust).

## 🚀 Running the Dashboard Locally

If you fork or clone this repository, it is completely ready to run on your local machine:

1. Ensure you have the required dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application using Streamlit:
   ```bash
   streamlit run app.py
   ```
3. Open the provided localhost URL (usually `http://localhost:8501`) in your browser to interact with the dashboard.

## 🌐 How to Deploy to the Web

Because this repository contains no hardcoded local paths and tracks all necessary CSV databases, you can easily deploy it to the web for free using Streamlit Community Cloud:

1. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
2. Click **New App**.
3. Select your repository (`your-username/churn-dashboard`).
4. Set the **Main file path** to `app.py`.
5. Click **Deploy**.

Within minutes, your dashboard will be live on a public URL!
