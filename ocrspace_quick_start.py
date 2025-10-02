#!/usr/bin/env python3
"""
OCR.space API Quick Start Guide
Simple examples to get started quickly
"""

import requests
import json

def quick_extract_text(image_path, api_key):
    """
    Quick and simple text extraction
    """
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

def extract_with_language(image_path, api_key, language="eng"):
    """
    Extract text with specific language
    """
    url = "https://api.ocr.space/parse/image"
    headers = {"apikey": api_key}
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'language': language}
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get('IsErroredOnProcessing', False):
            return result['ParsedResults'][0]['ParsedText']
    return None

def extract_with_overlay(image_path, api_key):
    """
    Extract text and generate overlay image
    """
    url = "https://api.ocr.space/parse/image"
    headers = {"apikey": api_key}
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {'isOverlayRequired': True}
        response = requests.post(url, headers=headers, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        if not result.get('IsErroredOnProcessing', False):
            return {
                'text': result['ParsedResults'][0]['ParsedText'],
                'overlay_url': result.get('SearchablePDFURL', '')
            }
    return None

# Example usage
if __name__ == "__main__":
    # Your API key
    api_key = "K89033969188957"
    
    # Test image path
    image_path = "image_samples/test_image.jpg"
    
    print("🚀 OCR.space Quick Start Examples")
    print("=" * 40)
    
    # Example 1: Basic extraction
    print("1. Basic text extraction:")
    text = quick_extract_text(image_path, api_key)
    if text:
        print(f"   ✅ Extracted: {text[:50]}...")
    else:
        print("   ❌ Failed")
    
    # Example 2: With language specification
    print("\n2. With language specification:")
    text = extract_with_language(image_path, api_key, "eng")
    if text:
        print(f"   ✅ Extracted: {text[:50]}...")
    else:
        print("   ❌ Failed")
    
    # Example 3: With overlay
    print("\n3. With overlay generation:")
    result = extract_with_overlay(image_path, api_key)
    if result:
        print(f"   ✅ Text: {result['text'][:50]}...")
        print(f"   ✅ Overlay URL: {result['overlay_url']}")
    else:
        print("   ❌ Failed")
