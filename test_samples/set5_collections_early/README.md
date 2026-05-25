# Set 5: Collections Early Stage

## Overview
This dataset represents an **early-stage collections scorecard** for managing accounts that are 30-90 days past due. It predicts recovery probability for early delinquency management.

## Dataset Characteristics

### Size
- **Training**: 1,500 rows
- **Test**: 800 rows
- **Out-of-Time (OOT)**: 500 rows

### Target Variable
- **Recovery Rate**: ~45% (realistic for early-stage collections)
- **Target**: Binary (0 = Not Recovered, 1 = Recovered)

### Features

| Feature | Description | Type | Range |
|---------|-------------|------|-------|
| `customer_id` | Unique customer identifier | String | CUST_TRAIN/TEST/OOT_XXXXXX |
| `days_past_due` | Days account is past due | Integer | 30-90 days |
| `outstanding_balance` | Amount owed | Float | $500-$25,000 |
| `contact_attempts` | Number of contact attempts | Integer | 0-10 |
| `previous_delinquencies` | Past delinquency count | Integer | 0-5 |
| `account_age_months` | Account age in months | Integer | 6-120 months |
| `payment_history_score` | Historical payment score | Float | 0.3-1.0 |
| `income_verified` | Income verification status | Binary | 0 or 1 |
| `employment_stable` | Employment stability | Binary | 0 or 1 |
| `score` | Recovery probability score | Float | 0-100 |
| `prediction` | Recovery probability | Float | 0.0-1.0 |
| `target` | Actual recovery (0/1) | Binary | 0 or 1 |

## Expected Validation Results

### ✅ Should PASS Most Checks

#### Statistical Tests
- **KS Statistic**: > 0.20 (Good for collections)
- **Gini Coefficient**: > 0.25 (Acceptable for collections)
- **PSI**: < 0.30 (Stable)
- **CSI**: < 0.25 (Stable)

#### Model-Specific Validation
- **Validation Type**: Collections - Early Stage
- **Use Case**: Early Delinquency Management (30-90 DPD)
- **Status**: ✅ PASSED or ⚠️ WARNING
- **Data Quality**: All required features present
  - ✅ days_past_due
  - ✅ outstanding_balance
  - ✅ contact_attempts

#### SR 11-7 Compliance
- **Expected Score**: 70-80%
- **Status**: Substantially Compliant
- **SR 11-7 Compliant**: Yes

## How to Use

### 1. Upload Files
Upload these 3 files to the validation system:
- `train.csv`
- `test.csv`
- `oot.csv`

### 2. Configure Model
- **Model Name**: "Collections Early Stage Scorecard"
- **Product Type**: "Credit Card" or "Personal Loan"
- **Scorecard Type**: **"Collections Early"** ⬅️ Important!
- **Model Type**: "Logistic Regression"

### 3. Expected Outcome
Most validations should **PASS** with good metrics for collections models.

## Use Case
Perfect for testing:
- ✅ Collections scorecard validation
- ✅ Early delinquency management
- ✅ Recovery probability modeling
- ✅ Different target variable (recovery vs default)

## Key Differences from Application/Behavioral

### Target Variable
- **Application/Behavioral**: Predicts default (bad outcome)
- **Collections**: Predicts recovery (good outcome)
- Higher score = Higher recovery probability

### Performance Thresholds
- **Lower Gini/KS requirements** (collections are harder to predict)
- **Higher PSI tolerance** (more volatile population)
- **Different default rate range** (40-50% recovery vs 5-10% default)

### Business Context
- Used for **existing delinquent accounts**
- Focus on **recovery optimization**
- Helps prioritize **collection efforts**
- Informs **contact strategy**

## Notes
- This is a **synthetic dataset** designed for testing
- Recovery rate is realistic for early-stage collections (45%)
- Features reflect typical collections data
- Score predicts likelihood of account recovery
- Lower predictive power than application/behavioral (expected)