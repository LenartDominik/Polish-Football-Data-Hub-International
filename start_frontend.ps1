# Start Frontend Script
Write-Host "🎨 Uruchamianie Frontend Streamlit..." -ForegroundColor Green
Write-Host ""

$projectPath = "e:\Python - Ready4 AI\polish-players-tracker"
$pythonExe = "$projectPath\.venv\Scripts\python.exe"

# Zmień katalog
Set-Location $projectPath

# Sprawdź czy Python istnieje
if (-Not (Test-Path $pythonExe)) {
    Write-Host "❌ Błąd: Nie znaleziono Pythona w .venv" -ForegroundColor Red
    Write-Host "Uruchom najpierw: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Sprawdź czy baza istnieje
if (-Not (Test-Path "$projectPath\players.db")) {
    Write-Host "⚠️  Ostrzeżenie: Baza danych 'players.db' nie istnieje lub jest pusta" -ForegroundColor Yellow
    Write-Host "   Uruchom backend i zsynchronizuj dane:" -ForegroundColor Yellow
    Write-Host "   curl http://127.0.0.1:8000/players/sync/scraper" -ForegroundColor Cyan
    Write-Host ""
}

# Uruchom frontend
Write-Host "🌐 Frontend będzie dostępny na: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Naciśnij Ctrl+C aby zatrzymać serwer" -ForegroundColor Yellow
Write-Host ""

$streamlitExe = "$projectPath\.venv\Scripts\streamlit.exe"

if (Test-Path $streamlitExe) {
    & $streamlitExe run app\frontend\streamlit_app.py
} else {
    Write-Host "⚠️  streamlit.exe nie znaleziony, próbuję przez Python..." -ForegroundColor Yellow
    & $pythonExe -m streamlit run app\frontend\streamlit_app.py
}
