#!/bin/bash

# Banking Model Validation - IBM Cloud Code Engine Deployment Script
# This script deploys the application using IBM Cloud CLI

set -e  # Exit on any error

echo "=========================================="
echo "Banking Model Validation - Code Engine Deployment"
echo "=========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# ==================== CONFIGURATION ====================
# Update these values with your actual credentials

# GitHub Configuration
GITHUB_REPO="https://github.com/ankur-diwan/bmv-app-v6"
GITHUB_BRANCH="main"

# Code Engine Configuration
PROJECT_NAME="COE-Dev"  # Your existing project name
BACKEND_APP_NAME="bankingmodel-v-backend-v2"
FRONTEND_APP_NAME="bankingmodel-v-frontend-v2"

# watsonx.ai Credentials (REQUIRED)
WATSONX_API_KEY="${WATSONX_API_KEY:-}"
WATSONX_PROJECT_ID="${WATSONX_PROJECT_ID:-}"
WATSONX_SPACE_ID="${WATSONX_SPACE_ID:-}"
WATSONX_URL="https://us-south.ml.cloud.ibm.com"

# Cloud Object Storage Credentials (REQUIRED)
COS_API_KEY="${COS_API_KEY:-}"
COS_RESOURCE_INSTANCE_ID="${COS_RESOURCE_INSTANCE_ID:-}"
COS_ENDPOINT_URL="${COS_ENDPOINT_URL:-https://s3.us-south.cloud-object-storage.appdomain.cloud}"
COS_BUCKET_NAME="${COS_BUCKET_NAME:-bankvalidationapp}"

# Optional: COS HMAC Credentials (for presigned URLs)
COS_ACCESS_KEY_ID="${COS_ACCESS_KEY_ID:-}"
COS_SECRET_ACCESS_KEY="${COS_SECRET_ACCESS_KEY:-}"

# ==================== VALIDATION ====================

echo "Step 1: Validating prerequisites..."
echo ""

# Check if IBM Cloud CLI is installed
if ! command -v ibmcloud &> /dev/null; then
    print_error "IBM Cloud CLI is not installed"
    echo "Install from: https://cloud.ibm.com/docs/cli?topic=cli-getting-started"
    exit 1
fi
print_success "IBM Cloud CLI is installed"

# Check if Code Engine plugin is installed
if ! ibmcloud plugin list | grep -q "code-engine"; then
    print_info "Installing Code Engine plugin..."
    ibmcloud plugin install code-engine -f
fi
print_success "Code Engine plugin is installed"

# Check for required credentials
if [ -z "$WATSONX_API_KEY" ]; then
    print_error "WATSONX_API_KEY is not set"
    echo "Set it with: export WATSONX_API_KEY='your_api_key'"
    exit 1
fi

if [ -z "$WATSONX_PROJECT_ID" ]; then
    print_error "WATSONX_PROJECT_ID is not set"
    echo "Set it with: export WATSONX_PROJECT_ID='your_project_id'"
    exit 1
fi

if [ -z "$COS_API_KEY" ]; then
    print_error "COS_API_KEY is not set"
    echo "Set it with: export COS_API_KEY='your_cos_api_key'"
    exit 1
fi

if [ -z "$COS_RESOURCE_INSTANCE_ID" ]; then
    print_error "COS_RESOURCE_INSTANCE_ID is not set"
    echo "Set it with: export COS_RESOURCE_INSTANCE_ID='your_cos_instance_id'"
    exit 1
fi

print_success "All required credentials are set"
echo ""

# ==================== LOGIN ====================

echo "Step 2: Logging in to IBM Cloud..."
echo ""

# Check if already logged in
if ! ibmcloud target &> /dev/null; then
    print_info "Please login to IBM Cloud"
    ibmcloud login --sso
else
    print_success "Already logged in to IBM Cloud"
fi

# ==================== SELECT PROJECT ====================

echo ""
echo "Step 3: Selecting Code Engine project..."
echo ""

# Select the project
ibmcloud ce project select --name "$PROJECT_NAME"
print_success "Selected project: $PROJECT_NAME"

