#!/usr/bin/env python3
"""
Get complete OCR.space output for both images
"""

import requests
import json
import os
from pathlib import Path

def get_full_ocrspace_output(image_path, api_key):
    """Get complete OCR.space output for an image"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image file not found: {image_path}")
        return None
    
    print(f"🧪 Getting full OCR.space output for: {image_path}")
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
                
                # Extract complete text
                if isinstance(result, dict):
                    if result.get('IsErroredOnProcessing', False):
                        print(f"❌ OCR.space error: {result.get('ErrorMessage', 'Unknown error')}")
                        return None
                    
                    if 'ParsedResults' in result and result['ParsedResults']:
                        parsed_text = result['ParsedResults'][0].get('ParsedText', '')
                        processing_time = result.get('ProcessingTimeInMilliseconds', 0)
                        
                        print(f"⏱️  Processing time: {processing_time}ms")
                        print(f"📄 Complete extracted text:")
                        print("-" * 50)
                        print(parsed_text)
                        print("-" * 50)
                        print(f"📊 Total characters: {len(parsed_text)}")
                        print(f"📊 Total words: {len(parsed_text.split())}")
                        
                        return {
                            'text': parsed_text,
                            'characters': len(parsed_text),
                            'words': len(parsed_text.split()),
                            'processing_time': processing_time
                        }
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
    """Main function to get complete outputs"""
    print("🧪 OCR.space Complete Output for Both Images")
    print("=" * 60)
    
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
    
    # Test each image and get complete output
    results = []
    for i, test_image in enumerate(image_files, 1):
        print(f"📤 IMAGE {i}: {test_image.name}")
        print("=" * 60)
        
        result = get_full_ocrspace_output(test_image, api_key)
        if result:
            results.append({
                'image': test_image.name,
                'result': result
            })
        
        print()
        print("-" * 60)
        print()
    
    # Final comparison
    print("🎯 OCR.space COMPLETE RESULTS SUMMARY")
    print("=" * 60)
    print()
    
    for i, result in enumerate(results, 1):
        print(f"📄 IMAGE {i}: {result['image']}")
        print(f"   Characters: {result['result']['characters']}")
        print(f"   Words: {result['result']['words']}")
        print(f"   Processing time: {result['result']['processing_time']}ms")
        print(f"   Text preview: {result['result']['text'][:100]}...")
        print()

if __name__ == "__main__":
    main()
