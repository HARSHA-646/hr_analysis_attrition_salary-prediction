# =================================================
# REQUIRED: Custom Transformer (for joblib loading)
# =================================================
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class SelectiveTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, transformer=None, columns=None, all_columns=None):
        self.transformer = transformer
        self.columns = columns
        self.all_columns = all_columns

    def _to_dataframe(self, X):
        if isinstance(X, pd.DataFrame):
            return X.copy()
        if self.all_columns is not None:
            return pd.DataFrame(X, columns=self.all_columns)
        return pd.DataFrame(X)

    def fit(self, X, y=None):
        X_df = self._to_dataframe(X)
        if self.columns:
            self.transformer.fit(X_df[self.columns])
        return self

    def transform(self, X):
        X_df = self._to_dataframe(X)
        if self.columns:
            X_df[self.columns] = self.transformer.transform(X_df[self.columns])
        return X_df

# =================================================
# STREAMLIT APP
# =================================================
import streamlit as st
import joblib
import time

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

# -------------------------------------------------
# LOAD MODELS (CACHED)
# -------------------------------------------------
@st.cache_resource
def load_models():
    salary_model = joblib.load("saved_models/monthly_income_final_pipeline.joblib")
    attrition_model = joblib.load("saved_models/attrition_full_pipeline.joblib")
    return salary_model, attrition_model

salary_model, attrition_model = load_models()

# -------------------------------------------------
# LOSS CALCULATION LOGIC
# -------------------------------------------------
def calculate_loss(salary, years_at_company, performance_rating, training_times):
    replacement_cost = salary * 6
    training_cost = training_times * 10000
    productivity_loss = salary * (5 - performance_rating)
    loyalty_offset = years_at_company * 2000
    return int(replacement_cost + training_cost + productivity_loss - loyalty_offset)

