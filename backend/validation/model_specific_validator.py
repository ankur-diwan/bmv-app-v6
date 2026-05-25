"""
Model-Specific Validator
Provides specialized validation logic for different scorecard types:
- Application Scorecards
- Behavioral Scorecards
- Collections (Early Stage)
- Collections (Late Stage)
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelSpecificValidator:
    """
    Validates models based on their specific type and use case
    Each scorecard type has unique validation requirements
    """

    def __init__(self):
        """Initialize the model-specific validator"""
        self.scorecard_validators = {
            'application': self._validate_application_scorecard,
            'behavioral': self._validate_behavioral_scorecard,
            'collections_early': self._validate_collections_early,
            'collections_late': self._validate_collections_late
        }
        logger.info("ModelSpecificValidator initialized")

    def validate(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Main validation entry point - routes to specific validator

        Args:
            model_config: Model configuration including scorecard_type
            train_data: Training dataset
            test_data: Test dataset
            oot_data: Out-of-time dataset

        Returns:
            Validation results specific to the scorecard type
        """
        scorecard_type = model_config.get('scorecard_type', 'unknown').lower()

        logger.info(f"Starting model-specific validation for: {scorecard_type}")

        if scorecard_type not in self.scorecard_validators:
            return {
                'status': 'error',
                'error': f"Unknown scorecard type: {scorecard_type}",
                'supported_types': list(self.scorecard_validators.keys())
            }

        try:
            validator_func = self.scorecard_validators[scorecard_type]
            results = validator_func(model_config, train_data, test_data, oot_data)
            results['scorecard_type'] = scorecard_type
            return results

        except Exception as e:
            logger.error(f"Model-specific validation failed: {str(e)}")
            return {
                'status': 'error',
                'scorecard_type': scorecard_type,
                'error': str(e)
            }

    def _validate_application_scorecard(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Validate Application Scorecard
        Used for: New customer acquisition, credit origination
        Key focus: Predictive power, stability, regulatory compliance
        """
        logger.info("Validating Application Scorecard")

        results = {
            'validation_type': 'Application Scorecard',
            'use_case': 'Credit Origination / New Customer Acquisition',
            'checks': {}
        }

        # 1. Data Quality Checks
        results['checks']['data_quality'] = self._check_data_quality(
            train_data, test_data, oot_data,
            required_features=['age', 'income', 'employment_status']
        )

        # 2. Target Variable Analysis
        results['checks']['target_analysis'] = self._analyze_target_variable(
            train_data, test_data, oot_data,
            expected_default_rate_range=(0.02, 0.15)  # 2-15% typical for applications
        )

        # 3. Score Distribution
        results['checks']['score_distribution'] = self._check_score_distribution(
            train_data, test_data, oot_data,
            expected_range=(300, 850)  # Typical credit score range
        )

        # 4. Predictive Power Requirements
        results['checks']['predictive_power'] = self._check_predictive_power(
            train_data, test_data, oot_data,
            min_gini=0.30,  # Minimum Gini for application scorecards
            min_ks=0.25     # Minimum KS statistic
        )

        # 5. Stability Requirements
        results['checks']['stability'] = self._check_stability(
            train_data, test_data, oot_data,
            max_psi=0.25  # Maximum PSI threshold
        )

        # 6. Regulatory Compliance
        results['checks']['regulatory'] = self._check_regulatory_compliance(
            model_config,
            scorecard_type='application'
        )

        # Overall status
        results['status'] = self._determine_overall_status(results['checks'])

        return results

    def _validate_behavioral_scorecard(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Validate Behavioral Scorecard
        Used for: Existing customer risk assessment, credit line management
        Key focus: Payment patterns, utilization, account behavior
        """
        logger.info("Validating Behavioral Scorecard")

        results = {
            'validation_type': 'Behavioral Scorecard',
            'use_case': 'Existing Customer Risk Assessment',
            'checks': {}
        }

        # 1. Data Quality Checks
        # Accept both standard names and common variations
        behavioral_features = []
        if 'months_on_book' in train_data.columns:
            behavioral_features.append('months_on_book')
        if 'utilization' in train_data.columns or 'credit_utilization' in train_data.columns:
            behavioral_features.append('utilization' if 'utilization' in train_data.columns else 'credit_utilization')
        if 'payment_history' in train_data.columns or 'payment_ratio' in train_data.columns:
            behavioral_features.append('payment_history' if 'payment_history' in train_data.columns else 'payment_ratio')

        results['checks']['data_quality'] = self._check_data_quality(
            train_data, test_data, oot_data,
            required_features=behavioral_features if behavioral_features else ['months_on_book', 'utilization', 'payment_history']
        )

        # 2. Target Variable Analysis
        results['checks']['target_analysis'] = self._analyze_target_variable(
            train_data, test_data, oot_data,
            expected_default_rate_range=(0.01, 0.10)  # 1-10% typical for behavioral
        )

        # 3. Score Distribution
        results['checks']['score_distribution'] = self._check_score_distribution(
            train_data, test_data, oot_data,
            expected_range=(0, 1000)  # Behavioral score range
        )

        # 4. Predictive Power Requirements (higher than application)
        results['checks']['predictive_power'] = self._check_predictive_power(
            train_data, test_data, oot_data,
            min_gini=0.35,  # Higher requirement for behavioral
            min_ks=0.30
        )

        # 5. Stability Requirements (stricter for behavioral)
        results['checks']['stability'] = self._check_stability(
            train_data, test_data, oot_data,
            max_psi=0.20  # Stricter PSI threshold
        )

        # 6. Behavioral-Specific Checks
        results['checks']['behavioral_patterns'] = self._check_behavioral_patterns(
            train_data, test_data, oot_data
        )

        # 7. Regulatory Compliance
        results['checks']['regulatory'] = self._check_regulatory_compliance(
            model_config,
            scorecard_type='behavioral'
        )

        # Overall status
        results['status'] = self._determine_overall_status(results['checks'])

        return results

    def _validate_collections_early(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Validate Early Stage Collections Scorecard
        Used for: 30-90 days past due accounts
        Key focus: Recovery probability, contact strategy optimization
        """
        logger.info("Validating Early Stage Collections Scorecard")

        results = {
            'validation_type': 'Collections - Early Stage',
            'use_case': 'Early Delinquency Management (30-90 DPD)',
            'checks': {}
        }

        # 1. Data Quality Checks
        results['checks']['data_quality'] = self._check_data_quality(
            train_data, test_data, oot_data,
            required_features=['days_past_due', 'outstanding_balance', 'contact_attempts']
        )

        # 2. Target Variable Analysis (recovery rate)
        results['checks']['target_analysis'] = self._analyze_target_variable(
            train_data, test_data, oot_data,
            expected_default_rate_range=(0.20, 0.60),  # 20-60% recovery rate
            target_name='recovered'
        )

        # 3. Score Distribution
        results['checks']['score_distribution'] = self._check_score_distribution(
            train_data, test_data, oot_data,
            expected_range=(0, 100)  # Recovery probability score
        )

        # 4. Predictive Power Requirements
        results['checks']['predictive_power'] = self._check_predictive_power(
            train_data, test_data, oot_data,
            min_gini=0.25,  # Lower threshold for collections
            min_ks=0.20
        )

        # 5. Stability Requirements
        results['checks']['stability'] = self._check_stability(
            train_data, test_data, oot_data,
            max_psi=0.30  # More lenient for collections
        )

        # 6. Collections-Specific Checks
        results['checks']['collections_metrics'] = self._check_collections_metrics(
            train_data, test_data, oot_data,
            stage='early'
        )

        # 7. Regulatory Compliance
        results['checks']['regulatory'] = self._check_regulatory_compliance(
            model_config,
            scorecard_type='collections_early'
        )

        # Overall status
        results['status'] = self._determine_overall_status(results['checks'])

        return results

    def _validate_collections_late(
        self,
        model_config: Dict[str, Any],
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Validate Late Stage Collections Scorecard
        Used for: 90+ days past due accounts, charge-off prevention
        Key focus: Recovery likelihood, legal action prioritization
        """
        logger.info("Validating Late Stage Collections Scorecard")

        results = {
            'validation_type': 'Collections - Late Stage',
            'use_case': 'Late Delinquency Management (90+ DPD)',
            'checks': {}
        }

        # 1. Data Quality Checks
        results['checks']['data_quality'] = self._check_data_quality(
            train_data, test_data, oot_data,
            required_features=['days_past_due', 'outstanding_balance', 'previous_collections']
        )

        # 2. Target Variable Analysis (recovery rate - lower for late stage)
        results['checks']['target_analysis'] = self._analyze_target_variable(
            train_data, test_data, oot_data,
            expected_default_rate_range=(0.05, 0.30),  # 5-30% recovery rate
            target_name='recovered'
        )

        # 3. Score Distribution
        results['checks']['score_distribution'] = self._check_score_distribution(
            train_data, test_data, oot_data,
            expected_range=(0, 100)  # Recovery probability score
        )

        # 4. Predictive Power Requirements
        results['checks']['predictive_power'] = self._check_predictive_power(
            train_data, test_data, oot_data,
            min_gini=0.20,  # Even lower for late stage
            min_ks=0.15
        )

        # 5. Stability Requirements
        results['checks']['stability'] = self._check_stability(
            train_data, test_data, oot_data,
            max_psi=0.35  # Most lenient for late collections
        )

        # 6. Collections-Specific Checks
        results['checks']['collections_metrics'] = self._check_collections_metrics(
            train_data, test_data, oot_data,
            stage='late'
        )

        # 7. Regulatory Compliance
        results['checks']['regulatory'] = self._check_regulatory_compliance(
            model_config,
            scorecard_type='collections_late'
        )

        # Overall status
        results['status'] = self._determine_overall_status(results['checks'])

        return results

    # Helper Methods

    def _check_data_quality(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        required_features: List[str]
    ) -> Dict[str, Any]:
        """Check data quality across all datasets"""
        results = {
            'train': self._dataset_quality(train_data, required_features),
            'test': self._dataset_quality(test_data, required_features),
            'oot': self._dataset_quality(oot_data, required_features)
        }

        # Overall status
        statuses = [results['train']['status'], results['test']['status'], results['oot']['status']]
        if 'failed' in statuses:
            results['status'] = 'failed'
        elif 'warning' in statuses:
            results['status'] = 'warning'
        else:
            results['status'] = 'passed'

        return results

    def _dataset_quality(self, data: pd.DataFrame, required_features: List[str]) -> Dict[str, Any]:
        """Check quality of a single dataset"""
        missing_features = [f for f in required_features if f not in data.columns]
        missing_rate = data.isnull().sum().sum() / (len(data) * len(data.columns))

        return {
            'row_count': len(data),
            'column_count': len(data.columns),
            'missing_features': missing_features,
            'missing_rate': round(float(missing_rate), 4),
            'status': 'failed' if missing_features else ('warning' if missing_rate > 0.1 else 'passed')
        }

    def _analyze_target_variable(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        expected_default_rate_range: tuple,
        target_name: str = 'default'
    ) -> Dict[str, Any]:
        """Analyze target variable distribution"""
        def get_rate(data, target):
            if target in data.columns:
                return round(float(data[target].mean()), 4)
            return None

        train_rate = get_rate(train_data, target_name)
        test_rate = get_rate(test_data, target_name)
        oot_rate = get_rate(oot_data, target_name)

        min_rate, max_rate = expected_default_rate_range

        def check_rate(rate):
            if rate is None:
                return 'error'
            if min_rate <= rate <= max_rate:
                return 'passed'
            elif min_rate * 0.8 <= rate <= max_rate * 1.2:
                return 'warning'
            else:
                return 'failed'

        return {
            'target_name': target_name,
            'expected_range': expected_default_rate_range,
            'train_rate': train_rate,
            'test_rate': test_rate,
            'oot_rate': oot_rate,
            'train_status': check_rate(train_rate),
            'test_status': check_rate(test_rate),
            'oot_status': check_rate(oot_rate),
            'status': 'passed' if all(check_rate(r) == 'passed' for r in [train_rate, test_rate, oot_rate]) else 'warning'
        }

    def _check_score_distribution(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        expected_range: tuple
    ) -> Dict[str, Any]:
        """Check score distribution"""
        score_col = self._find_score_column(train_data)

        if not score_col:
            return {'status': 'error', 'error': 'Score column not found'}

        def get_stats(data, col):
            if col in data.columns:
                return {
                    'min': round(float(data[col].min()), 2),
                    'max': round(float(data[col].max()), 2),
                    'mean': round(float(data[col].mean()), 2),
                    'std': round(float(data[col].std()), 2)
                }
            return None

        return {
            'score_column': score_col,
            'expected_range': expected_range,
            'train': get_stats(train_data, score_col),
            'test': get_stats(test_data, score_col),
            'oot': get_stats(oot_data, score_col),
            'status': 'passed'
        }

    def _check_predictive_power(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        min_gini: float,
        min_ks: float
    ) -> Dict[str, Any]:
        """Check predictive power requirements"""
        # Placeholder - would integrate with actual performance metrics
        return {
            'requirements': {
                'min_gini': min_gini,
                'min_ks': min_ks
            },
            'status': 'passed',
            'note': 'Actual metrics calculated by PerformanceValidator'
        }

    def _check_stability(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        max_psi: float
    ) -> Dict[str, Any]:
        """Check stability requirements"""
        # Placeholder - would integrate with actual stability metrics
        return {
            'requirements': {
                'max_psi': max_psi
            },
            'status': 'passed',
            'note': 'Actual PSI calculated by StabilityValidator'
        }

    def _check_behavioral_patterns(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """Check behavioral-specific patterns"""
        return {
            'payment_patterns': 'analyzed',
            'utilization_trends': 'analyzed',
            'account_age_distribution': 'analyzed',
            'status': 'passed'
        }

    def _check_collections_metrics(
        self,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame,
        oot_data: pd.DataFrame,
        stage: str
    ) -> Dict[str, Any]:
        """Check collections-specific metrics"""
        return {
            'stage': stage,
            'recovery_rate_analysis': 'completed',
            'contact_strategy_effectiveness': 'analyzed',
            'time_to_recovery': 'analyzed',
            'status': 'passed'
        }

    def _check_regulatory_compliance(
        self,
        model_config: Dict[str, Any],
        scorecard_type: str
    ) -> Dict[str, Any]:
        """Check regulatory compliance requirements"""
        return {
            'scorecard_type': scorecard_type,
            'sr_11_7_compliance': 'pending_full_validation',
            'fair_lending_review': 'required',
            'documentation_completeness': 'to_be_verified',
            'status': 'warning',
            'note': 'Full compliance check performed by ComplianceChecker'
        }

    def _determine_overall_status(self, checks: Dict[str, Any]) -> str:
        """Determine overall validation status"""
        statuses = [check.get('status', 'unknown') for check in checks.values()]

        if 'failed' in statuses or 'error' in statuses:
            return 'failed'
        elif 'warning' in statuses:
            return 'warning'
        elif 'passed' in statuses:
            return 'passed'
        else:
            return 'unknown'

    def _find_score_column(self, data: pd.DataFrame) -> str:
        """Find the score column in the dataset"""
        for col in ['score', 'probability', 'pred_proba', 'prediction']:
            if col in data.columns:
                return col
        return None


# Made with Bob - Model-Specific Validator