# 🚀 Final Railway Setup - Using Supabase Storage

## ✅ What I've Done

1. ✅ **Switched from R2 to Supabase Storage**
   - Modified `backend/app/services/storage.py` to use Supabase
   - Made R2 optional (no longer required)
   - Updated configuration

2. ✅ **Created Railway Variables File**
   - `railway-variables-supabase.txt` - Ready to paste

3. ✅ **Generated JWT Secret**
   - Saved in `jwt-secret.txt`

---

## 📋 What You Need to Add to Railway

### Step 1: Get Supabase Keys

Go to: **https://supabase.com/dashboard/project/pzsdvpemnroxylbhjirr**

1. Click **Settings** → **API**
2. Copy these 3 values:
   - **SUPABASE_URL** = `https://pzsdvpemnroxylbhjirr.supabase.co`
   - **SUPABASE_SERVICE_KEY** = (service_role key - secret!)
   - **SUPABASE_ANON_KEY** = (anon/public key)

3. Enable Storage:
   - Go to **Storage** section
   - Create bucket: `ai-interior-designer`
   - Make it **Public**

### Step 2: Add to Railway

1. Go to Railway: https://railway.com/project/df46718f-fd2b-48e5-94b7-8e95758397d8
2. Click your service → **Variables** tab → **Raw Editor**
3. Open `railway-variables-supabase.txt`
4. **Replace these 3 values:**
   ```
   SUPABASE_URL=https://pzsdvpemnroxylbhjirr.supabase.co
   SUPABASE_SERVICE_KEY=your-actual-service-key-here
   SUPABASE_ANON_KEY=your-actual-anon-key-here
   ```
5. **Add your API keys:**
   ```
   MINO_AI_API_KEY=your-actual-mino-key
   PERPLEXITY_API_KEY=your-actual-perplexity-key
   ```
6. Copy everything and paste into Railway Raw Editor
7. Click **Save**

---

## ✅ Variables Already Set (in railway-variables-supabase.txt)

These are already correct - just copy them:

- ✅ Database credentials (Supabase)
- ✅ Frontend/Backend URLs
- ✅ JWT_SECRET (generated)
- ✅ Environment settings
- ✅ All other config

---

## 🎯 Quick Checklist

- [ ] Get Supabase keys (URL, Service Key, Anon Key)
- [ ] Create Storage bucket: `ai-interior-designer` (public)
- [ ] Get Mino AI API key
- [ ] Get Perplexity API key
- [ ] Open `railway-variables-supabase.txt`
- [ ] Replace placeholder values
- [ ] Copy all content
- [ ] Railway → Variables → Raw Editor → Paste → Save
- [ ] Wait 2-3 minutes for redeploy
- [ ] Test backend: https://ai-interior-designer-backend-production.up.railway.app/api/v1/system/health

---

## 📁 Files Created

- ✅ `railway-variables-supabase.txt` - Ready to paste (just add 5 values)
- ✅ `HOW_TO_GET_SUPABASE_STORAGE_KEYS.md` - Detailed instructions
- ✅ `jwt-secret.txt` - Your generated JWT secret

---

## 🎉 Benefits of Supabase Storage

- ✅ No new account needed (you already have Supabase)
- ✅ Free tier available
- ✅ ✅ Easier setup than R2
- ✅ Integrated with your existing database

---

## ⚠️ Important Notes

1. **R2 is now optional** - You don't need it anymore!
2. **Supabase Storage is required** - Get the 3 keys from Supabase dashboard
3. **Storage bucket must be public** - So images can be accessed
4. **Service Key is secret** - Don't share it or commit to GitHub

---

## 🚀 After Setup

Once you add the variables to Railway:
1. Backend will automatically redeploy
2. Wait 2-3 minutes
3. Backend should start successfully
4. Image uploads will work with Supabase Storage!

---

## 📖 Full Instructions

See `HOW_TO_GET_SUPABASE_STORAGE_KEYS.md` for step-by-step guide to get Supabase keys.
