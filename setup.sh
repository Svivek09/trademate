#!/bin/bash

echo "🚀 Setting up TradeMate - Your Personal Trading Analytics Dashboard"
echo "================================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Setup Backend
echo ""
echo "📦 Setting up Backend (FastAPI)..."
cd server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Created .env file. Please update with your API keys."
fi

echo "✅ Backend setup complete"

# Setup Frontend
echo ""
echo "📦 Setting up Frontend (React)..."
cd ../client

# Install Node.js dependencies
npm install

# Copy environment file
if [ ! -f .env ]; then
    cp env.example .env
    echo "📝 Created .env file for frontend."
fi

echo "✅ Frontend setup complete"

# Return to root
cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Update server/.env with your API keys:"
echo "   - ALPHA_VANTAGE_API_KEY (get from https://www.alphavantage.co/)"
echo "   - GEMINI_API_KEY (get from https://makersuite.google.com/app/apikey)"
echo ""
echo "2. Start the backend:"
echo "   cd server && source venv/bin/activate && python main.py"
echo ""
echo "3. Start the frontend (in a new terminal):"
echo "   cd client && npm start"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see README.md" 