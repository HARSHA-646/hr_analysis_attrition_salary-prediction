import requests

API_URL = "http://127.0.0.1:8000/predict"

def call_backend(payload: dict):
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
