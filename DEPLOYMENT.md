# 🚀 TradeMate Deployment Guide

## Quick Deploy Options

### Option 1: Render Dashboard (Recommended)
1. Go to https://dashboard.render.com
2. Connect your GitHub repository: `Svivek09/trademate`
3. Create new **Web Service**
4. Configure:
   - **Name**: `trademate-backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Root Directory**: `server`

### Option 2: Render CLI
```bash
# Install Render CLI
brew install render

# Login to Render
render login

# Deploy
render deploy
```

### Option 3: Manual Deployment Script
```bash
# Set your Render credentials
export RENDER_TOKEN=your_token_here
export RENDER_SERVICE_ID=your_service_id_here

# Run deployment
./deploy-render.sh
```

## Environment Variables

Set these in your Render dashboard:

```
DATABASE_TYPE=mongodb
DATABASE_URL=your_mongodb_atlas_url
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
GEMINI_API_KEY=your_gemini_api_key
```

## Frontend Deployment (Netlify)

1. Go to https://app.netlify.com
2. Connect GitHub repository
3. Configure:
   - **Base directory**: `client`
   - **Build command**: `npm run build`
   - **Publish directory**: `build`
4. Set environment variable:
   - `REACT_APP_API_URL`: Your Render backend URL

## Troubleshooting

### Build Errors
If you get build errors, try using the minimal requirements:
```bash
# In render.yaml, change:
buildCommand: pip install -r requirements-minimal.txt
```

### Database Issues
- Ensure MongoDB Atlas is properly configured
- Check connection string format
- Verify network access settings

## URLs After Deployment

- **Backend**: `https://your-app-name.onrender.com`
- **Frontend**: `https://your-app-name.netlify.app`
- **API Docs**: `https://your-app-name.onrender.com/docs`

## Support

If deployment fails:
1. Check Render logs for specific errors
2. Verify all environment variables are set
3. Ensure GitHub repository is public or connected properly 