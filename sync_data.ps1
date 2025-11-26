# Synchronizacja danych ze scrapera
Write-Host "🕷️  Synchronizacja danych ze scrapera 90minut.pl..." -ForegroundColor Green
Write-Host ""

# Sprawdź czy backend działa
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend działa" -ForegroundColor Green
}
catch {
    Write-Host "❌ Backend nie działa!" -ForegroundColor Red
    Write-Host "   Uruchom backend: .\start_backend.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "⏳ Pobieranie danych... (może potrwać 30-60 sekund)" -ForegroundColor Yellow
Write-Host ""

try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/players/sync/scraper" -UseBasicParsing -TimeoutSec 120
    $data = $response.Content | ConvertFrom-Json
    
    Write-Host "✅ Synchronizacja zakończona!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📊 Wyniki:" -ForegroundColor Cyan
    Write-Host "   📥 Dodano nowych graczy: $($data.inserted)" -ForegroundColor White
    Write-Host "   🔄 Zaktualizowano graczy: $($data.updated)" -ForegroundColor White
    Write-Host "   📊 Całkowita liczba scrapowanych: $($data.total_scraped)" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Dane gotowe! Możesz teraz uruchomić frontend." -ForegroundColor Green
    Write-Host "   Uruchom: .\start_frontend.ps1" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Błąd podczas synchronizacji: $($_.Exception.Message)" -ForegroundColor Red
}
