# Set 4: Application Scorecard (High Performance)

## Overview
This dataset represents a **high-performing application scorecard** for new customer credit origination. It should **PASS all validations** with excellent metrics.

## Dataset Characteristics

### Size
- **Training**: 2,000 rows
- **Test**: 1,000 rows
- **Out-of-Time (OOT)**: 600 rows

### Target Variable
- **Default Rate**: ~7% (within optimal range of 5-8%)
- **Target**: Binary (0 = No Default, 1 = Default)

### Features

| Feature | Description | Type | Range |
|---------|-------------|------|-------|
| `customer_id` | Unique customer identifier | String | CUST_TRAIN/TEST/OOT_XXXXXX |
| `age` | Customer age | Integer | 21-70 years |
| `income` | Annual income | Integer | $25,000-$150,000 |
| `employment_status` | Employment type | Categorical | Employed, Self-Employed, Retired |
| `credit_history_length` | Years of credit history | Integer | 0-30 years |
| `num_credit_accounts` | Number of credit accounts | Integer | 1-15 |
| `debt_to_income` | Debt-to-income ratio | Float | 0.1-0.6 |
| `recent_inquiries` | Recent credit inquiries | Integer | 0-5 |
| `score` | Credit score | Float | 300-850 |
| `prediction` | Default probability | Float | 0.0-1.0 |
| `target` | Actual default (0/1) | Binary | 0 or 1 |

## Expected Validation Results

### ✅ Should PASS All Checks

#### Statistical Tests
- **KS Statistic**: > 0.30 (Excellent)
- **Gini Coefficient**: > 0.40 (Excellent)
- **PSI**: < 0.10 (Very Stable)
- **CSI**: < 0.15 (Very Stable)

#### Model-Specific Validation
- **Validation Type**: Application Scorecard
- **Use Case**: Credit Origination / New Customer Acquisition
- **Status**: ✅ PASSED
- **Data Quality**: All required features present
  - ✅ age
  - ✅ income
  - ✅ employment_status

#### SR 11-7 Compliance
- **Expected Score**: 75-85%
- **Status**: Substantially Compliant
- **SR 11-7 Compliant**: Yes

## How to Use

### 1. Upload Files
Upload these 3 files to the validation system:
- `train.csv`
- `test.csv`
- `oot.csv`

### 2. Configure Model
- **Model Name**: "Application Scorecard - High Performance"
- **Product Type**: "Personal Loan" or "Credit Card"
- **Scorecard Type**: **"Application"** ⬅️ Important!
- **Model Type**: "Logistic Regression"

### 3. Expected Outcome
All validations should **PASS** with excellent metrics!

## Use Case
Perfect for testing:
- ✅ Successful validation workflow
- ✅ High-performance model metrics
- ✅ Application scorecard validation
- ✅ Complete SR 11-7 compliance

## Notes
- This is a **synthetic dataset** designed for testing
- Default rate is realistic for application scorecards (7%)
- All features have realistic distributions
- Score is strongly predictive of default
- Excellent separation between defaulters and non-defaulters