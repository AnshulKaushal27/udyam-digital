@echo off
echo Starting ReachInbox Scheduler local services...

start "Redis Server" /B "redis-bin\redis-server.exe" --port 6379
start "PostgreSQL" /B "C:\Program Files\PostgreSQL\18\bin\postgres.exe" -D "postgres-data" -p 5433

timeout /t 2 /nobreak >nul

start "Backend Server" cmd /k "cd server && npm run dev"
start "Frontend Client" cmd /k "cd client && npm run dev"

echo All services launched!
echo Backend: http://localhost:5000
echo Bull-Board: http://localhost:5000/admin/queues
echo Frontend: http://localhost:5173
