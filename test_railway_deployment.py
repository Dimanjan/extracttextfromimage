#!/usr/bin/env python3
"""
Test script to verify Railway deployment readiness
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
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Version: {data.get('version')}")
            print(f"Platform: {data.get('platform')}")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_info():
    """Test info endpoint"""
    print("\nTesting info endpoint...")
    try:
        response = requests.get('http://localhost:5000/info')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"API: {data.get('name')} v{data.get('version')}")
            print(f"Platform: {data.get('platform')}")
            print(f"Max file size: {data.get('capabilities', {}).get('max_file_size')}")
            print(f"Accuracy: {data.get('capabilities', {}).get('accuracy')}")
            return True
        return False
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
            if response.status_code == 200:
                result = response.json()
                print(f"Success: {result.get('success', False)}")
                print(f"Text extracted: {len(result.get('extracted_text', []))} sentences")
                if result.get('extracted_text'):
                    for i, text in enumerate(result['extracted_text'][:3], 1):
                        print(f"  {i}. {text}")
                return True
            else:
                print(f"Error response: {response.json()}")
                return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Railway Deployment Readiness Test")
    print("=" * 50)
    print("Make sure the API is running: python api.py")
    print("=" * 50)
    
    # Wait for API to start
    print("Waiting for API to start...")
    time.sleep(3)
    
    tests = [
        ("Health Check", test_health),
        ("API Info", test_info),
        ("Single Image Extraction", test_extract_single)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        print(f"Result: {'✅ PASS' if success else '❌ FAIL'}")
    
    # Summary
    print(f"\n{'='*50}")
    print("DEPLOYMENT READINESS SUMMARY")
    print("=" * 50)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 API is ready for Railway deployment!")
        print("\nNext steps:")
        print("1. Go to railway.app")
        print("2. Connect your GitHub repo")
        print("3. Deploy automatically!")
    else:
        print("⚠️  Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()
