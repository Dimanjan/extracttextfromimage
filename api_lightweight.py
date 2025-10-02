#!/usr/bin/env python3
"""
Lightweight Image Text Extraction API for Railway
Optimized for Railway's build limits and free tier
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import uuid
import re

# Set environment variables for Railway optimization
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['PYTHONUNBUFFERED'] = '1'

try:
    from PIL import Image, ImageEnhance, ImageOps
    import pytesseract
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Please install: pip install pillow pytesseract")
    sys.exit(1)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4MB max file size (reduced for Railway)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def setup_tesseract():
    """Setup tesseract path for Railway"""
    possible_paths = [
        '/usr/bin/tesseract',
        '/usr/local/bin/tesseract'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    
    return False

def optimize_image_for_ocr(image_path):
    """Lightweight image optimization using PIL only"""
    try:
        # Open and convert to RGB
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (Railway memory limit)
        width, height = img.size
        if width > 600 or height > 600:  # Smaller limit for Railway
            ratio = min(600/width, 600/height)
            new_size = (int(width * ratio), int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to grayscale
        gray = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(1.5)
        
        # Auto-adjust levels
        auto_levels = ImageOps.autocontrast(enhanced)
        
        return auto_levels
        
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return None

def extract_text_lightweight(image_path):
    """Lightweight text extraction using Tesseract only"""
    try:
        # Optimize image
        optimized_img = optimize_image_for_ocr(image_path)
        if optimized_img is None:
            return []
        
        # Try multiple Tesseract configurations
        configs = [
            ('psm6', '--psm 6'),      # Uniform block
            ('psm7', '--psm 7'),      # Single text line
            ('psm8', '--psm 8'),      # Single word
            ('psm13', '--psm 13'),    # Raw line
        ]
        
        all_results = []
        
        for config_name, config in configs:
            try:
                text = pytesseract.image_to_string(optimized_img, config=config)
                if text and text.strip():
                    all_results.append((config_name, text.strip()))
            except Exception as e:
                print(f"    {config_name} failed: {e}")
                continue
        
        # Combine and clean results
        combined_text = []
        seen_texts = set()
        
        for config_name, text in all_results:
            # Clean the text
            cleaned = re.sub(r'[^\w\s\.\,\:\-\@\#\$\%\&\*\(\)\[\]\{\}\!\?\;\'\"\<\>\=\+\~\`\|\/\\]', '', text)
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            
            if cleaned and len(cleaned) > 3 and cleaned not in seen_texts:
                combined_text.append(cleaned)
                seen_texts.add(cleaned)
        
        return combined_text
        
    except Exception as e:
        print(f"Tesseract extraction error: {e}")
        return []

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0-lightweight',
        'platform': 'Railway'
    })

@app.route('/extract', methods=['POST'])
def extract_text():
    """
    Extract text from uploaded image (lightweight version)
    
    Expected form data:
    - file: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF)
    
    Returns:
    - JSON with extracted text and metadata
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided',
                'message': 'Please provide an image file'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select an image file'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type',
                'message': f'Allowed file types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{file_id}.{file_extension}"
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            image_path = temp_path / unique_filename
            
            # Save uploaded file
            file.save(str(image_path))
            
            # Extract text using lightweight method
            extracted_text = extract_text_lightweight(image_path)
            
            # Calculate metrics
            total_text = ' '.join(extracted_text)
            word_count = len(total_text.split())
            
            # Prepare response
            response = {
                'success': True,
                'file_id': file_id,
                'original_filename': filename,
                'extracted_text': extracted_text,
                'metadata': {
                    'text_length': len(total_text),
                    'word_count': word_count,
                    'sentence_count': len(extracted_text),
                    'has_text': len(total_text.strip()) > 0,
                    'processing_method': 'lightweight_tesseract'
                },
                'timestamp': datetime.now().isoformat()
            }
            
            return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'error': 'Processing failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/info', methods=['GET'])
def api_info():
    """API information and capabilities"""
    return jsonify({
        'name': 'Lightweight Image Text Extraction API',
        'version': '1.0.0-lightweight',
        'description': 'Extract text from images using lightweight Tesseract OCR',
        'platform': 'Railway',
        'capabilities': {
            'single_image': True,
            'batch_processing': False,  # Disabled for Railway free tier
            'supported_formats': list(ALLOWED_EXTENSIONS),
            'max_file_size': '4MB',
            'accuracy': '40-50%',
            'processing_time': '5-10 seconds per image'
        },
        'endpoints': {
            'POST /extract': 'Extract text from single image',
            'GET /health': 'Health check',
            'GET /info': 'API information'
        },
        'limitations': {
            'memory_usage': '50MB max',
            'cpu_time': '5-10 seconds per image',
            'no_batch_processing': 'Single image only',
            'lightweight_ocr': 'Tesseract only (no EasyOCR)'
        }
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'message': 'Maximum file size is 4MB for Railway free tier'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Check API documentation for available endpoints'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    # Setup tesseract
    if not setup_tesseract():
        print("Warning: Tesseract not found. Railway should have tesseract pre-installed.")
    
    # Get port from environment variable (Railway requirement)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=port)
