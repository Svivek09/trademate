#!/bin/bash

echo "🚀 Deploying TradeMate to Render..."

# Check if we have the necessary environment variables
if [ -z "$RENDER_TOKEN" ]; then
    echo "❌ RENDER_TOKEN not set. Please set it first:"
    echo "export RENDER_TOKEN=your_render_token"
    echo "Get your token from: https://dashboard.render.com/account/tokens"
    exit 1
fi

if [ -z "$RENDER_SERVICE_ID" ]; then
    echo "❌ RENDER_SERVICE_ID not set. Please set it first:"
    echo "export RENDER_SERVICE_ID=your_service_id"
    echo "Get your service ID from your Render dashboard"
    exit 1
fi

# Trigger deployment
echo "📤 Triggering deployment..."
curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_TOKEN" \
  -H "Content-Type: application/json"

echo "✅ Deployment triggered! Check your Render dashboard for status."
echo "🌐 Your app will be available at: https://your-app-name.onrender.com" 