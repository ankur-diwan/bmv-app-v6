# Set 3: Behavioral Scorecard Dataset

## Overview
This dataset represents a **Behavioral Scorecard** for existing credit card customers. It includes some population drift to demonstrate how the system handles stability issues.

## Dataset Characteristics

### Files
- **train.csv**: 1,500 records (training period: 12-18 months ago)
- **test.csv**: 800 records (test period: 6-12 months ago)
- **oot.csv**: 500 records (out-of-time: recent data with drift)

### Key Features

| Feature | Description | Range |
|---------|-------------|-------|
| `customer_id` | Unique customer identifier | CUST_XXX_XXXXXX |
| `age` | Customer age | 18-80 years |
| `account_balance` | Current account balance | $0-$50,000 |
| `credit_utilization` | Credit utilization ratio | 0-1 (0-100%) |
| `payment_ratio` | On-time payment ratio | 0-1 (0-100%) |
| `months_on_book` | Months as customer | 1-120 months |
| `num_transactions` | Monthly transactions | Poisson(15) |
| `avg_transaction_amount` | Average transaction | $10-$2,000 |
| `delinquency_history` | Past delinquencies | 0-3 |
| `target` | Default indicator | 0=Good, 1=Default |
| `score` | Model score | 300-850 |
| `prediction` | Default probability | 0-1 |

## Expected Results

### Performance Metrics
- **KS Statistic**: ~0.81 (Excellent discrimination)
- **Gini Coefficient**: ~0.70-0.75 (Good)
- **Accuracy**: ~82-85%

### Stability Metrics
- **PSI (Test)**: ~0.08 (Stable)
- **PSI (OOT)**: ~0.15-0.20 (Some drift - WARNING)
- **CSI**: ~0.12 (Moderate drift)

### Default Rates
- **Train**: 17.5%
- **Test**: 19.6%
- **OOT**: 32.8% ⚠️ (Significant increase - economic stress)

## Key Observations

### ✅ Strengths
1. **Excellent Discrimination**: KS > 0.80 shows strong model performance
2. **Good Sample Size**: Sufficient data for validation
3. **Realistic Features**: Behavioral metrics typical of credit cards

### ⚠️ Warnings
1. **Population Drift**: OOT period shows increased default rate
2. **Stability Concerns**: PSI in OOT period indicates population shift
3. **Economic Changes**: Higher utilization and lower payment ratios in recent data

### 📋 Validation Recommendations
1. **Monitor Drift**: Set up ongoing PSI/CSI monitoring
2. **Retraining**: Consider model retraining due to population changes
3. **Threshold Review**: Adjust decision thresholds for current environment
4. **Stress Testing**: Test model under various economic scenarios

## Use Case

### Model Configuration
```json
{
  "model_name": "Behavioral_Scorecard_v2",
  "model_type": "logistic_regression",
  "scorecard_type": "behavioral",
  "product_type": "credit_cards",
  "version": "2.0",
  "owner": "Credit Risk Analytics"
}
```

### Upload Command
```bash
curl -X POST http://localhost:8000/api/upload-documents \
  -F "files=@test_samples/set3_behavioral/train.csv" \
  -F "files=@test_samples/set3_behavioral/test.csv" \
  -F "files=@test_samples/set3_behavioral/oot.csv"
```

## Comparison with Set 1 (Application Scorecard)

| Metric | Set 1 (Application) | Set 3 (Behavioral) |
|--------|--------------------|--------------------|
| **Model Type** | Application | Behavioral |
| **Population** | New applicants | Existing customers |
| **KS Statistic** | ~0.45 | ~0.81 |
| **PSI (OOT)** | ~0.05 | ~0.15-0.20 |
| **Default Rate** | Stable (~15%) | Increasing (17%→33%) |
| **Stability** | ✅ Excellent | ⚠️ Some drift |

## Learning Objectives

This dataset helps you understand:
1. **Behavioral vs Application**: Different characteristics and challenges
2. **Population Drift**: How to detect and handle stability issues
3. **Economic Impact**: Effect of external factors on model performance
4. **Monitoring Needs**: Importance of ongoing validation

## Next Steps

After running validation:
1. Review the **Stability** section carefully
2. Check **PSI/CSI** values in OOT period
3. Examine **SR 11-7 Compliance** for monitoring recommendations
4. Consider **retraining** or **recalibration** strategies

---

**Generated**: 2026-05-11
**Purpose**: Demonstrate behavioral scorecard validation with drift detection