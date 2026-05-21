# Ragi Disease Detection System

AI-powered finger millet disease diagnosis with a FastAPI inference backend and a modern Next.js frontend.

## Folder Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── model/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── .env
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── .env.local.example
│   └── package.json
├── my_model/
├── class_indices.json
├── docker-compose.yml
├── Dockerfile
└── main.py
```

## Backend Setup

```powershell
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

If `uvicorn` is not on PATH, use:

```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Prediction endpoint:

```text
POST /predict
Content-Type: multipart/form-data
file=<image>
```

## Frontend Setup

```powershell
cd frontend
Copy-Item .env.local.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`.

## Environment Variables

Backend:

```text
RAGI_MODEL_DIR=../my_model
RAGI_CLASS_INDICES_PATH=../class_indices.json
RAGI_CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

Frontend:

```text
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Docker Compose

```powershell
docker compose up --build
```

Windows helper scripts:

```powershell
.\start_dev.bat
```

Services:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://localhost:3000`

## Notes

- The old Streamlit UI was removed.
- The root `main.py` remains as a compatibility shim for `uvicorn main:app`.
- The backend validates model assets during startup and exposes `GET /health`.
