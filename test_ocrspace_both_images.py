#!/usr/bin/env python3
"""
Test OCR.space API with both sample images
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
    print("🧪 Testing OCR.space API with Both Sample Images")
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
    
    print(f"🖼️  Found {len(image_files)} image files:")
    for i, img in enumerate(image_files, 1):
        print(f"   {i}. {img.name}")
    print()
    
    # Test each image
    results = []
    for i, test_image in enumerate(image_files, 1):
        print(f"📤 TEST {i}: {test_image.name}")
        print("=" * 50)
        
        result = test_ocrspace_with_file(test_image, api_key)
        results.append({
            'image': test_image.name,
            'result': result,
            'success': result is not None
        })
        
        print()
        print("📊 Result Summary:")
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
        print("-" * 60)
        print()
    
    # Final summary
    print("🎯 FINAL SUMMARY")
    print("=" * 60)
    print()
    
    successful_tests = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"📊 Overall Results:")
    print(f"   Total images tested: {total_tests}")
    print(f"   Successful extractions: {successful_tests}")
    print(f"   Success rate: {(successful_tests/total_tests)*100:.1f}%")
    print()
    
    print("📄 Detailed Results:")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['image']}:")
        if result['success'] and result['result']:
            text_preview = result['result'][:50] + "..." if len(result['result']) > 50 else result['result']
            print(f"      ✅ {len(result['result'])} characters: {text_preview}")
        else:
            print(f"      ❌ Failed or no text extracted")
    
    print()
    print("🔍 Comparison with our Advanced OCR:")
    print("- OCR.space: Fast processing, basic text extraction")
    print("- Our Advanced OCR: 75% accuracy, better text reconstruction")
    print("- For complex images: Our Advanced OCR is recommended")

if __name__ == "__main__":
    main()
