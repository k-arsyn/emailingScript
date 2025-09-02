#!/bin/bash
# IIIT Trichy Server Deployment Script

echo "📦 Installing Node.js dependencies..."
cd bulk-link-generator
npm install

echo "🔧 Setting up environment..."
# Create production environment file
cat > .env << EOF
NODE_ENV=production
PORT=3300
DATABASE_PATH=./mail-tracker.db
EOF

echo "🗃️ Setting up database..."
# Initialize database (SQLite will create it automatically)
node -e "console.log('Database will be created on first run')"

echo "📁 Creating necessary directories..."
mkdir -p public/images
mkdir -p logs

echo "🎯 Setting up PM2 for process management..."
npm install -g pm2

echo "🚀 Ready for deployment!"
echo "Next steps:"
echo "1. Copy this folder to your college server"
echo "2. Run: pm2 start enhanced-tracker.js --name email-tracker"
echo "3. Run: pm2 startup"
echo "4. Run: pm2 save"
