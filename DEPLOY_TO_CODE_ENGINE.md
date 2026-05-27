# Deploy to IBM Cloud Code Engine - Step by Step Guide

## Prerequisites Checklist

Before deploying, ensure you have:
- [ ] IBM Cloud account with Code Engine access
- [ ] Code Engine project created (e.g., `banking-validation`)
- [ ] watsonx.ai credentials ready
- [ ] Cloud Object Storage bucket created and credentials ready
- [ ] Changes pushed to GitHub (✅ Done)

## Deployment Steps

### Step 1: Deploy Backend Application

#### Option A: Using IBM Cloud Console (Recommended)

1. **Navigate to Code Engine**
   - Go to https://cloud.ibm.com/codeengine/overview
   - Select your project (or create one: `banking-validation`)

2. **Create Backend Application**
   - Click "Applications" → "Create"
   - **Name:** `banking-validation-backend`
   - **Code source:** Source code
   - **Code repo URL:** `https://github.com/ankur-diwan/bmv-app-v6.git`
   - **Branch:** `main`
   - **Context directory:** `/backend`
   - **Dockerfile:** `Dockerfile`

3. **Configure Build**
   - Build strategy: Dockerfile
   - Dockerfile location: `/backend/Dockerfile`
   - Build timeout: 10 minutes
   - Build resources: Medium (2 vCPU, 4 GB)

4. **Configure Runtime**
   - CPU: 1 vCPU
   - Memory: 2 GB
   - Min instances: 0 (or 1 for always-on)
   - Max instances: 10
   - Port: 8080
   - Request timeout: 300 seconds

5. **Add Environment Variables**
   
   Create these secrets first (Secrets and configmaps → Create):
   
   **Secret: `watsonx-credentials`**
   ```
   WATSONX_API_KEY=<your-watsonx-api-key>
   WATSONX_PROJECT_ID=<your-project-id>
   WATSONX_SPACE_ID=<your-space-id>
   ```
   
   **Secret: `cos-credentials`**
   ```
   COS_API_KEY=<your-cos-api-key>
   COS_RESOURCE_INSTANCE_ID=<your-cos-instance-id>
   COS_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud
   COS_BUCKET_NAME=bankvalidationapp
   ```
   
   Then add these as literal environment variables:
   ```
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   VALIDATION_TEMP_DIR=/app/temp/cos_validation
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   ALLOWED_ORIGINS=*
   ```
   
   Reference the secrets you created above.

6. **Create and Wait**
   - Click "Create"
   - Wait for build to complete (5-10 minutes)
   - **IMPORTANT:** Note the backend URL once deployed
   - Example: `https://banking-validation-backend.xxx.us-east.codeengine.appdomain.cloud`

7. **Test Backend**
   ```bash
   curl https://YOUR-BACKEND-URL/health
   # Should return: {"status": "healthy", ...}
   ```

#### Option B: Using IBM Cloud CLI

```bash
# Login to IBM Cloud
ibmcloud login

# Target your Code Engine project
ibmcloud ce project select --name banking-validation

# Create backend application
ibmcloud ce app create \
  --name banking-validation-backend \
  --build-source https://github.com/ankur-diwan/bmv-app-v6.git \
  --build-context-dir backend \
  --build-dockerfile Dockerfile \
  --port 8080 \
  --cpu 1 \
  --memory 2G \
  --min-scale 0 \
  --max-scale 10 \
  --env-from-secret watsonx-credentials \
  --env-from-secret cos-credentials \
  --env ENVIRONMENT=production \
  --env LOG_LEVEL=INFO \
  --env VALIDATION_TEMP_DIR=/app/temp/cos_validation \
  --env WATSONX_URL=https://us-south.ml.cloud.ibm.com \
  --env ALLOWED_ORIGINS=*

# Get the backend URL
ibmcloud ce app get --name banking-validation-backend --output url
```

---

### Step 2: Deploy Frontend Application

