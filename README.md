# 🛒 Retail Stockout Predictor (End-to-End Data Pipeline)

An end-to-end Data Science and Data Engineering project designed to predict inventory stockouts in a retail environment (pharmacy context). This project demonstrates the complete data lifecycle: from raw SQL data generation to deploying a Machine Learning model via a RESTful API, topped with an interactive web dashboard.

## 🚀 Tech Stack
* **Language:** Python
* **Data Engineering & ETL:** SQLite, Pandas, Numpy
* **Machine Learning:** Scikit-Learn (Random Forest Classifier)
* **Backend API:** FastAPI, Uvicorn
* **Frontend Dashboard:** Streamlit, Requests

## 🏗️ Project Architecture

The project is structured into a functional data pipeline using a microservices architecture:
1. **Data Generation (`data/gerar_banco.py`):** Simulates a transactional relational database (SQLite) generating random sales data for various products.
2. **Data Preparation & ETL (`data/preparar_dados.py`):** Extracts data using SQL `JOINs`, cleans it, and performs feature engineering (e.g., date parsing, weekend flags) using Pandas. Outputs a clean `.csv` for model training.
3. **The Brain - Model & API (`app/main.py`):** A FastAPI application that automatically trains a Random Forest model on startup and exposes endpoints for real-time predictions.
4. **The Face - Web Dashboard (`app/frontend.py`):** An interactive Streamlit application that communicates with the FastAPI backend, allowing users to input parameters and visualize the AI's risk assessment in real-time.

## 📸 Screenshots

![FastAPI Swagger UI] <img width="948" height="878" alt="image" src="https://github.com/user-attachments/assets/d25b6589-b225-4416-a0d1-cbf0b4f4643b" />

> *Backend API testing with Swagger UI returning JSON predictions.*

![Streamlit Dashboard] <img width="920" height="907" alt="image" src="https://github.com/user-attachments/assets/5d4c0dce-4cc6-436a-92c6-131e23f28edb" />

> *Interactive frontend built with Streamlit.*

## 💻 How to Run This Project Locally

**1. Clone the repository and install dependencies:**
pip install -r requirements.txt
2. Run the Data Pipeline (ETL):
python data/gerar_banco.py
python data/preparar_dados.py
3. Start the Backend API (Terminal 1):
python -m uvicorn app.main:app --reload
(The API will be available at http://127.0.0.1:8000/docs)
4. Start the Frontend Dashboard (Terminal 2):
python -m streamlit run app/frontend.py
(The Dashboard will automatically open in your browser at http://localhost:8501)
```bash
