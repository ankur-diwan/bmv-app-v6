# Code Engine Environment Variables Setup Guide

This guide explains exactly how to add environment variables in IBM Cloud Code Engine UI.

---

## Understanding the Options

When you click "Add environment variable" in Code Engine, you'll see these options:

### Option 1: **Literal value** ✅ Use for non-sensitive values
- Direct text values
- Example: `ENVIRONMENT=production`

### Option 2: **Reference to key in configmap**
- For configuration data stored in configmaps
- Not used in this deployment

### Option 3: **Reference to key in secret** ✅ Use for sensitive credentials
- For individual secret keys
- Example: Get `WATSONX_API_KEY` from `watsonx-credentials` secret

### Option 4: **Reference to full configmap**
- Imports all keys from a configmap
- Not used in this deployment

### Option 5: **Reference to full secret** ✅ Use to import entire secret
- Imports all keys from a secret at once
- Easiest method for multiple credentials

---

## Step-by-Step: Adding Environment Variables

### Method 1: Add Literal Values (Non-Sensitive)

For these variables, select **"Literal value"**:

1. Click "Add environment variable"
2. Select **"Literal value"** (first option)
3. Enter name and value:

```
Environment variable name: ENVIRONMENT
Value: production
```

**Repeat for these literal values:**
- `ENVIRONMENT` = `production`
- `LOG_LEVEL` = `INFO`
- `VALIDATION_TEMP_DIR` = `/app/temp/cos_validation`
- `WATSONX_URL` = `https://us-south.ml.cloud.ibm.com`

---

### Method 2: Reference Full Secret (Recommended for Credentials)

This is the **EASIEST** method - it imports all keys from a secret at once.

#### Step 1: Create Secrets First

Before adding to application, create these secrets:

**Secret 1: `watsonx-credentials`**
1. Go to "Secrets and configmaps" in Code Engine
2. Click "Create" → "Secret"
3. Name: `watsonx-credentials`
4. Type: Generic secret
5. Add these key-value pairs:
   - Key: `WATSONX_API_KEY`, Value: `your_actual_api_key`
   - Key: `WATSONX_PROJECT_ID`, Value: `your_actual_project_id`
   - Key: `WATSONX_SPACE_ID`, Value: `your_actual_space_id`
6. Click "Create"

**Secret 2: `cos-credentials`**
1. Click "Create" → "Secret"
2. Name: `cos-credentials`
3. Type: Generic secret
4. Add these key-value pairs:
   - Key: `COS_API_KEY`, Value: `your_cos_api_key`
   - Key: `COS_RESOURCE_INSTANCE_ID`, Value: `your_cos_instance_id`
   - Key: `COS_ENDPOINT_URL`, Value: `https://s3.us-south.cloud-object-storage.appdomain.cloud`
   - Key: `COS_BUCKET_NAME`, Value: `bankvalidationapp`
5. Click "Create"

**Secret 3: `cos-hmac-credentials`** (Optional)
1. Click "Create" → "Secret"
2. Name: `cos-hmac-credentials`
3. Type: Generic secret
4. Add these key-value pairs:
   - Key: `COS_ACCESS_KEY_ID`, Value: `your_hmac_access_key`
   - Key: `COS_SECRET_ACCESS_KEY`, Value: `your_hmac_secret_key`
5. Click "Create"

#### Step 2: Add Secrets to Application

Now add these secrets to your backend application:

1. Go to your backend application
2. Click "Environment variables" tab
3. Click "Add" → Select **"Reference to full secret"** (5th option)
4. **Prefix field**: **LEAVE EMPTY** (do not enter anything)
   - The prefix field is optional
   - Leave it blank to use the exact key names from your secret
   - Example: If your secret has `COS_API_KEY`, it will be available as `COS_API_KEY` in your app
5. **Secret dropdown**: Select `watsonx-credentials`
6. Click "Add"
7. Repeat for `cos-credentials` (leave prefix empty)
8. Repeat for `cos-hmac-credentials` if created (leave prefix empty)

**Result:** All keys from each secret are automatically added as environment variables with their original names!

**Important:** The "Prefix" field should be **EMPTY** for this deployment. Only use a prefix if you want to add a prefix to all variable names (e.g., prefix "DB_" would make `API_KEY` become `DB_API_KEY`).

