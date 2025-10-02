#!/usr/bin/env python3
"""
Test script for Image Text Extraction API
"""

import requests
import json
import time

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_info():
    """Test info endpoint"""
    print("\nTesting info endpoint...")
    try:
        response = requests.get('http://localhost:5000/info')
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_extract_single():
    """Test single image extraction"""
    print("\nTesting single image extraction...")
    try:
        # Use one of our sample images
        with open('image_samples/Screenshot 2025-10-02 at 10.57.19.png', 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/extract', files=files)
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Success: {result.get('success', False)}")
            print(f"Text extracted: {len(result.get('extracted_text', []))} sentences")
            if result.get('extracted_text'):
                for i, text in enumerate(result['extracted_text'][:3], 1):
                    print(f"  {i}. {text}")
            return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_extract_batch():
    """Test batch image extraction"""
    print("\nTesting batch image extraction...")
    try:
        files = []
        for filename in ['Screenshot 2025-10-02 at 10.57.19.png', 
                        'Screenshot 2025-10-02 at 10.57.28.png']:
            with open(f'image_samples/{filename}', 'rb') as f:
                files.append(('files', (filename, f.read(), 'image/png')))
        
        response = requests.post('http://localhost:5000/extract/batch', files=files)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Success: {result.get('success', False)}")
        print(f"Total files processed: {result.get('total_files', 0)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Image Text Extraction API Tests")
    print("=" * 50)
    
    # Wait for API to start
    print("Waiting for API to start...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_health),
        ("API Info", test_info),
        ("Single Image Extraction", test_extract_single),
        ("Batch Image Extraction", test_extract_batch)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✅ PASS' if success else '❌ FAIL'}")
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print("=" * 50)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API logs.")

if __name__ == "__main__":
    main()
