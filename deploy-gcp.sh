#!/bin/bash

# Google Cloud Deployment Script for Advanced OCR API
# This script deploys the full-featured OCR API to Google Cloud Run

set -e

echo "🚀 Deploying Advanced OCR API to Google Cloud..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please authenticate with Google Cloud:"
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
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
echo "🏗️  Building and deploying with Cloud Build..."
gcloud builds submit --config cloudbuild.yaml .

# Get the service URL
SERVICE_URL=$(gcloud run services describe extract-text-api --region=us-central1 --format="value(status.url)")

echo "✅ Deployment complete!"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "🧪 Test your API:"
echo "curl $SERVICE_URL/health"
echo "curl $SERVICE_URL/info"
echo ""
echo "📊 Monitor your service:"
echo "gcloud run services describe extract-text-api --region=us-central1"
