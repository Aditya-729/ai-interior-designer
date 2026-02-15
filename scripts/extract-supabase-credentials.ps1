# Extract Supabase credentials from connection string

param(
    [Parameter(Mandatory=$true)]
    [string]$ConnectionString
)

Write-Host "Extracting credentials from connection string..." -ForegroundColor Cyan
Write-Host ""

# Parse connection string
# Format: postgresql://user:password@host:port/database

if ($ConnectionString -match "postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)") {
    $user = $matches[1]
    $password = $matches[2]
    $host = $matches[3]
    $port = $matches[4]
    $database = $matches[5]
    
    Write-Host "Extracted Credentials:" -ForegroundColor Green
    Write-Host ""
    Write-Host "SUPABASE_DB_HOST=$host" -ForegroundColor Yellow
    Write-Host "SUPABASE_DB_PORT=$port" -ForegroundColor Yellow
    Write-Host "SUPABASE_DB_NAME=$database" -ForegroundColor Yellow
    Write-Host "SUPABASE_DB_USER=$user" -ForegroundColor Yellow
    Write-Host "SUPABASE_DB_PASSWORD=$password" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Add these to your .env file:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "# Supabase Database" -ForegroundColor Gray
    Write-Host "SUPABASE_DB_HOST=$host" -ForegroundColor White
    Write-Host "SUPABASE_DB_PORT=$port" -ForegroundColor White
    Write-Host "SUPABASE_DB_NAME=$database" -ForegroundColor White
    Write-Host "SUPABASE_DB_USER=$user" -ForegroundColor White
    Write-Host "SUPABASE_DB_PASSWORD=$password" -ForegroundColor White
    Write-Host ""
    
    # Optionally append to .env file
    $append = Read-Host "Append to .env file? (y/n)"
    if ($append -eq "y" -or $append -eq "Y") {
        $envContent = @"
# Supabase Database
SUPABASE_DB_HOST=$host
SUPABASE_DB_PORT=$port
SUPABASE_DB_NAME=$database
SUPABASE_DB_USER=$user
SUPABASE_DB_PASSWORD=$password
"@
        Add-Content -Path ".env" -Value $envContent
        Write-Host "Credentials added to .env file!" -ForegroundColor Green
    }
} else {
    Write-Host "Error: Invalid connection string format" -ForegroundColor Red
    Write-Host "Expected format: postgresql://user:password@host:port/database" -ForegroundColor Yellow
    exit 1
}
