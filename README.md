"# hr_analysis_attrition_salary-prediction" 
HR Attrition & Salary Analytics System

An end-to-end Machine Learning application to predict employee salary, attrition risk, and potential business loss using real-world HR data.
The project includes a FastAPI backend, Streamlit frontend, and production-ready ML pipelines saved with joblib.

🚀 Features
Salary Prediction (Regression Model)
Attrition Prediction (Classification Model)
Estimated Business Loss if Attrition = Yes
Manual Input & JSON Input support
Interactive and attractive Streamlit UI
FastAPI backend for scalable inference
Single-source-of-truth ML pipelines
No fake explanations or hardcoded logic
🛠️ Tech Stack

Python 3.10
scikit-learn 1.7.2
joblib 1.5.1
FastAPI
Uvicorn
Streamlit
Pandas, NumPy

⚙️ Environment Setup (First Time)
1️⃣ Clone the Repository
git clone <your-repo-url>
cd hr-analysis

2️⃣ Create Virtual Environment
python -m venv .venv

3️⃣ Activate Virtual Environment
Windows
.\.venv\Scripts\activate

Mac / Linux
source .venv/bin/activate

📦 Install Dependencies
pip install -r requirements.txt

▶️ Run Backend (FastAPI)

From project root:

uvicorn backend.app:app --reload
Backend will run at:
http://127.0.0.1:8000
