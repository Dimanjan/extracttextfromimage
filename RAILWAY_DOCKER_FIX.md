# 🔧 Railway Docker Build Fix

**Issue**: Docker build failing due to outdated package names in Debian

## 🚀 Quick Fix Options

### Option 1: Use Railway's Auto-Detection (Recommended)
Railway can auto-detect your Flask app without Docker:

1. **Delete Dockerfile** (Railway will use auto-detection)
2. **Keep Procfile**: `web: python api.py`
3. **Keep requirements_api.txt**
4. **Deploy normally**

### Option 2: Use Simplified Dockerfile
Use the updated Dockerfile with minimal dependencies:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy application
COPY . .

# Set environment variables
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "api.py"]
```

### Option 3: Use Alternative Base Image
Use Ubuntu base image (more stable):

```dockerfile
FROM ubuntu:22.04

WORKDIR /app

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip tesseract-ocr \
    libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

# Create python symlink
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install requirements
COPY requirements_api.txt .
RUN pip3 install --no-cache-dir -r requirements_api.txt

# Copy application
COPY . .

# Set environment variables
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
CMD ["python", "api.py"]
```

## 🎯 Recommended Solution

**Use Option 1** (Auto-detection):

1. **Delete Dockerfile**:
   ```bash
   rm Dockerfile
   ```

2. **Keep these files**:
   - `Procfile`: `web: python api.py`
   - `requirements_api.txt`: All dependencies
   - `api.py`: Your Flask app

3. **Deploy to Railway**:
   - Railway will auto-detect Python/Flask
   - Install dependencies automatically
   - Use your Procfile for startup

## 🚀 Deployment Steps

### 1. Remove Dockerfile (if using auto-detection)
```bash
rm Dockerfile
```

### 2. Deploy to Railway
- Go to [railway.app](https://railway.app)
- Connect your GitHub repo
- Railway will auto-detect Flask
- Deploy automatically

### 3. Add Environment Variables
In Railway dashboard:
```
OMP_NUM_THREADS=1
MKL_NUM_THREADS=1
PYTHONUNBUFFERED=1
```

## 📊 Why Auto-Detection Works Better

- ✅ **No Docker issues**: Railway handles the environment
- ✅ **Automatic optimization**: Railway optimizes for Python
- ✅ **Easier deployment**: No Docker configuration needed
- ✅ **Better performance**: Railway's optimized Python environment
- ✅ **Automatic scaling**: Railway handles resource management

## 🔧 If You Must Use Docker

Use the simplified Dockerfile with minimal dependencies:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY . .

ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
CMD ["python", "api.py"]
```

## 🎉 Expected Results

After fixing:
- ✅ **Build succeeds**: No package errors
- ✅ **API deploys**: Railway starts your app
- ✅ **Health check passes**: `/health` endpoint works
- ✅ **Text extraction works**: 75%+ accuracy maintained

---

**Recommendation**: Use Railway's auto-detection (delete Dockerfile) for easiest deployment! 🚀
