# IBM Cloud Code Engine Deployment Guide
## Banking Model Validation System

This guide provides step-by-step instructions for deploying the Banking Model Validation System to IBM Cloud Code Engine using the UI and GitHub integration.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Pre-Deployment Preparation](#pre-deployment-preparation)
3. [Database Setup](#database-setup)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Environment Configuration](#environment-configuration)
7. [Testing the Deployment](#testing-the-deployment)
8. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
9. [Scaling and Updates](#scaling-and-updates)

---

## Prerequisites

### Required IBM Cloud Services
- IBM Cloud Account (with appropriate permissions)
- IBM watsonx.ai instance
- IBM Cloud Object Storage (COS) bucket
- GitHub account with repository access

**Note:** PostgreSQL database is NOT required - the application uses IBM Cloud Object Storage for all data persistence.

### Required Tools
- Web browser for IBM Cloud Console
- Git (for local testing)
- Optional: IBM Cloud CLI for advanced operations

### Cost Considerations
- Code Engine: Pay-per-use (free tier available)
- Cloud Object Storage: ~$0-20/month (based on storage and requests)
- watsonx.ai: Based on usage
- **Total estimated cost: ~$0-70/month**

---

## Pre-Deployment Preparation

### 1. Push Code to GitHub

Ensure your code is in a GitHub repository:

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Prepare for Code Engine deployment"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

### 2. Prepare Environment Variables

Review and update `.env.codeengine` file with your actual values:
- watsonx API credentials
- Cloud Object Storage credentials
- Security keys

**Important**: Never commit actual credentials to GitHub. Use Code Engine secrets instead.

### 3. Create Cloud Object Storage Bucket

1. **Create COS Instance** (if you don't have one)
   - Go to IBM Cloud Catalog
   - Search for "Object Storage"
   - Click "Create"
   - Choose a plan (Lite plan available for testing)
   - Click "Create"

2. **Create Bucket**
   - Go to your COS instance
   - Click "Create bucket"
   - Choose "Customize your bucket"
   - Configure:
     - Bucket name: `bankvalidationapp` (or your choice)
     - Resiliency: Regional
     - Location: Same as Code Engine (e.g., us-south)
     - Storage class: Standard
   - Click "Create bucket"

3. **Get COS Credentials**
   - Go to "Service credentials"
   - Click "New credential"
   - Enable "Include HMAC Credential" (for presigned URLs)
   - Copy:
     - `apikey` → COS_API_KEY
     - `resource_instance_id` → COS_RESOURCE_INSTANCE_ID
     - `endpoints` → Find your regional endpoint (e.g., https://s3.us-south.cloud-object-storage.appdomain.cloud)
     - `cos_hmac_keys.access_key_id` → COS_ACCESS_KEY_ID (optional)
     - `cos_hmac_keys.secret_access_key` → COS_SECRET_ACCESS_KEY (optional)

4. **Note Bucket Details**
   - Bucket name: `bankvalidationapp`
   - Endpoint URL: `https://s3.us-south.cloud-object-storage.appdomain.cloud`
   - Region: `us-south` (or your chosen region)

---

## Backend Deployment

### Step 1: Create Code Engine Project

1. **Navigate to Code Engine**
   - Log in to IBM Cloud Console
   - Search for "Code Engine" in the catalog
   - Click "Code Engine"

2. **Create Project**
   - Click "Create project"
   - Project name: `banking-validation`
   - Region: `us-south` (or your preferred region)
   - Resource group: Default or your preferred group
   - Click "Create"

### Step 2: Create Backend Application

1. **Start Application Creation**
   - In your Code Engine project, click "Applications"
   - Click "Create"

2. **Configure Source**
   - Name: `banking-validation-backend`
   - Code source: Select "Source code"
   - Code repo URL: `https://github.com/YOUR_USERNAME/YOUR_REPO`
   - Branch: `main`
   - Context directory: `/backend`
   - Dockerfile: `Dockerfile`

3. **Configure Build**
   - Build strategy: Dockerfile
   - Dockerfile location: `/backend/Dockerfile`
   - Build timeout: 10 minutes
   - Build resources: Medium (2 vCPU, 4 GB)

4. **Configure Runtime**
   - CPU and memory: 
     - CPU: 1 vCPU (can scale up later)
     - Memory: 2 GB
   - Min instances: 0 (scale to zero when idle)
   - Max instances: 10
   - Concurrency: 100
   - Request timeout: 300 seconds
   - Port: 8080

5. **Add Environment Variables**
   Click "Add environment variable" for each:
   
   **From Literal Values:**
   - `ENVIRONMENT` = `production`
   - `LOG_LEVEL` = `INFO`
   - `VALIDATION_TEMP_DIR` = `/app/temp/cos_validation`
   - `WATSONX_URL` = `https://us-south.ml.cloud.ibm.com`

   **From Secrets (Create secrets first):**
   - Create secret named `watsonx-credentials`:
     - `WATSONX_API_KEY` = your_api_key
     - `WATSONX_PROJECT_ID` = your_project_id
     - `WATSONX_SPACE_ID` = your_space_id
   
   - Create secret named `cos-credentials`:
     - `COS_API_KEY` = your_cos_api_key
     - `COS_RESOURCE_INSTANCE_ID` = your_cos_resource_instance_id
     - `COS_ENDPOINT_URL` = https://s3.us-south.cloud-object-storage.appdomain.cloud
     - `COS_BUCKET_NAME` = bankvalidationapp
   
   - Create secret named `cos-hmac-credentials` (optional, for presigned URLs):
     - `COS_ACCESS_KEY_ID` = your_hmac_access_key
     - `COS_SECRET_ACCESS_KEY` = your_hmac_secret_key

6. **Configure Domain**
   - Domain mappings: Use default Code Engine domain
   - Visibility: Public
   - Note the generated URL (e.g., `https://banking-validation-backend.xxx.codeengine.appdomain.cloud`)

7. **Create Application**
   - Review all settings
   - Click "Create"
   - Wait for build and deployment (5-10 minutes)

### Step 3: Verify Backend Deployment

1. **Check Build Status**
   - Go to "Image builds" tab
   - Verify build completed successfully
   - Check logs if there are errors

2. **Test Health Endpoint**
   - Open browser
   - Navigate to: `https://YOUR-BACKEND-URL/health`
   - Should return: `{"status": "healthy", ...}`

3. **Test API Root**
   - Navigate to: `https://YOUR-BACKEND-URL/`
   - Should return service information

---

## Frontend Deployment

### Step 1: Create Frontend Application

1. **Start Application Creation**
   - In Code Engine project, click "Applications"
   - Click "Create"

2. **Configure Source**
   - Name: `banking-validation-frontend`
   - Code source: Select "Source code"
   - Code repo URL: `https://github.com/YOUR_USERNAME/YOUR_REPO`
   - Branch: `main`
   - Context directory: `/frontend`
   - Dockerfile: `Dockerfile`

3. **Configure Build**
   - Build strategy: Dockerfile
   - Dockerfile location: `/frontend/Dockerfile`
   - Build arguments:
     - Key: `VITE_API_URL`
     - Value: `https://YOUR-BACKEND-URL` (from backend deployment)
   - Build timeout: 10 minutes
   - Build resources: Medium (2 vCPU, 4 GB)

4. **Configure Runtime**
   - CPU and memory:
     - CPU: 0.5 vCPU
     - Memory: 1 GB
   - Min instances: 0
   - Max instances: 5
   - Concurrency: 100
   - Request timeout: 60 seconds
   - Port: 8080

5. **Configure Domain**
   - Domain mappings: Use default Code Engine domain
   - Visibility: Public
   - Note the generated URL (e.g., `https://banking-validation-frontend.xxx.codeengine.appdomain.cloud`)

6. **Create Application**
   - Review all settings
   - Click "Create"
   - Wait for build and deployment (5-10 minutes)

### Step 2: Update Backend CORS

After frontend deployment, update backend CORS settings:

1. **Edit Backend Application**
   - Go to backend application
   - Click "Environment variables"
   - Add new variable:
     - `ALLOWED_ORIGINS` = `https://YOUR-FRONTEND-URL`
   - Save and redeploy

### Step 3: Verify Frontend Deployment

1. **Access Frontend**
   - Open browser
   - Navigate to: `https://YOUR-FRONTEND-URL`
   - Should see the application UI

2. **Test Health Endpoint**
   - Navigate to: `https://YOUR-FRONTEND-URL/health`
   - Should return: `healthy`

---

## Environment Configuration

### Creating Secrets in Code Engine

1. **Navigate to Secrets**
   - In Code Engine project
   - Click "Secrets and configmaps"
   - Click "Create"

2. **Create watsonx Credentials Secret**
   - Name: `watsonx-credentials`
   - Type: Generic secret
   - Add key-value pairs:
     - `WATSONX_API_KEY`: your_api_key
     - `WATSONX_PROJECT_ID`: your_project_id
     - `WATSONX_SPACE_ID`: your_space_id
   - Click "Create"

3. **Create COS Credentials Secret**
   - Name: `cos-credentials`
   - Type: Generic secret
   - Add key-value pairs:
     - `COS_API_KEY`: your_cos_api_key
     - `COS_RESOURCE_INSTANCE_ID`: your_cos_resource_instance_id
     - `COS_ENDPOINT_URL`: https://s3.us-south.cloud-object-storage.appdomain.cloud
     - `COS_BUCKET_NAME`: bankvalidationapp
   - Click "Create"

4. **Create COS HMAC Credentials Secret** (Optional, for presigned URLs)
   - Name: `cos-hmac-credentials`
   - Type: Generic secret
   - Add key-value pairs:
     - `COS_ACCESS_KEY_ID`: your_hmac_access_key
     - `COS_SECRET_ACCESS_KEY`: your_hmac_secret_key
   - Click "Create"

5. **Create Security Keys Secret**
   - Name: `security-keys`
   - Type: Generic secret
   - Add key-value pairs:
     - `SECRET_KEY`: generate_random_string_here
     - `JWT_SECRET`: generate_random_string_here
   - Click "Create"

### Binding Secrets to Applications

1. **Edit Backend Application**
   - Go to backend application
   - Click "Environment variables"
   - Click "Add" → "Reference to full secret"
   - Select each secret created above
   - Save

---

## Testing the Deployment

### 1. Backend API Tests

```bash
# Health check
curl https://YOUR-BACKEND-URL/health

# Get options
curl https://YOUR-BACKEND-URL/api/v1/options

# Test validation endpoint (requires authentication)
curl -X POST https://YOUR-BACKEND-URL/api/v1/validate \
  -H "Content-Type: application/json" \
  -d '{"model_name": "test", "product_type": "secured", ...}'
```

### 2. Frontend Tests

1. Open frontend URL in browser
2. Navigate through different pages
3. Test file upload functionality
4. Verify API calls work correctly
5. Check browser console for errors

### 3. Integration Tests

1. Upload test data files
2. Run validation
3. Generate reports
4. Verify document generation
5. Test watsonx integration

---

## Monitoring and Troubleshooting

### Viewing Logs

1. **Application Logs**
   - Go to application in Code Engine
   - Click "Logging"
   - View real-time logs
   - Filter by severity, time range

2. **Build Logs**
   - Go to "Image builds"
   - Click on specific build
   - View build logs

### Common Issues and Solutions

#### Issue: Build Fails

**Solution:**
- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Check build logs for specific errors
- Ensure sufficient build resources

#### Issue: Application Won't Start

**Solution:**
- Check application logs
- Verify environment variables are set correctly
- Ensure port 8080 is exposed
- Check health endpoint configuration

#### Issue: COS Connection Fails

**Solution:**
- Verify COS_API_KEY is correct
- Check COS_RESOURCE_INSTANCE_ID is correct
- Ensure COS_BUCKET_NAME exists
- Verify bucket is in same region as Code Engine
- Check bucket access permissions
- Review backend logs for COS errors

#### Issue: File Upload Fails

**Solution:**
- Verify COS credentials are valid
- Check bucket exists and is accessible
- Ensure bucket has write permissions
- Verify CORS settings on bucket (if needed)
- Check backend logs for detailed error messages

#### Issue: Frontend Can't Connect to Backend

**Solution:**
- Verify VITE_API_URL is correct
- Check CORS settings in backend
- Ensure backend is running
- Check network connectivity

### Performance Monitoring

1. **Code Engine Metrics**
   - Go to application
   - Click "Monitoring"
   - View:
     - Request rate
     - Response time
     - Error rate
     - CPU/Memory usage

2. **Set Up Alerts**
   - Configure alerts for:
     - High error rate
     - High response time
     - Resource exhaustion
     - Application crashes

---

## Scaling and Updates

### Manual Scaling

1. **Edit Application**
   - Go to application
   - Click "Configuration"
   - Adjust:
     - Min/Max instances
     - CPU and memory
     - Concurrency
   - Save

### Auto-Scaling

Code Engine automatically scales based on:
- Incoming requests
- CPU usage
- Memory usage
- Concurrency limits

Configure scaling parameters:
- Min instances: 0 (scale to zero) or 1 (always running)
- Max instances: Based on expected load
- Concurrency: Requests per instance

### Updating Applications

#### Method 1: Automatic (GitHub Integration)

1. **Push Changes to GitHub**
   ```bash
   git add .
   git commit -m "Update application"
   git push origin main
   ```

2. **Trigger Rebuild**
   - Go to application in Code Engine
   - Click "Submit build"
   - Or configure webhook for automatic builds

#### Method 2: Manual Update

1. **Edit Application**
   - Go to application
   - Click "Configuration"
   - Update settings
   - Click "Deploy"

### Rolling Updates

Code Engine performs rolling updates automatically:
- New instances are created
- Traffic is gradually shifted
- Old instances are terminated
- Zero downtime deployment

### Rollback

If issues occur after update:

1. **View Revisions**
   - Go to application
   - Click "Revisions"
   - See all previous versions

2. **Rollback**
   - Select previous working revision
   - Click "Set as latest"
   - Traffic routes to previous version

---

## Best Practices

### Security

1. **Use Secrets for Credentials**
   - Never hardcode credentials
   - Use Code Engine secrets
   - Rotate secrets regularly

2. **Enable HTTPS**
   - Code Engine provides HTTPS by default
   - Use custom domains with SSL certificates

3. **Implement Authentication**
   - Use JWT tokens
   - Implement RBAC
   - Secure API endpoints

4. **Network Security**
   - Use private endpoints where possible
   - Configure security groups
   - Implement rate limiting

### Performance

1. **Optimize Container Images**
   - Use multi-stage builds
   - Minimize image size
   - Use .dockerignore

2. **Configure Caching**
   - Enable HTTP caching
   - Use CDN for static assets
   - Cache database queries

3. **Resource Allocation**
   - Right-size CPU and memory
   - Monitor resource usage
   - Adjust based on metrics

### Cost Optimization

1. **Scale to Zero**
   - Enable for non-production environments
   - Consider for low-traffic applications

2. **Right-Size Resources**
   - Don't over-provision
   - Monitor and adjust
   - Use appropriate instance sizes

3. **Use Free Tier**
   - Code Engine offers free tier
   - Monitor usage to stay within limits

### Monitoring

1. **Set Up Logging**
   - Use structured logging
   - Configure log levels
   - Archive logs for compliance

2. **Configure Alerts**
   - Monitor critical metrics
   - Set up notifications
   - Define escalation procedures

3. **Regular Health Checks**
   - Monitor health endpoints
   - Check application metrics
   - Review error logs

---

## Additional Resources

### IBM Cloud Documentation
- [Code Engine Documentation](https://cloud.ibm.com/docs/codeengine)
- [Cloud Object Storage Documentation](https://cloud.ibm.com/docs/cloud-object-storage)
- [watsonx.ai Documentation](https://cloud.ibm.com/docs/watsonx)

### Support
- IBM Cloud Support Portal
- Code Engine Community Forum
- GitHub Issues (for application-specific issues)

### Useful Commands (IBM Cloud CLI)

```bash
# Login to IBM Cloud
ibmcloud login

# Target Code Engine
ibmcloud ce project select --name banking-validation

# List applications
ibmcloud ce app list

# Get application details
ibmcloud ce app get --name banking-validation-backend

# View logs
ibmcloud ce app logs --name banking-validation-backend

# Update application
ibmcloud ce app update --name banking-validation-backend --env KEY=VALUE

# Scale application
ibmcloud ce app update --name banking-validation-backend --min-scale 1 --max-scale 10
```

---

## Troubleshooting Checklist

Before seeking support, verify:

- [ ] All environment variables are set correctly
- [ ] Secrets are created and bound to applications
- [ ] COS bucket is created and accessible
- [ ] COS credentials are valid
- [ ] watsonx credentials are valid
- [ ] Build completed successfully
- [ ] Application is running (check status)
- [ ] Health endpoints return 200 OK
- [ ] Logs don't show critical errors
- [ ] Network connectivity is working
- [ ] CORS is configured correctly
- [ ] Frontend can reach backend
- [ ] File uploads work to COS
- [ ] Resource limits are sufficient

---

## Conclusion

Your Banking Model Validation System should now be successfully deployed on IBM Cloud Code Engine. The system will automatically scale based on demand and provide high availability for your model validation workflows.

For questions or issues, refer to the troubleshooting section or contact support.

---

**Document Version:** 1.0  
**Last Updated:** 2026-05-25  
**Maintained By:** Development Team