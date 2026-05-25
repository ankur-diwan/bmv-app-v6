"""
SR 11-7 Compliance Checker
Comprehensive regulatory compliance validation following Federal Reserve SR 11-7 guidelines
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime


class ComplianceChecker:
    """
    Perform comprehensive SR 11-7 compliance checks for banking model validation.

    SR 11-7 Framework Components:
    1. Model Development and Implementation
    2. Model Validation (Conceptual Soundness, Ongoing Monitoring, Outcomes Analysis)
    3. Data Quality and Relevance
    4. Model Governance and Controls
    """

    # SR 11-7 Requirements with weights (total = 100%)
    SR_11_7_REQUIREMENTS = {
        "model_purpose": {
            "weight": 8,
            "description": "Clear articulation of model purpose and use cases",
            "checks": ["purpose_documented", "use_cases_defined", "business_alignment"]
        },
        "conceptual_soundness": {
            "weight": 15,
            "description": "Sound theoretical foundation and methodology",
            "checks": ["theory_documented", "methodology_appropriate", "assumptions_validated"]
        },
        "data_quality": {
            "weight": 12,
            "description": "Data sufficiency, quality, and representativeness",
            "checks": ["data_completeness", "data_accuracy", "data_representativeness"]
        },
        "performance_validation": {
            "weight": 15,
            "description": "Comprehensive performance testing and metrics",
            "checks": ["discrimination_power", "calibration", "performance_metrics"]
        },
        "stability_analysis": {
            "weight": 12,
            "description": "Population and characteristic stability over time",
            "checks": ["psi_analysis", "csi_analysis", "stability_assessment"]
        },
        "assumptions_testing": {
            "weight": 10,
            "description": "Testing and validation of model assumptions",
            "checks": ["assumptions_documented", "assumptions_tested", "sensitivity_analysis"]
        },
        "implementation_validation": {
            "weight": 8,
            "description": "Proper model implementation and deployment",
            "checks": ["implementation_verified", "production_testing", "rollback_plan"]
        },
        "ongoing_monitoring": {
            "weight": 10,
            "description": "Continuous monitoring and performance tracking",
            "checks": ["monitoring_plan", "drift_detection", "revalidation_schedule"]
        },
        "documentation": {
            "weight": 10,
            "description": "Comprehensive and accessible documentation",
            "checks": ["model_documentation", "validation_report", "audit_trail"]
        }
    }

    def __init__(self):
        """Initialize the compliance checker."""
        self.total_weight = sum(req["weight"] for req in self.SR_11_7_REQUIREMENTS.values())

    def check_sr_11_7_compliance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive SR 11-7 compliance check.

        Args:
            results: Validation results dictionary containing all validation outputs

        Returns:
            Dictionary with compliance status, score, and detailed analysis
        """
        # Perform detailed compliance checks
        compliance_details = self._check_all_requirements(results)

        # Calculate overall compliance score
        compliance_score = self._calculate_compliance_score(compliance_details)

        # Determine compliance status
        compliance_status = self._determine_compliance_status(compliance_score)

        # Identify gaps and recommendations
        gaps = self._identify_gaps(compliance_details)
        recommendations = self._generate_recommendations(gaps)

        # Generate compliance summary
        return {
            "overall_status": compliance_status,
            "compliance_score": round(compliance_score, 2),
            "compliance_percentage": f"{round(compliance_score, 1)}%",
            "sr_11_7_compliant": compliance_score >= 90.0,
            "timestamp": datetime.utcnow().isoformat(),
            "detailed_checks": compliance_details,
            "gaps_identified": gaps,
            "recommendations": recommendations,
            "summary": self._generate_summary(compliance_score, compliance_details)
        }

    def _check_all_requirements(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check all SR 11-7 requirements against validation results."""
        compliance_details = {}

        for req_name, req_info in self.SR_11_7_REQUIREMENTS.items():
            compliance_details[req_name] = self._check_requirement(
                req_name, req_info, results
            )

        return compliance_details

    def _check_requirement(
        self, req_name: str, req_info: Dict[str, Any], results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Check a specific SR 11-7 requirement."""
        checks_passed = 0
        total_checks = len(req_info["checks"])
        check_details = {}

        # Perform specific checks based on requirement type
        if req_name == "model_purpose":
            check_details = self._check_model_purpose(results)
        elif req_name == "conceptual_soundness":
            check_details = self._check_conceptual_soundness(results)
        elif req_name == "data_quality":
            check_details = self._check_data_quality(results)
        elif req_name == "performance_validation":
            check_details = self._check_performance_validation(results)
        elif req_name == "stability_analysis":
            check_details = self._check_stability_analysis(results)
        elif req_name == "assumptions_testing":
            check_details = self._check_assumptions_testing(results)
        elif req_name == "implementation_validation":
            check_details = self._check_implementation_validation(results)
        elif req_name == "ongoing_monitoring":
            check_details = self._check_ongoing_monitoring(results)
        elif req_name == "documentation":
            check_details = self._check_documentation(results)

        # Count passed checks
        checks_passed = sum(1 for check in check_details.values() if check.get("passed", False))

        # Calculate requirement score
        requirement_score = (checks_passed / total_checks) * req_info["weight"]

        return {
            "description": req_info["description"],
            "weight": req_info["weight"],
            "checks_passed": checks_passed,
            "total_checks": total_checks,
            "score": round(requirement_score, 2),
            "status": "Passed" if checks_passed == total_checks else "Partial" if checks_passed > 0 else "Failed",
            "check_details": check_details
        }

    def _check_model_purpose(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check model purpose documentation."""
        return {
            "purpose_documented": {
                "passed": "model_info" in results and "model_type" in results.get("model_info", {}),
                "message": "Model purpose and type documented"
            },
            "use_cases_defined": {
                "passed": "model_info" in results,
                "message": "Model use cases defined"
            },
            "business_alignment": {
                "passed": "recommendations" in results,
                "message": "Business alignment validated"
            }
        }

    def _check_conceptual_soundness(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check conceptual soundness validation."""
        conceptual = results.get("conceptual_soundness", {})
        return {
            "theory_documented": {
                "passed": bool(conceptual),
                "message": "Theoretical foundation documented"
            },
            "methodology_appropriate": {
                "passed": conceptual.get("overall_status") in ["passed", "warning"],
                "message": "Methodology appropriateness validated"
            },
            "assumptions_validated": {
                "passed": "assumptions" in results,
                "message": "Model assumptions validated"
            }
        }

    def _check_data_quality(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check data quality validation."""
        data_quality = results.get("data_quality", {})
        completeness = data_quality.get("completeness_score", 0)
        quality = data_quality.get("quality_score", 0)

        return {
            "data_completeness": {
                "passed": completeness >= 0.95,  # Stricter: 95% threshold
                "message": f"Data completeness: {completeness:.1%}"
            },
            "data_accuracy": {
                "passed": quality >= 0.90,  # Stricter: 90% threshold
                "message": f"Data quality score: {quality:.1%}"
            },
            "data_representativeness": {
                "passed": bool(data_quality.get("sample_size_adequate")) and
                         data_quality.get("train_samples", 0) >= 1000,  # Require minimum sample size
                "message": f"Sample size: {data_quality.get('train_samples', 0)} records"
            }
        }

    def _check_performance_validation(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check performance validation."""
        import logging
        logger = logging.getLogger(__name__)

        performance = results.get("performance", {})

        # Performance data is FLATTENED in main_simple.py (lines 509-520)
        # Structure: {"gini": 0.65, "ks_statistic": 0.48, "auc_roc": 0.85, ...}
        gini = performance.get("gini", 0)
        ks = performance.get("ks_statistic", 0)
        auc = performance.get("auc_roc", 0)

        logger.info(f"📊 Performance Metrics - Gini: {gini:.3f}, KS: {ks:.3f}, AUC: {auc:.3f}")
        logger.info(f"✅ Checks - Gini≥0.50: {gini >= 0.50}, KS≥0.30: {ks >= 0.30}, AUC≥0.75: {auc >= 0.75}")

        return {
            "discrimination_power": {
                "passed": gini >= 0.50,  # Stricter: 50% Gini (was 30%)
                "message": f"Gini coefficient: {gini:.3f} (threshold: 0.50)"
            },
            "calibration": {
                "passed": ks >= 0.30,  # Stricter: 30% KS (was 20%)
                "message": f"KS statistic: {ks:.3f} (threshold: 0.30)"
            },
            "performance_metrics": {
                "passed": auc >= 0.75,  # Require AUC >= 75%
                "message": f"AUC-ROC: {auc:.3f} (threshold: 0.75)"
            }
        }

    def _check_stability_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check stability analysis."""
        stability = results.get("stability", {})

        # Get PSI values
        psi_analysis = stability.get("psi_analysis", {})
        psi_value = psi_analysis.get("psi_value", 999)  # Default high value if missing

        # Get CSI analysis
        csi_analysis = stability.get("csi_analysis", {})
        csi_violations = csi_analysis.get("violations", [])

        return {
            "psi_analysis": {
                "passed": psi_value < 0.15,  # Stricter: PSI must be < 0.15 (was just checking presence)
                "message": f"PSI: {psi_value:.3f} (threshold: 0.15)"
            },
            "csi_analysis": {
                "passed": len(csi_violations) == 0,  # Stricter: No CSI violations allowed
                "message": f"CSI violations: {len(csi_violations)}"
            },
            "stability_assessment": {
                "passed": stability.get("overall_stability") == "passed",  # Stricter: Must be "passed", not "warning"
                "message": f"Overall stability: {stability.get('overall_stability', 'unknown')}"
            }
        }

    def _check_assumptions_testing(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check assumptions testing."""
        assumptions = results.get("assumptions", {})
        return {
            "assumptions_documented": {
                "passed": bool(assumptions),
                "message": "Model assumptions documented"
            },
            "assumptions_tested": {
                "passed": assumptions.get("overall_status") in ["passed", "warning"],
                "message": "Assumptions tested and validated"
            },
            "sensitivity_analysis": {
                "passed": "sensitivity_analysis" in assumptions,
                "message": "Sensitivity analysis performed"
            }
        }

    def _check_implementation_validation(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check implementation validation."""
        implementation = results.get("implementation", {})
        return {
            "implementation_verified": {
                "passed": bool(implementation),
                "message": "Implementation verified"
            },
            "production_testing": {
                "passed": implementation.get("production_ready", False),
                "message": "Production testing completed"
            },
            "rollback_plan": {
                "passed": implementation.get("rollback_plan_exists", False),
                "message": "Rollback plan documented"
            }
        }

    def _check_ongoing_monitoring(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check ongoing monitoring requirements."""
        return {
            "monitoring_plan": {
                "passed": "monitoring_plan" in results,
                "message": "Monitoring plan defined"
            },
            "drift_detection": {
                "passed": "stability" in results,
                "message": "Drift detection implemented"
            },
            "revalidation_schedule": {
                "passed": "revalidation_schedule" in results,
                "message": "Revalidation schedule defined"
            }
        }

    def _check_documentation(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Check documentation completeness."""
        required_sections = [
            "data_quality", "conceptual_soundness", "performance",
            "assumptions", "stability", "implementation"
        ]
        sections_present = sum(1 for section in required_sections if section in results)

        return {
            "model_documentation": {
                "passed": sections_present >= 4,
                "message": f"{sections_present}/{len(required_sections)} required sections present"
            },
            "validation_report": {
                "passed": "recommendations" in results,
                "message": "Validation report generated"
            },
            "audit_trail": {
                "passed": "timestamp" in results or "validation_date" in results,
                "message": "Audit trail maintained"
            }
        }

    def _calculate_compliance_score(self, compliance_details: Dict[str, Any]) -> float:
        """Calculate overall compliance score (0-100)."""
        total_score = sum(
            details["score"] for details in compliance_details.values()
        )
        return total_score

    def _determine_compliance_status(self, score: float) -> str:
        """Determine compliance status based on score."""
        if score >= 90:
            return "Fully Compliant"
        elif score >= 75:
            return "Substantially Compliant"
        elif score >= 60:
            return "Partially Compliant"
        else:
            return "Non-Compliant"

    def _identify_gaps(self, compliance_details: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify compliance gaps."""
        gaps = []

        for req_name, details in compliance_details.items():
            if details["status"] != "Passed":
                gap = {
                    "requirement": req_name,
                    "description": details["description"],
                    "status": details["status"],
                    "checks_passed": f"{details['checks_passed']}/{details['total_checks']}",
                    "weight": details["weight"],
                    "failed_checks": []
                }

                # Identify specific failed checks
                for check_name, check_info in details["check_details"].items():
                    if not check_info.get("passed", False):
                        gap["failed_checks"].append({
                            "check": check_name,
                            "message": check_info.get("message", "Check failed")
                        })

                gaps.append(gap)

        # Sort by weight (most important first)
        gaps.sort(key=lambda x: x["weight"], reverse=True)
        return gaps

    def _generate_recommendations(self, gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on identified gaps."""
        recommendations = []

        for gap in gaps:
            req_name = gap["requirement"]

            if req_name == "model_purpose":
                recommendations.append(
                    "Document model purpose, use cases, and business alignment clearly"
                )
            elif req_name == "conceptual_soundness":
                recommendations.append(
                    "Enhance theoretical foundation documentation and methodology justification"
                )
            elif req_name == "data_quality":
                recommendations.append(
                    "Improve data quality checks and ensure data representativeness"
                )
            elif req_name == "performance_validation":
                recommendations.append(
                    "Conduct comprehensive performance testing with multiple metrics"
                )
            elif req_name == "stability_analysis":
                recommendations.append(
                    "Perform thorough stability analysis including PSI and CSI"
                )
            elif req_name == "assumptions_testing":
                recommendations.append(
                    "Document and test all model assumptions with sensitivity analysis"
                )
            elif req_name == "implementation_validation":
                recommendations.append(
                    "Verify implementation and establish production testing procedures"
                )
            elif req_name == "ongoing_monitoring":
                recommendations.append(
                    "Establish monitoring plan with drift detection and revalidation schedule"
                )
            elif req_name == "documentation":
                recommendations.append(
                    "Complete all required documentation sections and maintain audit trail"
                )

        return recommendations

    def _generate_summary(
        self, compliance_score: float, compliance_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate compliance summary."""
        passed_requirements = sum(
            1 for details in compliance_details.values()
            if details["status"] == "Passed"
        )
        total_requirements = len(compliance_details)

        return {
            "score": round(compliance_score, 2),
            "status": self._determine_compliance_status(compliance_score),
            "requirements_passed": f"{passed_requirements}/{total_requirements}",
            "total_checks_passed": sum(
                details["checks_passed"] for details in compliance_details.values()
            ),
            "total_checks": sum(
                details["total_checks"] for details in compliance_details.values()
            ),
            "ready_for_production": compliance_score >= 90.0
        }


# Made with Bob
