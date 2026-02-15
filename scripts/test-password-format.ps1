# Test password format and provide correct encoding

param(
    [Parameter(Mandatory=$true)]
    [string]$Password
)

Write-Host "Testing password format..." -ForegroundColor Cyan
Write-Host ""

# Check for special characters
$specialChars = @('#', '@', '%', '&', '*', '(', ')', '[', ']', '{', '}', '|', '\', '/', '?', ':', ';', '=', '+', ' ', '$', '`', '!')
$foundSpecial = @()

foreach ($char in $specialChars) {
    if ($Password -like "*$char*") {
        $foundSpecial += $char
    }
}

if ($foundSpecial.Count -gt 0) {
    Write-Host "⚠️  Special characters found: $($foundSpecial -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Special characters in passwords:" -ForegroundColor Cyan
    Write-Host "  • May need URL encoding in connection strings" -ForegroundColor White
    Write-Host "  • May need quoting in .env files" -ForegroundColor White
    Write-Host "  • # character is used for comments in .env files" -ForegroundColor Yellow
    Write-Host ""
    
    # Check specifically for #
    if ($Password -like "*#*") {
        Write-Host "⚠️  WARNING: '#' character found!" -ForegroundColor Red
        Write-Host "   The '#' character is used for comments in .env files" -ForegroundColor Yellow
        Write-Host "   It needs to be handled carefully." -ForegroundColor Yellow
        Write-Host ""
    }
} else {
    Write-Host "✅ No special characters found - password should work fine" -ForegroundColor Green
    Write-Host ""
}

# Show correct formats
Write-Host "Correct formats for your password:" -ForegroundColor Cyan
Write-Host ""

# For .env file
Write-Host "1. In .env file (recommended - use quotes):" -ForegroundColor Yellow
$envFormat = "SUPABASE_DB_PASSWORD=`"$Password`""
Write-Host "   $envFormat" -ForegroundColor White
Write-Host ""

# For connection string (URL encoded)
Write-Host "2. In connection string (URL encoded):" -ForegroundColor Yellow
$urlEncoded = [System.Web.HttpUtility]::UrlEncode($Password)
$connString = "postgresql://postgres:$urlEncoded@db.pzsdvpemnroxylbhjirr.supabase.co:5432/postgres"
Write-Host "   $connString" -ForegroundColor White
Write-Host ""

# Show what # becomes
if ($Password -like "*#*") {
    Write-Host "Note: '#' becomes '%23' in URL encoding" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "✅ Recommended: Use quotes in .env file to be safe" -ForegroundColor Green
