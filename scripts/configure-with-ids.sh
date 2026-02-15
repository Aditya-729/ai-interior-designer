#!/bin/bash

# Configure project with your Supabase and Vercel IDs

set -e

echo "🔧 Configuring with your project IDs..."
echo ""

# Supabase Organization
SUPABASE_ORG="vqdppqslarmzzgmyixsw"
SUPABASE_URL="https://supabase.com/dashboard/org/${SUPABASE_ORG}"

# Vercel Project ID
VERCEL_PROJECT_ID="k6KjI0PFMQvhpMDtmzlZK9ca"

echo "📊 Your Project Information:"
echo "   Supabase Org: ${SUPABASE_ORG}"
echo "   Vercel Project ID: ${VERCEL_PROJECT_ID}"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    ./scripts/setup-env-template.sh
fi

echo ""
echo "🔑 Next Steps:"
echo ""
echo "1. Get Supabase Database Credentials:"
echo "   → Go to: ${SUPABASE_URL}"
echo "   → Click on your project"
echo "   → Settings → Database → Connection string (URI)"
echo "   → Copy and extract credentials"
echo ""
echo "2. Get Vercel Project URL:"
echo "   → Go to: https://vercel.com/dashboard"
echo "   → Find project ID: ${VERCEL_PROJECT_ID}"
echo "   → Copy the deployment URL"
echo ""
echo "3. Update .env file with:"
echo "   - Supabase credentials (from step 1)"
echo "   - Vercel URL (from step 2)"
echo "   - Your API keys"
echo ""
echo "4. Run verification:"
echo "   ./scripts/verify-setup.sh"
echo ""

# Create a quick reference file
cat > YOUR_PROJECT_IDS.txt << EOF
# Your Project IDs - Keep for Reference

## Supabase
Organization: ${SUPABASE_ORG}
Dashboard: ${SUPABASE_URL}
Projects: ${SUPABASE_URL}/projects

## Vercel
Project ID: ${VERCEL_PROJECT_ID}
Dashboard: https://vercel.com/dashboard

## Next Steps
1. Get Supabase database credentials (see scripts/get-supabase-credentials.md)
2. Get Vercel project URL (see scripts/get-vercel-credentials.md)
3. Update .env file
4. Run: ./scripts/verify-setup.sh
EOF

echo "✅ Created YOUR_PROJECT_IDS.txt for quick reference"
echo ""
echo "📚 Detailed guides:"
echo "   - Supabase: scripts/get-supabase-credentials.md"
echo "   - Vercel: scripts/get-vercel-credentials.md"