# ==================== CREATE SECRETS ====================

echo ""
echo "Step 4: Creating secrets..."
echo ""

# Create watsonx credentials secret
print_info "Creating watsonx-credentials secret..."
ibmcloud ce secret create --name watsonx-credentials \
    --from-literal WATSONX_API_KEY="$WATSONX_API_KEY" \
    --from-literal WATSONX_PROJECT_ID="$WATSONX_PROJECT_ID" \
    --from-literal WATSONX_SPACE_ID="$WATSONX_SPACE_ID" \
    --from-literal WATSONX_URL="$WATSONX_URL" \
    2>/dev/null || ibmcloud ce secret update --name watsonx-credentials \
    --from-literal WATSONX_API_KEY="$WATSONX_API_KEY" \
    --from-literal WATSONX_PROJECT_ID="$WATSONX_PROJECT_ID" \
    --from-literal WATSONX_SPACE_ID="$WATSONX_SPACE_ID" \
    --from-literal WATSONX_URL="$WATSONX_URL"
print_success "watsonx-credentials secret created/updated"

# Create COS credentials secret
print_info "Creating cos-credentials secret..."
ibmcloud ce secret create --name cos-credentials \
    --from-literal COS_API_KEY="$COS_API_KEY" \
    --from-literal COS_RESOURCE_INSTANCE_ID="$COS_RESOURCE_INSTANCE_ID" \
    --from-literal COS_ENDPOINT_URL="$COS_ENDPOINT_URL" \
    --from-literal COS_BUCKET_NAME="$COS_BUCKET_NAME" \
    2>/dev/null || ibmcloud ce secret update --name cos-credentials \
    --from-literal COS_API_KEY="$COS_API_KEY" \
    --from-literal COS_RESOURCE_INSTANCE_ID="$COS_RESOURCE_INSTANCE_ID" \
    --from-literal COS_ENDPOINT_URL="$COS_ENDPOINT_URL" \
    --from-literal COS_BUCKET_NAME="$COS_BUCKET_NAME"
print_success "cos-credentials secret created/updated"

# Create COS HMAC credentials secret (if provided)
if [ -n "$COS_ACCESS_KEY_ID" ] && [ -n "$COS_SECRET_ACCESS_KEY" ]; then
    print_info "Creating cos-hmac-credentials secret..."
    ibmcloud ce secret create --name cos-hmac-credentials \
        --from-literal COS_ACCESS_KEY_ID="$COS_ACCESS_KEY_ID" \
        --from-literal COS_SECRET_ACCESS_KEY="$COS_SECRET_ACCESS_KEY" \
        2>/dev/null || ibmcloud ce secret update --name cos-hmac-credentials \
        --from-literal COS_ACCESS_KEY_ID="$COS_ACCESS_KEY_ID" \
        --from-literal COS_SECRET_ACCESS_KEY="$COS_SECRET_ACCESS_KEY"
    print_success "cos-hmac-credentials secret created/updated"
fi

# ==================== DEPLOY BACKEND ====================

echo ""
echo "Step 5: Deploying backend application..."
echo ""

print_info "This will take 5-10 minutes for the build to complete..."

# Check if app exists
if ibmcloud ce app get --name "$BACKEND_APP_NAME" &> /dev/null; then
    print_info "Updating existing backend application..."
    ibmcloud ce app update --name "$BACKEND_APP_NAME" \
        --build-source "$GITHUB_REPO" \
        --build-context-dir "backend" \
        --build-commit "$GITHUB_BRANCH" \
        --env ENVIRONMENT=production \
        --env LOG_LEVEL=INFO \
        --env VALIDATION_TEMP_DIR=/app/temp/cos_validation \
        --env-from-secret watsonx-credentials \
        --env-from-secret cos-credentials \
        --cpu 1 \
        --memory 2G \
        --min-scale 0 \
        --max-scale 10 \
        --port 8080 \
        --wait
