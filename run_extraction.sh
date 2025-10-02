#!/bin/bash
# Script to run advanced text extraction

echo "Running ADVANCED text extraction..."
echo "Uses EasyOCR + Advanced Tesseract with text reconstruction"
echo "Optimized for scattered graphic design text"
echo ""

source venv/bin/activate
python extract_text.py
