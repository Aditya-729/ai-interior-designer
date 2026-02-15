# 🎯 Your Supabase Project Details

## Project Information
- **Project Name**: AI interior designer
- **Project ID**: `pzsdvpemnroxylbhjirr`
- **Organization**: `vqdppqslarmzzgmyixsw`

## Dashboard Links
- **General Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/general
- **Database Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database
- **Connection String**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database

---

## Step 1: Get Database Connection String

### Quick Access
👉 **Direct Link**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database

### Manual Steps
1. In your Supabase dashboard (where you are now)
2. Click **"Database"** in the left sidebar (under PROJECT SETTINGS)
3. Scroll down to **"Connection string"** section
4. Select the **"URI"** tab
5. **Copy the connection string**

The connection string will look like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

---

## Step 2: Extract Credentials

From the connection string, extract these values:

### Example Connection String:
```
postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

### Extracted Values:
| Variable | Value | Example |
|----------|-------|---------|
| `SUPABASE_DB_HOST` | Part after `@` | `db.abcdefghijklmnop.supabase.co` |
| `SUPABASE_DB_PORT` | Usually `5432` | `5432` |
| `SUPABASE_DB_NAME` | Usually `postgres` | `postgres` |
| `SUPABASE_DB_USER` | Usually `postgres` | `postgres` |
| `SUPABASE_DB_PASSWORD` | Your password | `MyPassword123` |

---

## Step 3: Add to .env File

Create or edit `.env` file in your project root:

```bash
# Supabase Database
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-actual-password-here

# Your Project IDs
SUPABASE_PROJECT_ID=pzsdvpemnroxylbhjirr
VERCEL_PROJECT_ID=k6KjI0PFMQvhpMDtmzlZK9ca
```

---

## Step 4: Test Connection

After adding credentials to `.env`, test the connection:

```bash
# On Linux/Mac
./scripts/supabase-init.sh

# On Windows (Git Bash or WSL)
bash scripts/supabase-init.sh
```

---

## Quick Reference

### Your Project URLs
- **General Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/general
- **Database Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database
- **API Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/api
- **Project Dashboard**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr

### Next Steps
1. ✅ Get connection string from Database settings
2. ✅ Extract credentials
3. ✅ Add to `.env` file
4. ✅ Test connection
5. → Get Vercel URL
6. → Initialize database
7. → Deploy!

---

## Security Note

⚠️ **Never share your database password!**
- Keep it only in `.env` file
- Don't commit `.env` to Git
- Use environment variables in production