else
    print_info "Creating new backend application..."
    ibmcloud ce app create --name "$BACKEND_APP_NAME" \
        --build-source "$GITHUB_REPO" \
        --build-context-dir "backend" \
        --build-commit "$GITHUB_BRANCH" \
        --strategy dockerfile \
        --env ENVIRONMENT=production \
        --env LOG_LEVEL=INFO \
        --env VALIDATION_TEMP_DIR=/app/temp/cos_validation \
        --env-from-secret watsonx-credentials \
        --env-from-secret cos-credentials \
        --cpu 1 \
        --memory 2G \
        --min-scale 0 \
        --max-scale 10 \
        --port 8080 \
        --wait
fi

# Get backend URL
BACKEND_URL=$(ibmcloud ce app get --name "$BACKEND_APP_NAME" --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)
print_success "Backend deployed successfully!"
print_info "Backend URL: $BACKEND_URL"

# Test backend health
echo ""
print_info "Testing backend health endpoint..."
sleep 10  # Wait for app to be ready
if curl -s "$BACKEND_URL/health" | grep -q "healthy"; then
    print_success "Backend health check passed!"
else
    print_error "Backend health check failed. Check logs with: ibmcloud ce app logs --name $BACKEND_APP_NAME"
fi

# ==================== DEPLOY FRONTEND ====================

echo ""
echo "Step 6: Deploying frontend application..."
echo ""

print_info "This will take 5-10 minutes for the build to complete..."

# Check if app exists
if ibmcloud ce app get --name "$FRONTEND_APP_NAME" &> /dev/null; then
    print_info "Updating existing frontend application..."
    ibmcloud ce app update --name "$FRONTEND_APP_NAME" \
        --build-source "$GITHUB_REPO" \
        --build-context-dir "frontend" \
        --build-commit "$GITHUB_BRANCH" \
        --build-arg VITE_API_URL="$BACKEND_URL" \
        --cpu 0.5 \
        --memory 1G \
        --min-scale 0 \
        --max-scale 5 \
        --port 8080 \
        --wait
else
    print_info "Creating new frontend application..."
    ibmcloud ce app create --name "$FRONTEND_APP_NAME" \
        --build-source "$GITHUB_REPO" \
        --build-context-dir "frontend" \
        --build-commit "$GITHUB_BRANCH" \
        --strategy dockerfile \
        --build-arg VITE_API_URL="$BACKEND_URL" \
        --cpu 0.5 \
        --memory 1G \
        --min-scale 0 \
        --max-scale 5 \
        --port 8080 \
        --wait
fi

# Get frontend URL
FRONTEND_URL=$(ibmcloud ce app get --name "$FRONTEND_APP_NAME" --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)
print_success "Frontend deployed successfully!"
print_info "Frontend URL: $FRONTEND_URL"

# ==================== UPDATE BACKEND CORS ====================

echo ""
echo "Step 7: Updating backend CORS configuration..."
echo ""

ibmcloud ce app update --name "$BACKEND_APP_NAME" \
    --env ALLOWED_ORIGINS="$FRONTEND_URL" \
    --wait

print_success "CORS configuration updated"

# ==================== DEPLOYMENT COMPLETE ====================

echo ""
echo "=========================================="
echo "✓ DEPLOYMENT COMPLETE!"
echo "=========================================="
echo ""
echo "Application URLs:"
echo "  Backend:  $BACKEND_URL"
echo "  Frontend: $FRONTEND_URL"
echo ""
echo "Next steps:"
echo "  1. Open frontend URL in browser: $FRONTEND_URL"
echo "  2. Test backend health: $BACKEND_URL/health"
echo "  3. View backend logs: ibmcloud ce app logs --name $BACKEND_APP_NAME"
echo "  4. View frontend logs: ibmcloud ce app logs --name $FRONTEND_APP_NAME"
echo ""
echo "Monitoring:"
echo "  - View apps: ibmcloud ce app list"
echo "  - Get app details: ibmcloud ce app get --name $BACKEND_APP_NAME"
echo "  - View logs: ibmcloud ce app logs --name $BACKEND_APP_NAME --follow"
echo ""
print_success "Deployment completed successfully!"

# Made with Bob
