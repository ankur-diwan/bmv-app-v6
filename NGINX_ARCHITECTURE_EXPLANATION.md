# Nginx Architecture in Banking Model Validation Application

## Overview

In this application, **nginx serves as a reverse proxy and web server** for the frontend. Here's why and how it's used:

---

## Architecture Flow

```
User Browser
    ↓
Frontend (nginx on port 8080)
    ↓ (for /api/* requests)
Backend (FastAPI on port 8080)
```

---

## Why Use Nginx?

### 1. **Serve Static Frontend Files**
- The React/Vite frontend is built into static files (HTML, CSS, JS)
- Nginx efficiently serves these static files
- Much faster and lighter than running a Node.js server

### 2. **Reverse Proxy for API Requests**
- **Problem:** Browser security (CORS) prevents frontend from directly calling backend on different domain
- **Solution:** Nginx proxies API requests from frontend to backend
- User sees: `https://frontend.com/api/upload`
- Nginx forwards to: `https://backend.com/api/upload`

### 3. **Single Domain for User**
- User only needs to know one URL (frontend)
- All API calls go through `/api/*` path on same domain
- Nginx handles routing to backend behind the scenes

---

## Current Configuration Breakdown

```nginx
location /api/ {
    proxy_pass ${BACKEND_URL};  # ← THIS IS THE ISSUE!
    # ... other settings
}
```

### The Problem

**Current behavior:**
- User requests: `https://frontend.com/api/upload-documents`
- Nginx tries to proxy to: `${BACKEND_URL}` (e.g., `https://backend.com`)
- **Missing the `/api/` path!**
- Backend receives: `https://backend.com/upload-documents` ❌
- Backend expects: `https://backend.com/api/upload-documents` ✅

**Result:** 502 Bad Gateway (backend doesn't have `/upload-documents` endpoint)

---

## The Fix Needed

```nginx
location /api/ {
    proxy_pass ${BACKEND_URL}/api/;  # ← Add /api/ to preserve the path
    # ... other settings
}
```

**Fixed behavior:**
- User requests: `https://frontend.com/api/upload-documents`
- Nginx proxies to: `${BACKEND_URL}/api/` + `upload-documents`
- Backend receives: `https://backend.com/api/upload-documents` ✅
- Backend responds correctly!

---

## Additional Benefits of Nginx

### 1. **Client-Side Routing (SPA Support)**
```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```
- Handles React Router
- All routes serve index.html
- React takes over routing in browser

### 2. **Static Asset Caching**
```nginx
location ~* \.(js|css|png|jpg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```
- Browsers cache static files for 1 year
- Faster page loads
- Reduced server load

### 3. **Security Headers**
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
```
- Protects against clickjacking
- Prevents MIME type sniffing
- Enhances security

### 4. **Compression**
```nginx
gzip on;
gzip_types text/plain text/css application/json;
```
- Compresses responses
- Reduces bandwidth
- Faster page loads

---

## Environment Variable Substitution

The Dockerfile uses `envsubst` to replace `${BACKEND_URL}` at container startup:

```dockerfile
envsubst '$BACKEND_URL' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf
```

**At runtime:**
- `BACKEND_URL` environment variable is set (e.g., `https://backend.com`)
- `envsubst` replaces `${BACKEND_URL}` in nginx config
- Nginx starts with the actual backend URL

---

## Why Not Direct Backend Calls?

### Option 1: Direct Backend Calls (Without Nginx Proxy)
```javascript
// Frontend code
fetch('https://backend.com/api/upload')
```

**Problems:**
- ❌ CORS issues (different domains)
- ❌ Exposes backend URL to users
- ❌ Can't change backend without rebuilding frontend
- ❌ More complex CORS configuration needed

### Option 2: Nginx Proxy (Current Approach)
```javascript
// Frontend code
fetch('/api/upload')  // Same domain!
```

**Benefits:**
- ✅ No CORS issues (same domain)
- ✅ Backend URL hidden from users
- ✅ Can change backend by updating env variable
- ✅ Simpler configuration

---

## Summary

**Nginx in this application:**
1. **Web Server:** Serves React static files
2. **Reverse Proxy:** Forwards `/api/*` requests to backend
3. **Router:** Handles SPA client-side routing
4. **Optimizer:** Caches, compresses, and secures content

**The current issue:** The proxy_pass directive is missing `/api/` path, causing 502 errors when uploading files.

**The fix:** Add `/api/` to proxy_pass so the full path is forwarded to the backend.

---

## Visualization

### Current (Broken)
```
Browser → /api/upload-documents
    ↓
Nginx → proxy_pass ${BACKEND_URL}
    ↓
Backend receives: /upload-documents ❌ (404 Not Found → 502 Bad Gateway)
```

### Fixed
```
Browser → /api/upload-documents
    ↓
Nginx → proxy_pass ${BACKEND_URL}/api/
    ↓
Backend receives: /api/upload-documents ✅ (200 OK)
```

---

**Conclusion:** Nginx is essential for serving the frontend and proxying API requests. The fix is simple: ensure the `/api/` path is preserved when proxying to the backend.