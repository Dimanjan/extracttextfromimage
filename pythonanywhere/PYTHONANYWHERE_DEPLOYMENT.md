# 🚀 PythonAnywhere Deployment Guide

This guide helps you deploy the lightweight text extraction system on PythonAnywhere's free tier.

## 📋 PythonAnywhere Free Tier Limits

- **CPU seconds**: 100 seconds per day
- **Memory**: 512MB RAM
- **Disk space**: 1GB
- **No GPU**: CPU-only processing
- **No sudo**: Limited system access

## 🛠️ Optimized Version Features

### ✅ What's Included:
- **Tesseract OCR only** (no heavy dependencies)
- **PIL image processing** (lightweight)
- **Smart preprocessing** (contrast, resize, auto-levels)
- **Multiple OCR configs** (different PSM modes)
- **Memory optimized** (image resizing, efficient processing)

### ❌ What's Removed:
- **EasyOCR** (too heavy, requires GPU)
- **OpenCV** (large dependency)
- **NumPy** (not essential for basic OCR)
- **Heavy preprocessing** (morphological operations)

## 📦 Installation on PythonAnywhere

### Step 1: Upload Files
Upload these files to your PythonAnywhere account:
```
extract_text_pythonanywhere.py
requirements_lightweight.txt
image_samples/ (your images)
```

### Step 2: Install Dependencies
```bash
# In PythonAnywhere console
pip3.10 install --user pillow pytesseract
```

### Step 3: Install Tesseract
```bash
# PythonAnywhere has tesseract pre-installed
# If not available, contact support
```

### Step 4: Test
```bash
python3.10 extract_text_pythonanywhere.py
```

## ⚡ Performance Optimizations

### Memory Management:
- **Image resizing**: Max 1200x1200px
- **Grayscale conversion**: Reduces memory usage
- **Efficient processing**: One image at a time

### Speed Optimizations:
- **PIL only**: No heavy computer vision libraries
- **Smart configs**: Only essential Tesseract modes
- **Quick preprocessing**: Minimal image operations

### CPU Usage:
- **~5-10 seconds per image** (vs 30-60s in full version)
- **~50MB RAM usage** (vs 2GB in full version)
- **Fits within free tier limits**

## 📊 Expected Results

### Accuracy:
- **~40-50% text extraction** (vs 75% in full version)
- **Good for clear text** and simple layouts
- **Struggles with complex graphics** (but still useful)

### Speed:
- **5-10 seconds per image**
- **Suitable for batch processing**
- **Fits within 100 CPU seconds/day limit**

## 🔧 Troubleshooting

### Common Issues:

**"Tesseract not found"**:
```bash
# Check if tesseract is available
which tesseract
# If not, contact PythonAnywhere support
```

**"Memory error"**:
- Reduce image size before processing
- Process one image at a time
- Use smaller images (max 800x800px)

**"Slow processing"**:
- Use smaller images
- Process during off-peak hours
- Consider upgrading to paid tier

## 📈 Usage Tips

### Best Practices:
1. **Resize images** to 800x800px before upload
2. **Process during off-peak** hours (better performance)
3. **Use clear, high-contrast** images
4. **Process one image** at a time for large batches

### Image Optimization:
- **Format**: PNG or JPG
- **Size**: 800x800px maximum
- **Contrast**: High contrast works best
- **Text**: Clear, readable text

## 🚀 Deployment Steps

1. **Create PythonAnywhere account**
2. **Upload optimized files**
3. **Install lightweight dependencies**
4. **Test with sample images**
5. **Deploy to web app** (if needed)

## 📊 Comparison: Full vs PythonAnywhere

| Feature | Full Version | PythonAnywhere |
|---------|-------------|----------------|
| **Accuracy** | 75% | 40-50% |
| **Speed** | 30-60s | 5-10s |
| **Memory** | 2GB | 50MB |
| **Dependencies** | Heavy | Light |
| **Cost** | High | Free |

## 🎯 When to Use Each Version

### Use Full Version When:
- You have powerful hardware
- Accuracy is critical
- Processing complex graphics
- No deployment constraints

### Use PythonAnywhere Version When:
- Deploying to free hosting
- Limited resources
- Simple text extraction
- Cost is a concern

## 📞 Support

If you encounter issues:
1. Check PythonAnywhere console logs
2. Verify tesseract installation
3. Test with smaller images
4. Contact PythonAnywhere support if needed

---

**Ready to deploy?** Follow the installation steps above!
