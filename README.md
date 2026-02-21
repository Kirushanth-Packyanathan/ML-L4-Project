### Set Up Virtual Environment

```bash
cd backend
python -m venv venv
```

### Install Dependencies

```bash
.\venv\Scripts\pip install fastapi uvicorn xgboost numpy pandas pydantic python-multipart streamlit requests
```

> **Linux/Mac:** Use `./venv/bin/pip` instead.

### Run the Backend (FastAPI)

```bash
.\venv\Scripts\python -m uvicorn main:app --port 8000
```

The API will be available at: `http://localhost:8000`

### Run the Frontend (Streamlit)

Open a **new terminal** and run:

```bash
.\backend\venv\Scripts\streamlit run streamlit_app.py --server.port 8501
```

```bash
docker build -t house-price-app .
docker run -p 8000:8000 -p 8501:8501 house-price-app
```

The app will be available at: `http://localhost:8501`

---