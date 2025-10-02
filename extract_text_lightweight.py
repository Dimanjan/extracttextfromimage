#!/usr/bin/env python3
"""
Lightweight Text Extraction - Optimized for PythonAnywhere Free Tier
Uses only Tesseract with smart preprocessing for fast, efficient text extraction
"""

import os
import sys
from pathlib import Path
import json
import re
from datetime import datetime

try:
    from PIL import Image, ImageEnhance, ImageFilter
    import pytesseract
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Please install required packages:")
    print("pip install pillow pytesseract")
    sys.exit(1)

def setup_tesseract():
    """Setup tesseract path"""
    possible_paths = [
        '/usr/local/bin/tesseract',
        '/opt/homebrew/bin/tesseract',
        '/usr/bin/tesseract'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    
    print("Tesseract not found. Please install tesseract:")
    print("brew install tesseract")
    return False

def preprocess_image_lightweight(image_path):
    """Lightweight image preprocessing using PIL only"""
    try:
        # Open image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to grayscale
        gray = img.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(gray)
        enhanced = enhancer.enhance(2.0)
        
        # Enhance sharpness
        sharpness = ImageEnhance.Sharpness(enhanced)
        sharp = sharpness.enhance(2.0)
        
        return sharp
        
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def extract_text_lightweight(image_path, output_dir):
    """Lightweight text extraction using Tesseract only"""
    print(f"  Processing with lightweight Tesseract...")
    
    # Preprocess image
    processed_img = preprocess_image_lightweight(image_path)
    if processed_img is None:
        return {
            'image': image_path.name,
            'error': 'Could not preprocess image',
            'text_length': 0,
            'has_text': False
        }
    
    # Try different Tesseract configurations
    results = []
    
    # Configuration 1: Default
    try:
        text1 = pytesseract.image_to_string(processed_img, config='--psm 6')
        if text1.strip():
            results.append(('default', text1.strip()))
    except:
        pass
    
    # Configuration 2: Single text line
    try:
        text2 = pytesseract.image_to_string(processed_img, config='--psm 7')
        if text2.strip():
            results.append(('single_line', text2.strip()))
    except:
        pass
    
    # Configuration 3: Raw line
    try:
        text3 = pytesseract.image_to_string(processed_img, config='--psm 13')
        if text3.strip():
            results.append(('raw_line', text3.strip()))
    except:
        pass
    
    # Configuration 4: Auto
    try:
        text4 = pytesseract.image_to_string(processed_img, config='--psm 3')
        if text4.strip():
            results.append(('auto', text4.strip()))
    except:
        pass
    
    # Combine and clean results
    all_text = []
    for method, text in results:
        if text and len(text.strip()) > 2:  # Only meaningful text
            all_text.append(text.strip())
    
    # Remove duplicates while preserving order
    unique_text = []
    seen = set()
    for text in all_text:
        if text not in seen:
            unique_text.append(text)
            seen.add(text)
    
    # Clean up text
    cleaned_text = []
    for text in unique_text:
        # Remove common OCR artifacts
        cleaned = re.sub(r'[^\w\s\.\,\:\-\@\#\$\%\&\*\(\)\[\]\{\}\!\?\;\'\"\<\>\=\+\~\`\|\/\\]', '', text)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        if cleaned and len(cleaned) > 2:
            cleaned_text.append(cleaned)
    
    # Create output
    output_filename = f"{image_path.stem}_extracted_text.txt"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Source Image: {image_path.name}\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("EXTRACTED TEXT:\n")
        f.write("-" * 20 + "\n")
        for i, text in enumerate(cleaned_text, 1):
            f.write(f"{i}. {text}\n")
        
        f.write(f"\nRAW RESULTS BY METHOD:\n")
        f.write("-" * 30 + "\n")
        for method, text in results:
            f.write(f"{method}: {text}\n")
    
    # Calculate metrics
    total_text = ' '.join(cleaned_text)
    word_count = len(total_text.split())
    
    return {
        'image': image_path.name,
        'text_length': len(total_text),
        'word_count': word_count,
        'sentence_count': len(cleaned_text),
        'has_text': len(total_text.strip()) > 0,
        'output_file': output_filename,
        'methods_used': len(results)
    }

def get_image_files(directory):
    """Get all image files from directory"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    image_files = []
    
    for file_path in Path(directory).iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            image_files.append(file_path)
    
    return sorted(image_files)

def main():
    """Main function"""
    script_dir = Path(__file__).parent
    image_dir = script_dir / "image_samples"
    output_dir = script_dir / "output"
    
    output_dir.mkdir(exist_ok=True)
    
    if not setup_tesseract():
        return
    
    image_files = get_image_files(image_dir)
    
    if not image_files:
        print(f"No image files found in {image_dir}")
        return
    
    print(f"Found {len(image_files)} image files")
    print("Starting LIGHTWEIGHT text extraction...")
    print("Optimized for PythonAnywhere free tier")
    print("-" * 50)
    
    results = []
    for i, image_path in enumerate(image_files, 1):
        print(f"Processing {i}/{len(image_files)}: {image_path.name}")
        result = extract_text_lightweight(image_path, output_dir)
        results.append(result)
        
        if result['has_text']:
            print(f"  ✅ Extracted: {result['sentence_count']} sentences, {result['word_count']} words")
        else:
            print(f"  ⚠️  No text found")
    
    # Generate summary
    summary = {
        'total_images': len(image_files),
        'successful_extractions': sum(1 for r in results if r.get('has_text', False)),
        'total_words': sum(r.get('word_count', 0) for r in results),
        'total_sentences': sum(r.get('sentence_count', 0) for r in results),
        'results': results,
        'timestamp': datetime.now().isoformat()
    }
    
    summary_path = output_dir / "lightweight_extraction_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print("LIGHTWEIGHT EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"Total images processed: {summary['total_images']}")
    print(f"Successful extractions: {summary['successful_extractions']}")
    print(f"Total words extracted: {summary['total_words']}")
    print(f"Total sentences: {summary['total_sentences']}")
    print(f"\nResults saved to: {output_dir}")
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
