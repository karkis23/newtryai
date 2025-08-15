# 🤖 AI Model Deployment Guide - Render.com Compatible

## 📋 Overview

This guide provides step-by-step instructions for deploying the AI trading model on Render.com with a lightweight, dependency-free implementation.

## 🔧 Fixed Deployment Issues

### Problem Solved
The original deployment failed due to pandas compilation issues on Render.com's Python 3.13 environment. The solution removes heavy dependencies while maintaining full functionality.

### Changes Made
- **Removed pandas**: Eliminated the problematic dependency
- **Removed numpy**: Simplified to pure Python implementation
- **Kept Flask**: Lightweight web framework for API endpoints
- **Added Gunicorn**: Production WSGI server

## 🚀 Deployment Steps

### 1. Render.com Setup

1. **Create Render Account**: Go to https://render.com and sign up
2. **Connect GitHub**: Link your GitHub repository
3. **Create Web Service**: 
   - Click "New" → "Web Service"
   - Connect your repository
   - Select the repository containing the backend folder

### 2. Render Configuration

#### Build Settings:
- **Environment**: Python 3
- **Build Command**: `pip install -r backend/requirements_fixed.txt`
- **Start Command**: `cd backend && gunicorn ai_model_api_fixed:app`
- **Root Directory**: Leave empty (or set to backend if needed)

#### Environment Variables:
```bash
PYTHON_VERSION=3.11.0
PORT=10000
```

### 3. File Structure

Ensure your repository has this structure:
```
your-repo/
├── backend/
│   ├── ai_model_api_fixed.py
│   └── requirements_fixed.txt
└── other-files...
```

### 4. Deployment Process

1. **Push to GitHub**: Commit and push your changes
2. **Deploy on Render**: 
   - Go to your Render dashboard
   - Click "Deploy latest commit"
   - Monitor build logs for any issues

### 5. Testing Deployment

Once deployed, test your API:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test prediction
curl -X POST https://your-app-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "rsi": 30,
    "momentum": 2.5,
    "volumeRatio": 1.8,
    "vix": 15,
    "sentiment": "BULLISH",
    "writersZone": "BULLISH"
  }'
```

## 🎯 API Endpoints

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "model_loaded": true,
  "total_signals": 0,
  "accuracy": 0.0
}
```

### 2. Signal Prediction
```http
POST /predict
Content-Type: application/json

{
  "rsi": 35,
  "macd": {"macd": 1.2, "signal": 0.8, "histogram": 0.4},
  "momentum": 1.8,
  "volumeRatio": 1.4,
  "vix": 16,
  "sentiment": "BULLISH",
  "writersZone": "BULLISH",
  "candlePattern": "HAMMER"
}
```

**Response:**
```json
{
  "signal": "BUY_CE",
  "confidence": 0.85,
  "analysis": {
    "detected_signals": ["RSI_OVERSOLD", "MOMENTUM_STRONG_BULLISH", "VOLUME_SURGE"],
    "total_strength": 2.3,
    "vix_condition": "NORMAL_VOLATILITY",
    "market_regime": "BULLISH_TREND"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. Update Model Accuracy
```http
POST /update_accuracy
Content-Type: application/json

{
  "predicted_signal": "BUY_CE",
  "actual_outcome": "correct"
}
```

### 4. Get Statistics
```http
GET /get_stats
```

## 🔧 Integration with n8n

### Update n8n AI Node Configuration

In your n8n workflow, update the AI Trade Confirmation node:

1. **URL**: `https://your-app-name.onrender.com/predict`
2. **Headers**:
   ```json
   {
     "Content-Type": "application/json"
   }
   ```
3. **Body**: Include all technical indicators and market data

### Environment Variable in n8n
```bash
AI_MODEL_URL=https://your-app-name.onrender.com
```

## 🚨 Troubleshooting

### Common Issues

#### Build Fails
- Check Python version compatibility
- Verify requirements.txt is correct
- Check file paths and structure

#### App Crashes
- Check logs in Render dashboard
- Verify environment variables
- Test locally first

#### Slow Response
- Render free tier has cold starts
- Consider upgrading to paid tier for better performance

### Performance Optimization

#### For Production:
1. **Upgrade to Paid Plan**: Eliminates cold starts
2. **Add Health Checks**: Keep service warm
3. **Enable Auto-Deploy**: Automatic deployments from GitHub
4. **Monitor Performance**: Use Render's monitoring tools

## 🎯 Alternative Deployment Options

If Render.com still has issues, consider these alternatives:

### 1. Heroku
```bash
# Procfile
web: cd backend && gunicorn ai_model_api_fixed:app
```

### 2. Railway
- Similar setup to Render
- Often better Python support
- Easy GitHub integration

### 3. PythonAnywhere
- Python-focused hosting
- Good for simple Flask apps
- Free tier available

### 4. Local Deployment
If cloud deployment continues to fail, you can run locally:

```bash
cd backend
pip install -r requirements_fixed.txt
python ai_model_api_fixed.py
```

Then use `http://localhost:5000` as your AI_MODEL_URL in n8n.

This simplified AI model maintains all the professional trading logic while being compatible with cloud deployment platforms.