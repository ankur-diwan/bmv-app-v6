# 🚀 Quick Start Guide - Banking Model Validation System

## ✅ Prerequisites (Already Done!)
- ✓ Backend running on http://localhost:8000
- ✓ Frontend running on http://localhost:3000
- ✓ Sample datasets available in `test_samples/` folder

---

## 📊 Step-by-Step Tutorial

### Step 1: Open the Application
Open your browser and go to: **http://localhost:3000**

### Step 2: Start a New Validation
You'll see the validation wizard with 4 steps:
1. Select Model Configuration
2. Review & Submit
3. Validation Progress
4. Results

---

## 🎯 Option A: Quick Test (No File Upload Required)

The system can generate synthetic data automatically!

### 1. Fill in Model Configuration:
- **Model Name**: `Test_Application_Scorecard_v1`
- **Product Type**: Select `Unsecured Personal Loans`
- **Scorecard Type**: Select `Application`
- **Model Type**: Select `Logistic Regression (GLM)`
- **Description**: `Test application scorecard for demo`
- **Version**: `1.0`
- **Owner**: `Model Risk Management`

### 2. Click "Next" → Review → "Start Validation"

### 3. Wait 30-60 seconds

### 4. View Results!
You'll see:
- Overall validation status
- Statistical tests (KS, Gini, PSI, CSI)
- Performance metrics
- **SR 11-7 Compliance with detailed reasons** ⭐ (Your new enhancement!)
- Model-specific validation

---

## 📁 Option B: Using Sample Datasets (Recommended for Best Results)

### Available Sample Files:
Located in `test_samples/` folder:

1. **successful_train.csv** - Training dataset (2,000 rows)
2. **successful_test.csv** - Test dataset (1,000 rows)
3. **successful_oot.csv** - Out-of-time dataset (600 rows)
4. **successful_model_documentation.docx** - Model documentation

### How to Upload:

**Currently, the simplified version doesn't have file upload in the UI.**

But you can test with the API directly:

```bash
# Upload documents
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/successful_train.csv" \
  -F "files=@test_samples/successful_test.csv" \
  -F "files=@test_samples/successful_oot.csv"
```

---

## 🎨 What You'll See in SR 11-7 Compliance Section

### Each Category Shows:

**1. Category Title**
- Example: "Clear articulation of model purpose and use cases"

**2. Status Chip** (Color-coded)
- 🟢 Passed
- 🟡 Partial
- 🔴 Failed

**3. Score**
- Example: "12.00 / 15"

**4. ⭐ Reason Summary Alert** (NEW!)
- **Failed**: "Failed: Model purpose and type NOT documented; Business alignment NOT validated"
- **Partial**: "Partial: Business alignment NOT validated"
- **Passed**: "Passed: All 3 checks completed successfully"

**5. Individual Check Details**
- ✓ Model use cases defined
- ✗ Model purpose and type NOT documented
- ✗ Business alignment NOT validated

---

## 📋 Understanding the Results

### Key Metrics to Look For:

| Metric | Good | Excellent | What It Means |
|--------|------|-----------|---------------|
| **KS Statistic** | > 0.30 | > 0.40 | Model separates good/bad customers |
| **Gini Coefficient** | > 0.40 | > 0.60 | Model discrimination power |
| **PSI** | < 0.10 | < 0.05 | Population is stable over time |
| **CSI** | < 0.10 | < 0.05 | Characteristics are stable |
| **Accuracy** | > 80% | > 85% | Overall prediction accuracy |
| **SR 11-7 Score** | > 70% | > 90% | Regulatory compliance |

### Overall Status:
- ✅ **PASS**: All critical metrics meet thresholds
- ⚠️ **WARNING**: Some metrics need attention
- ❌ **FAIL**: Critical metrics below thresholds

---

## 🎓 Sample Data Details

### What's in the Sample Files:

**successful_train.csv** (2,000 rows):
```csv
age,income,credit_score,dti_ratio,delinquencies,target,score
35,75000,720,0.35,0,0,650
42,95000,680,0.42,1,1,520
28,55000,750,0.28,0,0,720
...
```

**Columns:**
- `age`: Customer age (18-75)
- `income`: Annual income ($20K-$200K)
- `credit_score`: Credit score (300-850)
- `dti_ratio`: Debt-to-income ratio (0-1)
- `delinquencies`: Number of past delinquencies
- `target`: 0 = good customer, 1 = default
- `score`: Model prediction score (300-850)

**Expected Results with Sample Data:**
- ✅ KS Statistic: ~0.45 (Excellent)
- ✅ Gini: ~0.65 (Good)
- ✅ PSI: ~0.05 (Stable)
- ✅ Accuracy: ~88%
- ✅ SR 11-7: ~75%

---

## 🔧 Troubleshooting

### Issue: "No validation results"
**Solution**: Make sure you clicked "Start Validation" and waited for completion

### Issue: "Low compliance score"
**Solution**: This is expected without uploaded documentation. The system generates synthetic data which may not have all SR 11-7 documentation

### Issue: "Backend not responding"
**Solution**: Check if backend is running:
```bash
curl http://localhost:8000/api/health
```

### Issue: "Frontend not loading"
**Solution**: Check if frontend is running:
```bash
curl http://localhost:3000
```

---

## 📥 Download Validation Report

After validation completes:
1. Scroll to the bottom of results
2. Click **"Download Validation Report"** button
3. Get a Word document with complete validation details

---

## 🎯 Next Steps

1. **Try different model types**: Test with XGBoost, Random Forest, etc.
2. **Try different scorecard types**: Behavioral, Collections Early/Late
3. **Compare results**: Run multiple validations and compare
4. **Review SR 11-7 details**: Check why each category passed/failed
5. **Download reports**: Keep validation records for audit

---

## 💡 Tips for Best Results

1. ✅ Use realistic data with good model performance
2. ✅ Ensure target variable is correctly defined (0=good, 1=bad)
3. ✅ Check that scores correlate with risk (higher score = lower risk)
4. ✅ Use data from similar time periods for stability
5. ✅ Review all sections, not just overall status

---

## 📞 Need Help?

- Check backend logs: `tail -f /tmp/backend.log`
- Check frontend logs: Browser Console (F12)
- Review this guide: `QUICKSTART_GUIDE.md`
- Check detailed guide: `test_samples/INPUT_DATA_GUIDE.md`

---

## 🎉 You're Ready!

Open **http://localhost:3000** and start validating models!

The enhanced SR 11-7 Compliance section will show you detailed reasons for each category's pass/fail status.

---

**Built with ❤️ using IBM watsonx and FastAPI**