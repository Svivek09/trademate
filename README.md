# 🚀 TradeMate - Your Personal Trading Analytics Dashboard

A full-stack fintech application that provides real-time trading analytics, portfolio management, and AI-powered insights.

![TradeMate Dashboard](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/React-18.2.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-blue)

## ✨ Features

### 📊 **Dashboard Analytics**
- Real-time portfolio performance tracking
- Interactive charts and visualizations
- Market indices overview
- Recent trades tracking

### 💼 **Portfolio Management**
- Multi-portfolio support
- Asset allocation visualization
- Performance metrics
- Add/remove assets

### 🔁 **Trading Strategies**
- Moving Average Crossover
- RSI Strategy
- MACD Strategy
- Backtesting capabilities

### 🧠 **AI-Powered Insights**
- Gemini Pro integration
- Trading advice
- Technical analysis explanations
- Risk assessments

### 📈 **Market Data**
- Real-time stock quotes
- Technical indicators
- Market sentiment analysis
- Historical data

## 🛠️ Tech Stack

### **Frontend**
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Framer Motion** for animations
- **React Query** for state management

### **Backend**
- **FastAPI** with Python
- **MongoDB Atlas** for database
- **Google Gemini Pro** for AI
- **Alpha Vantage** for market data
- **Yahoo Finance** for stock data

### **Deployment**
- **Render** for backend hosting
- **Netlify** for frontend hosting
- **MongoDB Atlas** for database

## 🚀 Quick Start

### **Prerequisites**
- Node.js 18+
- Python 3.9+
- MongoDB Atlas account
- Google Gemini API key
- Alpha Vantage API key

### **Local Development**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/trademate.git
cd trademate
```

2. **Backend Setup**
```bash
cd server
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd ../client
npm install
```

4. **Environment Variables**
```bash
# Backend (.env)
DATABASE_TYPE=mongodb
DATABASE_URL=your_mongodb_atlas_url
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
GEMINI_API_KEY=your_gemini_api_key

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
```

5. **Run the Application**
```bash
# Backend (Terminal 1)
cd server && python3 main.py

# Frontend (Terminal 2)
cd client && npm start
```

6. **Access the Application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🌐 Deployment

### **Backend Deployment (Render)**

1. **Connect to GitHub**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Connect your GitHub repository

2. **Create Web Service**
   - **Name**: trademate-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

3. **Environment Variables**
   ```
   DATABASE_TYPE=mongodb
   DATABASE_URL=your_mongodb_atlas_url
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

### **Frontend Deployment (Netlify)**

1. **Connect to GitHub**
   - Go to [Netlify Dashboard](https://app.netlify.com)
   - Connect your GitHub repository

2. **Build Settings**
   - **Base directory**: `client`
   - **Build command**: `npm run build`
   - **Publish directory**: `build`

3. **Environment Variables**
   ```
   REACT_APP_API_URL=https://your-render-backend-url.onrender.com
   ```

### **Database Setup (MongoDB Atlas)**

1. **Create Cluster**
   - Go to [MongoDB Atlas](https://cloud.mongodb.com)
   - Create a free cluster

2. **Get Connection String**
   - Database → Connect → Connect your application
   - Copy the connection string

3. **Update Environment Variables**
   - Replace `your_mongodb_atlas_url` with your connection string

## 📁 Project Structure

```
trademate/
├── client/                 # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   └── App.tsx        # Main app component
│   └── package.json
├── server/                 # FastAPI backend
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── strategies/        # Trading strategies
│   ├── utils/             # Utility functions
│   └── main.py           # FastAPI app
├── README.md
└── setup.sh              # Setup script
```

## 🔧 API Endpoints

### **Market Data**
- `GET /api/market/quote/{symbol}` - Get stock quote
- `GET /api/market/historical/{symbol}` - Historical data
- `GET /api/market/indicators/{symbol}` - Technical indicators

### **Portfolio**
- `GET /api/portfolio/list` - List portfolios
- `POST /api/portfolio/create` - Create portfolio
- `GET /api/portfolio/{id}` - Get portfolio details

### **Trading Strategies**
- `GET /api/strategies/available` - List strategies
- `POST /api/strategies/backtest` - Run backtest
- `GET /api/strategies/signals/{symbol}` - Get signals

### **AI Insights**
- `POST /api/ai/ask` - Ask AI questions
- `GET /api/ai/trading-advice` - Get trading advice
- `GET /api/ai/risk-assessment/{symbol}` - Risk analysis

## 🎯 Features in Detail

### **Dashboard**
- Portfolio value tracking
- Performance charts
- Market overview
- Recent trades

### **Portfolio Management**
- Multiple portfolios
- Asset allocation
- Performance metrics
- Add/remove assets

### **Trading Strategies**
- Moving Average Crossover
- RSI Strategy
- MACD Strategy
- Backtesting results

### **AI Integration**
- Trading advice
- Technical analysis
- Risk assessment
- Market sentiment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and demonstration purposes only. It is not intended to provide financial advice. Always consult with a qualified financial advisor before making investment decisions.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/trademate/issues) page
2. Create a new issue with detailed information
3. Include your environment and steps to reproduce

## 🚀 Live Demo

- **Frontend**: [https://trademate-demo.netlify.app](https://trademate-demo.netlify.app)
- **Backend API**: [https://trademate-api.onrender.com](https://trademate-api.onrender.com)
- **API Documentation**: [https://trademate-api.onrender.com/docs](https://trademate-api.onrender.com/docs)

---

**Built with ❤️ for the fintech community** 