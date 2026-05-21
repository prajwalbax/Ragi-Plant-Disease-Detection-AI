@echo off
start "Ragi API" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
start "Ragi Frontend" cmd /k "cd /d %~dp0frontend && if not exist .env.local copy .env.local.example .env.local && npm.cmd run dev"
