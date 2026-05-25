# Quick Start: Deploy to IBM Cloud Code Engine

This is a condensed guide for experienced users. For detailed instructions, see [CODE_ENGINE_DEPLOYMENT_GUIDE.md](CODE_ENGINE_DEPLOYMENT_GUIDE.md).

---

## Prerequisites

✅ IBM Cloud account  
✅ GitHub repository with this code  
✅ IBM watsonx.ai instance  
✅ IBM Cloud Object Storage (COS) bucket

**Note:** PostgreSQL database is NOT required - the app uses COS for all storage.

---

## Step 1: Prepare Credentials (5 minutes)

Gather these values:

### Required:
- `WATSONX_API_KEY` - From watsonx.ai service credentials
- `WATSONX_PROJECT_ID` - From watsonx.ai project
- `COS_API_KEY` - From Cloud Object Storage service credentials
- `COS_RESOURCE_INSTANCE_ID` - From COS instance details
- `COS_BUCKET_NAME` - Your COS bucket name (e.g., `bankvalidationapp`)

### Optional (for presigned URLs):
- `COS_ACCESS_KEY_ID` - HMAC access key
- `COS_SECRET_ACCESS_KEY` - HMAC secret key

---

## Step 2: Create COS Bucket (3 minutes)

1. Go to [IBM Cloud Console](https://cloud.ibm.com)
2. Search "Object Storage" → Select your instance or create new
3. Create bucket:
   - Name: `bankvalidationapp` (or your choice)
   - Resiliency: Regional
   - Location: Same as Code Engine (e.g., us-south)
   - Storage class: Standard
4. Note the bucket name and endpoint URL

---

## Step 3: Create Code Engine Project (2 minutes)

1. Go to [IBM Cloud Console](https://cloud.ibm.com)
2. Search "Code Engine" → Create project
3. Name: `banking-validation`
4. Region: `us-south` (or your preferred region)

---

## Step 4: Create Secrets (3 minutes)

In Code Engine project → Secrets and configmaps → Create:

**Secret 1: `watsonx-credentials`**
```
WATSONX_API_KEY=your_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_SPACE_ID=your_space_id
```

**Secret 2: `cos-credentials`**
```
COS_API_KEY=your_cos_api_key
COS_RESOURCE_INSTANCE_ID=your_cos_resource_instance_id
COS_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_BUCKET_NAME=bankvalidationapp
```

**Optional Secret 3: `cos-hmac-credentials`** (for presigned URLs)
```
COS_ACCESS_KEY_ID=your_hmac_access_key
COS_SECRET_ACCESS_KEY=your_hmac_secret_key
```

---

## Step 5: Deploy Backend (10 minutes)

1. **Create Application**
   - Name: `banking-validation-backend`
   - Source: GitHub repository URL
   - Branch: `main`
   - Context: `/backend`
   - Dockerfile: `/backend/Dockerfile`

2. **Configure Build**
   - Strategy: Dockerfile
   - Resources: Medium (2 vCPU, 4 GB)

3. **Configure Runtime**
   - CPU: 1 vCPU
   - Memory: 2 GB
   - Port: 8080
   - Min/Max instances: 0/10

4. **Add Environment Variables**
   ```
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   VALIDATION_TEMP_DIR=/app/temp/cos_validation
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   ```

5. **Bind Secrets**
   - Add `watsonx-credentials`
   - Add `cos-credentials`
   - Add `cos-hmac-credentials` (if created)

6. **Create & Wait**
   - Build takes ~5-10 minutes
   - Note the backend URL

7. **Verify**
   ```bash
   curl https://YOUR-BACKEND-URL/health
   # Should return: {"status": "healthy", ...}
   ```

---

## Step 6: Deploy Frontend (10 minutes)

1. **Create Application**
   - Name: `banking-validation-frontend`
   - Source: Same GitHub repository
   - Branch: `main`
   - Context: `/frontend`
   - Dockerfile: `/frontend/Dockerfile`

2. **Configure Build**
   - Strategy: Dockerfile
   - Resources: Medium (2 vCPU, 4 GB)
   - **Build argument:**
     - Key: `VITE_API_URL`
     - Value: `https://YOUR-BACKEND-URL` (from Step 5)

3. **Configure Runtime**
   - CPU: 0.5 vCPU
   - Memory: 1 GB
   - Port: 8080
   - Min/Max instances: 0/5

4. **Create & Wait**
   - Build takes ~5-10 minutes
   - Note the frontend URL

5. **Verify**
   - Open `https://YOUR-FRONTEND-URL` in browser
   - Should see the application UI

---

## Step 7: Update Backend CORS (2 minutes)

1. Edit backend application
2. Add environment variable:
   ```
   ALLOWED_ORIGINS=https://YOUR-FRONTEND-URL
   ```
3. Save (triggers redeploy)

---

## Step 8: Test Integration (5 minutes)

1. Open frontend URL in browser
2. Navigate through the UI
3. Test file upload (files go to COS)
4. Run a validation
5. Check that API calls work
6. Verify documents are stored in COS bucket

---

## Architecture Overview

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│    Frontend     │ (Code Engine)
│   React + Vite  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│     Backend     │ (Code Engine)
│  FastAPI + AI   │
└────┬────────┬───┘
     │        │
     ▼        ▼
┌─────────┐ ┌──────────────┐
│watsonx.ai│ │ Cloud Object │
│          │ │   Storage    │
└──────────┘ └──────────────┘
```

**Key Points:**
- ✅ No database required
- ✅ All documents stored in COS
- ✅ Stateless architecture
- ✅ Auto-scaling enabled

---

## Troubleshooting

### Build Fails
```bash
# Check build logs in Code Engine console
# Common issues:
# - Missing dependencies in requirements.txt
# - Dockerfile syntax errors
# - Insufficient build resources
```

### App Won't Start
```bash
# Check application logs
# Common issues:
# - Missing environment variables
# - COS connection failed
# - Port not exposed (should be 8080)
```

### Frontend Can't Connect to Backend
```bash
# Check:
# - VITE_API_URL set correctly at build time
# - CORS configured in backend
# - Backend is running and accessible
```

### COS Connection Issues
```bash
# Verify:
# - COS_API_KEY is correct
# - COS_RESOURCE_INSTANCE_ID is correct
# - COS_BUCKET_NAME exists
# - Bucket is in same region as Code Engine
# - Bucket has public access or proper IAM policies
```

### File Upload Fails
```bash
# Check:
# - COS credentials are valid
# - Bucket exists and is accessible
# - Bucket has write permissions
# - Check backend logs for COS errors
```

---

## Quick Commands (IBM Cloud CLI)

```bash
# Install CLI
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh

# Login
ibmcloud login

# Target Code Engine
ibmcloud plugin install code-engine
ibmcloud ce project select --name banking-validation

# View apps
ibmcloud ce app list

# View logs
ibmcloud ce app logs --name banking-validation-backend --follow

# Update env var
ibmcloud ce app update --name banking-validation-backend \
  --env KEY=VALUE

# Restart app
ibmcloud ce app update --name banking-validation-backend
```

---

## URLs to Save

After deployment, save these URLs:

```
Backend:  https://banking-validation-backend.xxx.codeengine.appdomain.cloud
Frontend: https://banking-validation-frontend.xxx.codeengine.appdomain.cloud
COS Bucket: s3://bankvalidationapp
COS Endpoint: https://s3.us-south.cloud-object-storage.appdomain.cloud
```

---

## Cost Estimate

**Typical monthly costs:**
- Code Engine: $0-50 (depends on usage, free tier available)
- Cloud Object Storage: $0-20 (based on storage and requests)
- watsonx.ai: Variable (based on API usage)
- **Total: ~$0-70/month**

**Cost optimization tips:**
- Enable scale-to-zero for non-production
- Right-size CPU/memory allocations
- Use free tier where available
- Monitor COS storage and clean up old files
- Set lifecycle policies on COS bucket

---

## Next Steps

- [ ] Set up monitoring and alerts
- [ ] Configure custom domain (optional)
- [ ] Set up CI/CD pipeline (optional)
- [ ] Review security settings
- [ ] Configure COS lifecycle policies
- [ ] Set up COS bucket versioning
- [ ] Document for your team

---

## Support

- **Detailed Guide:** [CODE_ENGINE_DEPLOYMENT_GUIDE.md](CODE_ENGINE_DEPLOYMENT_GUIDE.md)
- **Checklist:** [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **IBM Cloud Docs:** https://cloud.ibm.com/docs/codeengine
- **COS Docs:** https://cloud.ibm.com/docs/cloud-object-storage
- **Issues:** Create GitHub issue in your repository

---

## Important Notes

1. **No Database Required**: This application uses IBM Cloud Object Storage for all data persistence. PostgreSQL is not needed.

2. **COS Bucket Setup**: Ensure your COS bucket is created before deployment and has appropriate access policies.

3. **HMAC Credentials**: Optional but recommended for generating presigned URLs for document downloads.

4. **Region Consistency**: Deploy Code Engine and COS in the same region for better performance and lower costs.

5. **Security**: Never commit credentials to GitHub. Always use Code Engine secrets.

---

**Total Time:** ~40 minutes  
**Difficulty:** Intermediate  
**Last Updated:** 2026-05-25