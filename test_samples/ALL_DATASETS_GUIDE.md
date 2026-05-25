# Complete Test Datasets Guide

## Overview
This directory contains **5 comprehensive test datasets** for validating different types of banking scorecards. Each dataset is designed to test specific validation scenarios and scorecard types.

---

## 📊 Available Datasets

### Set 1: Successful Application Scorecard
**Location**: `set1_successful/`

**Type**: Application Scorecard
**Status**: ✅ Should PASS
**Size**: Train: 1,000 | Test: 500 | OOT: 300

**Use For**:
- Testing successful validation workflow
- Application scorecard validation
- New customer acquisition models

**Key Features**:
- Default rate: ~5-8%
- Has `employment_status` column
- Good predictive power

---

### Set 2: Failed Application Scorecard
**Location**: `set2_failed/`

**Type**: Application Scorecard
**Status**: ❌ Should FAIL
**Size**: Train: 1,000 | Test: 500 | OOT: 300

**Use For**:
- Testing failure scenarios
- Poor model performance detection
- Validation threshold testing

**Key Features**:
- High default rate (intentionally poor)
- Low predictive power
- Unstable metrics

---

### Set 3: Behavioral Scorecard
**Location**: `set3_behavioral/`

**Type**: Behavioral Scorecard
**Status**: ✅ Should PASS
**Size**: Train: 1,500 | Test: 800 | OOT: 500

**Use For**:
- Existing customer risk assessment
- Behavioral scorecard validation
- Testing with documentation

**Key Features**:
- Default rate: ~3-5%
- Has `credit_utilization`, `payment_ratio`
- Includes model documentation (DOCX)
- Good for SR 11-7 compliance testing

**Important**: Select **"Behavioral"** as Scorecard Type!

---

### Set 4: Application Scorecard (High Performance)
**Location**: `set4_application_high/`

**Type**: Application Scorecard
**Status**: ✅ Should PASS (Excellent)
**Size**: Train: 2,000 | Test: 1,000 | OOT: 600

**Use For**:
- Testing high-performance models
- Excellent metrics validation
- Production-ready model testing

**Key Features**:
- Optimal default rate: ~7%
- Excellent KS/Gini metrics
- Very stable (low PSI)
- All required features present

**Important**: Select **"Application"** as Scorecard Type!

---

### Set 5: Collections Early Stage
**Location**: `set5_collections_early/`

**Type**: Collections - Early Stage
**Status**: ✅ Should PASS
**Size**: Train: 1,500 | Test: 800 | OOT: 500

**Use For**:
- Collections scorecard validation
- Early delinquency management (30-90 DPD)
- Recovery probability modeling

**Key Features**:
- Recovery rate: ~45%
- Has `days_past_due`, `outstanding_balance`, `contact_attempts`
- Different target (recovery vs default)
- Lower performance thresholds

**Important**: Select **"Collections Early"** as Scorecard Type!

---

## 🎯 Quick Selection Guide

### By Scorecard Type

| Scorecard Type | Use Dataset | Expected Result |
|----------------|-------------|-----------------|
| Application | Set 1, Set 2, or Set 4 | Set 1 & 4: PASS, Set 2: FAIL |
| Behavioral | Set 3 | PASS |
| Collections Early | Set 5 | PASS |

### By Test Scenario

| Scenario | Use Dataset |
|----------|-------------|
| Successful validation | Set 1, Set 3, Set 4, Set 5 |
| Failed validation | Set 2 |
| High performance | Set 4 |
| With documentation | Set 3 |
| Collections testing | Set 5 |

---

## 📋 Required Columns by Scorecard Type

### Application Scorecard (Set 1, 2, 4)
**Required**:
- `age`
- `income`
- `employment_status`

**Common**:
- `score`, `target`, `prediction`
- `customer_id`

### Behavioral Scorecard (Set 3)
**Required**:
- `months_on_book`
- `credit_utilization` (or `utilization`)
- `payment_ratio` (or `payment_history`)

**Common**:
- `score`, `target`, `prediction`
- `customer_id`

