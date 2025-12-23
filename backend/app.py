from fastapi import FastAPI
import pandas as pd

from backend.schemas import EmployeeInput
from backend.model_loader import salary_model, attrition_model
from backend.loss_logic import calculate_loss

app = FastAPI(title="HR Analytics API")


@app.post("/predict")
def predict(payload: EmployeeInput):

    # Convert input to DataFrame
    df = pd.DataFrame([payload.dict()])

    # Salary prediction
    salary_pred = float(salary_model.predict(df)[0])

    # 🔑 REQUIRED: inject MonthlyIncome for attrition model
    df["MonthlyIncome"] = salary_pred

    # Attrition prediction
    attrition_pred = int(attrition_model.predict(df)[0])

    # Loss calculation
    loss = 0
    if attrition_pred == 1:
        loss = calculate_loss(
            salary=salary_pred,
            years_at_company=payload.YearsAtCompany,
            performance_rating=payload.PerformanceRating,
            training_times_last_year=payload.TrainingTimesLastYear
        )

    return {
        "predicted_salary": round(salary_pred, 2),
        "attrition": "Yes" if attrition_pred == 1 else "No",
        "estimated_loss": loss
    }
