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

### Step 3: Configure Service (Auto-detected!)
Render will automatically detect the configuration from `render.yaml`:

- **Name**: cookbook
- **Region**: Oregon (US West)
- **Branch**: master
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 wsgi:app`
- **Plan**: Free

Just verify these settings and click **"Create Web Service"**

### Step 4: Wait for Deployment
- Deployment takes 3-5 minutes
- You'll see logs in real-time
- Wait for "Your service is live 🎉"

### Step 5: Access Your App!
Your app will be live at:
**https://cookbook.onrender.com** (or similar URL)

## Important Notes

### Free Tier Limitations
- ⚠️ **Sleeps after 15 minutes** of inactivity
- ⏱️ Takes ~30 seconds to wake up when accessed
- 🔄 Automatic wake-up on first request

### To Avoid Sleeping (Optional)
**Option 1**: Upgrade to paid plan ($7/month)
**Option 2**: Use UptimeRobot (free) to ping every 10 minutes
1. Go to https://uptimerobot.com
2. Add new monitor
3. URL: your Render app URL
4. Interval: 10 minutes

### Database
- ✅ SQLite database with 875 recipes is included
- ✅ Works perfectly for this application
- ✅ No additional setup needed

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
2. Verify Python version is 3.11.0
3. Make sure all files are committed to GitHub

### If app doesn't load:
1. Wait 30 seconds (might be waking up)
2. Check Render logs for errors
3. Verify environment variables are set

## Alternative: Railway.app

If you prefer Railway (also free, no sleep):

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select **cookbook**
5. Done! Live in 2 minutes

Railway gives you $5 free credit per month (enough for this app).

## Your Repository

**GitHub**: https://github.com/leonrod/cookbook  
**Visibility**: Private  
**Branch**: master

## Next Steps

1. Deploy on Render.com (follow steps above)
2. Get your permanent URL
3. Share with your friends!
4. Enjoy your Haven & Hearth recipe calculator 🎮

---

**Need help?** Check the Render documentation: https://render.com/docs