### Collections Early Stage (Set 5)
**Required**:
- `days_past_due`
- `outstanding_balance`
- `contact_attempts`

**Common**:
- `score`, `target`, `prediction`
- `customer_id`

---

## 🚀 How to Use

### Step 1: Choose Dataset
Select based on what you want to test (see tables above)

### Step 2: Upload Files
Upload the 3 CSV files:
- `train.csv`
- `test.csv`
- `oot.csv`

For Set 3, also upload:
- `behavioral_scorecard_documentation.docx`

### Step 3: Configure Model
**CRITICAL**: Match the Scorecard Type to your dataset!

| Dataset | Select Scorecard Type |
|---------|----------------------|
| Set 1, 2, 4 | **Application** |
| Set 3 | **Behavioral** |
| Set 5 | **Collections Early** |

### Step 4: Run Validation
Submit and wait for results

---

## 📊 Expected Metrics by Dataset

### Set 1 (Application - Successful)
- KS: 0.25-0.35
- Gini: 0.30-0.45
- PSI: < 0.20
- Compliance: 70-80%

### Set 2 (Application - Failed)
- KS: < 0.20 (Poor)
- Gini: < 0.25 (Poor)
- PSI: > 0.30 (Unstable)
- Compliance: 50-65%

### Set 3 (Behavioral)
- KS: 0.30-0.40
- Gini: 0.35-0.50
- PSI: < 0.15
- Compliance: 75-85% (with docs)

### Set 4 (Application - High Performance)
- KS: > 0.35 (Excellent)
- Gini: > 0.45 (Excellent)
- PSI: < 0.10 (Very Stable)
- Compliance: 75-85%

### Set 5 (Collections Early)
- KS: 0.20-0.30
- Gini: 0.25-0.35
- PSI: < 0.25
- Compliance: 70-80%

---

## 💡 Tips

### Common Mistakes
1. ❌ Using Set 3 with "Application" type → Will FAIL
2. ❌ Using Set 1/2/4 with "Behavioral" type → Will FAIL
3. ❌ Not uploading documentation for Set 3 → Lower compliance score

### Best Practices
1. ✅ Always match Scorecard Type to dataset
2. ✅ Read the README in each dataset folder
3. ✅ Check column names match requirements
4. ✅ Upload documentation when available

---

## 🔍 Troubleshooting

### "Model-Specific Validation Failed"
**Cause**: Wrong scorecard type selected
**Fix**: Match scorecard type to dataset (see table above)

### "Data Quality Check Failed"
**Cause**: Missing required columns
**Fix**: Verify dataset has all required columns for that scorecard type

### "Low Compliance Score"
**Cause**: No documentation uploaded (for Set 3)
**Fix**: Upload the DOCX file along with CSV files

---

## 📁 File Structure

```
test_samples/
├── set1_successful/
│   ├── train.csv
│   ├── test.csv
│   ├── oot.csv
│   └── README.md
├── set2_failed/
│   ├── train.csv
│   ├── test.csv
│   ├── oot.csv
│   └── README.md
├── set3_behavioral/
│   ├── train.csv
│   ├── test.csv
│   ├── oot.csv
│   ├── behavioral_scorecard_documentation.docx
│   └── README.md
├── set4_application_high/
│   ├── train.csv
│   ├── test.csv
│   ├── oot.csv
│   └── README.md
├── set5_collections_early/
│   ├── train.csv
│   ├── test.csv
│   ├── oot.csv
│   └── README.md
└── ALL_DATASETS_GUIDE.md (this file)
```

---

## 🎓 Learning Path

### Beginner
1. Start with **Set 1** (successful application)
2. Try **Set 2** (failed application) to see failures
3. Compare results

### Intermediate
4. Test **Set 3** (behavioral with documentation)
5. Observe SR 11-7 compliance improvements
6. Try **Set 4** (high performance)

### Advanced
7. Test **Set 5** (collections)
8. Compare different scorecard types
9. Experiment with different configurations

---

**Need help? Check the README.md file in each dataset folder for detailed information!**