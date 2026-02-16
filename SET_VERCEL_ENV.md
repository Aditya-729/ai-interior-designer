# 🔧 Setting Vercel Environment Variables

## Quick Fix for "Failed to upload image" Error

The frontend needs to know where your backend API is located. Set these environment variables:

### Step 1: Determine Your Backend URL

**If your backend is deployed:**
- Use your backend URL (e.g., `https://api.yourdomain.com`)

**If your backend is running locally:**
- Use a tunnel service like ngrok: `https://your-tunnel.ngrok.io`
- Or deploy your backend first

**If you don't have a backend yet:**
- Set a placeholder: `https://api.yourdomain.com`
- Update it later when you deploy your backend

### Step 2: Set Environment Variables

#### Option A: Via Vercel Dashboard (Easiest)

1. Go to: https://vercel.com/dashboard
2. Click on your project: `adityas-projects-e275b3df/frontend`
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Add these variables:

**Variable 1:**
- **Name:** `NEXT_PUBLIC_API_BASE`
- **Value:** `https://api.yourdomain.com` (replace with your actual backend URL)
- **Environment:** Production (and Preview if needed)

**Variable 2:**
- **Name:** `NEXT_PUBLIC_WS_URL`
- **Value:** `wss://api.yourdomain.com` (replace with your actual WebSocket URL)
- **Environment:** Production (and Preview if needed)

6. Click **Save**
7. Go to **Deployments** tab
8. Click **⋯** (three dots) on the latest deployment
9. Click **Redeploy**

#### Option B: Via Vercel CLI

```powershell
cd frontend

# Set API Base URL
vercel env add NEXT_PUBLIC_API_BASE production
# When prompted, enter: https://api.yourdomain.com

# Set WebSocket URL
vercel env add NEXT_PUBLIC_WS_URL production
# When prompted, enter: wss://api.yourdomain.com

# Redeploy
vercel --prod
```

### Step 3: Verify

After redeploying, test your app:
1. Open: https://frontend-jgsrttgb7-adityas-projects-e275b3df.vercel.app
2. Try uploading an image
3. Check browser console (F12) for any errors

### Troubleshooting

**Still getting "Failed to upload image"?**
- Check that your backend is running and accessible
- Verify CORS is configured on your backend to allow requests from your Vercel domain
- Check browser console (F12) for detailed error messages

**Backend not deployed yet?**
- You can set placeholder values now
- The frontend will deploy successfully
- You'll need to update the values once your backend is deployed

### Example Values

**For Production:**
```
NEXT_PUBLIC_API_BASE=https://api.yourdomain.com
NEXT_PUBLIC_WS_URL=wss://api.yourdomain.com
```

**For Testing with Local Backend (via ngrok):**
```
NEXT_PUBLIC_API_BASE=https://abc123.ngrok.io
NEXT_PUBLIC_WS_URL=wss://abc123.ngrok.io
```

**For Development (won't work from Vercel, but for reference):**
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```
