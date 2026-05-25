#!/bin/bash

# Fix Existing Code Engine Deployment
# This script updates your existing application with correct configuration

set -e

echo "=========================================="
echo "Fix Banking Model Validation Deployment"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}ℹ $1${NC}"; }

# ==================== CONFIGURATION ====================

# Your existing setup
PROJECT_NAME="COE-Dev"
BACKEND_APP_NAME="bankingmodel-v-backend-v2"
GITHUB_REPO="https://github.com/ankur-diwan/bmv-app-v6"
GITHUB_BRANCH="main"

# ==================== STEP 1: CHECK CREDENTIALS ====================

echo "Step 1: Checking environment variables..."
echo ""

if [ -z "$WATSONX_API_KEY" ]; then
    print_error "WATSONX_API_KEY not set"
    echo "Run: export WATSONX_API_KEY='your_key'"
    exit 1
fi

if [ -z "$WATSONX_PROJECT_ID" ]; then
    print_error "WATSONX_PROJECT_ID not set"
    echo "Run: export WATSONX_PROJECT_ID='your_project_id'"
    exit 1
fi

if [ -z "$COS_API_KEY" ]; then
    print_error "COS_API_KEY not set"
    echo "Run: export COS_API_KEY='your_cos_key'"
    exit 1
fi

if [ -z "$COS_RESOURCE_INSTANCE_ID" ]; then
    print_error "COS_RESOURCE_INSTANCE_ID not set"
    echo "Run: export COS_RESOURCE_INSTANCE_ID='your_cos_instance_id'"
    exit 1
fi

print_success "All credentials are set"

# ==================== STEP 2: LOGIN AND SELECT PROJECT ====================

echo ""
echo "Step 2: Connecting to IBM Cloud..."
echo ""

# Login if needed
if ! ibmcloud target &> /dev/null; then
    print_info "Logging in to IBM Cloud..."
    ibmcloud login --sso
fi

# Select project
print_info "Selecting project: $PROJECT_NAME"
ibmcloud ce project select --name "$PROJECT_NAME"
print_success "Project selected"

# ==================== STEP 3: CREATE/UPDATE SECRETS ====================

echo ""
echo "Step 3: Creating/updating secrets..."
echo ""

# watsonx credentials
print_info "Creating watsonx-credentials secret..."
ibmcloud ce secret delete --name watsonx-credentials --force 2>/dev/null || true
ibmcloud ce secret create --name watsonx-credentials \
    --from-literal WATSONX_API_KEY="$WATSONX_API_KEY" \
    --from-literal WATSONX_PROJECT_ID="$WATSONX_PROJECT_ID" \
    --from-literal WATSONX_SPACE_ID="${WATSONX_SPACE_ID:-}" \
    --from-literal WATSONX_URL="https://us-south.ml.cloud.ibm.com"
print_success "watsonx-credentials created"

# COS credentials
print_info "Creating cos-credentials secret..."
ibmcloud ce secret delete --name cos-credentials --force 2>/dev/null || true
ibmcloud ce secret create --name cos-credentials \
    --from-literal COS_API_KEY="$COS_API_KEY" \
    --from-literal COS_RESOURCE_INSTANCE_ID="$COS_RESOURCE_INSTANCE_ID" \
    --from-literal COS_ENDPOINT_URL="${COS_ENDPOINT_URL:-https://s3.us-south.cloud-object-storage.appdomain.cloud}" \
    --from-literal COS_BUCKET_NAME="${COS_BUCKET_NAME:-bankvalidationapp}"
print_success "cos-credentials created"

# COS HMAC (optional)
if [ -n "$COS_ACCESS_KEY_ID" ] && [ -n "$COS_SECRET_ACCESS_KEY" ]; then
    print_info "Creating cos-hmac-credentials secret..."
    ibmcloud ce secret delete --name cos-hmac-credentials --force 2>/dev/null || true
    ibmcloud ce secret create --name cos-hmac-credentials \
        --from-literal COS_ACCESS_KEY_ID="$COS_ACCESS_KEY_ID" \
        --from-literal COS_SECRET_ACCESS_KEY="$COS_SECRET_ACCESS_KEY"
    print_success "cos-hmac-credentials created"
fi

# ==================== STEP 4: UPDATE BACKEND APPLICATION ====================

echo ""
echo "Step 4: Updating backend application..."
echo ""

print_info "Updating $BACKEND_APP_NAME with correct configuration..."
print_info "This will trigger a rebuild (5-10 minutes)..."

ibmcloud ce app update --name "$BACKEND_APP_NAME" \
    --build-source "$GITHUB_REPO" \
    --build-context-dir "backend" \
    --build-commit "$GITHUB_BRANCH" \
    --strategy dockerfile \
    --dockerfile "Dockerfile" \
    --build-size large \
    --build-timeout 900 \
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
    --wait \
    --wait-timeout 900

print_success "Backend application updated!"

# ==================== STEP 5: GET STATUS ====================

echo ""
echo "Step 5: Checking deployment status..."
echo ""

# Get app details
BACKEND_URL=$(ibmcloud ce app get --name "$BACKEND_APP_NAME" --output json | grep -o '"url":"[^"]*' | cut -d'"' -f4)

if [ -n "$BACKEND_URL" ]; then
    print_success "Backend URL: $BACKEND_URL"
    
    # Test health endpoint
    echo ""
    print_info "Testing health endpoint (waiting 30 seconds for app to start)..."
    sleep 30
    
    if curl -s -f "$BACKEND_URL/health" > /dev/null 2>&1; then
        print_success "Health check passed!"
        curl -s "$BACKEND_URL/health" | python3 -m json.tool 2>/dev/null || curl -s "$BACKEND_URL/health"
    else
        print_error "Health check failed"
        print_info "Check logs with: ibmcloud ce app logs --name $BACKEND_APP_NAME"
    fi
else
    print_error "Could not get backend URL"
fi

# ==================== STEP 6: VIEW LOGS ====================

echo ""
echo "Step 6: Recent logs..."
echo ""

print_info "Last 20 log lines:"
ibmcloud ce app logs --name "$BACKEND_APP_NAME" --tail 20 || true

# ==================== COMPLETION ====================

echo ""
echo "=========================================="
echo "✓ UPDATE COMPLETE!"
echo "=========================================="
echo ""
echo "Backend URL: $BACKEND_URL"
echo ""
echo "Useful commands:"
echo "  View logs:    ibmcloud ce app logs --name $BACKEND_APP_NAME --follow"
echo "  Get status:   ibmcloud ce app get --name $BACKEND_APP_NAME"
echo "  List apps:    ibmcloud ce app list"
echo "  Test health:  curl $BACKEND_URL/health"
echo ""

if [ -n "$BACKEND_URL" ]; then
    print_success "Deployment fixed! Test at: $BACKEND_URL"
else
    print_error "Deployment may have issues. Check logs above."
fi

# Made with Bob
