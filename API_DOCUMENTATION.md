# 🚀 Image Text Extraction API

**Production-ready REST API for extracting text from images**

## 🎯 Overview

This API provides a simple, powerful interface to extract text from images using advanced OCR technology. Perfect for integrating text extraction into your applications.

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements_api.txt

# Run the API
python api.py
```

### Basic Usage
```bash
# Health check
curl http://localhost:5000/health

# Extract text from image
curl -X POST -F "file=@image.jpg" http://localhost:5000/extract
```

## 📡 API Endpoints

### 1. Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-02T12:00:00",
  "version": "1.0.0"
}
```

### 2. Extract Text (Single Image)
**POST** `/extract`

Extract text from a single image.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: `file` (image file)

**Response:**
```json
{
  "success": true,
  "file_id": "uuid-string",
  "original_filename": "image.jpg",
  "extracted_text": [
    "1. ASHWI FURNITURE BUTTERFLY SOFA 3.0 Rs 17000/",
    "2. Hugged by comfort, wrapped in style",
    "3. height: 34 inch width: 32 inch length: 7.4 ft"
  ],
  "metadata": {
    "text_length": 150,
    "word_count": 25,
    "sentence_count": 3,
    "has_text": true,
    "processing_time": 45.2
  },
  "timestamp": "2025-10-02T12:00:00"
}
```

### 3. Extract Text (Batch)
**POST** `/extract/batch`

Extract text from multiple images.

**Request:**
- **Content-Type**: `multipart/form-data`
- **Body**: `files` (multiple image files)

**Response:**
```json
{
  "success": true,
  "total_files": 2,
  "results": [
    {
      "file_id": "uuid-1",
      "original_filename": "image1.jpg",
      "extracted_text": ["Text from image 1"],
      "metadata": { ... }
    },
    {
      "file_id": "uuid-2", 
      "original_filename": "image2.jpg",
      "extracted_text": ["Text from image 2"],
      "metadata": { ... }
    }
  ],
  "timestamp": "2025-10-02T12:00:00"
}
```

### 4. API Information
**GET** `/info`

Get API capabilities and information.

**Response:**
```json
{
  "name": "Image Text Extraction API",
  "version": "1.0.0",
  "description": "Extract text from images using advanced OCR",
  "capabilities": {
    "single_image": true,
    "batch_processing": true,
    "supported_formats": ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "tif"],
    "max_file_size": "16MB",
    "accuracy": "75%+"
  },
  "endpoints": {
    "POST /extract": "Extract text from single image",
    "POST /extract/batch": "Extract text from multiple images",
    "GET /health": "Health check",
    "GET /info": "API information"
  }
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set Flask environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Optional: Set custom port
export PORT=5000
```

### File Limits
- **Max file size**: 16MB
- **Supported formats**: PNG, JPG, JPEG, GIF, BMP, TIFF, TIF
- **Concurrent requests**: Limited by server resources

## 📊 Performance

### Accuracy
- **75%+ text extraction** from complex images
- **Scattered text detection** in graphic designs
- **Multiple font support** and varying sizes

### Speed
- **30-60 seconds** per image (varies by complexity)
- **Batch processing** for multiple images
- **Concurrent processing** support

### Resource Usage
- **Memory**: 2GB+ RAM recommended
- **CPU**: Multi-core processing
- **Storage**: Temporary files cleaned automatically

## 🛠️ Integration Examples

### Python Client
```python
import requests

# Single image
with open('image.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/extract',
        files={'file': f}
    )
    result = response.json()
    print(result['extracted_text'])

# Batch processing
files = [('files', open('image1.jpg', 'rb')), 
         ('files', open('image2.jpg', 'rb'))]
response = requests.post(
    'http://localhost:5000/extract/batch',
    files=files
)
```

### JavaScript Client
```javascript
// Single image
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/extract', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.extracted_text));

// Batch processing
const formData = new FormData();
for (let file of fileInput.files) {
    formData.append('files', file);
}

fetch('http://localhost:5000/extract/batch', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data.results));
```

### cURL Examples
```bash
# Single image
curl -X POST -F "file=@image.jpg" http://localhost:5000/extract

# Batch processing
curl -X POST -F "files=@image1.jpg" -F "files=@image2.jpg" http://localhost:5000/extract/batch

# Health check
curl http://localhost:5000/health

# API info
curl http://localhost:5000/info
```

## 🐛 Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "error": "No file provided",
  "message": "Please provide an image file"
}
```

**413 Payload Too Large:**
```json
{
  "error": "File too large",
  "message": "Maximum file size is 16MB"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Processing failed",
  "message": "OCR processing error details",
  "timestamp": "2025-10-02T12:00:00"
}
```

## 🚀 Deployment

### Development
```bash
python api.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements_api.txt .
RUN pip install -r requirements_api.txt

COPY . .
EXPOSE 5000

CMD ["python", "api.py"]
```

## 📈 Monitoring

### Health Checks
- **GET /health** - Basic health check
- **GET /info** - API capabilities and status

### Logging
- Request/response logging
- Error tracking
- Performance metrics

## 🔒 Security

### File Validation
- File type validation
- File size limits
- Secure filename handling

### Input Sanitization
- Filename sanitization
- Content type validation
- Temporary file cleanup

## 📞 Support

For issues or questions:
1. Check the health endpoint: `GET /health`
2. Review error messages in responses
3. Check server logs for detailed errors
4. Ensure Tesseract is properly installed

---

**Ready to extract text from images?** Start the API and begin processing!
