#!/usr/bin/env python3
"""
Test script for Google Cloud deployed OCR API
"""

import requests
import json
import os
from pathlib import Path

def test_health_check(api_url):
    """Test health check endpoint"""
    try:
        response = requests.get(f"{api_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_api_info(api_url):
    """Test API info endpoint"""
    try:
        response = requests.get(f"{api_url}/info", timeout=10)
        if response.status_code == 200:
            print("✅ API info retrieved")
            info = response.json()
            print(f"   API Name: {info.get('api_name', 'N/A')}")
            print(f"   Version: {info.get('version', 'N/A')}")
            print(f"   Max file size: {info.get('max_file_size_mb', 'N/A')} MB")
            return True
        else:
            print(f"❌ API info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API info error: {e}")
        return False

def test_text_extraction(api_url, image_path):
    """Test text extraction with sample image"""
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{api_url}/extract", files=files, timeout=60)
        
        if response.status_code == 200:
            print("✅ Text extraction successful")
            result = response.json()
            print(f"   File ID: {result.get('file_id', 'N/A')}")
            print(f"   Text length: {result.get('metadata', {}).get('text_length', 0)}")
            print(f"   Word count: {result.get('metadata', {}).get('word_count', 0)}")
            print(f"   Extracted text: {result.get('extracted_text', [])[:2]}...")  # Show first 2 items
            return True
        else:
            print(f"❌ Text extraction failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Text extraction error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Google Cloud OCR API")
    print("=" * 50)
    
    # Get API URL from user or environment
    api_url = os.getenv('API_URL')
    if not api_url:
        api_url = input("Enter your Google Cloud API URL: ").strip()
        if not api_url:
            print("❌ No API URL provided")
            return
    
    if not api_url.startswith('http'):
        api_url = f"https://{api_url}"
    
    print(f"🌐 Testing API: {api_url}")
    print()
    
    # Test health check
    print("1. Testing health check...")
    health_ok = test_health_check(api_url)
    print()
    
    # Test API info
    print("2. Testing API info...")
    info_ok = test_api_info(api_url)
    print()
    
    # Test text extraction
    print("3. Testing text extraction...")
    image_samples = Path("image_samples")
    if image_samples.exists():
        image_files = list(image_samples.glob("*.jpg")) + list(image_samples.glob("*.png"))
        if image_files:
            test_image = image_files[0]
            print(f"   Using test image: {test_image}")
            extraction_ok = test_text_extraction(api_url, test_image)
        else:
            print("❌ No test images found in image_samples/")
            extraction_ok = False
    else:
        print("❌ image_samples/ directory not found")
        extraction_ok = False
    print()
    
    # Summary
    print("📊 Test Summary:")
    print(f"   Health check: {'✅' if health_ok else '❌'}")
    print(f"   API info: {'✅' if info_ok else '❌'}")
    print(f"   Text extraction: {'✅' if extraction_ok else '❌'}")
    
    if all([health_ok, info_ok, extraction_ok]):
        print("\n🎉 All tests passed! Your Google Cloud API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