# -------------------------------------------------
# STYLES
# -------------------------------------------------
st.markdown("""
<style>
.main { background-color: #f4f7fb; }

.header {
    padding: 32px;
    border-radius: 18px;
    background: linear-gradient(90deg,#0047ab,#00b4d8);
    color: white;
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 26px;
    border-radius: 18px;
    box-shadow: 0 10px 26px rgba(0,0,0,0.08);
    margin-bottom: 20px;
    text-align: center;
}

.badge-yes {
    background: linear-gradient(90deg,#ff4d4f,#ff7875);
    color: white;
    padding: 16px;
    border-radius: 16px;
    font-size: 22px;
    font-weight: bold;
}

.badge-no {
    background: linear-gradient(90deg,#2ecc71,#52c41a);
    color: white;
    padding: 16px;
    border-radius: 16px;
    font-size: 22px;
    font-weight: bold;
}

.loss-box {
    background-color: #fff1f0;
    border-left: 6px solid #ff4d4f;
    padding: 20px;
    border-radius: 14px;
    font-size: 22px;
    font-weight: bold;
}

.safe-box {
    background-color: #f0fff4;
    border-left: 6px solid #52c41a;
    padding: 20px;
    border-radius: 14px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="header">
    <h1>🏢 HR Attrition & Salary Analytics</h1>
    <p>End-to-End Machine Learning Deployment using Streamlit</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR INPUTS
# -------------------------------------------------
st.sidebar.header("Employee Details")

Age = st.sidebar.slider("Age", 18, 60, 36)
Gender = st.sidebar.selectbox("Gender", ["Male","Female"])
MaritalStatus = st.sidebar.selectbox("Marital Status", ["Single","Married","Divorced"])

JobLevel = st.sidebar.selectbox("Job Level", [1,2,3,4,5], index=1)
JobRole = st.sidebar.text_input("Job Role", "Sales Executive")
Department = st.sidebar.selectbox(
    "Department",
    ["Sales","Research & Development","Human Resources"]
)
BusinessTravel = st.sidebar.selectbox(
    "Business Travel",
    ["Travel_Rarely","Travel_Frequently","Non-Travel"]
)
OverTime = st.sidebar.selectbox("OverTime", ["Yes","No"])

Education = st.sidebar.selectbox("Education Level", [1,2,3,4,5], index=2)
EducationField = st.sidebar.selectbox(
    "Education Field",
    ["Life Sciences","Medical","Marketing","Technical Degree","Other"]
)

TotalWorkingYears = st.sidebar.slider("Total Working Years", 0,40,10)
YearsAtCompany = st.sidebar.slider("Years At Company", 0,40,5)
YearsInCurrentRole = st.sidebar.slider("Years In Current Role", 0,18,3)
YearsSinceLastPromotion = st.sidebar.slider("Years Since Last Promotion", 0,15,1)
YearsWithCurrManager = st.sidebar.slider("Years With Current Manager", 0,17,3)
NumCompaniesWorked = st.sidebar.slider("Companies Worked", 0,9,2)

DailyRate = st.sidebar.slider("Daily Rate", 103,1499,800)
DistanceFromHome = st.sidebar.slider("Distance From Home", 1,29,7)
StockOptionLevel = st.sidebar.selectbox("Stock Option Level", [0,1,2,3], index=1)

JobSatisfaction = st.sidebar.selectbox("Job Satisfaction", [1,2,3,4], index=2)
EnvironmentSatisfaction = st.sidebar.selectbox("Environment Satisfaction", [1,2,3,4], index=2)
RelationshipSatisfaction = st.sidebar.selectbox("Relationship Satisfaction", [1,2,3,4], index=2)
JobInvolvement = st.sidebar.selectbox("Job Involvement", [1,2,3,4], index=2)
WorkLifeBalance = st.sidebar.selectbox("Work Life Balance", [1,2,3,4], index=2)
PerformanceRating = st.sidebar.selectbox("Performance Rating", [1,2,3,4], index=2)
TrainingTimesLastYear = st.sidebar.slider("Trainings Last Year", 0,6,3)

# -------------------------------------------------
# INPUT DATAFRAME
# -------------------------------------------------
input_df = pd.DataFrame([{
    "Age": Age,
    "BusinessTravel": BusinessTravel,
    "DailyRate": DailyRate,
    "Department": Department,
    "DistanceFromHome": DistanceFromHome,
    "Education": Education,
    "EducationField": EducationField,
    "Gender": Gender,
    "JobLevel": JobLevel,
    "JobRole": JobRole,
    "JobSatisfaction": JobSatisfaction,
    "MaritalStatus": MaritalStatus,
    "NumCompaniesWorked": NumCompaniesWorked,
    "OverTime": OverTime,
    "PerformanceRating": PerformanceRating,
    "RelationshipSatisfaction": RelationshipSatisfaction,
    "StockOptionLevel": StockOptionLevel,
    "TotalWorkingYears": TotalWorkingYears,
    "TrainingTimesLastYear": TrainingTimesLastYear,
    "WorkLifeBalance": WorkLifeBalance,
    "YearsAtCompany": YearsAtCompany,
    "YearsInCurrentRole": YearsInCurrentRole,
    "YearsSinceLastPromotion": YearsSinceLastPromotion,
    "YearsWithCurrManager": YearsWithCurrManager,
    "EnvironmentSatisfaction": EnvironmentSatisfaction,
    "JobInvolvement": JobInvolvement
}])

# -------------------------------------------------
# PREDICT
# -------------------------------------------------
st.markdown("---")

if st.button("🔍 Predict"):
    with st.spinner("Running ML models..."):
        time.sleep(0.6)

        salary = float(salary_model.predict(input_df)[0])
        input_df["MonthlyIncome"] = salary
        attrition = int(attrition_model.predict(input_df)[0])

        loss = 0
        if attrition == 1:
            loss = calculate_loss(
                salary,
                YearsAtCompany,
                PerformanceRating,
                TrainingTimesLastYear
            )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if attrition == 1:
            st.markdown("<div class='badge-yes'>ATTRITION : YES</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='badge-no'>ATTRITION : NO</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("💰 Predicted Monthly Salary", f"₹ {salary:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if attrition == 1:
            st.markdown(
                f"<div class='loss-box'>Estimated Business Loss<br>₹ {loss:,.0f}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='safe-box'>Employee likely to stay<br>No immediate loss</div>",
                unsafe_allow_html=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "ℹ️ Predictions are generated using pre-trained machine learning pipelines. "
        "Models are loaded once and reused for inference."
    )
