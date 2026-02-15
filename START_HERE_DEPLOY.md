# 🚀 START HERE - Deployment Setup

## Quick Start (30 minutes total)

### 1. Supabase (10 min)
1. Go to **https://supabase.com** → Sign up
2. Create new project → Save password
3. Get credentials from Settings → Database
4. Add to `.env` file (see `SETUP_WIZARD.md`)

### 2. Vercel (10 min)
1. Go to **https://vercel.com** → Sign up
2. Import your repository
3. Set environment variables
4. Deploy

### 3. Verify (10 min)
1. Run: `./scripts/verify-setup.sh`
2. Run: `./scripts/supabase-init.sh`
3. Test: Open your Vercel URL

---

## Detailed Guides

- **`SETUP_WIZARD.md`** - Step-by-step setup instructions
- **`SETUP_ACCOUNTS.md`** - Detailed account creation guide
- **`QUICK_DEPLOY.md`** - Quick deployment reference
- **`docs/PUBLIC_DEPLOY.md`** - Complete deployment guide

---

## What You Need

### Accounts (Free)
- ✅ Supabase account (free tier)
- ✅ Vercel account (free tier)
- ✅ GitHub account (for Vercel integration)

### Credentials to Get
- ✅ Supabase database password
- ✅ Supabase connection string
- ✅ Vercel project URL (auto-generated)

### Already Have
- ✅ GPU VM with Docker
- ✅ Domain name (optional)
- ✅ API keys (Mino AI, Perplexity)

---

## First Time Setup

```bash
# 1. Create .env template
./scripts/setup-env-template.sh

# 2. Edit .env with your credentials
nano .env  # or use your editor

# 3. Verify setup
./scripts/verify-setup.sh

# 4. Initialize Supabase
./scripts/supabase-init.sh
```

---

## Need Help?

1. **Account issues**: See `SETUP_ACCOUNTS.md`
2. **Connection problems**: See `SETUP_WIZARD.md` troubleshooting
3. **Deployment issues**: See `docs/PUBLIC_DEPLOY.md`
4. **Domain setup**: See `docs/DOMAIN_SETUP.md`

---

## Next Steps After Setup

1. ✅ Supabase connected
2. ✅ Vercel deployed
3. → Setup domain (optional)
4. → Configure HTTPS
5. → Test complete flow
6. → Launch! 🎉
