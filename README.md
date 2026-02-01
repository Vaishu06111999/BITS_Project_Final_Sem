GenAI-Powered Conversational Assistant for Marketing Mix Modeling (MMM)
====================================================================

Project Overview
----------------
This project implements a GenAI-powered conversational assistant that allows non-technical users
to query and understand Marketing Mix Modeling (MMM) insights using natural language.

The system combines statistical marketing analytics with generative AI to convert complex MMM
outputs into simple, business-friendly explanations. Users can ask questions about channel
performance, top channels, and budget what-if scenarios without requiring analytical expertise.


Key Features
------------
- Marketing Mix Modeling using:
  * Linear Regression
  * Ridge Regression
  * Bayesian Regression (final selected model)
- Computation of marketing metrics:
  * Revenue Contribution
  * Contribution Share
  * ROI
  * Effectiveness
  * Elasticity
- Rule-based intent detection and entity extraction
- Budget what-if simulations using elasticity
- Generative AI-based explanation of analytical insights
- Streamlit-based web interface


Dataset
-------
Source: Kaggle  
Dataset Name: Sample Campaign PPC Dataset

The dataset contains historical Pay-Per-Click (PPC) campaign data including spend, impressions,
clicks, conversions, and channel identifiers. Data is aggregated at the channel level before
applying Marketing Mix Modeling.


Project Structure
-----------------
MMM_Code.ipynb              - EDA and MMM modeling
Chatbot_Analysis.py         - Conversational logic and MMM insight functions
MMM_UI_Streamlit_app.py     - Streamlit user interface
chatbot_dataset.csv         - Processed dataset for chatbot analysis
channel_summary.csv         - Channel-level aggregated metrics
README.txt                  - Project documentation


Methodology Summary
-------------------
1. Data extraction and exploratory data analysis
2. Linear Regression as baseline MMM
3. Ridge Regression for regularization
4. Bayesian Regression as final model
5. Computation of business metrics
6. Natural language query processing
7. Budget what-if simulation
8. Generative AI-based explanation
9. Streamlit-based user interface deployment


Technologies Used
-----------------
- Python
- Pandas, NumPy
- Scikit-learn
- Bayesian regression techniques
- Matplotlib, Seaborn
- Google Gemini API (Gemini 2.5 Flash)
- Streamlit
- Kaggle dataset


How to Run the Project
---------------------
1. Install required libraries:
   pip install pandas numpy scikit-learn streamlit google-genai matplotlib seaborn

2. Run the Streamlit application:
   streamlit run MMM_UI_Streamlit_app.py


Example Queries
---------------
- Give me an overall marketing summary
- Which are the top 3 marketing channels?
- How is Google performing?
- What happens if I increase Google budget by 10%?


Limitations
-----------
- MMM results are precomputed
- Budget simulations assume proportional elasticity
- Rule-based NLP limits flexibility
- Free-tier Gemini API has rate limits


Future Enhancements
-------------------
- Automated budget optimization
- Multi-turn conversational context
- Real-time data ingestion
- Advanced dashboards
- Cloud deployment


Author
------
Vaishali Ravichandran
Postgraduate Project – Marketing Analytics / Data Engineering
