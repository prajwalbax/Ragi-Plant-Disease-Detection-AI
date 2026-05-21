@echo off
cd /d "%~dp0"
if not exist ".env.local" copy ".env.local.example" ".env.local"
npm.cmd run dev
