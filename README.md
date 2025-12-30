🏢 HR Attrition & Salary Analytics (Machine Learning Project)
📌 Project Overview

This project is an end-to-end HR Analytics system built using Machine Learning to help organizations make data-driven decisions.
It predicts:

💰 Employee Salary (Regression)

🚪 Employee Attrition Risk (Classification)

📉 Estimated Business Loss if an employee is likely to leave

The application is deployed as an interactive Streamlit dashboard and uses real-world HR data.

🎯 Problem Statement

Organizations face challenges in:

Predicting fair employee salaries

Identifying employees at risk of attrition

Estimating the financial impact of employee turnover

Attrition data is often imbalanced (most employees do not leave), making prediction harder.
This project addresses these challenges using robust ML pipelines.

🧠 Solution Approach

We built three interconnected ML components:

Salary Prediction Model (Regression)

Predicts monthly income using employee experience, role, education, and performance data.

Attrition Prediction Model (Classification)

Predicts whether an employee is likely to leave (Yes / No).

Handles imbalanced data using proper evaluation and class weighting.

Business Loss Estimation

If attrition = Yes, estimates financial loss based on:

Predicted salary

Tenure

Performance

Training investment

All models are trained as scikit-learn pipelines and saved using joblib.

📂 Dataset Used

IBM HR Analytics Employee Attrition Dataset

Source: Kaggle

Link: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

Why this dataset?

Real-world HR data

Strong feature coverage

Naturally imbalanced attrition target

Widely accepted in industry and academia

⚙️ Tech Stack

Python 3.10

scikit-learn 1.7.2

joblib 1.5.1

NumPy 2.2.6

<img width="931" height="413" alt="image" src="https://github.com/user-attachments/assets/2ffea980-dede-41d2-aa4a-e8dde3416a4c" />

🚀 How to Run Locally
1️⃣ Create & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Streamlit App
streamlit run app.py


App will open at:

http://localhost:8501

☁️ Deployment (Streamlit Cloud)

Push project to GitHub

Go to 👉 https://streamlit.io/cloud

Click New App

Select:

Repository

Branch: main

File path: app.py

Deploy 🎉
link : https://hranalysisattritionsalary-prediction-awmkvleb7rult2pn7vntsp.streamlit.app/





Pandas

Streamlit (UI + Deployment)
