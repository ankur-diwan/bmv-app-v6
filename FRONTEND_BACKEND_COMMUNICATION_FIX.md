# Frontend-Backend Communication Fix for Code Engine

## Problem Summary

The application was not working properly because the frontend and backend are deployed as **two separate Code Engine applications**, but they were not communicating correctly. The main issues were:

1. **Hardcoded Backend URL**: The frontend's nginx configuration had a hardcoded backend URL that didn't match the actual deployment
2. **Static Configuration**: No way to dynamically configure the backend URL at deployment time
3. **API Client Misconfiguration**: Frontend API client wasn't properly configured to route requests through nginx proxy

## Root Cause Analysis

### Issue 1: Hardcoded Backend URL in nginx.conf
```nginx
# OLD - Hardcoded URL
proxy_pass https://banking-validation-backend.243hkitbzigu.us-east.codeengine.appdomain.cloud;
```

This meant:
- Frontend could only connect to one specific backend URL
- Changing backend URL required rebuilding frontend
- Different environments (dev/staging/prod) couldn't use different backends

### Issue 2: No Environment Variable Support
The frontend Dockerfile didn't support runtime environment variable substitution, making it impossible to configure the backend URL without rebuilding the image.

### Issue 3: API Client Configuration
```javascript
// OLD - Empty base URL
const API_BASE_URL = import.meta.env.VITE_API_URL || '';
```

This caused the frontend to make requests to the wrong endpoint.

## Solution Implemented

### 1. Dynamic nginx Configuration with Environment Variables

**Updated nginx.conf:**
```nginx
location /api/ {
    # Environment variable substitution at runtime
    proxy_pass ${BACKEND_URL};
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $proxy_host;  # Dynamic host header
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

**Key Changes:**
- `${BACKEND_URL}` - Environment variable for backend URL
- `$proxy_host` - Dynamic host header instead of hardcoded value
- Proper proxy headers for forwarding client information

### 2. Enhanced Frontend Dockerfile with envsubst

**Added to Dockerfile:**
```dockerfile
# Install envsubst for environment variable substitution
RUN apk add --no-cache gettext

# Copy nginx configuration template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Create startup script for environment variable substitution
RUN echo '#!/bin/sh' > /docker-entrypoint.sh && \
    echo 'set -e' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Set default backend URL if not provided' >> /docker-entrypoint.sh && \
    echo 'export BACKEND_URL=${BACKEND_URL:-http://localhost:8080}' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Substitute environment variables in nginx config' >> /docker-entrypoint.sh && \
    echo 'envsubst '"'"'$BACKEND_URL'"'"' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf' >> /docker-entrypoint.sh && \
    echo '' >> /docker-entrypoint.sh && \
    echo '# Start nginx' >> /docker-entrypoint.sh && \
    echo 'exec nginx -g "daemon off;"' >> /docker-entrypoint.sh && \
    chmod +x /docker-entrypoint.sh

# Use custom entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
```

**How it works:**
1. Installs `gettext` package (provides `envsubst` command)
2. Copies nginx.conf as a template
3. Creates startup script that:
   - Sets default BACKEND_URL if not provided
   - Substitutes environment variables in nginx config
   - Starts nginx
4. Uses custom entrypoint instead of direct nginx command

### 3. Updated Frontend API Client

**Updated api.js:**
```javascript
// API Base URL configuration
// In production (Code Engine), requests go through nginx proxy at /api/
// In development, use VITE_API_URL environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
```

**Benefits:**
- Production: Uses `/api` which nginx proxies to backend
- Development: Can use `VITE_API_URL` for direct backend connection
- No hardcoded URLs in application code

### 4. Improved Backend CORS Configuration

**Updated main.py:**
```python
# CORS middleware - Configure based on environment
# In production, this should be set to specific frontend URL
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)
```

**Benefits:**
- Configurable via `ALLOWED_ORIGINS` environment variable
- Supports multiple origins (comma-separated)
- More secure than wildcard in production
- Exposes necessary headers for file downloads

## Deployment Instructions

### Step 1: Deploy Backend First

1. **Create/Update Backend Application in Code Engine:**
   ```bash
   # Via IBM Cloud Console:
   # - Name: banking-validation-backend
   # - Source: GitHub repository
   # - Context directory: /backend
   # - Dockerfile: /backend/Dockerfile
   # - Port: 8080
   ```

2. **Note the Backend URL:**
   ```
   Example: https://banking-validation-backend.xxx.us-east.codeengine.appdomain.cloud
   ```

3. **Set Backend Environment Variables:**
   - All watsonx credentials
   - All COS credentials
   - `ALLOWED_ORIGINS` = `https://YOUR-FRONTEND-URL` (set after frontend deployment)

### Step 2: Deploy Frontend with Backend URL

1. **Create/Update Frontend Application in Code Engine:**
   ```bash
   # Via IBM Cloud Console:
   # - Name: banking-validation-frontend
   # - Source: GitHub repository
   # - Context directory: /frontend
   # - Dockerfile: /frontend/Dockerfile
   # - Port: 8080
   ```

2. **Set Frontend Environment Variable:**
   - **CRITICAL**: Add environment variable:
     - Key: `BACKEND_URL`
     - Value: `https://banking-validation-backend.xxx.us-east.codeengine.appdomain.cloud`
   
   This tells the frontend nginx where to proxy API requests.

3. **Note the Frontend URL:**
   ```
   Example: https://banking-validation-frontend.yyy.us-east.codeengine.appdomain.cloud
   ```