---

### Method 3: Reference Individual Secret Keys (Alternative)

If you prefer to add individual keys from secrets:

1. Click "Add environment variable"
2. Select **"Reference to key in secret"** (3rd option)
3. Fill in:
   - Environment variable name: `WATSONX_API_KEY`
   - Secret name: `watsonx-credentials`
   - Key: `WATSONX_API_KEY`
4. Click "Add"

**Repeat for each key you need.**

---

## Complete Configuration Example

### Backend Application Environment Variables

#### Literal Values (4 variables):
```
ENVIRONMENT = production
LOG_LEVEL = INFO
VALIDATION_TEMP_DIR = /app/temp/cos_validation
WATSONX_URL = https://us-south.ml.cloud.ibm.com
```

#### From Secrets (3 secrets with multiple keys each):
```
Reference to full secret: watsonx-credentials
  ↳ WATSONX_API_KEY
  ↳ WATSONX_PROJECT_ID
  ↳ WATSONX_SPACE_ID

Reference to full secret: cos-credentials
  ↳ COS_API_KEY
  ↳ COS_RESOURCE_INSTANCE_ID
  ↳ COS_ENDPOINT_URL
  ↳ COS_BUCKET_NAME

Reference to full secret: cos-hmac-credentials (optional)
  ↳ COS_ACCESS_KEY_ID
  ↳ COS_SECRET_ACCESS_KEY
```

#### Optional: CORS Configuration
```
ALLOWED_ORIGINS = https://your-frontend-url.codeengine.appdomain.cloud
```

---

## Visual Guide: Which Option to Choose

```
┌─────────────────────────────────────────────────────────────┐
│ Add environment variable                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Define as:                                                   │
│                                                              │
│ ⦿ Literal value                    ← Use for: ENVIRONMENT,  │
│                                       LOG_LEVEL, etc.        │
│                                                              │
│ ○ Reference to key in configmap    ← Not used               │
│                                                              │
│ ○ Reference to key in secret       ← Use for: Individual    │
│                                       secret keys            │
│                                                              │
│ ○ Reference to full configmap      ← Not used               │
│                                                              │
│ ○ Reference to full secret         ← Use for: Import entire │
│                                       secret (RECOMMENDED)   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Decision Tree

```
Is this a sensitive credential (API key, password)?
│
├─ YES → Use "Reference to full secret" (easiest)
│        or "Reference to key in secret"
│
└─ NO → Use "Literal value"
```

---

## Common Mistakes to Avoid

❌ **Don't** add sensitive credentials as literal values  
✅ **Do** use secrets for API keys and passwords

❌ **Don't** create secrets after adding to application  
✅ **Do** create secrets first, then reference them

❌ **Don't** forget to add CORS after frontend deployment  
✅ **Do** add `ALLOWED_ORIGINS` with frontend URL

---

## Verification Checklist

After adding all environment variables, verify:

- [ ] 4 literal values added (ENVIRONMENT, LOG_LEVEL, etc.)
- [ ] `watsonx-credentials` secret referenced
- [ ] `cos-credentials` secret referenced
- [ ] `cos-hmac-credentials` secret referenced (if using presigned URLs)
- [ ] All secrets show green checkmark in UI
- [ ] Application redeploys successfully
- [ ] Health endpoint returns 200 OK

---

## Troubleshooting

### Issue: Secret not found
**Solution:** Create the secret first in "Secrets and configmaps" before referencing it

### Issue: Environment variable not showing in app
**Solution:** Make sure you clicked "Add" after filling in the details

### Issue: Application won't start after adding variables
**Solution:** Check application logs for missing or incorrect variable names

### Issue: Can't find "Reference to full secret" option
**Solution:** Make sure you're in the "Environment variables" tab, not "Secrets" tab

---

## Summary

**For non-sensitive values:**
- Select: **"Literal value"**
- Example: `ENVIRONMENT=production`

**For sensitive credentials (RECOMMENDED):**
- Create secret first
- Select: **"Reference to full secret"**
- Choose your secret name
- All keys imported automatically

**Result:** Your application will have all required environment variables configured securely!

---

**Last Updated:** 2026-05-25  
**Version:** 1.0