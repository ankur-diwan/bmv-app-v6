#!/bin/bash

# Verification Script for Frontend-Backend Communication Fix
# This script helps verify that the fix has been properly applied

set -e

echo "=========================================="
echo "Frontend-Backend Communication Verification"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a file contains a pattern
check_file_contains() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description"
        return 1
    fi
}

# Function to check if a file does NOT contain a pattern
check_file_not_contains() {
    local file=$1
    local pattern=$2
    local description=$3
    
    if ! grep -q "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $description"
        return 0
    else
        echo -e "${RED}✗${NC} $description"
        return 1
    fi
}

echo "Checking Frontend Configuration..."
echo "-----------------------------------"

# Check nginx.conf
check_file_contains "frontend/nginx.conf" '\${BACKEND_URL}' "nginx.conf uses environment variable for backend URL"
check_file_not_contains "frontend/nginx.conf" 'banking-validation-backend.243hkitbzigu' "nginx.conf does not have hardcoded backend URL"
check_file_contains "frontend/nginx.conf" '\$proxy_host' "nginx.conf uses dynamic proxy host header"

echo ""

# Check Dockerfile
check_file_contains "frontend/Dockerfile" 'gettext' "Dockerfile installs envsubst (gettext package)"
check_file_contains "frontend/Dockerfile" 'docker-entrypoint.sh' "Dockerfile creates entrypoint script"
check_file_contains "frontend/Dockerfile" 'ENTRYPOINT.*docker-entrypoint.sh' "Dockerfile uses custom entrypoint"
check_file_contains "frontend/Dockerfile" 'nginx.conf /etc/nginx/templates' "Dockerfile copies nginx.conf as template"

echo ""

# Check API client
check_file_contains "frontend/src/services/api.js" "'/api'" "API client uses /api base URL"
check_file_contains "frontend/src/services/api.js" 'VITE_API_URL.*\/api' "API client has proper fallback configuration"

echo ""
echo "Checking Backend Configuration..."
echo "-----------------------------------"

# Check main.py CORS
check_file_contains "backend/main.py" 'ALLOWED_ORIGINS' "Backend uses ALLOWED_ORIGINS environment variable"
check_file_contains "backend/main.py" 'allow_origins=allowed_origins' "Backend CORS uses configurable origins"
check_file_contains "backend/main.py" 'expose_headers.*Content-Disposition' "Backend exposes Content-Disposition header"

echo ""
echo "=========================================="
echo "Configuration Check Complete"
echo "=========================================="
echo ""

# Summary
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Commit and push these changes to GitHub"
echo "2. Deploy backend application first and note its URL"
echo "3. Deploy frontend application with BACKEND_URL environment variable"
echo "4. Update backend ALLOWED_ORIGINS with frontend URL"
echo ""
echo "For detailed deployment instructions, see:"
echo "  - FRONTEND_BACKEND_COMMUNICATION_FIX.md"
echo "  - CODE_ENGINE_DEPLOYMENT_GUIDE.md"
echo ""

# Check if we're in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}Git Status:${NC}"
    echo "Modified files:"
    git status --short | grep -E "frontend/|backend/main.py|FRONTEND_BACKEND_COMMUNICATION_FIX.md" || echo "  (no relevant changes detected)"
    echo ""
    echo "To commit these changes:"
    echo "  git add frontend/ backend/main.py FRONTEND_BACKEND_COMMUNICATION_FIX.md verify-communication-fix.sh"
    echo "  git commit -m 'Fix frontend-backend communication for Code Engine deployment'"
    echo "  git push origin main"
fi

echo ""
echo -e "${GREEN}All checks passed!${NC} The fix has been properly applied."
echo ""

# Made with Bob
