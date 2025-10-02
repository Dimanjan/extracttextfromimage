# 📚 OCR.space API Documentation

**Complete guide to using OCR.space API for text extraction from images**

## 🎯 Overview

OCR.space is a powerful OCR (Optical Character Recognition) API service that extracts text from images. It's fast, reliable, and offers both free and premium tiers.

## 🔑 Getting Started

### 1. Get Your API Key
1. Visit [OCR.space](https://ocr.space/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes 25,000 requests per month

### 2. API Endpoint
```
https://api.ocr.space/parse/image
```

### 3. Authentication
Include your API key in the request header:
```
apikey: YOUR_API_KEY
```

## 📋 API Methods

### Method 1: File Upload (Recommended)
Upload image files directly to the API.

**Request:**
```bash
curl -X POST \
  https://api.ocr.space/parse/image \
  -H "apikey: YOUR_API_KEY" \
  -F "file=@image.jpg"
```

**Python Example:**
```python
import requests

def extract_text_with_ocrspace(image_path, api_key):
    url = "https://api.ocr.space/parse/image"
    headers = {"apikey": api_key}
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get('IsErroredOnProcessing', False):
            return result['ParsedResults'][0]['ParsedText']
    return None

# Usage
api_key = "YOUR_API_KEY"
text = extract_text_with_ocrspace("image.jpg", api_key)
print(text)
```

### Method 2: Base64 Encoding
Send base64 encoded image data.

**Python Example:**
```python
import requests
import base64

def extract_text_base64(image_path, api_key):
    url = "https://api.ocr.space/parse/image"
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    
    # Convert image to base64
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_data = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        "base64Image": f"data:image/jpeg;base64,{base64_data}",
        "language": "eng",
        "isOverlayRequired": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get('IsErroredOnProcessing', False):
            return result['ParsedResults'][0]['ParsedText']
    return None
```

### Method 3: Image URL
Process images from URLs.

**Python Example:**
```python
def extract_text_from_url(image_url, api_key):
    url = f"https://api.ocr.space/parse/imageurl"
    headers = {"apikey": api_key}
    
    payload = {
        "url": image_url,
        "language": "eng"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get('IsErroredOnProcessing', False):
            return result['ParsedResults'][0]['ParsedText']
    return None
```

## 📊 Response Format

### Success Response
```json
{
  "ParsedResults": [
    {
      "ParsedText": "Extracted text content",
      "ErrorMessage": "",
      "ErrorDetails": ""
    }
  ],
  "OCRExitCode": 1,
  "IsErroredOnProcessing": false,
  "ProcessingTimeInMilliseconds": "1171",
  "SearchablePDFURL": ""
}
```

### Error Response
```json
{
  "IsErroredOnProcessing": true,
  "ErrorMessage": "Error description",
  "OCRExitCode": 0
}
```

## 🔧 Advanced Parameters

### Language Support
```python
payload = {
    "language": "eng",  # English
    # Other options: "ara", "chi_sim", "chi_tra", "deu", "fra", "jpn", "kor", "spa"
}
```

### Overlay Generation
```python
payload = {
    "isOverlayRequired": True,  # Generate overlay image
    "overlayType": "hocr"       # or "xml"
}
```

### File Type Specification
```python
payload = {
    "filetype": "jpg",  # Specify file type
    "detectOrientation": True
}
```

## 📈 Performance Metrics

Based on our testing with furniture catalog images:

| Metric | Value |
|--------|-------|
| **Processing Time** | 0.6-1.2 seconds |
| **Success Rate** | 100% |
| **Text Accuracy** | Good for simple layouts |
| **File Size Limit** | 10MB (free tier) |
| **Rate Limit** | 25,000 requests/month (free) |

## 🎯 Use Cases

### ✅ Best For:
- **Document Processing**: Invoices, receipts, forms
- **Product Catalogs**: Furniture, electronics, books
- **Simple Layouts**: Clean, structured text
- **Quick Processing**: Fast turnaround needs
- **Basic OCR**: Standard text extraction

### ❌ Not Ideal For:
- **Complex Graphics**: Scattered, varying-sized text
- **Handwriting**: Cursive or messy handwriting
- **Low-Quality Images**: Blurry or distorted text
- **Multi-Language**: Mixed language documents
- **High Accuracy**: Critical text extraction

## 💰 Pricing

### Free Tier
- **25,000 requests/month**
- **10MB file size limit**
- **Basic OCR features**

### Premium Plans
- **Higher limits**
- **Advanced features**
- **Priority processing**
- **Custom models**

## 🚀 Complete Example

```python
#!/usr/bin/env python3
"""
Complete OCR.space API implementation
"""

import requests
import json
import os
from pathlib import Path

class OCRSpaceAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ocr.space/parse/image"
    
    def extract_text(self, image_path, language="eng", overlay=False):
        """Extract text from image file"""
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        headers = {"apikey": self.api_key}
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {
                'language': language,
                'isOverlayRequired': overlay
            }
            
            response = requests.post(
                self.base_url, 
                headers=headers, 
                files=files, 
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('IsErroredOnProcessing', False):
                raise Exception(f"OCR Error: {result.get('ErrorMessage', 'Unknown error')}")
            
            if 'ParsedResults' in result and result['ParsedResults']:
                return {
                    'text': result['ParsedResults'][0]['ParsedText'],
                    'processing_time': result.get('ProcessingTimeInMilliseconds', 0),
                    'success': True
                }
        
        return {'success': False, 'text': ''}
    
    def extract_text_base64(self, image_path, language="eng"):
        """Extract text using base64 encoding"""
        
        import base64
        
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
        
        headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "base64Image": f"data:image/jpeg;base64,{base64_data}",
            "language": language,
            "isOverlayRequired": False
        }
        
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('IsErroredOnProcessing', False):
                raise Exception(f"OCR Error: {result.get('ErrorMessage', 'Unknown error')}")
            
            if 'ParsedResults' in result and result['ParsedResults']:
                return {
                    'text': result['ParsedResults'][0]['ParsedText'],
                    'processing_time': result.get('ProcessingTimeInMilliseconds', 0),
                    'success': True
                }
        
        return {'success': False, 'text': ''}

# Usage Example
def main():
    # Initialize API
    api_key = "YOUR_API_KEY"
    ocr = OCRSpaceAPI(api_key)
    
    # Test with image
    image_path = "sample_image.jpg"
    
    try:
        # Method 1: File upload
        result = ocr.extract_text(image_path)
        
        if result['success']:
            print(f"✅ Text extracted successfully!")
            print(f"⏱️  Processing time: {result['processing_time']}ms")
            print(f"📄 Extracted text:")
            print(result['text'])
        else:
            print("❌ Text extraction failed")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## 🔍 Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `IsErroredOnProcessing: true` | Image processing failed | Check image format and quality |
| `Unable to recognize file type` | Unsupported format | Use JPG, PNG, or PDF |
| `File too large` | Exceeds size limit | Compress image or upgrade plan |
| `Rate limit exceeded` | Too many requests | Wait or upgrade plan |

### Error Handling Example
```python
def safe_extract_text(api_key, image_path):
    try:
        ocr = OCRSpaceAPI(api_key)
        result = ocr.extract_text(image_path)
        
        if result['success']:
            return result['text']
        else:
            return "No text detected"
    
    except FileNotFoundError:
        return "Image file not found"
    
    except Exception as e:
        return f"OCR Error: {str(e)}"
```

## 📊 Testing Results

Based on our testing with furniture catalog images:

### Image 1: Bed & Bench
- **Processing Time**: 1,171ms
- **Characters**: 69
- **Words**: 10
- **Text**: "12. ASHWI FURNITURE BED BENCH Rs. 17000/- 55 Ashwi Furniture"

### Image 2: Butterfly Sofa
- **Processing Time**: 1,187ms
- **Characters**: 167
- **Words**: 28
- **Text**: "07. BUTTERFLY SOFA Rs. 17000/- ASHWI FURNITURE Hugged by comfort, Ashwi Furniture wrapped in style..."

## 🎯 Best Practices

### 1. Image Preparation
- Use high-quality images (300+ DPI)
- Ensure good contrast between text and background
- Avoid blurry or distorted images
- Use standard formats (JPG, PNG, PDF)

### 2. API Usage
- Implement proper error handling
- Use appropriate timeouts (30+ seconds)
- Cache results when possible
- Monitor rate limits

### 3. Text Processing
- Clean extracted text (remove extra spaces, newlines)
- Validate important information
- Handle multiple languages if needed
- Store results efficiently

## 🔗 Resources

- **Official Website**: [OCR.space](https://ocr.space/)
- **API Documentation**: [OCR.space API Docs](https://ocr.space/ocrapi)
- **Support Forum**: [OCR.space Forum](https://ocr.space/forum/)
- **Pricing**: [OCR.space Pricing](https://ocr.space/pricing)

## 📞 Support

- **Free Support**: Community forum
- **Premium Support**: Email and phone support
- **Documentation**: Comprehensive API docs
- **Examples**: Code samples and tutorials

---

**OCR.space API Documentation**  
*Complete guide for text extraction from images*  
*Last updated: October 2025*
