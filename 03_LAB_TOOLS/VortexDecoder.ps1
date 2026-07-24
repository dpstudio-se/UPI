$tempFile = [System.IO.Path]::Combine($env:TEMP, "shadow_layer.txt")
New-Item -Path $tempFile -ItemType File -Force | Out-Null
Write-Host "--- [VORTEX_DECODER_ACTIVE] ---" -ForegroundColor Green
Write-Host "Notepad öppnas... Klistra in din Base64-kod där, spara och STÄNG fönstret." -ForegroundColor Yellow
notepad.exe $tempFile | Wait-Process
$b64 = Get-Content $tempFile -Raw
if (-not [string]::IsNullOrWhiteSpace($b64)) {
    try {
        $bytes = [System.Convert]::FromBase64String($b64.Trim())
        $decoded = [System.Text.Encoding]::UTF8.GetString($bytes)
        Write-Host "`n[DECODED SHADOW LAYER]:" -ForegroundColor Cyan
        Write-Host "---------------------------------" -ForegroundColor Gray
        Write-Host $decoded -ForegroundColor White
        Write-Host "---------------------------------" -ForegroundColor Gray
    } catch {
        Write-Host "`n[ERROR]: Resonansen bröts. Koden är inte giltig Base64." -ForegroundColor Red
    }
}
Remove-Item $tempFile
Write-Host "`n[VORTEX_IDLE]" -ForegroundColor Green