"""
Generate Additional Test Datasets
Set 4: Application Scorecard (High Performance)
Set 5: Collections Early Stage
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

def generate_set4_application_high_performance():
    """
    Set 4: Application Scorecard - High Performance
    Should PASS all validations with excellent metrics
    """
    print("Generating Set 4: Application Scorecard (High Performance)...")

    # Create directory
    Path("set4_application_high").mkdir(exist_ok=True)

    # Training data (2000 rows)
    n_train = 2000
    train_data = pd.DataFrame({
        'customer_id': [f'CUST_TRAIN_{i:06d}' for i in range(n_train)],
        'age': np.random.randint(21, 70, n_train),
        'income': np.random.randint(25000, 150000, n_train),
        'employment_status': np.random.choice(['Employed', 'Self-Employed', 'Retired'], n_train, p=[0.7, 0.2, 0.1]),
        'credit_history_length': np.random.randint(0, 30, n_train),
        'num_credit_accounts': np.random.randint(1, 15, n_train),
        'debt_to_income': np.random.uniform(0.1, 0.6, n_train),
        'recent_inquiries': np.random.randint(0, 5, n_train),
    })

    # Generate score (higher score = lower risk)
    train_data['score'] = (
        train_data['age'] * 5 +
        train_data['income'] / 200 +
        train_data['credit_history_length'] * 10 -
        train_data['debt_to_income'] * 300 -
        train_data['recent_inquiries'] * 20 +
        np.random.normal(0, 50, n_train)
    ).clip(300, 850)

    # Generate target (default) - lower for higher scores
    train_data['prediction'] = 1 / (1 + np.exp((train_data['score'] - 600) / 50))
    train_data['target'] = (train_data['prediction'] > np.random.uniform(0, 1, n_train)).astype(int)

    # Adjust to get good default rate (5-8%)
    default_rate = train_data['target'].mean()
    if default_rate > 0.08:
        # Reduce defaults
        excess = int((default_rate - 0.07) * n_train)
        default_indices = train_data[train_data['target'] == 1].sample(excess).index
        train_data.loc[default_indices, 'target'] = 0

    train_data.to_csv('set4_application_high/train.csv', index=False)
    print(f"  Train: {len(train_data)} rows, Default rate: {train_data['target'].mean():.2%}")

    # Test data (1000 rows) - similar distribution
    n_test = 1000
    test_data = pd.DataFrame({
        'customer_id': [f'CUST_TEST_{i:06d}' for i in range(n_test)],
        'age': np.random.randint(21, 70, n_test),
        'income': np.random.randint(25000, 150000, n_test),
        'employment_status': np.random.choice(['Employed', 'Self-Employed', 'Retired'], n_test, p=[0.7, 0.2, 0.1]),
        'credit_history_length': np.random.randint(0, 30, n_test),
        'num_credit_accounts': np.random.randint(1, 15, n_test),
        'debt_to_income': np.random.uniform(0.1, 0.6, n_test),
        'recent_inquiries': np.random.randint(0, 5, n_test),
    })

    test_data['score'] = (
        test_data['age'] * 5 +
        test_data['income'] / 200 +
        test_data['credit_history_length'] * 10 -
        test_data['debt_to_income'] * 300 -
        test_data['recent_inquiries'] * 20 +
        np.random.normal(0, 50, n_test)
    ).clip(300, 850)

    test_data['prediction'] = 1 / (1 + np.exp((test_data['score'] - 600) / 50))
    test_data['target'] = (test_data['prediction'] > np.random.uniform(0, 1, n_test)).astype(int)

    # Adjust default rate
    default_rate = test_data['target'].mean()
    if default_rate > 0.08:
        excess = int((default_rate - 0.07) * n_test)
        default_indices = test_data[test_data['target'] == 1].sample(excess).index
        test_data.loc[default_indices, 'target'] = 0

    test_data.to_csv('set4_application_high/test.csv', index=False)
    print(f"  Test: {len(test_data)} rows, Default rate: {test_data['target'].mean():.2%}")

    # OOT data (600 rows) - similar distribution
    n_oot = 600
    oot_data = pd.DataFrame({
        'customer_id': [f'CUST_OOT_{i:06d}' for i in range(n_oot)],
        'age': np.random.randint(21, 70, n_oot),
        'income': np.random.randint(25000, 150000, n_oot),
        'employment_status': np.random.choice(['Employed', 'Self-Employed', 'Retired'], n_oot, p=[0.7, 0.2, 0.1]),
        'credit_history_length': np.random.randint(0, 30, n_oot),
        'num_credit_accounts': np.random.randint(1, 15, n_oot),
        'debt_to_income': np.random.uniform(0.1, 0.6, n_oot),
        'recent_inquiries': np.random.randint(0, 5, n_oot),
    })

    oot_data['score'] = (
        oot_data['age'] * 5 +
        oot_data['income'] / 200 +
        oot_data['credit_history_length'] * 10 -
        oot_data['debt_to_income'] * 300 -
        oot_data['recent_inquiries'] * 20 +
        np.random.normal(0, 50, n_oot)
    ).clip(300, 850)

    oot_data['prediction'] = 1 / (1 + np.exp((oot_data['score'] - 600) / 50))
    oot_data['target'] = (oot_data['prediction'] > np.random.uniform(0, 1, n_oot)).astype(int)

    # Adjust default rate
    default_rate = oot_data['target'].mean()
    if default_rate > 0.08:
        excess = int((default_rate - 0.07) * n_oot)
        default_indices = oot_data[oot_data['target'] == 1].sample(excess).index
        oot_data.loc[default_indices, 'target'] = 0

    oot_data.to_csv('set4_application_high/oot.csv', index=False)
    print(f"  OOT: {len(oot_data)} rows, Default rate: {oot_data['target'].mean():.2%}")

    print("✅ Set 4 generated successfully!\n")


def generate_set5_collections_early():
    """
    Set 5: Collections Early Stage (30-90 DPD)
    For early delinquency management
    """
    print("Generating Set 5: Collections Early Stage...")

    # Create directory
    Path("set5_collections_early").mkdir(exist_ok=True)

    # Training data (1500 rows)
    n_train = 1500
    train_data = pd.DataFrame({
        'customer_id': [f'CUST_TRAIN_{i:06d}' for i in range(n_train)],
        'days_past_due': np.random.randint(30, 90, n_train),
        'outstanding_balance': np.random.uniform(500, 25000, n_train),
        'contact_attempts': np.random.randint(0, 10, n_train),
        'previous_delinquencies': np.random.randint(0, 5, n_train),
        'account_age_months': np.random.randint(6, 120, n_train),
        'payment_history_score': np.random.uniform(0.3, 1.0, n_train),
        'income_verified': np.random.choice([0, 1], n_train, p=[0.3, 0.7]),
        'employment_stable': np.random.choice([0, 1], n_train, p=[0.4, 0.6]),
    })

    # Generate recovery probability score (0-100)
    train_data['score'] = (
        (90 - train_data['days_past_due']) * 0.5 +
        train_data['payment_history_score'] * 30 +
        train_data['income_verified'] * 15 +
        train_data['employment_stable'] * 15 -
        train_data['previous_delinquencies'] * 5 -
        train_data['contact_attempts'] * 2 +
        np.random.normal(0, 10, n_train)
    ).clip(0, 100)

    # Generate prediction (recovery probability)
    train_data['prediction'] = train_data['score'] / 100

    # Generate target (recovered = 1, not recovered = 0)
    # Higher score = higher recovery probability
    train_data['target'] = (train_data['prediction'] > np.random.uniform(0, 1, n_train)).astype(int)

    # Adjust to get realistic recovery rate (40-50% for early stage)
    recovery_rate = train_data['target'].mean()
    if recovery_rate < 0.40:
        # Increase recoveries
        deficit = int((0.45 - recovery_rate) * n_train)
        non_recovery_indices = train_data[train_data['target'] == 0].sample(min(deficit, (train_data['target'] == 0).sum())).index
        train_data.loc[non_recovery_indices, 'target'] = 1
    elif recovery_rate > 0.50:
        # Decrease recoveries
        excess = int((recovery_rate - 0.45) * n_train)
        recovery_indices = train_data[train_data['target'] == 1].sample(min(excess, (train_data['target'] == 1).sum())).index
        train_data.loc[recovery_indices, 'target'] = 0

    train_data.to_csv('set5_collections_early/train.csv', index=False)
    print(f"  Train: {len(train_data)} rows, Recovery rate: {train_data['target'].mean():.2%}")

    # Test data (800 rows)
    n_test = 800
    test_data = pd.DataFrame({
        'customer_id': [f'CUST_TEST_{i:06d}' for i in range(n_test)],
        'days_past_due': np.random.randint(30, 90, n_test),
        'outstanding_balance': np.random.uniform(500, 25000, n_test),
        'contact_attempts': np.random.randint(0, 10, n_test),
        'previous_delinquencies': np.random.randint(0, 5, n_test),
        'account_age_months': np.random.randint(6, 120, n_test),
        'payment_history_score': np.random.uniform(0.3, 1.0, n_test),
        'income_verified': np.random.choice([0, 1], n_test, p=[0.3, 0.7]),
        'employment_stable': np.random.choice([0, 1], n_test, p=[0.4, 0.6]),
    })

    test_data['score'] = (
        (90 - test_data['days_past_due']) * 0.5 +
        test_data['payment_history_score'] * 30 +
        test_data['income_verified'] * 15 +
        test_data['employment_stable'] * 15 -
        test_data['previous_delinquencies'] * 5 -
        test_data['contact_attempts'] * 2 +
        np.random.normal(0, 10, n_test)
    ).clip(0, 100)

    test_data['prediction'] = test_data['score'] / 100
    test_data['target'] = (test_data['prediction'] > np.random.uniform(0, 1, n_test)).astype(int)

    # Adjust recovery rate
    recovery_rate = test_data['target'].mean()
    if recovery_rate < 0.40:
        deficit = int((0.45 - recovery_rate) * n_test)
        non_recovery_indices = test_data[test_data['target'] == 0].sample(min(deficit, (test_data['target'] == 0).sum())).index
        test_data.loc[non_recovery_indices, 'target'] = 1
    elif recovery_rate > 0.50:
        excess = int((recovery_rate - 0.45) * n_test)
        recovery_indices = test_data[test_data['target'] == 1].sample(min(excess, (test_data['target'] == 1).sum())).index
        test_data.loc[recovery_indices, 'target'] = 0

    test_data.to_csv('set5_collections_early/test.csv', index=False)
    print(f"  Test: {len(test_data)} rows, Recovery rate: {test_data['target'].mean():.2%}")

    # OOT data (500 rows)
    n_oot = 500
    oot_data = pd.DataFrame({
        'customer_id': [f'CUST_OOT_{i:06d}' for i in range(n_oot)],
        'days_past_due': np.random.randint(30, 90, n_oot),
        'outstanding_balance': np.random.uniform(500, 25000, n_oot),
        'contact_attempts': np.random.randint(0, 10, n_oot),
        'previous_delinquencies': np.random.randint(0, 5, n_oot),
        'account_age_months': np.random.randint(6, 120, n_oot),
        'payment_history_score': np.random.uniform(0.3, 1.0, n_oot),
        'income_verified': np.random.choice([0, 1], n_oot, p=[0.3, 0.7]),
        'employment_stable': np.random.choice([0, 1], n_oot, p=[0.4, 0.6]),
    })

    oot_data['score'] = (
        (90 - oot_data['days_past_due']) * 0.5 +
        oot_data['payment_history_score'] * 30 +
        oot_data['income_verified'] * 15 +
        oot_data['employment_stable'] * 15 -
        oot_data['previous_delinquencies'] * 5 -
        oot_data['contact_attempts'] * 2 +
        np.random.normal(0, 10, n_oot)
    ).clip(0, 100)

    oot_data['prediction'] = oot_data['score'] / 100
    oot_data['target'] = (oot_data['prediction'] > np.random.uniform(0, 1, n_oot)).astype(int)

    # Adjust recovery rate
    recovery_rate = oot_data['target'].mean()
    if recovery_rate < 0.40:
        deficit = int((0.45 - recovery_rate) * n_oot)
        non_recovery_indices = oot_data[oot_data['target'] == 0].sample(min(deficit, (oot_data['target'] == 0).sum())).index
        oot_data.loc[non_recovery_indices, 'target'] = 1
    elif recovery_rate > 0.50:
        excess = int((recovery_rate - 0.45) * n_oot)
        recovery_indices = oot_data[oot_data['target'] == 1].sample(min(excess, (oot_data['target'] == 1).sum())).index
        oot_data.loc[recovery_indices, 'target'] = 0

    oot_data.to_csv('set5_collections_early/oot.csv', index=False)
    print(f"  OOT: {len(oot_data)} rows, Recovery rate: {oot_data['target'].mean():.2%}")

    print("✅ Set 5 generated successfully!\n")


if __name__ == "__main__":
    print("="*80)
    print("Generating Additional Test Datasets")
    print("="*80 + "\n")

    generate_set4_application_high_performance()
    generate_set5_collections_early()

    print("="*80)
    print("✅ All datasets generated successfully!")
    print("="*80)
    print("\nGenerated:")
    print("  • Set 4: test_samples/set4_application_high/")
    print("  • Set 5: test_samples/set5_collections_early/")

# Made with Bob
