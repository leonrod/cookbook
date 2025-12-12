# 🚀 Deploy Your Cookbook to Render.com

Your code is now on GitHub at: **https://github.com/leonrod/cookbook**

## Deploy Steps (5 minutes)

### Step 1: Sign Up on Render.com
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account (@leonrod)

### Step 2: Create New Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect GitHub"
4. Find and select your repository: **cookbook**
5. Click "Connect"

### Step 3: Configure Service

Render detected Docker in your repository. Configure as follows:

#### Basic Settings
- **Name**: `cookbook` (or any name you prefer)
- **Language**: Docker (auto-detected)
- **Branch**: `master`
- **Region**: Oregon (US West) or any region you prefer

#### Instance Type
Select **Free** plan:
- 512 MB RAM
- 0.1 CPU
- $0/month
- ⚠️ Spins down after periods of inactivity

#### Environment Variables
Click "+ Add Environment Variable" and add:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Click "Generate" to auto-generate |

**Note**: You can leave other variables with defaults. The app will use built-in defaults.

#### Advanced Settings (Optional)

Expand "Advanced" section if you want to customize:

- **Health Check Path**: `/health` (optional, for monitoring)
- **Docker Command**: Leave empty (uses Dockerfile's CMD)
- **Auto-Deploy**: On Commit (default, recommended)

### Step 4: Deploy!

Click **"Deploy Web Service"** at the bottom.

### Step 5: Wait for Deployment
- Deployment takes 3-5 minutes
- You'll see logs in real-time:
  - Building Docker image
  - Installing dependencies
  - Starting Gunicorn server
- Wait for "Your service is live 🎉"

### Step 6: Access Your App!
Your app will be live at:
**https://cookbook-XXXX.onrender.com**

(Render will assign a unique URL)

## Important Notes

### Free Tier Limitations
- ⚠️ **Sleeps after 15 minutes** of inactivity
- ⏱️ Takes ~30 seconds to wake up when accessed
- 🔄 Automatic wake-up on first request
- 💾 SQLite database persists (included in Docker image)

### To Avoid Sleeping

**Option 1: Upgrade to Paid Plan**
- Starter: $7/month (0.5 CPU, 512 MB RAM)
- Standard: $25/month (1 CPU, 2 GB RAM)
- No sleep, always online

**Option 2: Use UptimeRobot (Free)**
1. Go to https://uptimerobot.com
2. Sign up (free)
3. Add new monitor:
   - Monitor Type: HTTP(s)
   - URL: Your Render app URL
   - Monitoring Interval: 10 minutes
4. UptimeRobot will ping your app every 10 minutes, keeping it awake

### Database
- ✅ SQLite database with 875 recipes is included in Docker image
- ✅ Works perfectly for this application
- ✅ No additional setup needed
- ⚠️ Data resets on redeployment (use persistent disk for production)

## Features Included

✅ 875 Haven & Hearth recipes  
✅ Advanced search with complex filters  
✅ Character Engineer with multipliers  
✅ Exclusion system (ingredients/recipes)  
✅ Meal planner & shopping list  
✅ Expected FEP calculations (bug-fixed)  
✅ Persistent data (localStorage)

## Troubleshooting

### If deployment fails:
1. Check logs in Render dashboard
2. Look for Docker build errors
3. Verify Dockerfile is correct
4. Make sure all files are committed to GitHub

### If app doesn't load:
1. Wait 30 seconds (might be waking up from sleep)
2. Check Render logs for errors
3. Verify environment variables are set correctly
4. Check Health Check status in Render dashboard

### If you see "Application failed to respond":
1. Check if PORT environment variable is set (should be auto-set by Render)
2. Verify Gunicorn is binding to `0.0.0.0:$PORT`
3. Check Dockerfile CMD is correct

## Alternative Deployment Options

### Railway.app (No Sleep on Free Tier)

If you prefer Railway (also free, $5 credit/month, no sleep):

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select **cookbook**
5. Railway will auto-detect Docker
6. Click "Deploy"
7. Done! Live in 2 minutes

**Advantages**:
- $5 free credit per month (enough for this app)
- No sleep on free tier
- Faster wake-up times
- Better for continuous use

### Fly.io (Global Edge Network)

For advanced users:

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
cd /path/to/cookbook
flyctl launch --name cookbook
flyctl deploy
```

## Your Repository

**GitHub**: https://github.com/leonrod/cookbook  
**Visibility**: Private  
**Branch**: master

## Configuration Files

Your repository includes:
- ✅ `Dockerfile` - Docker image configuration
- ✅ `docker-compose.yml` - Local development
- ✅ `render.yaml` - Render configuration (alternative to UI)
- ✅ `requirements.txt` - Python dependencies
- ✅ `gunicorn.conf.py` - Production server config

## Next Steps

1. ✅ Complete configuration in Render.com (follow steps above)
2. ✅ Click "Deploy Web Service"
3. ✅ Wait 3-5 minutes for deployment
4. ✅ Get your permanent URL
5. ✅ (Optional) Set up UptimeRobot to avoid sleeping
6. ✅ Share with your friends!
7. ✅ Enjoy your Haven & Hearth recipe calculator 🎮

---

**Need help?** 
- Check Render documentation: https://render.com/docs
- Check deployment logs in Render dashboard
- Open an issue on GitHub
