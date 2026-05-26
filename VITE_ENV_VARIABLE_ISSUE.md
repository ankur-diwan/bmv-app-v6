# Vite Environment Variable Issue - Critical Understanding

## Date: 2026-05-26 14:42 IST

## 🎯 THE REAL PROBLEM: Build-Time vs Runtime

### Why Updating Environment Variable Didn't Work

**Critical Concept**: Vite environment variables are **build-time** variables, not runtime variables.

### How Vite Works

1. **Build Time** (when `npm run build` executes):
   ```javascript
   // In source code:
   const API_URL = import.meta.env.VITE_API_URL;
   
   // After build (baked into bundle.js):
   const API_URL = "https://banking-validation-backend...";
   ```

2. **Runtime** (when user opens browser):
   - The value is already hardcoded in the JavaScript bundle
   - Changing environment variable has NO effect
   - Must rebuild to change the value

### What We Did Wrong

```bash
# Step 1: Updated environment variable
ibmcloud ce app update --name banking-validation-frontend \
  --env VITE_API_URL=https://...

# Result: Environment variable updated in Code Engine
# BUT: The JavaScript bundle still has the OLD value baked in
# WHY: The bundle was built with the old value
```

### What We're Doing Now (Correct)

```bash
# Rebuild with correct environment variable
ibmcloud ce app update --name banking-validation-frontend \
  --build-source https://github.com/ankur-diwan/bmv-app-v6.git \
  --build-context-dir frontend \
  --env VITE_API_URL=https://...

# This will:
# 1. Pull latest code from git
# 2. Set VITE_API_URL environment variable
# 3. Run npm run build (which reads VITE_API_URL)
# 4. Bake the correct value into bundle.js
# 5. Deploy new image with correct bundle
```

---

## 📊 Timeline of Issues

### Original Deployment (April 24)
- Built with `VITE_API_URL=ttps://...` (typo)
- JavaScript bundle has incorrect URL baked in
- Upload fails with 405 errors

### First Fix Attempt (Today, 14:20)
- Updated nginx.conf
- Committed to git
- Triggered rebuild
- **BUT**: Environment variable still had typo
- New build still used `ttps://...`
- Upload still failed

### Second Fix Attempt (Today, 14:33)
- Updated environment variable to `https://...`
- **BUT**: Didn't rebuild
- Old JavaScript bundle still in use
- Upload still failed

### Third Fix Attempt (Today, 14:42) - CURRENT
- Rebuilding with correct environment variable
- Will bake correct URL into new bundle
- Should fix the upload issue

---

## 🔍 How to Verify After Deployment

### Step 1: Check Built JavaScript
```bash
# After deployment completes, check the bundle
curl https://banking-validation-frontend.243hkitbzigu.us-east.codeengine.appdomain.cloud/assets/index-*.js | grep -o "https://banking-validation-backend"
```

Should output: `https://banking-validation-backend` (not `ttps://`)

### Step 2: Check Browser Console
1. Open frontend in browser
2. Open DevTools Console (F12)
3. Type: `import.meta.env.VITE_API_URL`
4. Should show: `https://banking-validation-backend...`

### Step 3: Check Network Requests
1. Try to upload a file
2. Check Network tab
3. Request should go to: `https://banking-validation-backend.../api/upload-documents`
4. NOT to: `https://banking-validation-frontend.../api/upload-documents`

---

## 📝 Key Learnings

### 1. Vite Environment Variables Are Build-Time
- `VITE_*` variables are replaced at build time
- Not available at runtime
- Must rebuild to change values

### 2. Code Engine Environment Variables
- Setting env var updates the container environment
- But doesn't affect already-built JavaScript bundles
- Must trigger rebuild to apply to Vite variables

### 3. Two-Step Process Required
```bash
# Wrong (what we did initially):
ibmcloud ce app update --env VITE_API_URL=new_value

# Right (what we're doing now):
ibmcloud ce app update --build-source ... --env VITE_API_URL=new_value
```

---

## 🎯 Expected Outcome

After this rebuild completes:

1. ✅ JavaScript bundle will have correct `https://` URL
2. ✅ Frontend will connect to backend correctly
3. ✅ Upload requests will go to backend, not frontend
4. ✅ nginx proxy will work as backup (if needed)
5. ✅ Upload will succeed

---

## 🚨 Important Notes

### For Future Deployments

**Always use `--build-source` when updating Vite environment variables:**

```bash
# Correct way to update Vite env vars:
ibmcloud ce app update --name APP_NAME \
  --build-source REPO_URL \
  --build-context-dir CONTEXT \
  --env VITE_VAR=value
```

**Don't just update the env var without rebuilding:**

```bash
# This WON'T work for Vite variables:
ibmcloud ce app update --name APP_NAME --env VITE_VAR=value
```

### Runtime vs Build-Time Variables

**Build-Time (Vite):**
- Prefix: `VITE_*`
- Available in frontend code
- Baked into JavaScript bundle
- Require rebuild to change

**Runtime (Backend):**
- Any name (e.g., `COS_API_KEY`)
- Available in backend code
- Read from environment at runtime
- Can be updated without rebuild

---

## ⏱️ Current Status

**Build In Progress**: Rebuilding frontend with correct `VITE_API_URL`

**ETA**: 3-7 minutes

**Next Steps**:
1. Wait for build to complete
2. Clear browser cache
3. Test upload
4. Verify success

---

## 📚 References

- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [Code Engine Environment Variables](https://cloud.ibm.com/docs/codeengine?topic=codeengine-envvar)
- [Build-Time vs Runtime Configuration](https://12factor.net/config)