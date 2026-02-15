# 🔑 Get Your Database Credentials - Quick Guide

## Your Supabase Project
- **Project ID**: `pzsdvpemnroxylbhjirr`
- **Project Name**: AI interior designer

---

## Step 1: Go to Database Settings

👉 **Click here**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database

Or manually:
1. In your Supabase dashboard
2. Click **"Database"** in the left sidebar (under PROJECT SETTINGS)
3. You'll see the database settings page

---

## Step 2: Get Connection String

1. Scroll down to **"Connection string"** section
2. You'll see tabs: **"URI"**, **"JDBC"**, **"Golang"**, etc.
3. Click the **"URI"** tab
4. You'll see a connection string like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
5. **Click the copy button** (or select and copy)

---

## Step 3: Extract Credentials

### Option A: Use the Script (Easiest)

```powershell
# Paste your connection string
.\scripts\extract-supabase-credentials.ps1 "postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres"
```

### Option B: Manual Extraction

From this connection string:
```
postgresql://postgres:MyPassword123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

Extract:
- **Host**: `db.abcdefghijklmnop.supabase.co` (part after `@`)
- **Port**: `5432` (number after the host)
- **Database**: `postgres` (part after the last `/`)
- **User**: `postgres` (part after `//`)
- **Password**: `MyPassword123` (part between `:` and `@`)

---

## Step 4: Add to .env File

Create or edit `.env` file in project root:

```bash
# Supabase Database
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-actual-password
```

---

## Step 5: Test Connection

```bash
# On Windows (Git Bash or WSL)
bash scripts/supabase-init.sh

# Or test manually
psql -h db.xxxxx.supabase.co -U postgres -d postgres
```

---

## Quick Links

- **Database Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/database
- **General Settings**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr/settings/general
- **Project Dashboard**: https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr

---

## What You'll See

In the Database settings page, you'll see:
- **Connection pooling** section
- **Connection string** section (this is what you need!)
- **Database password** section (to reset password)
- **SSL mode** information

**Look for the "Connection string" section and click the "URI" tab!**

---

## Next Steps

After getting credentials:
1. ✅ Add to `.env` file
2. ✅ Test connection: `bash scripts/supabase-init.sh`
3. ✅ Get Vercel URL
4. ✅ Initialize database
5. ✅ Deploy!
