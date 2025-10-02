#!/usr/bin/env python3
"""
Advanced Text Extraction with Proper Reconstruction
Combines multiple OCR engines and focuses on clean text reconstruction
"""

import os
import sys
from pathlib import Path
import json
import re
from datetime import datetime
import cv2
import numpy as np

try:
    from PIL import Image, ImageEnhance, ImageFilter
    import pytesseract
    import easyocr
except ImportError as e:
    print(f"Missing required packages: {e}")
    print("Please install required packages:")
    print("pip install pillow pytesseract opencv-python easyocr")
    sys.exit(1)

def setup_tesseract():
    """Setup tesseract path for macOS"""
    possible_paths = [
        '/usr/local/bin/tesseract',
        '/opt/homebrew/bin/tesseract',
        '/usr/bin/tesseract'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True
    return False

def clean_and_reconstruct_text(text_blocks):
    """Clean and reconstruct text from multiple sources"""
    if not text_blocks:
        return ""
    
    # Combine all text
    all_text = []
    for block in text_blocks:
        if isinstance(block, dict):
            text = block.get('text', '')
        else:
            text = str(block)
        if text.strip():
            all_text.append(text.strip())
    
    # Join and clean
    combined = ' '.join(all_text)
    
    # Remove common OCR artifacts
    cleaned = re.sub(r'[^\w\s\.\,\:\-\@\#\$\%\&\*\(\)\[\]\{\}\!\?\;\'\"\<\>\=\+\~\`\|\/\\]', '', combined)
    
    # Fix common OCR mistakes
    replacements = {
        r'\b0\b': 'O',  # Zero to O in words
        r'\b1\b': 'I',  # One to I in words
        r'\b5\b': 'S',  # Five to S in words
        r'\b8\b': 'B',  # Eight to B in words
        r'@\s*': '@',   # Fix @ symbols
        r'\s+': ' ',    # Multiple spaces to single
    }
    
    for pattern, replacement in replacements.items():
        cleaned = re.sub(pattern, replacement, cleaned)
    
    # Split into meaningful chunks
    sentences = []
    current_sentence = []
    
    words = cleaned.split()
    for word in words:
        # Check if word looks like end of sentence
        if word.endswith('.') or word.endswith('!') or word.endswith('?'):
            current_sentence.append(word)
            if current_sentence:
                sentences.append(' '.join(current_sentence))
                current_sentence = []
        else:
            current_sentence.append(word)
    
    # Add remaining words
    if current_sentence:
        sentences.append(' '.join(current_sentence))
    
    return sentences

def extract_with_easyocr(image_path):
    """Extract text using EasyOCR"""
    try:
        reader = easyocr.Reader(['en'])
        results = reader.readtext(str(image_path))
        
        text_blocks = []
        for (bbox, text, confidence) in results:
            if confidence > 0.3:  # Only high confidence text
                text_blocks.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
        
        return text_blocks
    except Exception as e:
        print(f"EasyOCR error: {e}")
        return []

def extract_with_tesseract_advanced(image_path):
    """Advanced Tesseract extraction with multiple methods"""
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return []
        
        # Multiple preprocessing approaches
        methods = []
        
        # 1. Original
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        methods.append(('original', gray))
        
        # 2. Denoised
        denoised = cv2.fastNlMeansDenoising(gray)
        methods.append(('denoised', denoised))
        
        # 3. Enhanced contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        methods.append(('enhanced', enhanced))
        
        # 4. Adaptive threshold
        adaptive = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        methods.append(('adaptive', adaptive))
        
        # 5. Morphological
        kernel = np.ones((2,2), np.uint8)
        morph = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)
        methods.append(('morphological', morph))
        
        all_results = []
        
        for method_name, processed_img in methods:
            try:
                # Convert to PIL
                pil_img = Image.fromarray(processed_img)
                
                # Try different PSM modes
                psm_modes = [6, 7, 8, 13]  # Different text detection modes
                
                for psm in psm_modes:
                    try:
                        data = pytesseract.image_to_data(
                            pil_img,
                            config=f'--psm {psm}',
                            output_type=pytesseract.Output.DICT
                        )
                        
                        # Extract high confidence text
                        for i in range(len(data['text'])):
                            text = data['text'][i].strip()
                            conf = int(data['conf'][i])
                            
                            if text and conf > 30:
                                all_results.append({
                                    'text': text,
                                    'confidence': conf / 100.0,
                                    'method': f"{method_name}_psm{psm}"
                                })
                    except:
                        continue
                        
            except Exception as e:
                continue
        
        return all_results
        
    except Exception as e:
        print(f"Tesseract advanced error: {e}")
        return []

