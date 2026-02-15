# 🎯 Your Setup - Quick Reference

## Your Project IDs

### Supabase
- **Organization**: `vqdppqslarmzzgmyixsw`
- **Dashboard**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw
- **Projects**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/projects

### Vercel
- **Project ID**: `k6KjI0PFMQvhpMDtmzlZK9ca`
- **Dashboard**: https://vercel.com/dashboard

---

## Quick Setup Steps

### 1. Get Supabase Database Credentials (5 min)

1. Go to: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw
2. Click on your project (or create one)
3. Go to **Settings** → **Database**
4. Scroll to **Connection string** → Select **URI**
5. Copy the connection string
6. Extract credentials (see `scripts/get-supabase-credentials.md`)

**Add to `.env`:**
```bash
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password
```

### 2. Get Vercel Project URL (2 min)

1. Go to: https://vercel.com/dashboard
2. Find project: `k6KjI0PFMQvhpMDtmzlZK9ca`
3. Copy the deployment URL (e.g., `https://your-project.vercel.app`)

**Add to `.env`:**
```bash
FRONTEND_PUBLIC_URL=https://your-project.vercel.app
```

**Add to Vercel Environment Variables:**
```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

### 3. Initialize Database (2 min)

```bash
./scripts/supabase-init.sh
```

### 4. Verify Setup (1 min)

```bash
./scripts/verify-setup.sh
```

---

## Configuration Script

Run this to set up with your IDs:
```bash
./scripts/configure-with-ids.sh
```

---

## Direct Links

### Supabase
- **Dashboard**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw
- **Projects**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/projects
- **Settings**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/settings

### Vercel
- **Dashboard**: https://vercel.com/dashboard
- **Project**: https://vercel.com/dashboard/[your-project]

---

## Environment Variables Checklist

### Backend (.env)
- [ ] `SUPABASE_DB_HOST`
- [ ] `SUPABASE_DB_PORT`
- [ ] `SUPABASE_DB_NAME`
- [ ] `SUPABASE_DB_USER`
- [ ] `SUPABASE_DB_PASSWORD`
- [ ] `FRONTEND_PUBLIC_URL` (from Vercel)
- [ ] `PUBLIC_BACKEND_URL` (your domain or localhost)
- [ ] API keys (MINO_AI_API_KEY, PERPLEXITY_API_KEY)
- [ ] R2 storage credentials

### Vercel (Environment Variables)
- [ ] `NEXT_PUBLIC_API_BASE`
- [ ] `NEXT_PUBLIC_WS_URL`
- [ ] `NEXT_PUBLIC_DEMO_MODE`

---

## Testing

### Test Supabase Connection
```bash
./scripts/supabase-init.sh
```

### Test Vercel Deployment
1. Open your Vercel URL
2. Check browser console for errors
3. Test API connection

### Test Complete Flow
```bash
./scripts/public-smoke-test.sh
```

---

## Troubleshooting

### Can't find Supabase project?
- Make sure you're logged in
- Check: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/projects
- Create a new project if needed

### Can't find Vercel project?
- Search for ID: `k6KjI0PFMQvhpMDtmzlZK9ca`
- Or go to: https://vercel.com/dashboard
- Check all projects

### Connection issues?
- Verify credentials are correct
- Check firewall allows outbound connections
- Test with: `./scripts/verify-setup.sh`

---

## Next Steps

1. ✅ Get Supabase credentials → Add to `.env`
2. ✅ Get Vercel URL → Add to `.env` and Vercel env vars
3. ✅ Initialize database → `./scripts/supabase-init.sh`
4. ✅ Verify setup → `./scripts/verify-setup.sh`
5. ✅ Test deployment → Open Vercel URL
6. ✅ Setup domain (optional) → See `docs/DOMAIN_SETUP.md`

---

## Helpful Scripts

- `./scripts/configure-with-ids.sh` - Configure with your IDs
- `./scripts/setup-env-template.sh` - Create .env template
- `./scripts/verify-setup.sh` - Verify configuration
- `./scripts/supabase-init.sh` - Initialize database
- `./scripts/public-smoke-test.sh` - Test deployment

---

## Documentation

- **Supabase Setup**: `scripts/get-supabase-credentials.md`
- **Vercel Setup**: `scripts/get-vercel-credentials.md`
- **Complete Guide**: `SETUP_WIZARD.md`
- **Deployment**: `docs/PUBLIC_DEPLOY.md`
