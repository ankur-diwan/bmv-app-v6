# 📊 Complete Test Datasets Guide

## Overview
This guide describes all available test datasets for the Banking Model Validation System. Each dataset demonstrates different scenarios and validation outcomes.

---

## 🎯 Available Datasets

### Set 1: Successful Application Scorecard ✅
**Location**: `test_samples/set1_successful/`

**Scenario**: New loan applicants with excellent model performance

**Files**:
- `train.csv` (2,000 records)
- `test.csv` (1,000 records)
- `oot.csv` (600 records)

**Key Characteristics**:
- **Model Type**: Application Scorecard
- **Product**: Unsecured Personal Loans
- **Performance**: Excellent (KS ~0.45, Gini ~0.65)
- **Stability**: Excellent (PSI ~0.05)
- **Default Rate**: Stable (~15%)

**Expected Results**:
```
✅ Overall Status: PASS
✅ KS Statistic: 0.45 (Excellent)
✅ Gini: 0.65 (Good)
✅ PSI: 0.05 (Stable)
✅ Accuracy: ~88%
✅ SR 11-7: ~75%
```

**Use Case**: Baseline validation, demonstrating ideal scenario

**Model Config**:
```json
{
  "model_name": "Application_Scorecard_v1",
  "model_type": "logistic_regression",
  "scorecard_type": "application",
  "product_type": "unsecured_personal_loans"
}
```

---

### Set 2: Failed Application Scorecard ❌
**Location**: `test_samples/set2_failed/`

**Scenario**: Poor model performance with validation failures

**Files**:
- `train.csv` (2,000 records)
- `test.csv` (1,000 records)
- `oot.csv` (600 records)

**Key Characteristics**:
- **Model Type**: Application Scorecard
- **Product**: Unsecured Personal Loans
- **Performance**: Poor (KS ~0.15, Gini ~0.25)
- **Stability**: Issues (PSI ~0.30)
- **Default Rate**: Unstable

**Expected Results**:
```
❌ Overall Status: FAIL
❌ KS Statistic: 0.15 (Poor)
❌ Gini: 0.25 (Weak)
❌ PSI: 0.30 (Significant drift)
❌ Accuracy: ~60%
⚠️ SR 11-7: ~40%
```

**Use Case**: Testing failure scenarios, understanding validation issues

**Model Config**:
```json
{
  "model_name": "Application_Scorecard_Failed",
  "model_type": "logistic_regression",
  "scorecard_type": "application",
  "product_type": "unsecured_personal_loans"
}
```

---

### Set 3: Behavioral Scorecard with Drift ⚠️
**Location**: `test_samples/set3_behavioral/`

**Scenario**: Existing customers with population drift

**Files**:
- `train.csv` (1,500 records)
- `test.csv` (800 records)
- `oot.csv` (500 records)

**Key Characteristics**:
- **Model Type**: Behavioral Scorecard
- **Product**: Credit Cards
- **Performance**: Excellent (KS ~0.81, Gini ~0.72)
- **Stability**: Warning (PSI ~0.15-0.20 in OOT)
- **Default Rate**: Increasing (17% → 33%)

**Expected Results**:
```
⚠️ Overall Status: WARNING
✅ KS Statistic: 0.81 (Excellent)
✅ Gini: 0.72 (Excellent)
⚠️ PSI: 0.15-0.20 (Some drift)
✅ Accuracy: ~82%
⚠️ SR 11-7: ~70% (monitoring needed)
```

**Use Case**: Demonstrating drift detection, monitoring needs

**Model Config**:
```json
{
  "model_name": "Behavioral_Scorecard_v2",
  "model_type": "logistic_regression",
  "scorecard_type": "behavioral",
  "product_type": "credit_cards"
}
```

---

## 📋 Dataset Comparison Matrix

| Feature | Set 1 (Success) | Set 2 (Failed) | Set 3 (Drift) |
|---------|----------------|----------------|---------------|
| **Scorecard Type** | Application | Application | Behavioral |
| **Product** | Personal Loans | Personal Loans | Credit Cards |
| **Train Size** | 2,000 | 2,000 | 1,500 |
| **Test Size** | 1,000 | 1,000 | 800 |
| **OOT Size** | 600 | 600 | 500 |
| **KS Statistic** | 0.45 ✅ | 0.15 ❌ | 0.81 ✅ |
| **Gini** | 0.65 ✅ | 0.25 ❌ | 0.72 ✅ |
| **PSI (OOT)** | 0.05 ✅ | 0.30 ❌ | 0.18 ⚠️ |
| **Accuracy** | 88% ✅ | 60% ❌ | 82% ✅ |
| **Default Rate** | Stable | Unstable | Increasing |
| **Overall Status** | PASS | FAIL | WARNING |
| **Learning Focus** | Baseline | Failures | Drift |

