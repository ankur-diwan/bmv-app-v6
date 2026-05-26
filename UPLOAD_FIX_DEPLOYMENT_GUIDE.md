# Document Upload Fix - Deployment Guide

## 🎯 Overview
This guide documents the fixes implemented to ensure document upload works correctly on Code Engine and that uploaded documents are used for validation (matching local behavior).

## 🔧 Changes Made

### 1. Added COS Integration to Upload Endpoints
**File: `backend/main.py`**

#### Changes:
- Added `from utils.cos_client import get_cos_client` import (line 22)
- Added `cos_client = None` to global instances (line 45)
- Initialize COS client in startup event (lines 149-156)
- Added COS upload logic in batch upload endpoint (lines 841-868)
- Store COS key in document metadata (line 881)
- Store dataset info with COS keys (lines 896-901)

#### What it does:
- Files are now uploaded to BOTH local storage AND COS bucket
- COS keys are stored in document metadata for later retrieval
- Gracefully handles COS unavailability (falls back to local only)

### 2. Modified Validation to Use Uploaded Data
**File: `backend/agents/validation_orchestrator.py`**

#### Changes:
- Added imports: `pandas`, `tempfile`, `os` (lines 10-12)
- Added `cos_client` attribute and `set_cos_client()` method (lines 32-36)
- Completely rewrote `_generate_validation_data()` method (lines 195-235)
- Added new `_load_csv_from_cos()` method (lines 237-262)

#### What it does:
- **First**: Checks COS for uploaded train/test/oot datasets
- **If found**: Downloads and uses uploaded CSV files
- **If not found**: Falls back to synthetic data generation
- Logs all actions for debugging

### 3. Connected COS Client to Orchestrator
**File: `backend/main.py`**

#### Changes:
- Pass COS client to orchestrator after initialization (line 150)

#### What it does:
- Enables orchestrator to access COS for loading datasets

---

## 📋 Deployment Steps

### Step 1: Update Backend Code
The code changes are already committed. Deploy the updated backend:

```bash
# Navigate to project directory
cd /Users/ad/workspace/banking-model-validation-code-engine\ v6\ CE

# Build and push backend image
docker build -t us.icr.io/banking-validation/backend:latest -f backend/Dockerfile .
docker push us.icr.io/banking-validation/backend:latest

# Update Code Engine application
ibmcloud ce application update banking-validation-backend \
  --image us.icr.io/banking-validation/backend:latest
```

### Step 2: Configure COS Environment Variables
Add COS credentials to the backend application:

```bash
ibmcloud ce application update banking-validation-backend \
  --env COS_API_KEY=<your_cos_api_key> \
  --env COS_RESOURCE_INSTANCE_ID=<your_cos_resource_instance_id> \
  --env COS_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud \
  --env COS_BUCKET_NAME=bankingvalidationapp \
  --env COS_ACCESS_KEY_ID=<your_hmac_access_key> \
  --env COS_SECRET_ACCESS_KEY=<your_hmac_secret_key>
```

**Get your credentials from `.env` file:**
```bash
cat .env | grep COS_
```

### Step 3: Fix Frontend Configuration (CRITICAL)
The frontend needs to know the backend URL:

```bash
# Get backend URL
BACKEND_URL=$(ibmcloud ce application get banking-validation-backend --output json | jq -r '.status.url')

# Update frontend with correct backend URL
ibmcloud ce application update banking-validation-frontend \
  --env VITE_API_URL=$BACKEND_URL

# Rebuild frontend (required for env vars to take effect)
ibmcloud ce application update banking-validation-frontend \
  --build-source . \
  --build-context-dir frontend
```

---

## 🧪 Testing the Fix

### Test 1: Upload Documents
1. Open frontend URL in browser
2. Navigate to document upload section
3. Upload train.csv, test.csv, and oot.csv files
4. Verify upload success message

### Test 2: Check COS Upload
```bash
# Check backend logs
ibmcloud ce application logs banking-validation-backend --tail 50

# Look for:
# ✓ Uploaded to COS: uploads/DOC_xxx_train.csv
# ✓ Uploaded to COS: uploads/DOC_xxx_test.csv
# ✓ Uploaded to COS: uploads/DOC_xxx_oot.csv
```

### Test 3: Run Validation
1. Start a validation workflow
2. Check logs for dataset loading:

```bash
ibmcloud ce application logs banking-validation-backend --tail 100

# Look for:
# Checking for uploaded datasets in COS...
# ✓ Found uploaded datasets in COS, loading...
# ✓ Loaded datasets - Train: 10000, Test: 3000, OOT: 2000
```

### Test 4: Verify Behavior Matches Local
- Upload same files locally and on Code Engine
- Run validation on both
- Compare results - should be identical

---

## 🔍 Verification Checklist

