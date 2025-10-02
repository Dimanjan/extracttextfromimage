#!/usr/bin/env python3
"""
Test API Layer OCR API using URL endpoint
"""

import requests
import json
import os
from pathlib import Path

def test_apilayer_url_endpoint(image_url, api_key):
    """Test API Layer OCR with image URL"""
    
    print(f"🧪 Testing API Layer OCR with URL: {image_url}")
    print()
    
    # API Layer endpoint with URL parameter
    url = f"https://api.apilayer.com/image_to_text/url?url={image_url}"
    
    # Headers with API key
    headers = {
        "apikey": api_key
    }
    
    try:
        print("📤 Sending GET request to API Layer...")
        response = requests.get(url, headers=headers, timeout=30)
        
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

def main():
    """Main test function"""
    print("🧪 Testing API Layer OCR API with URL endpoint")
    print("=" * 60)
    
    # API key
    api_key = "Gr2DJAt4f6lGFNJHMvpFeOCE4nCHh4hB"
    
    # Test with a publicly accessible image URL
    # Using a sample image URL that should be accessible
    test_urls = [
        "https://via.placeholder.com/600x400/000000/FFFFFF?text=Sample+Text+for+OCR+Testing",
        "https://httpbin.org/image/png",
        "https://picsum.photos/600/400"
    ]
    
    print("🖼️  Testing with sample URLs:")
    print()
    
    for i, image_url in enumerate(test_urls, 1):
        print(f"📤 Test {i}: {image_url}")
        result = test_apilayer_url_endpoint(image_url, api_key)
        
        print()
        print("📊 Result Summary:")
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
        print("-" * 60)
        print()
    
    print("🔍 Final Comparison:")
    print("- API Layer OCR: External service, per-request pricing")
    print("- Our Advanced OCR: Self-hosted, 75% accuracy, free after deployment")

if __name__ == "__main__":
    main()