---

## 🎓 Learning Path

### Beginner: Start with Set 1
1. Upload Set 1 files
2. Run validation
3. Understand successful validation
4. Review all metrics
5. Download validation report

### Intermediate: Compare Set 1 vs Set 2
1. Run Set 1 (success case)
2. Run Set 2 (failure case)
3. Compare results side-by-side
4. Understand why Set 2 fails
5. Learn validation thresholds

### Advanced: Analyze Set 3
1. Run Set 3 (drift scenario)
2. Focus on stability metrics
3. Understand PSI/CSI warnings
4. Review monitoring recommendations
5. Plan retraining strategy

---

## 🚀 Quick Start Commands

### Set 1: Successful Validation
```bash
# Upload files
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set1_successful/train.csv" \
  -F "files=@test_samples/set1_successful/test.csv" \
  -F "files=@test_samples/set1_successful/oot.csv"

# Or use the UI at http://localhost:3000
```

### Set 2: Failed Validation
```bash
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set2_failed/train.csv" \
  -F "files=@test_samples/set2_failed/test.csv" \
  -F "files=@test_samples/set2_failed/oot.csv"
```

### Set 3: Behavioral with Drift
```bash
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set3_behavioral/train.csv" \
  -F "files=@test_samples/set3_behavioral/test.csv" \
  -F "files=@test_samples/set3_behavioral/oot.csv"
```

---

## 📊 Data Format (All Sets)

### Required Columns
All CSV files must contain:
- `score`: Model score (300-850)
- `target`: Binary outcome (0=good, 1=default)

### Optional Columns (Recommended)
- `age`: Customer age
- `income`: Annual income
- `credit_score`: Credit score
- `prediction`: Probability of default (0-1)
- Additional features specific to scorecard type

### Example Row
```csv
score,target,age,income,credit_score,prediction
650,0,35,75000,720,0.25
```

---

## 🎯 Validation Metrics Explained

### Performance Metrics

**KS Statistic** (Kolmogorov-Smirnov)
- Measures separation between good/bad customers
- Range: 0-1
- ✅ Good: > 0.30
- ✅ Excellent: > 0.40
- ❌ Poor: < 0.20

**Gini Coefficient**
- Measures discrimination power
- Range: 0-1
- ✅ Good: > 0.40
- ✅ Excellent: > 0.60
- ❌ Poor: < 0.30

**Accuracy**
- Overall prediction accuracy
- Range: 0-100%
- ✅ Good: > 80%
- ⚠️ Acceptable: 70-80%
- ❌ Poor: < 70%

### Stability Metrics

**PSI** (Population Stability Index)
- Measures population drift
- Range: 0-∞
- ✅ Stable: < 0.10
- ⚠️ Some drift: 0.10-0.25
- ❌ Significant drift: > 0.25

**CSI** (Characteristic Stability Index)
- Measures feature drift
- Range: 0-∞
- ✅ Stable: < 0.10
- ⚠️ Some drift: 0.10-0.25
- ❌ Significant drift: > 0.25

---

## 🔍 What to Look For

### In Set 1 (Success)
- ✅ All metrics in green
- ✅ High KS and Gini
- ✅ Low PSI/CSI
- ✅ Stable default rates
- ✅ High SR 11-7 compliance

### In Set 2 (Failed)
- ❌ Low KS and Gini
- ❌ High PSI (drift)
- ❌ Poor accuracy
- ❌ Unstable default rates
- ⚠️ Low SR 11-7 compliance

### In Set 3 (Drift)
- ✅ Excellent discrimination (KS, Gini)
- ⚠️ Moderate PSI in OOT
- ⚠️ Increasing default rate
- ⚠️ Population shift detected
- 📋 Monitoring recommendations

---

## 💡 Tips for Testing

1. **Start Simple**: Begin with Set 1 to understand the UI
2. **Compare Results**: Run multiple sets to see differences
3. **Focus on SR 11-7**: Check the enhanced compliance section
4. **Download Reports**: Save validation reports for reference
5. **Experiment**: Try different model configurations

---

## 📚 Additional Resources

- **QUICKSTART_GUIDE.md**: Step-by-step usage instructions
- **DOCUMENT_PROCESSING_LOGIC.md**: How documentation affects scoring
- **Set-specific READMEs**: Detailed info for each dataset
- **INPUT_DATA_GUIDE.md**: Data format requirements

---

## 🎉 Ready to Start!

1. Choose a dataset (recommend Set 1 for first time)
2. Open http://localhost:3000
3. Upload the CSV files
4. Fill in model configuration
5. Click "Start Validation"
6. Review results with enhanced SR 11-7 details!

---

**Last Updated**: 2026-05-11
**System Version**: 2.0.0
**Total Datasets**: 3 (Success, Failed, Drift)