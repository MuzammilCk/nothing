Write-Host "🧠 Starting MindWell Setup..." -ForegroundColor Cyan

# 1. Check Python
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Error "Python is not installed or not in PATH."
    exit
}
Write-Host "✅ Found $pythonVersion" -ForegroundColor Green

# 2. Setup venv
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# 3. Activate and Install
Write-Host "Installing dependencies..." -ForegroundColor Yellow
if (Test-Path ".\venv\Scripts\activate.ps1") {
    . .\venv\Scripts\activate.ps1
} else {
    # Fallback for some systems
    cmd /c "venv\Scripts\activate.bat && exit"
}

pip install -r backend/requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies."
    exit
}

# 4. Check Config
if (-not (Test-Path "backend/config.py")) {
    Write-Warning "Config file missing!"
} else {
    Write-Host "✅ Config found. Please ensure backend/config.py has your API keys!" -ForegroundColor Magenta
}

# 5. Start Backend
Write-Host "🚀 Starting MindWell Backend on http://localhost:8000" -ForegroundColor Cyan
# Start in new process to keep this window open or run in parallel
Start-Process -FilePath "python" -ArgumentList "-m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000" -NoNewWindow

# 6. Open Frontend
Write-Host "🌍 Opening Frontend..." -ForegroundColor Cyan
Start-Process "frontend\index.html"

Write-Host "
Code is running! 
1. If the audio analysis fails, check the backend console for API Key errors.
2. Press Ctrl+C in the backend terminal to stop.
" -ForegroundColor Green
