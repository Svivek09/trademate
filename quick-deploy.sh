#!/bin/bash

echo "🚀 Quick Deploy to Render..."

# Check if we have a Render account
echo "📋 Prerequisites:"
echo "1. Create account at https://render.com"
echo "2. Get API key from https://dashboard.render.com/account/tokens"
echo "3. Create a new Web Service manually first time"
echo ""

# Get API key
read -p "Enter your Render API key: " RENDER_TOKEN

if [ -z "$RENDER_TOKEN" ]; then
    echo "❌ No API key provided. Exiting."
    exit 1
fi

# Get service ID
read -p "Enter your Render service ID: " RENDER_SERVICE_ID

if [ -z "$RENDER_SERVICE_ID" ]; then
    echo "❌ No service ID provided. Exiting."
    exit 1
fi

echo "📤 Triggering deployment..."
curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
  -H "Authorization: Bearer $RENDER_TOKEN" \
  -H "Content-Type: application/json"

echo ""
echo "✅ Deployment triggered!"
echo "🌐 Check your Render dashboard for status"
echo "📊 Monitor at: https://dashboard.render.com" 