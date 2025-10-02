#!/bin/bash

# Google Compute Engine Deployment Script for Advanced OCR API
# This script deploys the full-featured OCR API to Compute Engine

set -e

echo "🚀 Deploying Advanced OCR API to Google Compute Engine..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "�� Please authenticate with Google Cloud:"
    gcloud auth login
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No project set. Please set a project:"
    echo "   gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Project: $PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable compute.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create VM instance
echo "🏗️  Creating Compute Engine instance..."
gcloud compute instances create ocr-api-instance \
    --zone=us-central1-a \
    --machine-type=e2-standard-4 \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-standard \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --tags=ocr-api \
    --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y docker.io
    systemctl start docker
    systemctl enable docker
    usermod -aG docker $USER
    docker run -d -p 8080:8080 --name ocr-api gcr.io/'$PROJECT_ID'/extract-text-api:latest'

# Create firewall rule
echo "🔥 Creating firewall rule..."
gcloud compute firewall-rules create allow-ocr-api \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --target-tags ocr-api

# Get the external IP
EXTERNAL_IP=$(gcloud compute instances describe ocr-api-instance --zone=us-central1-a --format="value(networkInterfaces[0].accessConfigs[0].natIP)")

echo "✅ Deployment complete!"
echo "🌐 Service URL: http://$EXTERNAL_IP:8080"
echo ""
echo "🧪 Test your API:"
echo "curl http://$EXTERNAL_IP:8080/health"
echo "curl http://$EXTERNAL_IP:8080/info"
echo ""
echo "📊 Monitor your instance:"
echo "gcloud compute instances describe ocr-api-instance --zone=us-central1-a"
