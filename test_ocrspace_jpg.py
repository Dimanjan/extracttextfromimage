#!/usr/bin/env python3
"""
Test OCR.space API with JPG image
"""

import requests
import json
import os
from pathlib import Path

def test_ocrspace_with_file(image_path, api_key):
    """Test OCR.space API with image file upload"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None
    
    print(f"🧪 Testing OCR.space API with: {image_path}")
    print(f"📁 File size: {os.path.getsize(image_path) / 1024:.1f} KB")
    print()
    
    # OCR.space API endpoint
    url = "https://api.ocr.space/parse/image"
    
    # Headers
    headers = {
        "apikey": api_key
    }
    
    try:
        # Read image file and send as multipart/form-data
        with open(image_path, 'rb') as f:
            files = {'file': f}
            
            print("📤 Sending file upload to OCR.space...")
            response = requests.post(url, headers=headers, files=files, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            
            try:
                result = response.json()
                print(f"📝 Response type: {type(result)}")
                print(f"📝 Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                
                # Extract text if available
                if isinstance(result, dict):
                    if result.get('IsErroredOnProcessing', False):
                        print(f"❌ OCR.space error: {result.get('ErrorMessage', 'Unknown error')}")
                        return None
                    
                    if 'ParsedResults' in result and result['ParsedResults']:
                        parsed_text = result['ParsedResults'][0].get('ParsedText', '')
                        if parsed_text.strip():
                            print(f"📄 Extracted text length: {len(parsed_text)} characters")
                            print(f"📄 Extracted text preview: {parsed_text[:200]}...")
                            return parsed_text
                        else:
                            print("📄 No text detected in image")
                            return ""
                    else:
                        print("📄 No parsed results found")
                        return None
                else:
                    print("📄 Raw response:")
                    print(result)
                    return result
                    
            except json.JSONDecodeError:
                print("📄 Raw response (not JSON):")
                print(response.text)
                return response.text
                
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"📄 Error response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing OCR.space API with JPG image")
    print("=" * 50)
    
    # API key
    api_key = "K89033969188957"
    
    # Test with JPG image
    jpg_path = "image_samples/test_image.jpg"
    if not os.path.exists(jpg_path):
        print("❌ JPG file not found. Please convert PNG to JPG first.")
        return
    
    print(f"🖼️  Testing with: {jpg_path}")
    print()
    
    # Test OCR.space with JPG
    result = test_ocrspace_with_file(jpg_path, api_key)
    
    print()
    print("📊 Test Summary:")
    if result is not None:
        print("✅ OCR.space API test completed")
        print(f"📄 Result type: {type(result)}")
        if isinstance(result, str) and len(result) > 0:
            print(f"📄 Text length: {len(result)} characters")
            print(f"📄 Text preview: {result[:100]}...")
        else:
            print("📄 Result:", result)
    else:
        print("❌ OCR.space API test failed")
    
    print()
    print("🔍 Comparison with our advanced OCR:")
    print("- Our advanced OCR: 75% accuracy, 30-60s processing")
    print("- OCR.space API: Unknown accuracy, fast processing")
    print("- Cost: OCR.space has free tier, our solution is free after deployment")

if __name__ == "__main__":
    main()
