#!/usr/bin/env python3
"""
Image Text Extraction API
Production-ready Flask API for extracting text from images
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid

# Import our text extraction module
from extract_text import extract_text_advanced

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def setup_tesseract():
    """Setup tesseract path"""
    possible_paths = [
        '/usr/local/bin/tesseract',
        '/opt/homebrew/bin/tesseract',
        '/usr/bin/tesseract'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            import pytesseract
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    
    return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/extract', methods=['POST'])
def extract_text():
    """
    Extract text from uploaded image
    
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
            
            # Create output directory
            output_dir = temp_path / "output"
            output_dir.mkdir(exist_ok=True)
            
            # Extract text using our advanced system
            result = extract_text_advanced(image_path, output_dir)
            
            # Read extracted text from output file
            extracted_text = []
            if result.get('output_file'):
                output_file = output_dir / result['output_file']
                if output_file.exists():
                    with open(output_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract just the reconstructed text section
                        lines = content.split('\n')
                        in_text_section = False
                        for line in lines:
                            if 'EXTRACTED TEXT:' in line:
                                in_text_section = True
                                continue
                            elif in_text_section and line.startswith('RAW'):
                                break
                            elif in_text_section and line.strip() and not line.startswith('-'):
                                extracted_text.append(line.strip())
            
            # Prepare response
            response = {
                'success': True,
                'file_id': file_id,
                'original_filename': filename,
                'extracted_text': extracted_text,
                'metadata': {
                    'text_length': result.get('text_length', 0),
                    'word_count': result.get('word_count', 0),
                    'sentence_count': result.get('sentence_count', 0),
                    'has_text': result.get('has_text', False),
                    'processing_time': result.get('processing_time', 0)
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

@app.route('/extract/batch', methods=['POST'])
def extract_text_batch():
    """
    Extract text from multiple images
    
    Expected form data:
    - files: Multiple image files
    
    Returns:
    - JSON with extracted text from all images
    """
    try:
        # Check if files are present
        if 'files' not in request.files:
            return jsonify({
                'error': 'No files provided',
                'message': 'Please provide image files'
            }), 400
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({
                'error': 'No files selected',
                'message': 'Please select image files'
            }), 400
        
        results = []
        
        # Process each file
        for file in files:
            if file and allowed_file(file.filename):
                # Generate unique filename
                file_id = str(uuid.uuid4())
                filename = secure_filename(file.filename)
                file_extension = filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{file_id}.{file_extension}"
                
                # Create temporary directory for this file
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    image_path = temp_path / unique_filename
                    
                    # Save uploaded file
                    file.save(str(image_path))
                    
                    # Create output directory
                    output_dir = temp_path / "output"
                    output_dir.mkdir(exist_ok=True)
                    
                    # Extract text
                    result = extract_text_advanced(image_path, output_dir)
                    
                    # Read extracted text
                    extracted_text = []
                    if result.get('output_file'):
                        output_file = output_dir / result['output_file']
                        if output_file.exists():
                            with open(output_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                                lines = content.split('\n')
                                in_text_section = False
                                for line in lines:
                                    if 'EXTRACTED TEXT:' in line:
                                        in_text_section = True
                                        continue
                                    elif in_text_section and line.startswith('RAW'):
                                        break
                                    elif in_text_section and line.strip() and not line.startswith('-'):
                                        extracted_text.append(line.strip())
                    
                    results.append({
                        'file_id': file_id,
                        'original_filename': filename,
                        'extracted_text': extracted_text,
                        'metadata': {
                            'text_length': result.get('text_length', 0),
                            'word_count': result.get('word_count', 0),
                            'sentence_count': result.get('sentence_count', 0),
                            'has_text': result.get('has_text', False)
                        }
                    })
        
        return jsonify({
            'success': True,
            'total_files': len(results),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Batch processing failed',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/info', methods=['GET'])
def api_info():
    """API information and capabilities"""
    return jsonify({
        'name': 'Image Text Extraction API',
        'version': '1.0.0',
        'description': 'Extract text from images using advanced OCR',
        'capabilities': {
            'single_image': True,
            'batch_processing': True,
            'supported_formats': list(ALLOWED_EXTENSIONS),
            'max_file_size': '16MB',
            'accuracy': '75%+'
        },
        'endpoints': {
            'POST /extract': 'Extract text from single image',
            'POST /extract/batch': 'Extract text from multiple images',
            'GET /health': 'Health check',
            'GET /info': 'API information'
        }
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'message': 'Maximum file size is 16MB'
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
        print("Warning: Tesseract not found. Please install tesseract.")
        print("On macOS: brew install tesseract")
        print("On Ubuntu: sudo apt-get install tesseract-ocr")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
