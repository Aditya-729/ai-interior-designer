# How to Get Supabase Storage Keys

## What You Need

You need **3 values** from Supabase:

1. **SUPABASE_URL** - Your Supabase project URL
2. **SUPABASE_SERVICE_KEY** - Service role key (for storage operations)
3. **SUPABASE_ANON_KEY** - Anonymous key (optional but recommended)

---

## Step-by-Step Instructions

### Step 1: Go to Supabase Dashboard
1. Open your browser
2. Go to: **https://supabase.com/dashboard**
3. **Log in** with your Supabase account

### Step 2: Select Your Project
1. Click on your project: **`pzsdvpemnroxylbhjirr`** (or your project name)
2. You'll see the project dashboard

### Step 3: Get Your Project URL
1. Look at the **URL in your browser**
2. It will be: `https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr`
3. Your **SUPABASE_URL** is: `https://pzsdvpemnroxylbhjirr.supabase.co`
   - Format: `https://[project-ref].supabase.co`

### Step 4: Get API Keys
1. In the left sidebar, click **"Settings"** (gear icon)
2. Click **"API"** in the settings menu
3. You'll see two sections:
   - **Project API keys**
   - **Service role key** (⚠️ Keep this secret!)

### Step 5: Copy the Keys
1. **SUPABASE_ANON_KEY** (anon/public key):
   - Under "Project API keys"
   - Find **"anon"** or **"public"** key
   - Click the eye icon to reveal it
   - Copy this value

2. **SUPABASE_SERVICE_KEY** (service_role key):
   - Under "Project API keys"
   - Find **"service_role"** key
   - ⚠️ **This is secret!** Click to reveal
   - Copy this value
   - This is what you need for storage operations

### Step 6: Enable Storage (if not already enabled)
1. In the left sidebar, click **"Storage"**
2. If you see "Storage is not enabled", click **"Enable Storage"**
3. Create a bucket named: **`ai-interior-designer`**
   - Click **"New bucket"**
   - Name: `ai-interior-designer`
   - Make it **Public** (so images can be accessed)
   - Click **"Create bucket"**

---

## What You Should Have

After completing all steps:

1. ✅ **SUPABASE_URL** = `https://pzsdvpemnroxylbhjirr.supabase.co`
2. ✅ **SUPABASE_ANON_KEY** = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (long JWT token)
3. ✅ **SUPABASE_SERVICE_KEY** = `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (long JWT token)
4. ✅ **Storage bucket** = `ai-interior-designer` (created and public)

---

## Quick Reference

**Supabase Dashboard:** https://supabase.com/dashboard

**Your Project:** https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr

**API Settings:** Dashboard → Settings → API

**Storage:** Dashboard → Storage

---

## Security Notes

⚠️ **Important:**
- **SUPABASE_SERVICE_KEY** has full access - keep it secret!
- Never commit service keys to GitHub
- Use service key only on backend/server
- Anon key is safe for frontend use

---

## Troubleshooting

### "I can't find the service_role key"
- Go to Settings → API
- Look for "service_role" under "Project API keys"
- Click to reveal it

### "Storage bucket not found"
- Go to Storage section
- Create bucket: `ai-interior-designer`
- Make it Public

### "Where is my project URL?"
- Look at the URL when you're in your project dashboard
- Format: `https://[project-ref].supabase.co`
- Your project ref is in the URL: `dashboard/project/[project-ref]`

---

## Next Steps

After getting the keys:
1. Add them to `railway-variables-supabase.txt`
2. Copy all variables to Railway Raw Editor
3. Save and redeploy
