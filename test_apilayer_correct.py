#!/usr/bin/env python3
"""
Test API Layer OCR API with correct format
"""

import requests
import json
import os
import base64
from pathlib import Path

def test_apilayer_with_base64(image_path, api_key):
    """Test API Layer OCR with base64 encoded image"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None
    
    print(f"🧪 Testing API Layer OCR with: {image_path}")
    print(f"📁 File size: {os.path.getsize(image_path) / 1024:.1f} KB")
    print()
    
    try:
        # Read image and convert to base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # API Layer endpoint
        url = "https://api.apilayer.com/image_to_text/url"
        
        # Headers with API key
        headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }
        
        # Payload with base64 data
        payload = {
            "image": base64_data
        }
        
        print("📤 Sending base64 encoded image to API Layer...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            
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

def test_alternative_api(image_path, api_key):
    """Test alternative API endpoint"""
    
    print("🔄 Trying alternative API endpoint...")
    
    # Alternative endpoint
    url = "https://api.apilayer.com/image_to_text/upload"
    
    headers = {
        "apikey": api_key
    }
    
    try:
        # Try with different file format
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'application/octet-stream')}
            
            print("📤 Sending file with application/octet-stream...")
            response = requests.post(url, headers=headers, files=files, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            result = response.json()
            print(f"📄 Response: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"❌ Request failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main test function"""
    print("🧪 Testing API Layer OCR API")
    print("=" * 50)
    
    # API key
    api_key = "Gr2DJAt4f6lGFNJHMvpFeOCE4nCHh4hB"
    
    # Test with JPG image
    jpg_path = "image_samples/test_image.jpg"
    if not os.path.exists(jpg_path):
        print("❌ JPG file not found. Please convert PNG to JPG first.")
        return
    
    print(f"🖼️  Testing with: {jpg_path}")
    print()
    
    # Test API Layer with base64
    print("📤 Method 1: Base64 encoding")
    result1 = test_apilayer_with_base64(jpg_path, api_key)
    
    print()
    print("📤 Method 2: Alternative endpoint")
    result2 = test_alternative_api(jpg_path, api_key)
    
    print()
    print("📊 Test Summary:")
    if result1 or result2:
        print("✅ API Layer OCR test completed")
        if result1:
            print(f"📄 Method 1 result: {type(result1)}")
            if isinstance(result1, str) and len(result1) > 0:
                print(f"📄 Text length: {len(result1)} characters")
                print(f"📄 Text preview: {result1[:100]}...")
        if result2:
            print(f"📄 Method 2 result: {type(result2)}")
    else:
        print("❌ API Layer OCR test failed")
    
    print()
    print("�� Comparison with our advanced OCR:")
    print("- Our advanced OCR: 75% accuracy, 30-60s processing")
    print("- API Layer OCR: Unknown accuracy, fast processing")
    print("- Cost: API Layer charges per request, our solution is free after deployment")

if __name__ == "__main__":
    main()
