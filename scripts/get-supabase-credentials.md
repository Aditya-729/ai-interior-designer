# 🔑 Getting Supabase Credentials

## Your Supabase Organization
**URL**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw

## Steps to Get Database Credentials

### 1. Access Your Project
1. Go to: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw
2. Click on your project (or create one if you haven't)

### 2. Get Database Connection String
1. In your project dashboard, click **Settings** (gear icon) in the left sidebar
2. Click **Database** in the settings menu
3. Scroll down to **Connection string** section
4. Select **URI** tab
5. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

### 3. Extract Credentials
From the connection string, extract:

**Example connection string:**
```
postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

**Extracted values:**
- **SUPABASE_DB_HOST**: `db.abcdefghijklmnop.supabase.co`
- **SUPABASE_DB_PORT**: `5432`
- **SUPABASE_DB_NAME**: `postgres`
- **SUPABASE_DB_USER**: `postgres`
- **SUPABASE_DB_PASSWORD**: `MyPassword123` (the password you set when creating the project)

### 4. Add to .env File
Add these to your `.env` file:
```bash
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-actual-password-here
```

### 5. Test Connection
```bash
./scripts/verify-setup.sh
```

---

## Alternative: Get from Connection Pooling

If you want to use connection pooling (recommended for production):

1. Go to **Settings** → **Database**
2. Scroll to **Connection pooling**
3. Use the **Session mode** connection string
4. Port will be different (usually `6543` instead of `5432`)

---

## Quick Access Links

- **Dashboard**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw
- **Projects**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/projects
- **Settings**: https://supabase.com/dashboard/org/vqdppqslarmzzgmyixsw/settings

---

## Security Note

⚠️ **Never share your database password publicly!**
- Keep it in `.env` file only
- Don't commit `.env` to Git
- Use environment variables in production
