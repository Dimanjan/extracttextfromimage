#!/usr/bin/env python3
"""
Demo script showing how to use the Image Text Extraction API
"""

import requests
import json
import time

def demo_single_image():
    """Demo single image extraction"""
    print("📸 Demo: Single Image Text Extraction")
    print("-" * 50)
    
    # Use one of our sample images
    image_path = 'image_samples/Screenshot 2025-10-02 at 10.57.19.png'
    
    try:
        with open(image_path, 'rb') as f:
            print(f"Uploading image: {image_path}")
            response = requests.post(
                'http://localhost:5000/extract',
                files={'file': f}
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Extracted {len(result['extracted_text'])} sentences")
            print("\nExtracted Text:")
            for i, text in enumerate(result['extracted_text'], 1):
                print(f"  {i}. {text}")
            
            print(f"\nMetadata:")
            print(f"  - Text length: {result['metadata']['text_length']} characters")
            print(f"  - Word count: {result['metadata']['word_count']} words")
            print(f"  - Sentence count: {result['metadata']['sentence_count']} sentences")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_batch_processing():
    """Demo batch image processing"""
    print("\n📸 Demo: Batch Image Processing")
    print("-" * 50)
    
    try:
        files = []
        image_files = [
            'image_samples/Screenshot 2025-10-02 at 10.57.19.png',
            'image_samples/Screenshot 2025-10-02 at 10.57.28.png'
        ]
        
        for image_path in image_files:
            with open(image_path, 'rb') as f:
                files.append(('files', (image_path.split('/')[-1], f.read(), 'image/png')))
        
        print(f"Uploading {len(files)} images for batch processing...")
        response = requests.post('http://localhost:5000/extract/batch', files=files)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Processed {result['total_files']} images")
            
            for i, file_result in enumerate(result['results'], 1):
                print(f"\nImage {i}: {file_result['original_filename']}")
                print(f"  Extracted {len(file_result['extracted_text'])} sentences:")
                for j, text in enumerate(file_result['extracted_text'], 1):
                    print(f"    {j}. {text}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.json())
    
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_api_info():
    """Demo API information"""
    print("\n📊 Demo: API Information")
    print("-" * 50)
    
    try:
        response = requests.get('http://localhost:5000/info')
        if response.status_code == 200:
            info = response.json()
            print(f"API: {info['name']} v{info['version']}")
            print(f"Description: {info['description']}")
            print(f"Supported formats: {', '.join(info['capabilities']['supported_formats'])}")
            print(f"Max file size: {info['capabilities']['max_file_size']}")
            print(f"Accuracy: {info['capabilities']['accuracy']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run API demos"""
    print("🚀 Image Text Extraction API Demo")
    print("=" * 60)
    print("Make sure the API is running: python api.py")
    print("API should be available at: http://localhost:5000")
    print("=" * 60)
    
    # Wait for user to start API
    input("Press Enter when the API is running...")
    
    # Check if API is running
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code != 200:
            print("❌ API is not responding. Please start the API first.")
            return
    except:
        print("❌ API is not running. Please start the API first.")
        print("Run: python api.py")
        return
    
    print("✅ API is running! Starting demos...\n")
    
    # Run demos
    demo_api_info()
    demo_single_image()
    demo_batch_processing()
    
    print("\n🎉 Demo completed!")
    print("Check the API documentation for more details.")

if __name__ == "__main__":
    main()