**CRITICAL:** You need the backend URL from Step 1 before proceeding!

#### Option A: Using IBM Cloud Console (Recommended)

1. **Create Frontend Application**
   - In Code Engine project, click "Applications" → "Create"
   - **Name:** `banking-validation-frontend`
   - **Code source:** Source code
   - **Code repo URL:** `https://github.com/ankur-diwan/bmv-app-v6.git`
   - **Branch:** `main`
   - **Context directory:** `/frontend`
   - **Dockerfile:** `Dockerfile`

2. **Configure Build**
   - Build strategy: Dockerfile
   - Dockerfile location: `/frontend/Dockerfile`
   - Build timeout: 10 minutes
   - Build resources: Medium (2 vCPU, 4 GB)

3. **Configure Runtime**
   - CPU: 0.5 vCPU
   - Memory: 1 GB
   - Min instances: 0 (or 1 for always-on)
   - Max instances: 5
   - Port: 8080
   - Request timeout: 60 seconds

4. **Add Environment Variable - CRITICAL!**
   
   Add this literal environment variable:
   ```
   BACKEND_URL=https://banking-validation-backend.xxx.us-east.codeengine.appdomain.cloud
   ```
   
   **Replace with your actual backend URL from Step 1!**

5. **Create and Wait**
   - Click "Create"
   - Wait for build to complete (5-10 minutes)
   - Note the frontend URL
   - Example: `https://banking-validation-frontend.yyy.us-east.codeengine.appdomain.cloud`

6. **Test Frontend**
   ```bash
   curl https://YOUR-FRONTEND-URL/health
   # Should return: healthy
   ```

#### Option B: Using IBM Cloud CLI

```bash
# Create frontend application
ibmcloud ce app create \
  --name banking-validation-frontend \
  --build-source https://github.com/ankur-diwan/bmv-app-v6.git \
  --build-context-dir frontend \
  --build-dockerfile Dockerfile \
  --port 8080 \
  --cpu 0.5 \
  --memory 1G \
  --min-scale 0 \
  --max-scale 5 \
  --env BACKEND_URL=https://YOUR-BACKEND-URL-FROM-STEP-1

# Get the frontend URL
ibmcloud ce app get --name banking-validation-frontend --output url
```

---

### Step 3: Update Backend CORS

Now that you have the frontend URL, update the backend to allow requests from it.

#### Option A: Using IBM Cloud Console

1. Go to backend application
2. Click "Environment variables"
3. Find `ALLOWED_ORIGINS` and update it:
   ```
   ALLOWED_ORIGINS=https://banking-validation-frontend.yyy.us-east.codeengine.appdomain.cloud
   ```
4. Click "Save and deploy"

#### Option B: Using IBM Cloud CLI

```bash
ibmcloud ce app update \
  --name banking-validation-backend \
  --env ALLOWED_ORIGINS=https://YOUR-FRONTEND-URL
```

---

### Step 4: Verify Deployment

1. **Test Backend Health**
   ```bash
   curl https://YOUR-BACKEND-URL/health
   ```
   Expected: `{"status": "healthy", ...}`

2. **Test Frontend Health**
   ```bash
   curl https://YOUR-FRONTEND-URL/health
   ```
   Expected: `healthy`

3. **Test API Proxy**
   ```bash
   curl https://YOUR-FRONTEND-URL/api/v1/options
   ```
   Expected: JSON response with validation options

4. **Test in Browser**
   - Open `https://YOUR-FRONTEND-URL` in browser
   - Open DevTools (F12) → Network tab
   - Navigate through the application
   - Verify:
     - ✅ No CORS errors
     - ✅ API requests to `/api/*` return 200 OK
     - ✅ Application loads correctly

---

## Quick Reference

### Your Deployment URLs

Fill these in after deployment:

```
Backend URL:  https://banking-validation-backend._____.codeengine.appdomain.cloud
Frontend URL: https://banking-validation-frontend._____.codeengine.appdomain.cloud
```

