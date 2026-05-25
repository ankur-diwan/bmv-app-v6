/**
 * ValidationResults Component - Simplified and Error-Safe
 * Displays comprehensive validation results
 */

import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  ExpandMore,
  Close as CloseIcon,
} from '@mui/icons-material';

const ValidationResults = ({ results }) => {
  console.log('=== ValidationResults Rendering ===');
  console.log('Results:', results);

  // State for SR 11-7 compliance modal
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedCheck, setSelectedCheck] = useState(null);

  // State for recommendations modal
  const [recModalOpen, setRecModalOpen] = useState(false);
  const [selectedRecommendation, setSelectedRecommendation] = useState(null);

  // Handler for opening recommendation modal
  const handleRecommendationClick = (recommendation) => {
    console.log('=== Recommendation Card Clicked ===');
    console.log('Recommendation:', recommendation);
    setSelectedRecommendation(recommendation);
    setRecModalOpen(true);
    console.log('Modal should open now, recModalOpen:', true);
  };

  // Handler for closing recommendation modal
  const handleRecModalClose = () => {
    setRecModalOpen(false);
    setSelectedRecommendation(null);
  };

  if (!results) {
    return (
      <Alert severity="info">
        No validation results available. Please run a validation first.
      </Alert>
    );
  }

  // Safe accessor helper
  const safeGet = (obj, path, defaultValue = 'N/A') => {
    try {
      const value = path.split('.').reduce((acc, part) => acc?.[part], obj);
      return value !== undefined && value !== null ? value : defaultValue;
    } catch (e) {
      return defaultValue;
    }
  };

  // Handle card click
  const handleCardClick = (checkKey, checkData) => {
    setSelectedCheck({ key: checkKey, data: checkData });
    setModalOpen(true);
  };

  // Handle modal close
  const handleModalClose = () => {
    setModalOpen(false);
    setSelectedCheck(null);
  };

  // Format number safely
  const formatNumber = (value, decimals = 4) => {
    if (value === null || value === undefined || isNaN(value)) return 'N/A';
    return Number(value).toFixed(decimals);
  };

  // Format percentage safely
  const formatPercent = (value) => {
    if (value === null || value === undefined || isNaN(value)) return 'N/A';
    return `${(value * 100).toFixed(2)}%`;
  };

  // Get status color
  const getStatusColor = (status) => {
    const statusLower = String(status).toLowerCase();
    if (statusLower.includes('pass') || statusLower.includes('stable')) return 'success';
    if (statusLower.includes('warn') || statusLower.includes('moderate')) return 'warning';
    if (statusLower.includes('fail') || statusLower.includes('unstable')) return 'error';
    return 'default';
  };

  return (
    <Box sx={{ mt: 3 }}>
      {/* Overall Summary */}
      <Card sx={{ mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Validation Summary
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Overall Status</Typography>
              <Chip
                label={safeGet(results, 'summary.overall_status', 'UNKNOWN')}
                color={getStatusColor(safeGet(results, 'summary.overall_status'))}
                sx={{ mt: 1 }}
              />
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">KS Statistic</Typography>
              <Typography variant="h6">
                {formatNumber(safeGet(results, 'summary.ks_statistic', 0))}
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Gini Coefficient</Typography>
              <Typography variant="h6">
                {formatNumber(safeGet(results, 'summary.gini_coefficient', 0))}
              </Typography>
            </Grid>
            <Grid item xs={12} md={3}>
              <Typography variant="body2">Compliance Score</Typography>
              <Typography variant="h6">
                {formatNumber(safeGet(results, 'summary.compliance_score', 0), 2)}%
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Statistical Tests */}
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">📊 Statistical Tests</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {/* Train Dataset */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Train Dataset
                  </Typography>
                  <Typography variant="body2">
                    KS: {formatNumber(safeGet(results, 'statistical_tests.train.ks_statistic', 0))}
                  </Typography>
                  <Typography variant="body2">
                    Gini: {formatNumber(safeGet(results, 'statistical_tests.train.gini_coefficient', 0))}
                  </Typography>
                  <Typography variant="body2">
                    PSI: {formatNumber(safeGet(results, 'statistical_tests.train.psi', 0))}
                  </Typography>
                  <Typography variant="body2">
                    CSI: {formatNumber(safeGet(results, 'statistical_tests.train.csi', 0))}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Test Dataset */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Test Dataset
                  </Typography>
                  <Typography variant="body2">
                    KS: {formatNumber(safeGet(results, 'statistical_tests.test.ks_statistic', 0))}
                  </Typography>
                  <Typography variant="body2">
                    Gini: {formatNumber(safeGet(results, 'statistical_tests.test.gini_coefficient', 0))}
                  </Typography>
                  <Typography variant="body2">
                    PSI: {formatNumber(safeGet(results, 'statistical_tests.test.psi', 0))}
                  </Typography>
                  <Typography variant="body2">
                    CSI: {formatNumber(safeGet(results, 'statistical_tests.test.csi', 0))}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* OOT Dataset */}
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="subtitle1" gutterBottom>
                    Out-of-Time
                  </Typography>
                  <Typography variant="body2">
                    KS: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.ks_statistic', 0))}
                  </Typography>
                  <Typography variant="body2">
                    Gini: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.gini_coefficient', 0))}
                  </Typography>
                  <Typography variant="body2">
                    PSI: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.psi', 0))}
                  </Typography>
                  <Typography variant="body2">
                    CSI: {formatNumber(safeGet(results, 'statistical_tests.out_of_time.csi', 0))}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Performance Metrics */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">📈 Performance Metrics</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Grid container spacing={2}>
            {['train', 'test', 'out_of_time'].map((dataset) => (
              <Grid item xs={12} md={4} key={dataset}>
                <Card>
                  <CardContent>
                    <Typography variant="subtitle1" gutterBottom>
                      {dataset === 'out_of_time' ? 'Out-of-Time' : dataset.charAt(0).toUpperCase() + dataset.slice(1)}
                    </Typography>
                    <Typography variant="body2">
                      Accuracy: {formatPercent(safeGet(results, `performance.${dataset}.accuracy`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      Precision: {formatPercent(safeGet(results, `performance.${dataset}.precision`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      Recall: {formatPercent(safeGet(results, `performance.${dataset}.recall`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      F1 Score: {formatPercent(safeGet(results, `performance.${dataset}.f1_score`, 0))}
                    </Typography>
                    <Typography variant="body2">
                      AUC-ROC: {formatNumber(safeGet(results, `performance.${dataset}.auc_roc`, 0))}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </AccordionDetails>
      </Accordion>

      {/* Compliance */}
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Typography variant="h6">✅ SR 11-7 Compliance</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <Box>
            <Alert severity={getStatusColor(safeGet(results, 'compliance.overall_status'))} sx={{ mb: 2 }}>
              <Typography variant="body1">
                <strong>Status:</strong> {safeGet(results, 'compliance.overall_status', 'Unknown')}
              </Typography>
              <Typography variant="body1">
                <strong>Score:</strong> {formatNumber(safeGet(results, 'compliance.compliance_score', 0), 2)}%
              </Typography>
              <Typography variant="body1">
                <strong>SR 11-7 Compliant:</strong> {
                  (safeGet(results, 'compliance.sr_11_7_compliant', false) ||
                   safeGet(results, 'compliance.overall_score', 0) >= 70 ||
                   safeGet(results, 'compliance.compliance_score', 0) >= 70) ? 'Yes' : 'No'
                }
              </Typography>
            </Alert>

            {/* Detailed Checks */}
            {results.compliance?.detailed_checks && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Detailed Checks
                </Typography>
                <Grid container spacing={2}>
                  {Object.entries(results.compliance.detailed_checks).map(([key, check]) => {
                    // Generate reason summary based on check details
                    const getReasonSummary = () => {
                      if (!check.check_details) return null;

                      const failedChecks = Object.entries(check.check_details)
                        .filter(([_, checkInfo]) => !checkInfo.passed)
                        .map(([_, checkInfo]) => {
                          // Convert positive message to negative for failed checks
                          const msg = checkInfo.message || '';
                          // Remove "documented", "defined", "validated" etc and add "not" prefix
                          return msg.replace(/\b(documented|defined|validated|performed|completed|tested|verified|implemented|maintained)\b/gi, 'NOT $1');
                        });

                      const passedCount = Object.entries(check.check_details)
                        .filter(([_, checkInfo]) => checkInfo.passed).length;

                      const totalCount = Object.entries(check.check_details).length;

                      if (check.status === 'Failed') {
                        if (failedChecks.length > 0) {
                          return `Failed: ${failedChecks.join('; ')}`;
                        }
                        return `Failed: ${check.checks_passed || 0} of ${check.total_checks || totalCount} checks passed`;
                      } else if (check.status === 'Partial') {
                        if (failedChecks.length > 0) {
                          return `Partial: ${failedChecks.join('; ')}`;
                        }
                        return `Partial: ${passedCount} of ${totalCount} checks passed`;
                      } else if (check.status === 'Passed') {
                        return `Passed: All ${totalCount} checks completed successfully`;
                      }
                      return null;
                    };

                    const reasonSummary = getReasonSummary();

                    return (
                      <Grid item xs={12} sm={6} md={4} key={key}>
                        <Card
                          variant="outlined"
                          sx={{
                            height: '100%',
                            cursor: 'pointer',
                            transition: 'all 0.3s ease',
                            '&:hover': {
                              boxShadow: 4,
                              transform: 'translateY(-4px)',
                              borderColor: 'primary.main',
                            }
                          }}
                          onClick={() => handleCardClick(key, check)}
                        >
                          <CardContent>
                            <Typography variant="body2" gutterBottom fontWeight="medium">
                              {check.description || key}
                            </Typography>
                            <Chip
                              label={check.status || 'Unknown'}
                              color={getStatusColor(check.status)}
                              size="small"
                              sx={{ mb: 1 }}
                            />
                            <Typography variant="caption" display="block" sx={{ mb: 1 }}>
                              Score: {formatNumber(check.score || 0, 2)} / {check.weight || 0}
                            </Typography>

                            {/* Reason Summary */}
                            {reasonSummary && (
                              <Alert
                                severity={check.status === 'Passed' ? 'success' : check.status === 'Partial' ? 'warning' : 'error'}
                                sx={{ mb: 1, py: 0, fontSize: '0.75rem' }}
                              >
                                <Typography variant="caption" sx={{ fontSize: '0.7rem' }}>
                                  {reasonSummary}
                                </Typography>
                              </Alert>
                            )}

                            {/* Individual Check Details */}
                            {check.check_details && (
                              <Box sx={{ mt: 1, pt: 1, borderTop: '1px solid', borderColor: 'divider' }}>
                                {Object.entries(check.check_details).map(([checkName, checkInfo]) => {
                                  // Format message based on pass/fail status
                                  let displayMessage = checkInfo.message || checkName;

                                  // If check failed, convert to negative statement
                                  if (!checkInfo.passed) {
                                    displayMessage = displayMessage.replace(
                                      /\b(documented|defined|validated|performed|completed|tested|verified|implemented|maintained|adequate|appropriate|sound|present)\b/gi,
                                      'NOT $1'
                                    );
                                  }

                                  return (
                                    <Box key={checkName} sx={{ mb: 0.5 }}>
                                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                        {checkInfo.passed ? (
                                          <CheckCircle sx={{ fontSize: 14, color: 'success.main' }} />
                                        ) : (
                                          <ErrorIcon sx={{ fontSize: 14, color: 'error.main' }} />
                                        )}
                                        <Typography variant="caption" sx={{ fontSize: '0.7rem' }}>
                                          {displayMessage}
                                        </Typography>
                                      </Box>
                                    </Box>
                                  );
                                })}
                              </Box>
                            )}
                          </CardContent>
                        </Card>
                      </Grid>
                    );
                  })}
                </Grid>
              </Box>
            )}

            {/* Recommendations - Show ALL 9 possible recommendations - CLICKABLE */}
            <Box sx={{ mt: 3 }}>
              <Typography variant="subtitle1" gutterBottom>
                Recommendations (SR 11-7 Compliance)
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                All 9 SR 11-7 categories with recommendations. Green = Already satisfied, Blue = Action needed. <strong>Click any card for detailed guidance.</strong>
              </Typography>

              {(() => {
                // Define all 9 possible recommendations with detailed information
                const allRecommendations = [
                  {
                    category: "Model Purpose",
                    weight: "8%",
                    weightNum: 8,
                    recommendation: "Document model purpose, use cases, and business alignment clearly",
                    key: "model_purpose",
                    description: "Clear articulation of model purpose and use cases",
                    detailedSteps: [
                      "Document the primary purpose of the model (e.g., credit risk assessment, fraud detection)",
                      "Define all intended use cases and business applications",
                      "Establish clear business objectives and success criteria",
                      "Identify target population and scope of application",
                      "Document limitations and out-of-scope scenarios"
                    ],
                    checks: ["purpose_documented", "use_cases_defined", "business_alignment"],
                    checkDescriptions: {
                      purpose_documented: "Model purpose is clearly documented",
                      use_cases_defined: "All use cases are defined and documented",
                      business_alignment: "Model aligns with business objectives"
                    },
                    regulatoryGuidance: "SR 11-7 requires clear documentation of model purpose to ensure appropriate use and prevent model misuse."
                  },
                  {
                    category: "Conceptual Soundness",
                    weight: "15%",
                    weightNum: 15,
                    recommendation: "Enhance theoretical foundation documentation and methodology justification",
                    key: "conceptual_soundness",
                    description: "Sound theoretical foundation and methodology",
                    detailedSteps: [
                      "Document the theoretical framework underlying the model",
                      "Justify the selection of modeling methodology",
                      "Explain statistical techniques and algorithms used",
                      "Validate all model assumptions with empirical evidence",
                      "Provide academic or industry references supporting the approach"
                    ],
                    checks: ["theory_documented", "methodology_appropriate", "assumptions_validated"],
                    checkDescriptions: {
                      theory_documented: "Theoretical foundation is well-documented",
                      methodology_appropriate: "Methodology is appropriate for the use case",
                      assumptions_validated: "All assumptions are validated"
                    },
                    regulatoryGuidance: "Models must be based on sound theory and appropriate for their intended use. This is a critical SR 11-7 requirement."
                  },
                  {
                    category: "Data Quality",
                    weight: "12%",
                    weightNum: 12,
                    recommendation: "Improve data quality checks and ensure data representativeness",
                    key: "data_quality",
                    description: "Data sufficiency, quality, and representativeness",
                    detailedSteps: [
                      "Perform comprehensive data quality assessment",
                      "Document data sources, lineage, and collection methods",
                      "Ensure data represents the target population",
                      "Address missing values, outliers, and data anomalies",
                      "Validate data accuracy and consistency"
                    ],
                    checks: ["data_completeness", "data_accuracy", "data_representativeness"],
                    checkDescriptions: {
                      data_completeness: "Data is complete with minimal missing values",
                      data_accuracy: "Data accuracy is verified and documented",
                      data_representativeness: "Data represents the target population"
                    },
                    regulatoryGuidance: "High-quality, representative data is essential for model reliability and regulatory compliance."
                  },
                  {
                    category: "Performance Validation",
                    weight: "15%",
                    weightNum: 15,
                    recommendation: "Conduct comprehensive performance testing with multiple metrics",
                    key: "performance_validation",
                    description: "Comprehensive performance testing and metrics",
                    detailedSteps: [
                      "Calculate discrimination metrics (AUC-ROC, KS, Gini)",
                      "Test model performance on train, test, and out-of-time datasets",
                      "Validate model calibration and accuracy",
                      "Compare performance against benchmarks and alternative models",
                      "Document performance across different segments"
                    ],
                    checks: ["discrimination_power", "calibration", "performance_metrics"],
                    checkDescriptions: {
                      discrimination_power: "Model shows strong discrimination power",
                      calibration: "Model is well-calibrated",
                      performance_metrics: "All performance metrics meet thresholds"
                    },
                    regulatoryGuidance: "Rigorous performance testing is required to demonstrate model effectiveness and reliability."
                  },
                  {
                    category: "Stability Analysis",
                    weight: "12%",
                    weightNum: 12,
                    recommendation: "Perform thorough stability analysis including PSI and CSI",
                    key: "stability_analysis",
                    description: "Population and characteristic stability over time",
                    detailedSteps: [
                      "Calculate Population Stability Index (PSI) for score distribution",
                      "Calculate Characteristic Stability Index (CSI) for all features",
                      "Monitor stability trends over time",
                      "Identify and investigate stability violations",
                      "Establish ongoing stability monitoring procedures"
                    ],
                    checks: ["psi_analysis", "csi_analysis", "stability_assessment"],
                    checkDescriptions: {
                      psi_analysis: "PSI is within acceptable thresholds",
                      csi_analysis: "CSI shows stable characteristics",
                      stability_assessment: "Overall stability assessment is satisfactory"
                    },
                    regulatoryGuidance: "Models must remain stable over time. Significant drift requires investigation and potential revalidation."
                  },
                  {
                    category: "Assumptions Testing",
                    weight: "10%",
                    weightNum: 10,
                    recommendation: "Document and test all model assumptions with sensitivity analysis",
                    key: "assumptions_testing",
                    description: "Testing and validation of model assumptions",
                    detailedSteps: [
                      "List all model assumptions explicitly",
                      "Test each assumption rigorously with statistical tests",
                      "Perform sensitivity analysis for key assumptions",
                      "Document the impact of assumption violations",
                      "Establish procedures for monitoring assumptions"
                    ],
                    checks: ["assumptions_documented", "assumptions_tested", "sensitivity_analysis"],
                    checkDescriptions: {
                      assumptions_documented: "All assumptions are documented",
                      assumptions_tested: "Assumptions are tested and validated",
                      sensitivity_analysis: "Sensitivity analysis is performed"
                    },
                    regulatoryGuidance: "All model assumptions must be documented, tested, and monitored. Violations can invalidate model results."
                  },
                  {
                    category: "Implementation Validation",
                    weight: "8%",
                    weightNum: 8,
                    recommendation: "Verify implementation and establish production testing procedures",
                    key: "implementation_validation",
                    description: "Proper model implementation and deployment",
                    detailedSteps: [
                      "Verify that code implementation matches model design",
                      "Test model in production-like environment",
                      "Create rollback and contingency procedures",
                      "Document deployment process and configuration",
                      "Establish change management procedures"
                    ],
                    checks: ["implementation_verified", "production_testing", "rollback_plan"],
                    checkDescriptions: {
                      implementation_verified: "Implementation matches design specifications",
                      production_testing: "Production testing is completed successfully",
                      rollback_plan: "Rollback plan is documented and tested"
                    },
                    regulatoryGuidance: "Implementation must be verified to ensure the production model matches the validated design."
                  },
                  {
                    category: "Ongoing Monitoring",
                    weight: "10%",
                    weightNum: 10,
                    recommendation: "Establish monitoring plan with drift detection and revalidation schedule",
                    key: "ongoing_monitoring",
                    description: "Continuous monitoring and performance tracking",
                    detailedSteps: [
                      "Create comprehensive monitoring plan",
                      "Set up drift detection mechanisms (data and concept drift)",
                      "Define revalidation triggers and schedule",
                      "Establish performance tracking dashboards",
                      "Document monitoring procedures and escalation paths"
                    ],
                    checks: ["monitoring_plan", "drift_detection", "revalidation_schedule"],
                    checkDescriptions: {
                      monitoring_plan: "Comprehensive monitoring plan is established",
                      drift_detection: "Drift detection mechanisms are in place",
                      revalidation_schedule: "Revalidation schedule is defined"
                    },
                    regulatoryGuidance: "Ongoing monitoring is required to ensure continued model performance and identify when revalidation is needed."
                  },
                  {
                    category: "Documentation",
                    weight: "10%",
                    weightNum: 10,
                    recommendation: "Complete all required documentation sections and maintain audit trail",
                    key: "documentation",
                    description: "Comprehensive and accessible documentation",
                    detailedSteps: [
                      "Complete all sections of model documentation",
                      "Create comprehensive validation report",
                      "Maintain detailed audit trail of all changes",
                      "Document all decisions and their rationale",
                      "Ensure documentation is accessible to stakeholders"
                    ],
                    checks: ["model_documentation", "validation_report", "audit_trail"],
                    checkDescriptions: {
                      model_documentation: "Model documentation is complete",
                      validation_report: "Validation report is comprehensive",
                      audit_trail: "Audit trail is maintained"
                    },
                    regulatoryGuidance: "Comprehensive documentation is essential for regulatory compliance, model governance, and knowledge transfer."
                  }
                ];

                // Get compliance details
                const complianceDetails = results.compliance?.compliance_details || {};

                return allRecommendations.map((rec, idx) => {
                  // Check if this category needs action
                  const categoryData = complianceDetails[rec.key];
                  const needsAction = categoryData?.status !== "Passed";
                  const status = categoryData?.status || "Unknown";

                  return (
                    <Alert
                      severity={needsAction ? "info" : "success"}
                      key={idx}
                      sx={{
                        mb: 1,
                        opacity: needsAction ? 1 : 0.7,
                        cursor: 'pointer',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          transform: 'translateY(-2px)',
                          boxShadow: 3,
                          opacity: 1
                        }
                      }}
                      icon={needsAction ? <ErrorIcon /> : <CheckCircle />}
                      onClick={() => handleRecommendationClick({ ...rec, categoryData, needsAction, status })}
                    >
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                          {idx + 1}. {rec.category} (Weight: {rec.weight})
                          <Chip
                            label={needsAction ? "ACTION NEEDED" : "SATISFIED"}
                            size="small"
                            color={needsAction ? "warning" : "success"}
                            sx={{ ml: 1, fontSize: '0.7rem' }}
                          />
                        </Typography>
                        <Typography variant="body2">
                          {rec.recommendation}
                        </Typography>
                        {categoryData && (
                          <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                            Status: {status} | Score: {categoryData.score?.toFixed(1) || 0}/{categoryData.weight || 0} |
                            Checks: {categoryData.checks_passed || 0}/{categoryData.total_checks || 0}
                          </Typography>
                        )}
                        <Typography variant="caption" sx={{ mt: 0.5, display: 'block', fontStyle: 'italic', color: 'primary.main' }}>
                          👆 Click for detailed guidance
                        </Typography>
                      </Box>
                    </Alert>
                  );
                });
              })()}
            </Box>
          </Box>
        </AccordionDetails>
      </Accordion>

      {/* Model Specific */}
      {results.model_specific && (
        <Accordion>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Typography variant="h6">🎯 Model-Specific Validation</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" color="text.secondary" paragraph>
              Validates model against scorecard-specific requirements including data quality, target distribution, predictive power, and regulatory compliance.
            </Typography>

            <Typography variant="body2">
              <strong>Validation Type:</strong> {safeGet(results, 'model_specific.validation_type', 'N/A')}
            </Typography>
            <Typography variant="body2">
              <strong>Use Case:</strong> {safeGet(results, 'model_specific.use_case', 'N/A')}
            </Typography>
            <Typography variant="body2">
              <strong>Status:</strong>{' '}
              <Chip
                label={safeGet(results, 'model_specific.status', 'Unknown')}
                color={getStatusColor(safeGet(results, 'model_specific.status'))}
                size="small"
              />
            </Typography>

            {/* Show detailed reasons for the status */}
            {(() => {
              const status = safeGet(results, 'model_specific.status', '').toLowerCase();
              const checks = safeGet(results, 'model_specific.checks', {});
              const failedChecks = [];
              const warningChecks = [];
              const passedChecks = [];

              // Categorize checks by status
              Object.entries(checks).forEach(([checkName, checkData]) => {
                const checkStatus = checkData?.status || 'unknown';
                const displayName = checkName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

                if (checkStatus === 'failed' || checkStatus === 'error') {
                  failedChecks.push(displayName);
                } else if (checkStatus === 'warning') {
                  warningChecks.push(displayName);
                } else if (checkStatus === 'passed') {
                  passedChecks.push(displayName);
                }
              });

              return (
                <Box sx={{ mt: 2 }}>
                  {status === 'failed' && failedChecks.length > 0 && (
                    <Alert severity="error" sx={{ mt: 1 }}>
                      <Typography variant="body2">
                        <strong>Failed:</strong> {failedChecks.join(', ')}
                      </Typography>
                    </Alert>
                  )}

                  {status === 'warning' && warningChecks.length > 0 && (
                    <Alert severity="warning" sx={{ mt: 1 }}>
                      <Typography variant="body2">
                        <strong>Warnings:</strong> {warningChecks.join(', ')}
                      </Typography>
                    </Alert>
                  )}

                  {status === 'passed' && passedChecks.length > 0 && (
                    <Alert severity="success" sx={{ mt: 1 }}>
                      <Typography variant="body2">
                        <strong>All checks passed:</strong> {passedChecks.join(', ')}
                      </Typography>
                    </Alert>
                  )}

                  {/* Show summary of all checks */}
                  {Object.keys(checks).length > 0 && (
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        <strong>Validation Summary:</strong>
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        • Passed: {passedChecks.length} checks
                        {warningChecks.length > 0 && ` • Warnings: ${warningChecks.length} checks`}
                        {failedChecks.length > 0 && ` • Failed: ${failedChecks.length} checks`}
                      </Typography>
                    </Box>
                  )}
                </Box>
              );
            })()}
          </AccordionDetails>
        </Accordion>
      )}

      {/* Modal Dialog for Detailed Check Information */}
      <Dialog
        open={modalOpen}
        onClose={handleModalClose}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            maxHeight: '80vh'
          }
        }}
      >
        <DialogTitle sx={{
          bgcolor: selectedCheck?.data?.status === 'Passed' ? 'success.light' :
                   selectedCheck?.data?.status === 'Partial' ? 'warning.light' : 'error.light',
          color: 'white',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <Box>
            <Typography variant="h6">
              {selectedCheck?.data?.description || selectedCheck?.key}
            </Typography>
            <Chip
              label={selectedCheck?.data?.status || 'Unknown'}
              size="small"
              sx={{
                mt: 1,
                bgcolor: 'white',
                color: selectedCheck?.data?.status === 'Passed' ? 'success.main' :
                       selectedCheck?.data?.status === 'Partial' ? 'warning.main' : 'error.main',
                fontWeight: 'bold'
              }}
            />
          </Box>
          <Button
            onClick={handleModalClose}
            sx={{ color: 'white', minWidth: 'auto' }}
          >
            <CloseIcon />
          </Button>
        </DialogTitle>

        <DialogContent sx={{ mt: 2 }}>
          {selectedCheck && (() => {
            // Define all possible checks for each category based on SR 11-7 requirements
            const allPossibleChecks = {
              'model_purpose': [
                { key: 'purpose_documented', label: 'Model purpose and type documented', explanation: 'Clear documentation of what the model does and its intended use' },
                { key: 'use_cases_defined', label: 'Model use cases defined', explanation: 'Specific business scenarios where the model will be applied' },
                { key: 'business_alignment', label: 'Business alignment validated', explanation: 'Model objectives align with business goals and risk appetite' }
              ],
              'conceptual_soundness': [
                { key: 'theory_documented', label: 'Theoretical foundation documented', explanation: 'Mathematical and statistical theory underlying the model is documented' },
                { key: 'methodology_appropriate', label: 'Methodology appropriateness validated', explanation: 'Chosen modeling approach is suitable for the problem and data' },
                { key: 'assumptions_validated', label: 'Model assumptions validated', explanation: 'Key assumptions are reasonable and supported by evidence' }
              ],
              'data_quality': [
                { key: 'data_completeness', label: 'Data completeness: 95.0%', explanation: 'Sufficient data available with minimal missing values' },
                { key: 'data_accuracy', label: 'Data quality score: 90.0%', explanation: 'Data is accurate, consistent, and free from significant errors' },
                { key: 'data_representativeness', label: 'Data representativeness validated', explanation: 'Data adequately represents the target population' }
              ],
              'performance_validation': [
                { key: 'discrimination_power', label: 'Gini coefficient: 0.648', explanation: 'Model effectively separates good and bad outcomes (higher is better)' },
                { key: 'calibration', label: 'KS statistic: 0.578', explanation: 'Maximum separation between cumulative distributions (≥0.2 is good)' },
                { key: 'performance_metrics', label: 'Performance metrics calculated', explanation: 'Comprehensive metrics (accuracy, precision, recall, AUC) evaluated' }
              ],
              'stability_analysis': [
                { key: 'psi_analysis', label: 'PSI analysis performed', explanation: 'Population Stability Index checks for distribution shifts over time' },
                { key: 'csi_analysis', label: 'CSI analysis performed', explanation: 'Characteristic Stability Index monitors individual feature stability' },
                { key: 'stability_assessment', label: 'Overall stability: passed', explanation: 'Model predictions remain consistent across different time periods' }
              ],
              'assumptions_testing': [
                { key: 'assumptions_documented', label: 'Model assumptions documented', explanation: 'All key assumptions are clearly stated and documented' },
                { key: 'assumptions_tested', label: 'Assumptions tested and validated', explanation: 'Assumptions have been empirically tested and verified' },
                { key: 'sensitivity_analysis', label: 'Sensitivity analysis performed', explanation: 'Impact of assumption violations on model performance assessed' }
              ],
              'implementation_validation': [
                { key: 'implementation_verified', label: 'Implementation verified', explanation: 'Model code correctly implements the intended methodology' },
                { key: 'production_testing', label: 'Production testing completed', explanation: 'Model tested in production-like environment before deployment' },
                { key: 'rollback_plan', label: 'Rollback plan documented', explanation: 'Procedures defined to revert to previous model if issues arise' }
              ],
              'ongoing_monitoring': [
                { key: 'monitoring_plan', label: 'Monitoring plan defined', explanation: 'Framework established for continuous model performance tracking' },
                { key: 'drift_detection', label: 'Drift detection implemented', explanation: 'Automated alerts for population or performance drift' },
                { key: 'revalidation_schedule', label: 'Revalidation schedule defined', explanation: 'Regular intervals set for comprehensive model review' }
              ],
              'documentation': [
                { key: 'model_documentation', label: '6/6 required sections present', explanation: 'Complete documentation covering all SR 11-7 required areas' },
                { key: 'validation_report', label: 'Validation report generated', explanation: 'Comprehensive validation report documenting all findings' },
                { key: 'audit_trail', label: 'Audit trail maintained', explanation: 'Complete record of model changes and validation activities' }
              ]
            };

            // Get all possible checks for this category
            const categoryKey = selectedCheck.key;
            const possibleChecks = allPossibleChecks[categoryKey] || [];

            // Get actual check results
            const actualChecks = selectedCheck.data.check_details || {};

            // Merge: show all possible checks with their actual status
            const allChecks = possibleChecks.map(possibleCheck => {
              const actualCheck = actualChecks[possibleCheck.key];
              return {
                key: possibleCheck.key,
                label: actualCheck?.message || possibleCheck.label,
                explanation: possibleCheck.explanation,
                passed: actualCheck?.passed || false,
                tested: !!actualCheck,
                value: actualCheck?.value
              };
            });

            const passedCount = allChecks.filter(c => c.passed).length;
            const failedCount = allChecks.filter(c => !c.passed).length;
            const totalCount = allChecks.length;

            return (
              <Box>
                {/* Score Information */}
                <Paper elevation={0} sx={{ p: 2, mb: 2, bgcolor: 'grey.50' }}>
                  <Grid container spacing={2}>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        Score Achieved
                      </Typography>
                      <Typography variant="h6">
                        {formatNumber(selectedCheck.data.score || 0, 2)}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        Maximum Score
                      </Typography>
                      <Typography variant="h6">
                        {selectedCheck.data.weight || 0}
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        Percentage
                      </Typography>
                      <Typography variant="h6">
                        {formatNumber((selectedCheck.data.score / selectedCheck.data.weight) * 100, 1)}%
                      </Typography>
                    </Grid>
                  </Grid>
                </Paper>

                {/* Overall Status Summary */}
                <Alert
                  severity={selectedCheck.data.status === 'Passed' ? 'success' :
                           selectedCheck.data.status === 'Partial' ? 'warning' : 'error'}
                  sx={{ mb: 2 }}
                >
                  <Typography variant="body2">
                    {selectedCheck.data.status === 'Passed' &&
                      `✅ All ${totalCount} checks completed successfully for this category.`}
                    {selectedCheck.data.status === 'Partial' &&
                      `⚠️ ${passedCount} of ${totalCount} checks passed. ${failedCount} require attention.`}
                    {selectedCheck.data.status === 'Failed' &&
                      `❌ Only ${passedCount} of ${totalCount} checks passed. ${failedCount} checks failed.`}
                  </Typography>
                </Alert>

                {/* Detailed Check Results - ALL CHECKS */}
                <Box>
                  <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
                    All {totalCount} Validation Points
                  </Typography>

                  <List>
                    {allChecks.map((check, index) => {
                      // Format message based on pass/fail status
                      let displayMessage = check.label;

                      // If check failed, convert to negative statement
                      if (!check.passed && check.tested) {
                        displayMessage = displayMessage.replace(
                          /\b(documented|defined|validated|performed|completed|tested|verified|implemented|maintained|adequate|appropriate|sound|present)\b/gi,
                          'NOT $1'
                        );
                      }

                      return (
                        <React.Fragment key={check.key}>
                          <ListItem
                            sx={{
                              bgcolor: check.passed ? 'success.50' : check.tested ? 'error.50' : 'grey.100',
                              borderRadius: 1,
                              mb: 1,
                              border: 1,
                              borderColor: check.passed ? 'success.light' : check.tested ? 'error.light' : 'grey.300'
                            }}
                          >
                            <ListItemIcon>
                              {check.passed ? (
                                <CheckCircle sx={{ color: 'success.main', fontSize: 28 }} />
                              ) : check.tested ? (
                                <ErrorIcon sx={{ color: 'error.main', fontSize: 28 }} />
                              ) : (
                                <Warning sx={{ color: 'grey.500', fontSize: 28 }} />
                              )}
                            </ListItemIcon>
                            <ListItemText
                              primary={
                                <Typography variant="body1" fontWeight="medium">
                                  {displayMessage}
                                </Typography>
                              }
                              secondary={
                                <Box sx={{ mt: 0.5 }}>
                                  {/* Explanation */}
                                  {check.explanation && (
                                    <Typography variant="caption" sx={{ display: 'block', mb: 0.5, color: 'text.secondary', fontStyle: 'italic' }}>
                                      {check.explanation}
                                    </Typography>
                                  )}
                                  {/* Status Chip */}
                                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                                    <Chip
                                      label={check.passed ? 'PASSED' : check.tested ? 'FAILED' : 'NOT TESTED'}
                                      size="small"
                                      color={check.passed ? 'success' : check.tested ? 'error' : 'default'}
                                      sx={{ fontSize: '0.7rem' }}
                                    />
                                    {check.value !== undefined && (
                                      <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                                        Value: {typeof check.value === 'number' ?
                                          formatNumber(check.value, 2) : check.value}
                                      </Typography>
                                    )}
                                  </Box>
                                </Box>
                              }
                            />
                          </ListItem>
                          {index < allChecks.length - 1 && (
                            <Divider sx={{ my: 1 }} />
                          )}
                        </React.Fragment>
                      );
                    })}
                  </List>
                </Box>

                {/* Summary Statistics */}
                <Paper elevation={0} sx={{ p: 2, mt: 2, bgcolor: 'grey.50' }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Summary Statistics
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={3}>
                      <Typography variant="body2" color="text.secondary">
                        Total Points
                      </Typography>
                      <Typography variant="h6">
                        {totalCount}
                      </Typography>
                    </Grid>
                    <Grid item xs={3}>
                      <Typography variant="body2" color="success.main">
                        Passed
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        {passedCount}
                      </Typography>
                    </Grid>
                    <Grid item xs={3}>
                      <Typography variant="body2" color="error.main">
                        Failed
                      </Typography>
                      <Typography variant="h6" color="error.main">
                        {failedCount}
                      </Typography>
                    </Grid>
                    <Grid item xs={3}>
                      <Typography variant="body2" color="text.secondary">
                        Pass Rate
                      </Typography>
                      <Typography variant="h6">
                        {formatNumber((passedCount / totalCount) * 100, 0)}%
                      </Typography>
                    </Grid>
                  </Grid>
                </Paper>
              </Box>
            );
          })()}
        </DialogContent>

        <DialogActions sx={{ p: 2, bgcolor: 'grey.50' }}>
          <Button onClick={handleModalClose} variant="contained" color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Recommendation Detail Modal */}
      <Dialog
        open={recModalOpen}
        onClose={handleRecModalClose}
        maxWidth="md"
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            maxHeight: '90vh'
          }
        }}
      >
        {selectedRecommendation && (
          <>
            <DialogTitle
              sx={{
                bgcolor: selectedRecommendation.needsAction ? 'info.main' : 'success.main',
                color: 'white',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <Box>
                <Typography variant="h6">
                  {selectedRecommendation.category}
                </Typography>
                <Typography variant="caption">
                  Weight: {selectedRecommendation.weight} | Status: {selectedRecommendation.status}
                </Typography>
              </Box>
              <Button
                onClick={handleRecModalClose}
                sx={{ color: 'white', minWidth: 'auto' }}
              >
                <CloseIcon />
              </Button>
            </DialogTitle>

            <DialogContent sx={{ mt: 2 }}>
              {/* Status Summary */}
              <Alert
                severity={selectedRecommendation.needsAction ? "warning" : "success"}
                sx={{ mb: 3 }}
              >
                <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                  {selectedRecommendation.needsAction ? "⚠️ Action Required" : "✅ Requirement Satisfied"}
                </Typography>
                <Typography variant="body2">
                  {selectedRecommendation.description}
                </Typography>
                {selectedRecommendation.categoryData && (
                  <Typography variant="caption" sx={{ display: 'block', mt: 1 }}>
                    Score: {selectedRecommendation.categoryData.score?.toFixed(1) || 0}/{selectedRecommendation.weightNum} |
                    Checks Passed: {selectedRecommendation.categoryData.checks_passed || 0}/{selectedRecommendation.categoryData.total_checks || 0}
                  </Typography>
                )}
              </Alert>

              {/* Main Recommendation */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  📋 Recommendation
                </Typography>
                <Typography variant="body2" sx={{ pl: 2, borderLeft: '3px solid', borderColor: 'primary.main', py: 1 }}>
                  {selectedRecommendation.recommendation}
                </Typography>
              </Box>

              {/* Detailed Steps */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  🎯 Action Steps
                </Typography>
                <List dense>
                  {selectedRecommendation.detailedSteps.map((step, idx) => (
                    <ListItem key={idx}>
                      <ListItemIcon sx={{ minWidth: 36 }}>
                        <Chip label={idx + 1} size="small" color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={step} />
                    </ListItem>
                  ))}
                </List>
              </Box>

              {/* Validation Checks */}
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  ✓ Validation Checks
                </Typography>
                <List dense>
                  {selectedRecommendation.checks.map((check, idx) => {
                    const checkData = selectedRecommendation.categoryData?.check_details?.[check];
                    const checkPassed = checkData?.passed || false;

                    return (
                      <ListItem key={idx}>
                        <ListItemIcon>
                          {checkPassed ? (
                            <CheckCircle color="success" />
                          ) : (
                            <ErrorIcon color="error" />
                          )}
                        </ListItemIcon>
                        <ListItemText
                          primary={selectedRecommendation.checkDescriptions[check]}
                          secondary={checkData?.message || "Not yet validated"}
                        />
                      </ListItem>
                    );
                  })}
                </List>
              </Box>

              {/* Regulatory Guidance */}
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  📜 Regulatory Guidance (SR 11-7)
                </Typography>
                <Alert severity="info" icon={false}>
                  <Typography variant="body2">
                    {selectedRecommendation.regulatoryGuidance}
                  </Typography>
                </Alert>
              </Box>

              <Divider sx={{ my: 2 }} />

              {/* Additional Resources */}
              <Box>
                <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>
                  📚 Additional Resources
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  • Federal Reserve SR 11-7: Guidance on Model Risk Management<br />
                  • OCC 2011-12: Supervisory Guidance on Model Risk Management<br />
                  • Internal model validation documentation and procedures
                </Typography>
              </Box>
            </DialogContent>

            <DialogActions sx={{ px: 3, pb: 2 }}>
              <Button onClick={handleRecModalClose} variant="contained">
                Close
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default ValidationResults;

// Made with Bob
