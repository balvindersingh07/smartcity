$ErrorActionPreference = "Stop"

Write-Output "Running Smart City smoke test..."

$base = $env:SMART_CITY_API_BASE
if (-not $base) {
  $base = "http://localhost:8004"
}

$endpoints = @(
  "$base/health",
  "$base/metrics",
  "$base/sensors",
  "$base/alerts"
)

foreach ($url in $endpoints) {
  $response = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 15
  if ($null -eq $response) {
    throw "Smoke test failed: empty response from $url"
  }
  Write-Output "PASS $url"
}

Write-Output "Smoke test completed successfully."