def extract_text_advanced(image_path, output_dir):
    """Advanced text extraction combining multiple engines"""
    print(f"  Processing with multiple OCR engines...")
    
    # Extract with EasyOCR
    easyocr_results = extract_with_easyocr(image_path)
    print(f"    EasyOCR: {len(easyocr_results)} text blocks")
    
    # Extract with advanced Tesseract
    tesseract_results = extract_with_tesseract_advanced(image_path)
    print(f"    Tesseract: {len(tesseract_results)} text blocks")
    
    # Combine all results
    all_text_blocks = easyocr_results + tesseract_results
    
    # Clean and reconstruct
    reconstructed_sentences = clean_and_reconstruct_text(all_text_blocks)
    
    # Create output
    output_filename = f"{image_path.stem}_advanced_extraction.txt"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Source Image: {image_path.name}\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("RECONSTRUCTED TEXT:\n")
        f.write("-" * 30 + "\n")
        for i, sentence in enumerate(reconstructed_sentences, 1):
            f.write(f"{i}. {sentence}\n")
        
        f.write(f"\nRAW EASYOCR RESULTS:\n")
        f.write("-" * 30 + "\n")
        for i, result in enumerate(easyocr_results, 1):
            f.write(f"{i}. {result['text']} (conf: {result['confidence']:.2f})\n")
        
        f.write(f"\nRAW TESSERACT RESULTS:\n")
        f.write("-" * 30 + "\n")
        for i, result in enumerate(tesseract_results, 1):
            f.write(f"{i}. {result['text']} (conf: {result['confidence']:.2f})\n")
    
    # Calculate metrics
    total_text = ' '.join(reconstructed_sentences)
    word_count = len(total_text.split())
    unique_words = len(set(total_text.lower().split()))
    
    return {
        'image': image_path.name,
        'text_length': len(total_text),
        'word_count': word_count,
        'unique_words': unique_words,
        'sentence_count': len(reconstructed_sentences),
        'has_text': len(total_text.strip()) > 0,
        'output_file': output_filename,
        'easyocr_blocks': len(easyocr_results),
        'tesseract_blocks': len(tesseract_results)
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
        print("Tesseract not found. Please install: brew install tesseract")
        return
    
    image_files = get_image_files(image_dir)
    
    if not image_files:
        print(f"No image files found in {image_dir}")
        return
    
    print(f"Found {len(image_files)} image files")
    print("Starting ADVANCED text extraction...")
    print("Using EasyOCR + Advanced Tesseract with text reconstruction")
    print("-" * 60)
    
    results = []
    for i, image_path in enumerate(image_files, 1):
        print(f"Processing {i}/{len(image_files)}: {image_path.name}")
        result = extract_text_advanced(image_path, output_dir)
        results.append(result)
        
        if result['has_text']:
            print(f"  ✅ Reconstructed: {result['sentence_count']} sentences, {result['word_count']} words")
            print(f"      EasyOCR: {result['easyocr_blocks']} blocks, Tesseract: {result['tesseract_blocks']} blocks")
        else:
            print(f"  ⚠️  No text reconstructed")
    
    # Generate summary
    summary = {
        'total_images': len(image_files),
        'successful_extractions': sum(1 for r in results if r.get('has_text', False)),
        'total_words': sum(r.get('word_count', 0) for r in results),
        'total_sentences': sum(r.get('sentence_count', 0) for r in results),
        'results': results,
        'timestamp': datetime.now().isoformat()
    }
    
    summary_path = output_dir / "advanced_extraction_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("ADVANCED EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"Total images processed: {summary['total_images']}")
    print(f"Successful extractions: {summary['successful_extractions']}")
    print(f"Total words extracted: {summary['total_words']}")
    print(f"Total sentences: {summary['total_sentences']}")
    print(f"\nResults saved to: {output_dir}")
    print(f"Summary saved to: {summary_path}")

if __name__ == "__main__":
    main()
