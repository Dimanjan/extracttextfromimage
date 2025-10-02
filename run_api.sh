#!/bin/bash
# Script to run the Image Text Extraction API

echo "🚀 Starting Image Text Extraction API..."
echo "API will be available at: http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo "API docs: http://localhost:5000/info"
echo ""

# Activate virtual environment
source venv/bin/activate

# Install API dependencies if needed
if [ ! -f "venv/lib/python3.12/site-packages/flask" ]; then
    echo "Installing API dependencies..."
    pip install -r requirements_api.txt
fi

# Start the API
echo "Starting Flask API server..."
python api.py
