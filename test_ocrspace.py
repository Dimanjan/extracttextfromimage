#!/usr/bin/env python3
"""
Test OCR.space API with image samples
"""

import requests
import json
import os
import base64
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

def test_ocrspace_with_base64(image_path, api_key):
    """Test OCR.space API with base64 encoded image"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None
    
    print(f"�� Testing OCR.space API with base64: {image_path}")
    print(f"📁 File size: {os.path.getsize(image_path) / 1024:.1f} KB")
    print()
    
    try:
        # Read image and convert to base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # OCR.space API endpoint
        url = "https://api.ocr.space/parse/image"
        
        # Headers
        headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }
        
        # Payload with base64 data
        payload = {
            "base64Image": f"data:image/jpeg;base64,{base64_data}",
            "language": "eng",
            "isOverlayRequired": False
        }
        
        print("📤 Sending base64 encoded image to OCR.space...")
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
    print("🧪 Testing OCR.space API")
    print("=" * 50)
    
    # API key
    api_key = "K89033969188957"
    
    # Find image samples
    image_samples = Path("image_samples")
    if not image_samples.exists():
        print("❌ image_samples directory not found")
        return
    
    image_files = list(image_samples.glob("*.png")) + list(image_samples.glob("*.jpg"))
    if not image_files:
        print("❌ No image files found in image_samples/")
        return
    
    # Test with first image
    test_image = image_files[0]
    print(f"🖼️  Testing with: {test_image.name}")
    print()
    
    # Test OCR.space with file upload
    print("📤 Method 1: File upload")
    result1 = test_ocrspace_with_file(test_image, api_key)
    
    print()
    print("📤 Method 2: Base64 encoding")
    result2 = test_ocrspace_with_base64(test_image, api_key)
    
    print()
    print("📊 Test Summary:")
    if result1 is not None or result2 is not None:
        print("✅ OCR.space API test completed")
        if result1 is not None:
            print(f"📄 Method 1 result: {type(result1)}")
            if isinstance(result1, str) and len(result1) > 0:
                print(f"📄 Text length: {len(result1)} characters")
                print(f"📄 Text preview: {result1[:100]}...")
        if result2 is not None:
            print(f"📄 Method 2 result: {type(result2)}")
            if isinstance(result2, str) and len(result2) > 0:
                print(f"📄 Text length: {len(result2)} characters")
                print(f"📄 Text preview: {result2[:100]}...")
    else:
        print("❌ OCR.space API test failed")
    
    print()
    print("🔍 Comparison with our advanced OCR:")
    print("- Our advanced OCR: 75% accuracy, 30-60s processing")
    print("- OCR.space API: Unknown accuracy, fast processing")
    print("- Cost: OCR.space has free tier, our solution is free after deployment")

if __name__ == "__main__":
    main()
