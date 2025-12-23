import joblib
from pathlib import Path
import sys

# 🔑 Import the custom transformer
from backend.custom_transformers import SelectiveTransformer

# 🔑 CRITICAL: register it under __main__ for pickle
sys.modules["__main__"].SelectiveTransformer = SelectiveTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "saved_models"

SALARY_MODEL_PATH = MODELS_DIR / "monthly_income_final_pipeline.joblib"
ATTRITION_MODEL_PATH = MODELS_DIR / "attrition_full_pipeline.joblib"

salary_model = joblib.load(SALARY_MODEL_PATH)
attrition_model = joblib.load(ATTRITION_MODEL_PATH)
