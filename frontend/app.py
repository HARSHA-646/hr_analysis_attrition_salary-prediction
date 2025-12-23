import streamlit as st
import json
import time
from utils import call_backend

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    layout="wide"
)

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
    <p>Machine Learning Based Salary & Attrition Prediction</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT MODE
# -------------------------------------------------
st.sidebar.header("Input Mode")
input_mode = st.sidebar.radio(
    "Choose input method",
    ["Manual Input", "Upload JSON"]
)

payload = None

# -------------------------------------------------
# MANUAL INPUT
# -------------------------------------------------
if input_mode == "Manual Input":
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

    payload = {
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
    }

# -------------------------------------------------
# JSON INPUT
# -------------------------------------------------
else:
    uploaded = st.sidebar.file_uploader("Upload Employee JSON", type=["json"])
    if uploaded:
        payload = json.load(uploaded)
        st.sidebar.success("JSON loaded successfully")

# -------------------------------------------------
# PREDICTION
# -------------------------------------------------
st.markdown("---")

if st.button("🔍 Predict"):
    if payload is None:
        st.warning("Please provide input data")
    else:
        with st.spinner("Running ML models..."):
            time.sleep(0.7)
            result = call_backend(payload)

        salary = result["predicted_salary"]
        attrition = result["attrition"]
        loss = result["estimated_loss"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            if attrition == "Yes":
                st.markdown("<div class='badge-yes'>ATTRITION : YES</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='badge-no'>ATTRITION : NO</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.metric("💰 Predicted Monthly Salary", f"₹ {salary:,.0f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            if attrition == "Yes":
                st.markdown(
                    f"<div class='loss-box'>Estimated Business Loss<br>₹ {loss:,.0f}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='safe-box'>Employee is likely to stay<br>No immediate loss</div>",
                    unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        st.caption(
            "ℹ️ Predictions are generated purely by trained machine learning models "
            "based on historical employee data. No manual rules applied."
        )
