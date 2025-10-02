# 🚀 Railway Deployment Guide

**Deploy your Image Text Extraction API to Railway in minutes!**

## �� Why Railway?

- ✅ **$5 free credits/month** (usually enough for your API)
- ✅ **512MB RAM** (sufficient for your API)
- ✅ **No CPU time limits**
- ✅ **Easiest deployment** (just connect GitHub)
- ✅ **Automatic HTTPS** and custom domains
- ✅ **Auto-scaling** and monitoring

## 📋 Prerequisites

- ✅ Your code is already on GitHub: `https://github.com/Dimanjan/extracttextfromimage.git`
- ✅ All deployment files are ready
- ✅ API is tested and working

## 🚀 Step-by-Step Deployment

### Step 1: Go to Railway
1. **Visit**: [railway.app](https://railway.app)
2. **Sign up** with your GitHub account
3. **Authorize** Railway to access your repositories

### Step 2: Create New Project
1. **Click** "New Project"
2. **Select** "Deploy from GitHub repo"
3. **Find** your repository: `Dimanjan/extracttextfromimage`
4. **Click** "Deploy Now"

### Step 3: Railway Auto-Configuration
Railway will automatically:
- ✅ **Detect** it's a Flask app
- ✅ **Install** dependencies from `requirements_api.txt`
- ✅ **Set** environment variables
- ✅ **Deploy** your API

### Step 4: Configure Environment Variables
In Railway dashboard, add these environment variables:

```
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
PYTHONUNBUFFERED=1
```

### Step 5: Deploy!
1. **Click** "Deploy"
2. **Wait** for deployment to complete (2-5 minutes)
3. **Get** your API URL (e.g., `https://your-app.railway.app`)

## 🧪 Test Your Deployed API

### Health Check
```bash
curl https://your-app.railway.app/health
```

### API Info
```bash
curl https://your-app.railway.app/info
```

### Extract Text (using your sample images)
```bash
# Download a sample image first
curl -X POST -F "file=@image.jpg" https://your-app.railway.app/extract
```

## 📊 Expected Performance

### Resource Usage:
- **Memory**: ~2GB (might need optimization)
- **CPU**: 30-60 seconds per image
- **Storage**: Temporary files cleaned automatically

### Railway Limits:
- **$5 credits/month** (usually enough for 100+ images)
- **512MB RAM** (might need optimization)
- **No CPU limits** (unlimited processing)

## 🔧 Optimization for Railway

### Memory Optimization:
If you hit memory limits, add these to your API:

```python
# In api.py, add at the top
import os
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
```

### CPU Optimization:
```python
# Use CPU-only mode for EasyOCR
reader = easyocr.Reader(['en'], gpu=False)
```

## 📈 Monitoring Your API

### Railway Dashboard:
- **Logs**: Real-time application logs
- **Metrics**: CPU, memory, network usage
- **Deployments**: Automatic deployments from GitHub
- **Settings**: Environment variables and configuration

### Health Monitoring:
- **GET /health**: Basic health check
- **GET /info**: API capabilities and status

## 🚀 Advanced Configuration

### Custom Domain:
1. **Go to** Railway dashboard
2. **Click** on your project
3. **Go to** Settings → Domains
4. **Add** your custom domain
5. **Configure** DNS records

### Environment Variables:
```
# Performance optimization
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
PYTHONUNBUFFERED=1

# API configuration
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🐛 Troubleshooting

### Common Issues:

**"Out of memory" error**:
- Add memory optimization environment variables
- Reduce image size limits
- Use CPU-only mode for EasyOCR

**"Deployment failed"**:
- Check Railway logs
- Verify all dependencies are in requirements_api.txt
- Ensure Tesseract is available

**"API not responding"**:
- Check health endpoint: `/health`
- Verify environment variables
- Check Railway logs for errors

### Debug Commands:
```bash
# Check API health
curl https://your-app.railway.app/health

# Check API info
curl https://your-app.railway.app/info

# Test with sample image
curl -X POST -F "file=@test.jpg" https://your-app.railway.app/extract
```

## 📊 Cost Estimation

### Railway Pricing:
- **Free tier**: $5 credits/month
- **Your API usage**: ~$2-3/month (estimated)
- **Remaining credits**: $2-3 for other projects

### Usage Calculation:
- **100 images/month**: ~$2
- **500 images/month**: ~$4
- **1000+ images/month**: Consider upgrading

## 🎉 Success!

Once deployed, you'll have:
- ✅ **Live API** at `https://your-app.railway.app`
- ✅ **Automatic HTTPS** and security
- ✅ **Auto-deployments** from GitHub
- ✅ **Monitoring** and logs
- ✅ **Custom domain** support

## 📞 Support

If you encounter issues:
1. **Check Railway logs** in dashboard
2. **Verify environment variables**
3. **Test locally** first
4. **Contact Railway support** if needed

---

**Ready to deploy?** Go to [railway.app](https://railway.app) and deploy your API! ��
