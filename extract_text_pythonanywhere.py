#!/usr/bin/env python3
"""
PythonAnywhere Optimized Text Extraction
Ultra-lightweight version for free tier deployment
"""

import os
import sys
from pathlib import Path
import json
import re
from datetime import datetime

try:
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    import pytesseract
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Please install required packages:")
    print("pip install pillow pytesseract")
    sys.exit(1)

def setup_tesseract():
    """Setup tesseract path for PythonAnywhere"""
    # PythonAnywhere typically has tesseract in /usr/bin/
    possible_paths = [
        '/usr/bin/tesseract',
        '/usr/local/bin/tesseract',
        '/opt/homebrew/bin/tesseract'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    
    print("Tesseract not found. Please install tesseract on PythonAnywhere:")
    print("pip3.10 install --user pytesseract")
    return False

def optimize_image_for_ocr(image_path):
    """Optimize image for better OCR using PIL only"""
    try:
        # Open and convert to RGB
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large (PythonAnywhere memory limit)
        width, height = img.size
        if width > 1200 or height > 1200:
            ratio = min(1200/width, 1200/height)
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

def extract_text_pythonanywhere(image_path, output_dir):
    """PythonAnywhere optimized text extraction"""
    print(f"  Processing with PythonAnywhere optimized Tesseract...")
    
    # Optimize image
    optimized_img = optimize_image_for_ocr(image_path)
    if optimized_img is None:
        return {
            'image': image_path.name,
            'error': 'Could not optimize image',
            'text_length': 0,
            'has_text': False
        }
    
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
    
    # Create output
    output_filename = f"{image_path.stem}_pythonanywhere_extraction.txt"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Source Image: {image_path.name}\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("EXTRACTED TEXT:\n")
        f.write("-" * 20 + "\n")
        for i, text in enumerate(combined_text, 1):
            f.write(f"{i}. {text}\n")
        
        f.write(f"\nRAW RESULTS BY CONFIG:\n")
        f.write("-" * 30 + "\n")
        for config_name, text in all_results:
            f.write(f"{config_name}: {text}\n")
    
    # Calculate metrics
    total_text = ' '.join(combined_text)
    word_count = len(total_text.split())
    
    return {
        'image': image_path.name,
        'text_length': len(total_text),
        'word_count': word_count,
        'sentence_count': len(combined_text),
        'has_text': len(total_text.strip()) > 0,
        'output_file': output_filename,
        'configs_used': len(all_results)
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
    print("Starting PYTHONANYWHERE optimized text extraction...")
    print("Ultra-lightweight for free tier deployment")
    print("-" * 50)
    
    results = []
    for i, image_path in enumerate(image_files, 1):
        print(f"Processing {i}/{len(image_files)}: {image_path.name}")
        result = extract_text_pythonanywhere(image_path, output_dir)
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
    
    summary_path = output_dir / "pythonanywhere_extraction_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 50)
    print("PYTHONANYWHERE EXTRACTION SUMMARY")
    print("=" * 50)
    print(f"Total images processed: {summary['total_images']}")
    print(f"Successful extractions: {summary['successful_extractions']}")
    print(f"Total words extracted: {summary['total_words']}")
    print(f"Total sentences: {summary['total_sentences']}")
    print(f"\nResults saved to: {output_dir}")
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
