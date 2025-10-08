#!/bin/bash

# Quick deployment script for enhanced email tracker
# This script helps you deploy to various platforms

echo "🚀 Enhanced Email Tracker - Deployment Helper"
echo "============================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ This is not a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin YOUR_GITHUB_REPO_URL"
    echo "   git push -u origin master"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 You have uncommitted changes. Committing them now..."
    git add .
    git commit -m "Prepare for deployment - $(date)"
    git push
    echo "✅ Changes committed and pushed!"
else
    echo "✅ Git repository is clean"
fi

echo ""
echo "🌟 Your app is ready for deployment!"
echo ""
echo "Choose your deployment platform:"
echo ""
echo "1. 🔥 Render (Recommended)"
echo "   - Go to: https://render.com"
echo "   - Connect your GitHub repo: k-arsyn/emailingScript"
echo "   - Select folder: bulk-link-generator"
echo "   - render.yaml will handle the rest!"
echo ""
echo "2. ⚡ Vercel"
echo "   - Run: npx vercel"
echo "   - Follow the prompts"
echo ""
echo "3. 🐳 Fly.io"
echo "   - Install flyctl CLI"
echo "   - Run: fly launch"
echo ""
echo "4. 🚀 Koyeb"
echo "   - Go to: https://koyeb.com"
echo "   - Connect GitHub repo"
echo ""
echo "📋 Don't forget to:"
echo "   ✅ Set environment variables (see .env.production)"
echo "   ✅ Configure Google Sheets credentials"
echo "   ✅ Update GOOGLE_SHEETS_ID in your platform's env vars"
echo ""
echo "📖 Full guide: See DEPLOYMENT-GUIDE.md"
echo ""
echo "Good luck with your deployment! 🎉"
