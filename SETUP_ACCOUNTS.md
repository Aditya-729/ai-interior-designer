# 🔐 Setting Up Vercel & Supabase Accounts

## Step 1: Create Supabase Account & Project

### 1.1 Sign Up
1. Go to **https://supabase.com**
2. Click **"Start your project"** or **"Sign up"**
3. Sign up with:
   - GitHub (recommended - easiest)
   - Email
   - Google

### 1.2 Create New Project
1. Click **"New Project"** button
2. Fill in:
   - **Name**: `AI Interior Designer` (or your choice)
   - **Database Password**: 
     - Generate a STRONG password (save it!)
     - Use password manager or write it down securely
   - **Region**: Choose closest to your GPU VM location
   - **Pricing Plan**: Free tier is fine for MVP

3. Click **"Create new project"**
4. Wait 2-3 minutes for project to be created

### 1.3 Get Database Credentials
1. In your project dashboard, go to **Settings** (gear icon)
2. Click **Database** in left sidebar
3. Scroll to **Connection string** section
4. Select **URI** format
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

### 1.4 Extract Connection Details
From the connection string, extract:
- **Host**: `db.xxxxx.supabase.co` (part after `@`)
- **Port**: `5432` (usually)
- **Database**: `postgres` (usually)
- **User**: `postgres` (usually)
- **Password**: The password you set

### 1.5 Add to Your .env File
```bash
# Supabase Database
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-password-here
```

---

## Step 2: Create Vercel Account & Project

### 2.1 Sign Up
1. Go to **https://vercel.com**
2. Click **"Sign up"**
3. Sign up with:
   - GitHub (recommended - connects to your repo)
   - Email
   - GitLab
   - Bitbucket

### 2.2 Import Your Repository
1. After signing in, click **"Add New..."** → **"Project"**
2. If using GitHub:
   - Authorize Vercel to access your GitHub
   - Select your repository: `AI Interior Designer`
3. If not using GitHub:
   - You'll need to push your code to a Git provider first
   - Then import from that provider

### 2.3 Configure Project Settings
1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)
5. **Install Command**: `npm install` (default)

### 2.4 Set Environment Variables
Before deploying, click **"Environment Variables"** and add:

```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
NEXT_PUBLIC_DEMO_MODE=false
```

**Note**: Replace `yourdomain.com` with your actual domain (or use Vercel's default URL for testing)

### 2.5 Deploy
1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. Your app will be live at: `https://your-project.vercel.app`

---

## Step 3: Get Your Credentials

### Supabase Credentials Needed:
- ✅ Database Host
- ✅ Database Port (usually 5432)
- ✅ Database Name (usually postgres)
- ✅ Database User (usually postgres)
- ✅ Database Password

### Vercel Credentials Needed:
- ✅ Project URL (auto-generated)
- ✅ Environment variables (you set them)

---

## Step 4: Test Connections

### Test Supabase Connection
```bash
# On your GPU VM
./scripts/supabase-init.sh
```

### Test Vercel Deployment
```bash
# Open your Vercel URL
open https://your-project.vercel.app
```

---

## Troubleshooting

### Supabase Issues

**"Connection refused"**
- Check firewall allows outbound connections
- Verify host/port are correct
- Check password is correct

**"SSL required"**
- Supabase requires SSL
- Connection string should include `?sslmode=require`
- Our code handles this automatically

### Vercel Issues

**"Build failed"**
- Check `frontend/package.json` has all dependencies
- Verify `npm run build` works locally
- Check build logs in Vercel dashboard

**"API calls failing"**
- Verify `NEXT_PUBLIC_API_BASE` is set correctly
- Check CORS settings on backend
- Ensure backend is accessible

---

## Quick Checklist

### Supabase ✅
- [ ] Account created
- [ ] Project created
- [ ] Database password saved
- [ ] Connection details extracted
- [ ] Added to `.env` file
- [ ] Tested connection

### Vercel ✅
- [ ] Account created
- [ ] Repository connected
- [ ] Project configured
- [ ] Environment variables set
- [ ] Deployed successfully
- [ ] Tested frontend

---

## Next Steps

After both accounts are set up:

1. **Update `.env`** with Supabase credentials
2. **Run Supabase init**: `./scripts/supabase-init.sh`
3. **Update Vercel env vars** with your backend URL
4. **Redeploy Vercel** if needed
5. **Test complete flow**: Upload → Edit → Share

---

## Security Notes

⚠️ **Never commit `.env` file to Git**
- Add `.env` to `.gitignore`
- Use Vercel's environment variables UI
- Use Supabase's built-in security features

✅ **Best Practices**
- Use strong passwords
- Enable 2FA on both accounts
- Rotate credentials regularly
- Monitor usage in dashboards

---

## Need Help?

- **Supabase Docs**: https://supabase.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Our Docs**: See `docs/PUBLIC_DEPLOY.md`
