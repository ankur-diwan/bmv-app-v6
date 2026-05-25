# IBM Cloud Code Engine Deployment Checklist
## Banking Model Validation System

Use this checklist to ensure all steps are completed for a successful deployment.

---

## Pre-Deployment Checklist

### 1. Code Repository Setup
- [ ] Code is committed to GitHub repository
- [ ] Repository is accessible (public or private with access token)
- [ ] All sensitive data removed from code
- [ ] `.gitignore` properly configured
- [ ] README.md updated with deployment information

### 2. IBM Cloud Account Setup
- [ ] IBM Cloud account created and active
- [ ] Billing information configured
- [ ] Appropriate permissions assigned
- [ ] Resource group created (if needed)
- [ ] Region selected (e.g., us-south, eu-de)

### 3. Required Services Provisioned
- [ ] IBM watsonx.ai instance created
- [ ] watsonx API key generated
- [ ] watsonx Project ID obtained
- [ ] IBM Cloud Databases for PostgreSQL provisioned
- [ ] Database connection string obtained
- [ ] Database initialized with schema (init.sql)
- [ ] (Optional) Cloud Object Storage bucket created

### 4. Credentials and Secrets Prepared
- [ ] watsonx API key documented
- [ ] watsonx Project ID documented
- [ ] watsonx Space ID documented (if applicable)
- [ ] Database connection string documented
- [ ] Secret keys generated (SECRET_KEY, JWT_SECRET)
- [ ] All credentials stored securely (NOT in code)

### 5. Configuration Files Ready
- [ ] `.env.codeengine` file reviewed
- [ ] Backend Dockerfile optimized
- [ ] Frontend Dockerfile optimized
- [ ] `.dockerignore` files created
- [ ] Health check endpoints verified in code

---

## Backend Deployment Checklist

### 1. Code Engine Project Setup
- [ ] Code Engine project created
- [ ] Project name: `banking-validation`
- [ ] Region selected and matches database region
- [ ] Resource group assigned

### 2. Secrets Created
- [ ] Secret `watsonx-credentials` created with:
  - [ ] WATSONX_API_KEY
  - [ ] WATSONX_PROJECT_ID
  - [ ] WATSONX_SPACE_ID
- [ ] Secret `database-credentials` created with:
  - [ ] DATABASE_URL
- [ ] Secret `security-keys` created with:
  - [ ] SECRET_KEY
  - [ ] JWT_SECRET

### 3. Backend Application Configuration
- [ ] Application name: `banking-validation-backend`
- [ ] Source code repository URL configured
- [ ] Branch: `main` (or your branch)
- [ ] Context directory: `/backend`
- [ ] Dockerfile path: `/backend/Dockerfile`
- [ ] Build strategy: Dockerfile
- [ ] Build resources: Medium (2 vCPU, 4 GB)

### 4. Backend Runtime Configuration
- [ ] CPU: 1 vCPU (minimum)
- [ ] Memory: 2 GB (minimum)
- [ ] Min instances: 0 or 1
- [ ] Max instances: 10 (adjust based on needs)
- [ ] Concurrency: 100
- [ ] Request timeout: 300 seconds
- [ ] Port: 8080

### 5. Backend Environment Variables
- [ ] ENVIRONMENT = production
- [ ] LOG_LEVEL = INFO
- [ ] VALIDATION_TEMP_DIR = /app/temp/cos_validation
- [ ] WATSONX_URL = https://us-south.ml.cloud.ibm.com
- [ ] All secrets bound to application

