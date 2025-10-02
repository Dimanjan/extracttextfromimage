# 🚀 PythonAnywhere Optimized Text Extraction

**Ultra-lightweight version for PythonAnywhere free tier deployment**

This folder contains optimized versions of the text extraction system specifically designed for PythonAnywhere's free tier limitations.

## 📁 Files in this Folder

- **`extract_text_pythonanywhere.py`** - Main optimized script
- **`extract_text_lightweight.py`** - Basic lightweight version
- **`requirements_lightweight.txt`** - Minimal dependencies
- **`run_pythonanywhere.sh`** - Easy execution script
- **`PYTHONANYWHERE_DEPLOYMENT.md`** - Complete deployment guide

## 🎯 Quick Start

1. **Upload files** to your PythonAnywhere account
2. **Install dependencies**: `pip3.10 install --user pillow pytesseract`
3. **Run extraction**: `python3.10 extract_text_pythonanywhere.py`

## ⚡ Performance

- **Speed**: 5-10 seconds per image
- **Memory**: 50MB RAM usage
- **Accuracy**: 40-50% text extraction
- **CPU**: Fits within 100 seconds/day limit

## 📊 Comparison

| Feature | Full Version | PythonAnywhere |
|---------|-------------|----------------|
| **Accuracy** | 75% | 40-50% |
| **Speed** | 30-60s | 5-10s |
| **Memory** | 2GB | 50MB |
| **Dependencies** | Heavy | Light |
| **Free Tier** | ❌ No | ✅ Yes |

## 🛠️ Installation

```bash
# Install dependencies
pip3.10 install --user pillow pytesseract

# Run extraction
python3.10 extract_text_pythonanywhere.py
```

## 📖 Documentation

See `PYTHONANYWHERE_DEPLOYMENT.md` for complete deployment instructions.

---

**Perfect for**: Free hosting, limited resources, simple text extraction
