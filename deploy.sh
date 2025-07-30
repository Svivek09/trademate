#!/bin/bash

echo "🚀 TradeMate Deployment Script"
echo "=============================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Git remote not set. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/trademate.git"
    exit 1
fi

echo "✅ Git repository ready"

# Check environment files
echo ""
echo "📋 Environment Setup Check:"
echo "---------------------------"

if [ -f "server/.env" ]; then
    echo "✅ Backend .env file exists"
else
    echo "❌ Backend .env file missing"
    echo "   Create server/.env with your API keys"
fi

if [ -f "client/.env" ]; then
    echo "✅ Frontend .env file exists"
else
    echo "❌ Frontend .env file missing"
    echo "   Create client/.env with REACT_APP_API_URL"
fi

echo ""
echo "🌐 Deployment Steps:"
echo "==================="
echo ""
echo "1. 📤 Push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for deployment'"
echo "   git push origin main"
echo ""
echo "2. 🔧 Backend (Render):"
echo "   - Go to https://dashboard.render.com"
echo "   - Connect your GitHub repository"
echo "   - Create new Web Service"
echo "   - Set environment variables:"
echo "     * DATABASE_TYPE=mongodb"
echo "     * DATABASE_URL=your_mongodb_atlas_url"
echo "     * ALPHA_VANTAGE_API_KEY=your_key"
echo "     * GEMINI_API_KEY=your_key"
echo ""
echo "3. 🎨 Frontend (Netlify):"
echo "   - Go to https://app.netlify.com"
echo "   - Connect your GitHub repository"
echo "   - Set build settings:"
echo "     * Base directory: client"
echo "     * Build command: npm run build"
echo "     * Publish directory: build"
echo "   - Set environment variable:"
echo "     * REACT_APP_API_URL=https://your-render-url.onrender.com"
echo ""
echo "4. 🗄️ Database (MongoDB Atlas):"
echo "   - Create free cluster at https://cloud.mongodb.com"
echo "   - Get connection string"
echo "   - Update DATABASE_URL in Render"
echo ""
echo "✅ Your TradeMate application will be live!"
echo ""
echo "🔗 Expected URLs:"
echo "   Frontend: https://your-app-name.netlify.app"
echo "   Backend: https://trademate-backend.onrender.com"
echo "   API Docs: https://trademate-backend.onrender.com/docs" 