### 6. Backend Deployment
- [ ] Application created
- [ ] Build started automatically
- [ ] Build completed successfully (check logs)
- [ ] Application deployed
- [ ] Application status: Ready
- [ ] Backend URL noted (e.g., https://banking-validation-backend.xxx.codeengine.appdomain.cloud)

### 7. Backend Verification
- [ ] Health endpoint accessible: `https://BACKEND-URL/health`
- [ ] Health endpoint returns: `{"status": "healthy", ...}`
- [ ] Root endpoint accessible: `https://BACKEND-URL/`
- [ ] API documentation accessible: `https://BACKEND-URL/docs`
- [ ] No errors in application logs
- [ ] Database connection successful (check logs)
- [ ] watsonx connection successful (check logs)

---

## Frontend Deployment Checklist

### 1. Frontend Application Configuration
- [ ] Application name: `banking-validation-frontend`
- [ ] Source code repository URL configured
- [ ] Branch: `main` (or your branch)
- [ ] Context directory: `/frontend`
- [ ] Dockerfile path: `/frontend/Dockerfile`
- [ ] Build strategy: Dockerfile
- [ ] Build resources: Medium (2 vCPU, 4 GB)

### 2. Frontend Build Arguments
- [ ] Build argument added: `VITE_API_URL`
- [ ] Value set to backend URL: `https://BACKEND-URL`

### 3. Frontend Runtime Configuration
- [ ] CPU: 0.5 vCPU (minimum)
- [ ] Memory: 1 GB (minimum)
- [ ] Min instances: 0 or 1
- [ ] Max instances: 5 (adjust based on needs)
- [ ] Concurrency: 100
- [ ] Request timeout: 60 seconds
- [ ] Port: 8080

### 4. Frontend Deployment
- [ ] Application created
- [ ] Build started automatically
- [ ] Build completed successfully (check logs)
- [ ] Application deployed
- [ ] Application status: Ready
- [ ] Frontend URL noted (e.g., https://banking-validation-frontend.xxx.codeengine.appdomain.cloud)

### 5. Frontend Verification
- [ ] Health endpoint accessible: `https://FRONTEND-URL/health`
- [ ] Health endpoint returns: `healthy`
- [ ] Main page loads: `https://FRONTEND-URL/`
- [ ] UI renders correctly
- [ ] No console errors in browser
- [ ] Static assets load correctly
- [ ] Navigation works

---

## Integration and Testing Checklist

### 1. Backend-Frontend Integration
- [ ] Frontend can reach backend API
- [ ] CORS configured correctly in backend
- [ ] Backend ALLOWED_ORIGINS includes frontend URL
- [ ] API calls from frontend succeed
- [ ] Authentication flow works (if implemented)

### 2. Database Integration
- [ ] Backend connects to database successfully
- [ ] Database queries execute without errors
- [ ] Data persists correctly
- [ ] Migrations applied (if any)

### 3. watsonx Integration
- [ ] watsonx.ai API calls succeed
- [ ] Model validation features work
- [ ] Document generation works
- [ ] AI-powered features functional

### 4. Functional Testing
- [ ] User can access the application
- [ ] File upload works
- [ ] Model validation executes
- [ ] Reports generate successfully
- [ ] Documents download correctly
- [ ] All major features tested

### 5. Performance Testing
- [ ] Application responds within acceptable time
- [ ] No timeout errors under normal load
- [ ] Auto-scaling works (if configured)
- [ ] Resource usage is reasonable

---

## Post-Deployment Checklist

### 1. Monitoring Setup
- [ ] Application logs accessible
- [ ] Metrics dashboard reviewed
- [ ] Alerts configured (optional)
- [ ] Health checks passing

### 2. Security Review
- [ ] All credentials stored as secrets
- [ ] No sensitive data in logs
- [ ] HTTPS enabled (default in Code Engine)
- [ ] Security headers configured
- [ ] CORS properly restricted

### 3. Documentation
- [ ] Deployment guide reviewed
- [ ] URLs documented
- [ ] Credentials documented (securely)
- [ ] Team members informed
- [ ] Runbook created (optional)

### 4. Backup and Recovery
- [ ] Database backup configured
- [ ] Recovery procedure documented
- [ ] Rollback plan prepared

### 5. Cost Management
- [ ] Resource usage monitored
- [ ] Cost estimates reviewed
- [ ] Scaling limits set appropriately
- [ ] Budget alerts configured (optional)

---

## Troubleshooting Checklist

If deployment fails, check:

### Build Issues
- [ ] Dockerfile syntax correct
- [ ] All dependencies in requirements.txt/package.json
- [ ] Build logs reviewed for errors
- [ ] Context directory path correct
- [ ] Sufficient build resources allocated

### Runtime Issues
- [ ] Application logs reviewed
- [ ] Environment variables set correctly
- [ ] Secrets bound to application
- [ ] Port 8080 exposed
- [ ] Health endpoint configured

### Connection Issues
- [ ] Database URL format correct
- [ ] Database accessible from Code Engine
- [ ] SSL/TLS configured for database
- [ ] watsonx credentials valid
- [ ] Network connectivity working

### Frontend Issues
- [ ] VITE_API_URL set correctly at build time
- [ ] Backend URL accessible from browser
- [ ] CORS configured in backend
- [ ] Static assets building correctly
- [ ] Browser console checked for errors

---

## Maintenance Checklist

### Regular Tasks
- [ ] Monitor application logs weekly
- [ ] Review metrics and performance monthly
- [ ] Update dependencies quarterly
- [ ] Rotate secrets every 90 days
- [ ] Review and optimize costs monthly
- [ ] Test backup and recovery quarterly

### Update Procedure
- [ ] Test changes locally first
- [ ] Commit and push to GitHub
- [ ] Trigger rebuild in Code Engine
- [ ] Monitor deployment
- [ ] Verify functionality
- [ ] Rollback if issues occur

---

## Sign-Off

### Deployment Completed By
- Name: ___________________________
- Date: ___________________________
- Signature: _______________________

### Verified By
- Name: ___________________________
- Date: ___________________________
- Signature: _______________________

### Production Ready
- [ ] All checklist items completed
- [ ] Testing successful
- [ ] Documentation updated
- [ ] Team trained
- [ ] Monitoring active

---

## Notes and Comments

Use this section to document any issues, workarounds, or special configurations:

```
[Add your notes here]
```

---

## Quick Reference

### Backend URL
```
https://banking-validation-backend.xxx.codeengine.appdomain.cloud
```

### Frontend URL
```
https://banking-validation-frontend.xxx.codeengine.appdomain.cloud
```

### Database Connection
```
postgresql://username:password@host:port/banking_validation?sslmode=require
```

### Important Commands
```bash
# View logs
ibmcloud ce app logs --name banking-validation-backend

# Update application
ibmcloud ce app update --name banking-validation-backend --env KEY=VALUE

# Restart application
ibmcloud ce app update --name banking-validation-backend
```

---

**Checklist Version:** 1.0  
**Last Updated:** 2026-05-25  
**Next Review Date:** ___________________________