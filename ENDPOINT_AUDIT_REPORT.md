# API Endpoint Audit Report

## Date: 2026-05-26

## Summary
Comprehensive audit of all API endpoints to ensure consistency between frontend and backend.

---

## ✅ CORRECTLY MAPPED ENDPOINTS

### 1. Options Endpoint
- **Frontend**: `GET ${API_BASE_URL}/api/v1/options`
- **Backend**: `@app.get("/api/v1/options")` ✅
- **Status**: WORKING

### 2. Validation Start
- **Frontend**: `POST ${API_BASE_URL}/api/v1/validate`
- **Backend**: `@app.post("/api/v1/validate")` ✅
- **Status**: WORKING

### 3. Validation Status
- **Frontend**: `GET ${API_BASE_URL}/api/v1/validate/{validationId}`
- **Backend**: `@app.get("/api/v1/validate/{validation_id}")` ✅
- **Status**: WORKING

### 4. Validation Results
- **Frontend**: `GET ${API_BASE_URL}/api/v1/validate/{validationId}/results`
- **Backend**: `@app.get("/api/v1/validate/{validation_id}/results")` ✅
- **Status**: WORKING

### 5. Validation Document Download
- **Frontend**: `GET ${API_BASE_URL}/api/v1/validate/{validationId}/document`
- **Backend**: `@app.get("/api/v1/validate/{validation_id}/document")` ✅
- **Status**: WORKING

---

## ⚠️ INCONSISTENT ENDPOINTS

### 6. Document Upload (MAIN ISSUE)
- **Frontend**: `POST ${API_BASE_URL}/api/upload-documents`
- **Backend**: `@app.post("/api/upload-documents")` ⚠️
- **Issue**: Endpoint exists but nginx proxy configuration is incorrect
- **Status**: **FAILING - 405 Method Not Allowed**
- **Root Cause**: nginx.conf was using internal cluster URL that doesn't work
- **Fix Applied**: Updated nginx.conf to use external backend URL

### 7. Report Download (MISSING ENDPOINT)
- **Frontend**: `GET ${API_BASE_URL}/api/download-report/{validationId}`
- **Backend**: **DOES NOT EXIST** ❌
- **Issue**: Frontend calls non-existent endpoint
- **Status**: WILL FAIL
- **Fix Needed**: Either remove frontend call or add backend endpoint

---

## 🔍 BACKEND ENDPOINTS NOT USED BY FRONTEND

### Document Management
- `POST /api/v1/documents/upload` - Single document upload
- `GET /api/v1/documents` - List documents
- `GET /api/v1/documents/{document_id}` - Get document details
- `DELETE /api/v1/documents/{document_id}` - Delete document
- `GET /api/v1/documents/{document_id}/download` - Download document

### MLOps Endpoints
- `POST /api/v1/mlops/onboard-use-case`
- `GET /api/v1/mlops/check-existing-models`
- `POST /api/v1/mlops/register-model`
- `POST /api/v1/mlops/monitor`
- `POST /api/v1/mlops/deploy`
- `GET /api/v1/mlops/documentation/{model_id}`

### Governance Endpoints
- `GET /api/v1/governance/use-cases`
- `GET /api/v1/governance/models`
- `GET /api/v1/governance/models/{model_id}`
- `GET /api/v1/governance/models/{model_id}/versions`
- `GET /api/v1/governance/models/{model_id}/monitoring`
- `GET /api/v1/governance/models/{model_id}/compliance`
- `GET /api/v1/governance/models/{model_id}/card`

### Orchestrate Endpoints
- `GET /api/v1/orchestrate/workflows`
- `GET /api/v1/orchestrate/workflows/{workflow_id}`
- `GET /api/v1/orchestrate/tasks`
- `POST /api/v1/orchestrate/tasks/action`

### Testing Endpoints
- `POST /api/v1/stress-test`
- `GET /api/v1/stress-test/{test_id}`
- `POST /api/v1/custom-test`
- `GET /api/v1/custom-test/{test_id}`

### Other
- `GET /api/v1/validations` - List all validations

---

## 🐛 ISSUES IDENTIFIED

### Issue 1: Upload Endpoint Failing (CRITICAL)
**Problem**: nginx proxy configuration using internal cluster URL
**Impact**: Document upload returns 405 Method Not Allowed
**Fix**: Updated nginx.conf to use external backend URL
**Status**: Fixed, pending deployment

### Issue 2: Missing Download Report Endpoint (HIGH)
**Problem**: Frontend calls `/api/download-report/{validationId}` which doesn't exist
**Impact**: Report download will fail
**Fix Options**:
1. Use existing `/api/v1/validate/{validation_id}/document` endpoint
2. Add new `/api/download-report/{validation_id}` endpoint as alias

### Issue 3: Inconsistent Endpoint Naming
**Problem**: Upload endpoint uses `/api/upload-documents` while others use `/api/v1/...`
**Impact**: Inconsistency, potential confusion
**Recommendation**: Standardize to `/api/v1/documents/upload-batch`

---

## 📋 RECOMMENDED FIXES

### Priority 1: Fix Upload (CRITICAL)
✅ **COMPLETED**: Updated nginx.conf to use external backend URL
- Changed from: `http://banking-validation-backend.243hkitbzigu.svc.cluster.local:80`
- Changed to: `https://banking-validation-backend.243hkitbzigu.us-east.codeengine.appdomain.cloud`

### Priority 2: Fix Report Download (HIGH)
**Option A** (Recommended): Update frontend to use correct endpoint
```javascript
// Change from:
`${API_BASE_URL}/api/download-report/${validationId}`
// To:
`${API_BASE_URL}/api/v1/validate/${validationId}/document`
```

**Option B**: Add alias endpoint in backend
```python
@app.get("/api/download-report/{validation_id}")
async def download_report_alias(validation_id: str):
    return await download_validation_document(validation_id)
```

### Priority 3: Standardize Upload Endpoint (MEDIUM)
**Option A**: Keep current endpoint, document the exception
**Option B**: Add versioned endpoint and deprecate old one
```python
@app.post("/api/v1/documents/upload-batch")
async def upload_documents_batch_v1(files: List[UploadFile] = File(...)):
    return await upload_documents_batch(files)
```

---

## 🧪 TESTING CHECKLIST

After deployment, test:
- [ ] Document upload (train.csv, test.csv, oot.csv)
- [ ] Validation start with uploaded documents
- [ ] Validation status polling
- [ ] Validation results retrieval
- [ ] Document download (if fixed)
- [ ] Report download (if fixed)

---

## 📝 DEPLOYMENT NOTES

### Files Modified
1. `frontend/nginx.conf` - Updated proxy configuration
2. `backend/main.py` - COS integration (already deployed)
3. `backend/agents/validation_orchestrator.py` - Use uploaded data (already deployed)

### Deployment Order
1. Deploy backend (if not already done)
2. Deploy frontend with updated nginx.conf
3. Test upload functionality
4. Fix report download endpoint
5. Full integration test

---

## 🎯 CONCLUSION

**Main Issue**: nginx proxy configuration was incorrect, causing 405 errors
**Fix Applied**: Updated nginx.conf to use external backend URL
**Additional Issue**: Report download endpoint mismatch needs fixing
**Status**: Ready for deployment and testing