# Test Supabase database connection

Write-Host "🧪 Testing Supabase Connection..." -ForegroundColor Cyan
Write-Host ""

# Load .env file
if (-not (Test-Path .env)) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    exit 1
}

# Parse .env file
$envVars = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        # Remove quotes if present
        if ($value -like '"*"') {
            $value = $value.Trim('"')
        }
        $envVars[$key] = $value
    }
}

$host = $envVars['SUPABASE_DB_HOST']
$port = $envVars['SUPABASE_DB_PORT']
$database = $envVars['SUPABASE_DB_NAME']
$user = $envVars['SUPABASE_DB_USER']
$password = $envVars['SUPABASE_DB_PASSWORD']

if (-not $host -or -not $password) {
    Write-Host "❌ Missing Supabase credentials in .env" -ForegroundColor Red
    exit 1
}

Write-Host "Connection Details:" -ForegroundColor Yellow
Write-Host "  Host: $host" -ForegroundColor White
Write-Host "  Port: $port" -ForegroundColor White
Write-Host "  Database: $database" -ForegroundColor White
Write-Host "  User: $user" -ForegroundColor White
Write-Host "  Password: [HIDDEN]" -ForegroundColor White
Write-Host ""

# Check if psql is available
$psqlPath = Get-Command psql -ErrorAction SilentlyContinue
if (-not $psqlPath) {
    Write-Host "⚠️  psql not found in PATH" -ForegroundColor Yellow
    Write-Host "   Install PostgreSQL client tools to test connection" -ForegroundColor Yellow
    Write-Host "   Or use: bash scripts/supabase-init.sh" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "✅ Configuration looks correct!" -ForegroundColor Green
    Write-Host "   You can test the connection when you run the backend" -ForegroundColor White
    exit 0
}

Write-Host "Testing connection..." -ForegroundColor Yellow
$env:PGPASSWORD = $password
$testQuery = "SELECT 1 as test;"
$result = & psql -h $host -p $port -U $user -d $database -c $testQuery 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Connection successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next step: Initialize database" -ForegroundColor Cyan
    Write-Host "  cd backend" -ForegroundColor White
    Write-Host "  alembic upgrade head" -ForegroundColor White
} else {
    Write-Host "❌ Connection failed!" -ForegroundColor Red
    Write-Host "Error: $result" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check:" -ForegroundColor Yellow
    Write-Host "  1. Password is correct" -ForegroundColor White
    Write-Host "  2. Host and port are correct" -ForegroundColor White
    Write-Host "  3. Firewall allows connection" -ForegroundColor White
    exit 1
}
