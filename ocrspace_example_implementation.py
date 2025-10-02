#!/usr/bin/env python3
"""
Complete OCR.space API implementation with examples
Based on our testing and real-world usage
"""

import requests
import json
import os
import base64
from pathlib import Path
from typing import Dict, Optional, Union

class OCRSpaceAPI:
    """
    Complete OCR.space API implementation
    """
    
    def __init__(self, api_key: str):
        """
        Initialize OCR.space API client
        
        Args:
            api_key (str): Your OCR.space API key
        """
        self.api_key = api_key
        self.base_url = "https://api.ocr.space/parse/image"
        self.timeout = 30
    
    def extract_text(self, image_path: str, language: str = "eng", 
                    overlay: bool = False, filetype: str = None) -> Dict:
        """
        Extract text from image file using file upload method
        
        Args:
            image_path (str): Path to image file
            language (str): Language code (default: "eng")
            overlay (bool): Generate overlay image (default: False)
            filetype (str): Specify file type (optional)
        
        Returns:
            Dict: Result with text, processing time, and success status
        """
        
        if not os.path.exists(image_path):
            return {
                'success': False,
                'error': f"Image not found: {image_path}",
                'text': ''
            }
        
        headers = {"apikey": self.api_key}
        
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'language': language,
                    'isOverlayRequired': overlay
                }
                
                if filetype:
                    data['filetype'] = filetype
                
                response = requests.post(
                    self.base_url, 
                    headers=headers, 
                    files=files, 
                    data=data,
                    timeout=self.timeout
                )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('IsErroredOnProcessing', False):
                    return {
                        'success': False,
                        'error': result.get('ErrorMessage', 'OCR processing failed'),
                        'text': ''
                    }
                
                if 'ParsedResults' in result and result['ParsedResults']:
                    parsed_text = result['ParsedResults'][0].get('ParsedText', '')
                    return {
                        'success': True,
                        'text': parsed_text,
                        'processing_time': result.get('ProcessingTimeInMilliseconds', 0),
                        'characters': len(parsed_text),
                        'words': len(parsed_text.split()),
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No text detected in image',
                        'text': ''
                    }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'text': ''
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timed out',
                'text': ''
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'text': ''
            }
    
    def extract_text_base64(self, image_path: str, language: str = "eng") -> Dict:
        """
        Extract text using base64 encoding method
        
        Args:
            image_path (str): Path to image file
            language (str): Language code (default: "eng")
        
        Returns:
            Dict: Result with text, processing time, and success status
        """
        
        if not os.path.exists(image_path):
            return {
                'success': False,
                'error': f"Image not found: {image_path}",
                'text': ''
            }
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
                base64_data = base64.b64encode(image_data).decode('utf-8')
            
            headers = {
                "apikey": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "base64Image": f"data:image/jpeg;base64,{base64_data}",
                "language": language,
                "isOverlayRequired": False
            }
            
            response = requests.post(
                self.base_url, 
                headers=headers, 
                json=payload, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('IsErroredOnProcessing', False):
                    return {
                        'success': False,
                        'error': result.get('ErrorMessage', 'OCR processing failed'),
                        'text': ''
                    }
                
                if 'ParsedResults' in result and result['ParsedResults']:
                    parsed_text = result['ParsedResults'][0].get('ParsedText', '')
                    return {
                        'success': True,
                        'text': parsed_text,
                        'processing_time': result.get('ProcessingTimeInMilliseconds', 0),
                        'characters': len(parsed_text),
                        'words': len(parsed_text.split()),
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No text detected in image',
                        'text': ''
                    }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'text': ''
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'text': ''
            }
    
    def extract_text_from_url(self, image_url: str, language: str = "eng") -> Dict:
        """
        Extract text from image URL
        
        Args:
            image_url (str): URL of the image
            language (str): Language code (default: "eng")
        
        Returns:
            Dict: Result with text, processing time, and success status
        """
        
        url = "https://api.ocr.space/parse/imageurl"
        headers = {"apikey": self.api_key}
        
        payload = {
            "url": image_url,
            "language": language
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('IsErroredOnProcessing', False):
                    return {
                        'success': False,
                        'error': result.get('ErrorMessage', 'OCR processing failed'),
                        'text': ''
                    }
                
                if 'ParsedResults' in result and result['ParsedResults']:
                    parsed_text = result['ParsedResults'][0].get('ParsedText', '')
                    return {
                        'success': True,
                        'text': parsed_text,
                        'processing_time': result.get('ProcessingTimeInMilliseconds', 0),
                        'characters': len(parsed_text),
                        'words': len(parsed_text.split()),
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No text detected in image',
                        'text': ''
                    }
            else:
                return {
                    'success': False,
                    'error': f"HTTP {response.status_code}: {response.text}",
                    'text': ''
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f"Request failed: {str(e)}",
                'text': ''
            }
    
    def batch_extract(self, image_paths: list, language: str = "eng") -> Dict:
        """
        Extract text from multiple images
        
        Args:
            image_paths (list): List of image file paths
            language (str): Language code (default: "eng")
        
        Returns:
            Dict: Results for all images
        """
        
        results = []
        successful = 0
        
        for i, image_path in enumerate(image_paths):
            print(f"Processing image {i+1}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            result = self.extract_text(image_path, language)
            result['image_path'] = image_path
            result['image_name'] = os.path.basename(image_path)
            
            if result['success']:
                successful += 1
            
            results.append(result)
        
        return {
            'results': results,
            'total_images': len(image_paths),
            'successful': successful,
            'success_rate': (successful / len(image_paths)) * 100 if image_paths else 0
        }

def main():
    """
    Example usage of OCRSpaceAPI
    """
    
    # Initialize API with your key
    api_key = "K89033969188957"  # Replace with your actual API key
    ocr = OCRSpaceAPI(api_key)
    
    print("🧪 OCR.space API Example")
    print("=" * 50)
    
    # Test with sample images
    image_samples = Path("image_samples")
    if image_samples.exists():
        image_files = list(image_samples.glob("*.png")) + list(image_samples.glob("*.jpg"))
        
        if image_files:
            print(f"Found {len(image_files)} images to test")
            print()
            
            # Test single image
            test_image = image_files[0]
            print(f"📤 Testing: {test_image.name}")
            
            result = ocr.extract_text(str(test_image))
            
            if result['success']:
                print("✅ Text extracted successfully!")
                print(f"⏱️  Processing time: {result['processing_time']}ms")
                print(f"📄 Characters: {result['characters']}")
                print(f"📄 Words: {result['words']}")
                print(f"📄 Text preview: {result['text'][:100]}...")
            else:
                print(f"❌ Error: {result['error']}")
            
            print()
            
            # Test batch processing
            print("📤 Batch processing all images...")
            batch_result = ocr.batch_extract([str(img) for img in image_files])
            
            print(f"📊 Batch Results:")
            print(f"   Total images: {batch_result['total_images']}")
            print(f"   Successful: {batch_result['successful']}")
            print(f"   Success rate: {batch_result['success_rate']:.1f}%")
            
            print()
            print("📄 Individual Results:")
            for result in batch_result['results']:
                status = "✅" if result['success'] else "❌"
                print(f"   {status} {result['image_name']}: {result['characters']} chars")
        
        else:
            print("❌ No image files found in image_samples/")
    else:
        print("❌ image_samples directory not found")
    
    print()
    print("🔍 Usage Tips:")
    print("- Use high-quality images for better results")
    print("- Supported formats: JPG, PNG, PDF")
    print("- Free tier: 25,000 requests/month")
    print("- Processing time: 0.6-1.2 seconds per image")

if __name__ == "__main__":
    main()