- [ ] Backend deployed with latest code
- [ ] COS environment variables configured
- [ ] Frontend VITE_API_URL configured correctly
- [ ] Frontend rebuilt after env var update
- [ ] Documents upload successfully
- [ ] COS upload logs appear in backend
- [ ] Validation uses uploaded datasets
- [ ] Results match local behavior

---

## 🐛 Troubleshooting

### Issue: Upload still fails with 405 error
**Solution:** Frontend VITE_API_URL not configured
```bash
# Check frontend env vars
ibmcloud ce application get banking-validation-frontend --output json | jq '.spec.template.containers[0].env'

# Should show VITE_API_URL pointing to backend
```

### Issue: Files upload but validation uses synthetic data
**Solution:** COS credentials not configured or incorrect
```bash
# Check backend logs for COS initialization
ibmcloud ce application logs banking-validation-backend | grep "COS"

# Should see: "IBM Cloud Object Storage: Connected"
# If not, check COS_API_KEY and COS_RESOURCE_INSTANCE_ID
```

### Issue: COS upload fails
**Solution:** Check COS bucket permissions
```bash
# Verify bucket exists and is accessible
# Check COS_BUCKET_NAME matches actual bucket name
# Verify API key has write permissions
```

### Issue: Validation can't find uploaded files
**Solution:** Files not uploaded to correct COS path
```bash
# Check COS bucket contents
# Files should be in: uploads/DOC_xxx_filename.csv
# Verify get_latest_files_by_type() finds them
```

---

## 📊 Architecture After Fix

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Frontend (Nginx)                                        │
│  - VITE_API_URL → backend URL ✅ FIXED                  │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ POST /api/upload-documents
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Backend (FastAPI)                                       │
│  1. Save to /app/uploads (local)                         │
│  2. Upload to COS bucket ✅ NEW                          │
│  3. Store COS key in metadata ✅ NEW                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Upload files
                     ▼
┌─────────────────────────────────────────────────────────┐
│  IBM Cloud Object Storage                                │
│  Bucket: bankingvalidationapp                            │
│  Path: uploads/DOC_xxx_filename.csv                      │
└─────────────────────────────────────────────────────────┘

When validation runs:
┌─────────────────────────────────────────────────────────┐
│  Validation Orchestrator                                 │
│  1. Check COS for uploaded files ✅ NEW                  │
│  2. Download and use if found ✅ NEW                     │
│  3. Fallback to synthetic data if not found              │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ Success Criteria

After deployment, the system should:

1. ✅ Accept document uploads through frontend
2. ✅ Store documents in COS bucket
3. ✅ Use uploaded CSV files for validation
4. ✅ Match local behavior exactly
5. ✅ Gracefully handle COS unavailability
6. ✅ Log all operations for debugging

---

## 📝 Notes

- **COS is optional**: System works without COS (local storage only)
- **Dual storage**: Files stored both locally and in COS for redundancy
- **Automatic fallback**: If COS unavailable, uses local storage
- **Smart validation**: Prefers uploaded data, falls back to synthetic
- **Production ready**: All error handling and logging in place

---

## 🚀 Quick Deploy Script

```bash
#!/bin/bash
# Quick deployment script

# Get backend URL
BACKEND_URL=$(ibmcloud ce application get banking-validation-backend --output json | jq -r '.status.url')

# Update backend
docker build -t us.icr.io/banking-validation/backend:latest -f backend/Dockerfile .
docker push us.icr.io/banking-validation/backend:latest
ibmcloud ce application update banking-validation-backend \
  --image us.icr.io/banking-validation/backend:latest

# Configure COS (replace with your values)
ibmcloud ce application update banking-validation-backend \
  --env COS_API_KEY=$(grep COS_API_KEY .env | cut -d'=' -f2) \
  --env COS_RESOURCE_INSTANCE_ID=$(grep COS_RESOURCE_INSTANCE_ID .env | cut -d'=' -f2) \
  --env COS_ENDPOINT_URL=$(grep COS_ENDPOINT_URL .env | cut -d'=' -f2) \
  --env COS_BUCKET_NAME=$(grep COS_BUCKET_NAME .env | cut -d'=' -f2) \
  --env COS_ACCESS_KEY_ID=$(grep COS_ACCESS_KEY_ID .env | cut -d'=' -f2) \
  --env COS_SECRET_ACCESS_KEY=$(grep COS_SECRET_ACCESS_KEY .env | cut -d'=' -f2)

# Fix frontend
ibmcloud ce application update banking-validation-frontend \
  --env VITE_API_URL=$BACKEND_URL \
  --build-source . \
  --build-context-dir frontend

echo "✅ Deployment complete!"
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $(ibmcloud ce application get banking-validation-frontend --output json | jq -r '.status.url')"
```

Save as `deploy-upload-fix.sh` and run:
```bash
chmod +x deploy-upload-fix.sh
./deploy-upload-fix.sh