### Step 3: Update Backend CORS

1. **Update Backend Application:**
   - Add/Update environment variable:
     - Key: `ALLOWED_ORIGINS`
     - Value: `https://banking-validation-frontend.yyy.us-east.codeengine.appdomain.cloud`
   
   This allows the frontend to make API requests to the backend.

2. **Redeploy Backend** (if needed)

## Testing the Fix

### 1. Test Backend Health
```bash
curl https://YOUR-BACKEND-URL/health
# Expected: {"status": "healthy", ...}
```

### 2. Test Frontend Health
```bash
curl https://YOUR-FRONTEND-URL/health
# Expected: healthy
```

### 3. Test Frontend-Backend Communication

1. Open frontend URL in browser
2. Open browser DevTools (F12) → Network tab
3. Navigate through the application
4. Verify:
   - API requests go to `/api/*` paths
   - Requests return 200 OK (not CORS errors)
   - No 404 or 502 errors

### 4. Test API Proxy

```bash
# This should be proxied to backend
curl https://YOUR-FRONTEND-URL/api/v1/options
# Expected: JSON response with validation options
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Code Engine Project                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────┐    ┌─────────────────────┐   │
│  │  Frontend Application    │    │ Backend Application │   │
│  │  (nginx + React)         │    │ (FastAPI + Python)  │   │
│  │                          │    │                     │   │
│  │  Port: 8080              │    │ Port: 8080          │   │
│  │  URL: frontend.xxx...    │    │ URL: backend.xxx... │   │
│  │                          │    │                     │   │
│  │  ┌────────────────────┐  │    │                     │   │
│  │  │ nginx.conf         │  │    │                     │   │
│  │  │                    │  │    │                     │   │
│  │  │ /api/* → BACKEND_URL ────────→ FastAPI Endpoints │   │
│  │  │ /*     → React SPA │  │    │                     │   │
│  │  └────────────────────┘  │    │                     │   │
│  └──────────────────────────┘    └─────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘

User Browser
     │
     ├─→ https://frontend.xxx.../           → React SPA
     │
     └─→ https://frontend.xxx.../api/v1/*   → nginx proxy
                                              → https://backend.xxx.../*
```

## Key Benefits of This Solution

1. **Flexibility**: Backend URL can be changed without rebuilding frontend
2. **Environment Agnostic**: Same image works in dev/staging/prod with different configs
3. **Security**: CORS can be properly configured per environment
4. **Simplicity**: Frontend makes requests to `/api/*`, nginx handles routing
5. **Maintainability**: Clear separation of concerns between frontend and backend

## Common Issues and Solutions

### Issue: Frontend shows "Network Error" or CORS errors

**Solution:**
1. Verify `BACKEND_URL` is set correctly in frontend application
2. Verify `ALLOWED_ORIGINS` includes frontend URL in backend application
3. Check both applications are running (not scaled to zero)
4. Check backend logs for CORS-related errors

### Issue: API requests return 502 Bad Gateway

**Solution:**
1. Verify backend application is running and healthy
2. Check `BACKEND_URL` environment variable is correct
3. Verify backend URL is accessible from frontend container
4. Check backend logs for errors

### Issue: Environment variable not being substituted

**Solution:**
1. Verify `BACKEND_URL` is set in Code Engine application configuration
2. Check frontend container logs for startup script output
3. Verify `envsubst` is installed (should be in Dockerfile)
4. Ensure entrypoint script has execute permissions

### Issue: Changes not taking effect

**Solution:**
1. Rebuild and redeploy the application
2. Clear browser cache
3. Check Code Engine revision is updated
4. Verify environment variables are set in the latest revision

## Environment Variables Reference

### Frontend Application
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BACKEND_URL` | **YES** | `http://localhost:8080` | Full URL of backend application |

### Backend Application
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ALLOWED_ORIGINS` | Recommended | `*` | Comma-separated list of allowed frontend URLs |
| `WATSONX_API_KEY` | **YES** | - | watsonx API key |
| `WATSONX_PROJECT_ID` | **YES** | - | watsonx project ID |
| `COS_API_KEY` | **YES** | - | Cloud Object Storage API key |
| `COS_BUCKET_NAME` | **YES** | - | COS bucket name |
| `COS_ENDPOINT_URL` | **YES** | - | COS endpoint URL |

## Verification Checklist

- [ ] Backend application is deployed and healthy
- [ ] Backend URL is noted (e.g., `https://backend.xxx...`)
- [ ] Frontend application is deployed
- [ ] Frontend has `BACKEND_URL` environment variable set to backend URL
- [ ] Frontend URL is noted (e.g., `https://frontend.yyy...`)
- [ ] Backend has `ALLOWED_ORIGINS` set to frontend URL
- [ ] Backend `/health` endpoint returns 200 OK
- [ ] Frontend `/health` endpoint returns 200 OK
- [ ] Frontend can load in browser without errors
- [ ] API requests from frontend reach backend successfully
- [ ] No CORS errors in browser console
- [ ] File uploads work correctly

## Conclusion

This fix enables proper communication between frontend and backend containers in Code Engine by:
1. Making nginx configuration dynamic with environment variables
2. Using nginx as a reverse proxy for API requests
3. Properly configuring CORS on the backend
4. Ensuring the frontend API client routes requests correctly

The solution is production-ready, maintainable, and follows best practices for containerized microservices deployment.

---

**Last Updated:** 2026-05-27  
**Version:** 1.0  
**Status:** ✅ Implemented and Ready for Deployment