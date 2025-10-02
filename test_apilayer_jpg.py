#!/usr/bin/env python3
"""
Test API Layer OCR API with JPG image
"""

import requests
import json
import os
from pathlib import Path

def test_apilayer_ocr_jpg(image_path, api_key):
    """Test API Layer OCR with a JPG image file"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None
    
    print(f"🧪 Testing API Layer OCR with: {image_path}")
    print(f"📁 File size: {os.path.getsize(image_path) / 1024:.1f} KB")
    print()
    
    # API Layer endpoint
    url = "https://api.apilayer.com/image_to_text/upload"
    
    # Headers with API key
    headers = {
        "apikey": api_key
    }
    
    try:
        # Read image file and send as multipart/form-data with correct mimetype
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            
            print("📤 Sending JPG request to API Layer...")
            response = requests.post(url, headers=headers, files=files, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            
            # Parse response
            try:
                result = response.json()
                print(f"📝 Response type: {type(result)}")
                print(f"📝 Response keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                
                # Extract text if available
                if isinstance(result, dict):
                    if 'text' in result:
                        extracted_text = result['text']
                        print(f"📄 Extracted text length: {len(extracted_text)} characters")
                        print(f"📄 Extracted text preview: {extracted_text[:200]}...")
                        return extracted_text
                    elif 'result' in result:
                        extracted_text = result['result']
                        print(f"📄 Extracted text length: {len(extracted_text)} characters")
                        print(f"📄 Extracted text preview: {extracted_text[:200]}...")
                        return extracted_text
                    else:
                        print("📄 Full response:")
                        print(json.dumps(result, indent=2))
                        return result
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
    print("🧪 Testing API Layer OCR API with JPG")
    print("=" * 50)
    
    # API key
    api_key = "Gr2DJAt4f6lGFNJHMvpFeOCE4nCHh4hB"
    
    # Test with converted JPG
    jpg_path = "image_samples/test_image.jpg"
    if not os.path.exists(jpg_path):
        print("❌ JPG file not found. Please convert PNG to JPG first.")
        return
    
    print(f"🖼️  Testing with: {jpg_path}")
    print()
    
    # Test API Layer with JPG
    result = test_apilayer_ocr_jpg(jpg_path, api_key)
    
    print()
    print("📊 Test Summary:")
    if result:
        print("✅ API Layer OCR test completed")
        print(f"📄 Result type: {type(result)}")
        if isinstance(result, str) and len(result) > 0:
            print(f"📄 Text length: {len(result)} characters")
            print(f"📄 Text preview: {result[:100]}...")
        else:
            print("📄 Result:", result)
    else:
        print("❌ API Layer OCR test failed")
    
    print()
    print("🔍 Comparison with our advanced OCR:")
    print("- Our advanced OCR: 75% accuracy, 30-60s processing")
    print("- API Layer OCR: Unknown accuracy, fast processing")
    print("- Cost: API Layer charges per request, our solution is free after deployment")

if __name__ == "__main__":
    main()
