Write-Host "Starting ReachInbox Full-Stack Email Job Scheduler..." -ForegroundColor Cyan

# 1. Start Redis
Start-Process -FilePath "$PSScriptRoot\redis-bin\redis-server.exe" -ArgumentList "--port", "6379" -WindowStyle Hidden

# 2. Start Postgres
Start-Process -FilePath "C:\Program Files\PostgreSQL\18\bin\postgres.exe" -ArgumentList "-D", "$PSScriptRoot\postgres-data", "-p", "5433" -WindowStyle Hidden

Start-Sleep -Seconds 2

# 3. Start Backend & Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd server; npm run dev"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd client; npm run dev"

Write-Host "Services successfully running!" -ForegroundColor Green
Write-Host "Backend API:  http://localhost:5000" -ForegroundColor Yellow
Write-Host "Bull-Board:   http://localhost:5000/admin/queues" -ForegroundColor Yellow
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor Yellow
