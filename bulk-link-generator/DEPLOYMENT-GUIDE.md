# 🚀 Deployment Guide - Email Tracking App

Since Railway subscription is over, here are **FREE** alternatives to deploy your email tracking application:

## 🌟 Option 1: Render (Recommended - Most Railway-like)

### Free Tier Limits:
- 750 hours/month (enough for hobby projects)
- Auto-sleep after 15 minutes of inactivity
- Custom domains supported
- Automatic builds from GitHub

### Steps to Deploy on Render:

1. **Push to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin master
   ```

2. **Go to Render.com**:
   - Sign up with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `k-arsyn/emailingScript`
   - Select the `bulk-link-generator` folder as root directory

3. **Configure the deployment**:
   - **Name**: `enhanced-email-tracker`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `npm start`
   - **Plan**: Free

4. **Set Environment Variables**:
   Go to Environment tab and add:
   ```
   NODE_ENV=production
   PORT=10000
   GOOGLE_SHEETS_ID=your_sheet_id
   GOOGLE_SHEETS_PRIVATE_KEY=your_private_key
   GOOGLE_SHEETS_CLIENT_EMAIL=your_client_email
   ```

5. **Deploy**: Click "Create Web Service"

### ✅ What works on Render:
- ✅ Express.js app
- ✅ SQLite database (stored in memory, resets on restart)
- ✅ File uploads
- ✅ Environment variables
- ✅ Custom domains

### ⚠️ Important Notes for Render:
- SQLite database will reset when the service restarts
- For persistent data, consider using PostgreSQL (also free on Render)

---

## 🌐 Option 2: Vercel (Serverless)

**Good for**: Static/serverless apps
**Limitation**: Requires converting to serverless functions

### Quick Setup:
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Follow the prompts

**Note**: Your current Express app needs modification for serverless.

---

## 🐳 Option 3: Fly.io

### Free Tier:
- 3 shared-cpu-1x 256MB VMs
- 3GB persistent volume storage

### Setup:
1. Install flyctl CLI
2. Run `fly launch` in your project directory
3. Follow deployment prompts

---

## 🔄 Option 4: Railway Alternative - Koyeb

### Free Tier:
- 512MB RAM
- 100GB bandwidth/month

### Setup:
1. Go to koyeb.com
2. Connect GitHub repository
3. Auto-detects Node.js and deploys

---

## 📋 Environment Variables You'll Need

Create these in your hosting platform's dashboard:

```env
# Required for Google Sheets integration
GOOGLE_SHEETS_ID=your_google_sheets_id
GOOGLE_SHEETS_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
GOOGLE_SHEETS_CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com

# Optional
NODE_ENV=production
PORT=10000
```

## 🔧 Pre-deployment Checklist

- [x] ✅ Package.json has start script
- [x] ✅ App uses process.env.PORT
- [x] ✅ Dependencies are listed in package.json
- [x] ✅ render.yaml created for easy deployment
- [ ] ⚠️ Environment variables configured
- [ ] ⚠️ Google Sheets credentials set up

## 🎯 Quick Start - Deploy to Render Now:

1. **Commit and push your code**:
   ```bash
   git add .
   git commit -m "Add render deployment config"
   git push
   ```

2. **Go to [render.com](https://render.com)**

3. **Connect GitHub and deploy** - the `render.yaml` file will handle the rest!

4. **Set your environment variables** in the Render dashboard

5. **Your app will be live** at: `https://your-app-name.onrender.com`

## 📱 Alternative Free Platforms Summary:

| Platform | Free Tier | Best For | Database |
|----------|-----------|----------|----------|
| **Render** | 750hrs/month | Full-stack apps | PostgreSQL free |
| **Vercel** | Unlimited | Frontend/API | External DB needed |
| **Fly.io** | 3 VMs | Docker apps | 3GB storage |
| **Koyeb** | 512MB RAM | Simple apps | External DB |
| **Cyclic** | 1000hrs/month | Node.js apps | DynamoDB included |

## 🆘 Need Help?

If you face any issues:
1. Check the deployment logs in your platform's dashboard
2. Ensure all environment variables are set correctly
3. Verify your Google Sheets credentials are properly formatted

**Recommendation**: Start with **Render** as it's most similar to Railway and requires minimal changes to your existing code.