### Environment Variables Summary

**Backend:**
- `WATSONX_API_KEY` (from secret)
- `WATSONX_PROJECT_ID` (from secret)
- `WATSONX_SPACE_ID` (from secret)
- `COS_API_KEY` (from secret)
- `COS_RESOURCE_INSTANCE_ID` (from secret)
- `COS_ENDPOINT_URL` (from secret)
- `COS_BUCKET_NAME` (from secret)
- `ENVIRONMENT=production`
- `LOG_LEVEL=INFO`
- `VALIDATION_TEMP_DIR=/app/temp/cos_validation`
- `WATSONX_URL=https://us-south.ml.cloud.ibm.com`
- `ALLOWED_ORIGINS=<frontend-url>`

**Frontend:**
- `BACKEND_URL=<backend-url>` ← **CRITICAL!**

---

## Troubleshooting

### Build Fails

**Check:**
- GitHub repository is accessible
- Context directory is correct (`/backend` or `/frontend`)
- Dockerfile exists in the context directory
- Build logs for specific errors

**Solution:**
```bash
# View build logs
ibmcloud ce buildrun logs --name <buildrun-name>
```

### Application Won't Start

**Check:**
- Application logs for errors
- Environment variables are set correctly
- Port 8080 is exposed
- Health endpoint is accessible

**Solution:**
```bash
# View application logs
ibmcloud ce app logs --name banking-validation-backend
ibmcloud ce app logs --name banking-validation-frontend
```

### CORS Errors

**Check:**
- `ALLOWED_ORIGINS` in backend includes frontend URL
- Frontend URL is correct (no trailing slash)
- Both applications are running

**Solution:**
Update backend `ALLOWED_ORIGINS` to include frontend URL

### API Requests Fail (502 Bad Gateway)

**Check:**
- `BACKEND_URL` in frontend is correct
- Backend application is running and healthy
- Backend URL is accessible

**Solution:**
```bash
# Test backend directly
curl https://YOUR-BACKEND-URL/health

# Update frontend BACKEND_URL if needed
ibmcloud ce app update \
  --name banking-validation-frontend \
  --env BACKEND_URL=https://YOUR-CORRECT-BACKEND-URL
```

---

## Post-Deployment

### Monitor Applications

```bash
# View application status
ibmcloud ce app list

# View application details
ibmcloud ce app get --name banking-validation-backend
ibmcloud ce app get --name banking-validation-frontend

# View logs
ibmcloud ce app logs --name banking-validation-backend --follow
ibmcloud ce app logs --name banking-validation-frontend --follow
```

### Update Applications

When you push new changes to GitHub:

```bash
# Trigger rebuild for backend
ibmcloud ce app update --name banking-validation-backend --build-source https://github.com/ankur-diwan/bmv-app-v6.git

# Trigger rebuild for frontend
ibmcloud ce app update --name banking-validation-frontend --build-source https://github.com/ankur-diwan/bmv-app-v6.git
```

Or use the IBM Cloud Console:
- Go to application → "Submit build"

---

## Success Criteria

✅ Backend application deployed and healthy  
✅ Frontend application deployed and healthy  
✅ Backend URL noted and configured in frontend  
✅ Frontend URL noted and configured in backend CORS  
✅ `/health` endpoints return 200 OK  
✅ Frontend loads in browser without errors  
✅ API requests work (no CORS errors)  
✅ File uploads work correctly  

---

**Need Help?**
- Review: [`FRONTEND_BACKEND_COMMUNICATION_FIX.md`](FRONTEND_BACKEND_COMMUNICATION_FIX.md)
- Review: [`CODE_ENGINE_DEPLOYMENT_GUIDE.md`](CODE_ENGINE_DEPLOYMENT_GUIDE.md)
- Check application logs for detailed error messages
- Verify all environment variables are set correctly

---

**Last Updated:** 2026-05-27  
**Status:** Ready for Deployment