import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress,
  Divider
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Description,
  Assessment,
  CloudDownload
} from '@mui/icons-material';
import axios from 'axios';
import DocumentUpload from './components/DocumentUpload';
import ValidationResults from './components/ValidationResults';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const steps = ['Upload Model Documentation', 'Select Model Configuration', 'Review & Submit', 'Validation Progress', 'Results'];

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [options, setOptions] = useState(null);
  const [uploadedDocuments, setUploadedDocuments] = useState([]);
  const [uploadedDatasets, setUploadedDatasets] = useState(() => {
    // Initialize from localStorage if available
    const saved = localStorage.getItem('uploadedDatasets');
    return saved ? JSON.parse(saved) : null;
  }); // Store CSV dataset paths
  const [modelConfig, setModelConfig] = useState({
    model_name: '',
    product_type: '',
    scorecard_type: '',
    model_type: '',
    description: '',
    version: '1.0',
    owner: 'Model Risk Management'
  });
  const [validationId, setValidationId] = useState(null);
  const [validationStatus, setValidationStatus] = useState(null);
  const [validationResults, setValidationResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchOptions();
  }, []);

  // Persist uploadedDatasets to localStorage whenever it changes
  useEffect(() => {
    if (uploadedDatasets) {
      localStorage.setItem('uploadedDatasets', JSON.stringify(uploadedDatasets));
      console.log('✅ Saved uploadedDatasets to localStorage:', uploadedDatasets);
    }
  }, [uploadedDatasets]);

  useEffect(() => {
    if (validationId && activeStep === 3) {
      const interval = setInterval(() => {
        fetchValidationStatus();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [validationId, activeStep]);

  const fetchOptions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/options`);
      setOptions(response.data);
    } catch (err) {
      setError('Failed to load options');
      console.error(err);
    }
  };

  const fetchValidationStatus = async () => {
    try {
      console.log('Fetching validation status for:', validationId);
      const response = await axios.get(`${API_BASE_URL}/api/v1/validate/${validationId}`);
      console.log('Validation status:', response.data);
      setValidationStatus(response.data);

      if (response.data.status === 'completed') {
        fetchValidationResults();
      }
    } catch (err) {
      console.error('Failed to fetch validation status:', err);
      setError(`Failed to fetch validation status: ${err.message}`);
    }
  };

  const fetchValidationResults = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/v1/validate/${validationId}/results`);
      console.log('=== VALIDATION RESULTS FROM API ===');
      console.log('Full response:', response.data);
      console.log('statistical_tests:', response.data.statistical_tests);
      console.log('performance:', response.data.performance);
      console.log('performance.statistical_tests:', response.data.performance?.statistical_tests);
      console.log('stability:', response.data.stability);
      console.log('stability.psi:', response.data.stability?.psi);
      console.log('stability.csi:', response.data.stability?.csi);
      setValidationResults(response.data);
      setActiveStep(4);
    } catch (err) {
      console.error('Failed to fetch validation results:', err);
    }
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
    setModelConfig({
      model_name: '',
      product_type: '',
      scorecard_type: '',
      model_type: '',
      description: '',
      version: '1.0',
      owner: 'Model Risk Management'
    });
    setValidationId(null);
    setValidationStatus(null);
    setValidationResults(null);
    setError(null);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      const requestPayload = {
        model_config: modelConfig,
        generate_document: true,
        register_governance: true
      };

      // Add uploaded CSV file paths if available
      if (uploadedDatasets && Object.keys(uploadedDatasets).length > 0) {
        requestPayload.uploaded_files = {
          datasets: uploadedDatasets
        };
        console.log('Including uploaded datasets in validation request:', uploadedDatasets);
      } else {
        console.log('No uploaded datasets found, backend will use sample data');
      }

      const response = await axios.post(`${API_BASE_URL}/api/v1/validate`, requestPayload);

      console.log('Validation started:', response.data);
      setValidationId(response.data.validation_id);
      handleNext();
    } catch (err) {
      console.error('Validation start error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to start validation');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadDocument = async () => {
    try {
      setError(null);

      // Check if validationId is available
      if (!validationId) {
        setError('No validation ID available. Please run a validation first.');
        return;
      }

      const response = await axios.get(
        `${API_BASE_URL}/api/v1/validate/${validationId}/document`,
        { responseType: 'blob' }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${modelConfig.model_name}_validation_report.docx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Download error:', err);
      setError('Failed to download document: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDocumentsUploaded = (documents, datasets) => {
    console.log('[UPLOAD DEBUG] Documents uploaded:', documents);
    console.log('[UPLOAD DEBUG] Datasets mapped:', datasets);
    console.log('[UPLOAD DEBUG] Timestamp:', new Date().toISOString());

    setUploadedDocuments(documents);
    setUploadedDatasets(datasets);

    // VISIBLE DEBUG: Show alert with datasets info
    if (datasets && Object.keys(datasets).length > 0) {
      alert(`✅ Datasets uploaded successfully!\nTrain: ${datasets.train ? '✓' : '✗'}\nTest: ${datasets.test ? '✓' : '✗'}\nOOT: ${datasets.oot ? '✓' : '✗'}`);
    } else {
      alert('⚠️ WARNING: No datasets were mapped from upload response!');
    }
  };

  const renderStepContent = (step) => {
    switch (step) {
      case 0:
        return renderDocumentUpload();
      case 1:
        return renderModelConfiguration();
      case 2:
        return renderReviewSubmit();
      case 3:
        return renderValidationProgress();
      case 4:
        return renderResults();
      default:
        return null;
    }
  };

  const renderDocumentUpload = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Upload Model Documentation (Required)
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Upload model documentation for SR 11-7 compliance validation. Model documentation is required to perform
        comprehensive validation including conceptual soundness, data quality, assumptions, and regulatory compliance checks.
      </Typography>

      <DocumentUpload onDocumentsUploaded={handleDocumentsUploaded} />

      {uploadedDocuments.length > 0 && (
        <Alert severity="success" sx={{ mt: 3 }}>
          <Typography variant="body2">
            {uploadedDocuments.length} document(s) uploaded successfully. These will be analyzed for SR 11-7 compliance validation.
          </Typography>
        </Alert>
      )}

      {uploadedDocuments.length === 0 && (
        <Alert severity="warning" sx={{ mt: 3 }}>
          <Typography variant="body2">
            <strong>Required:</strong> Please upload at least one model documentation file to proceed with SR 11-7 validation.
          </Typography>
        </Alert>
      )}

      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>Supported formats:</strong> PDF, DOCX, CSV
        </Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>
          <strong>What happens next:</strong> Uploaded documents will be analyzed to extract model information,
          identify SR 11-7 sections, validate conceptual soundness, assess data quality, and check regulatory compliance.
        </Typography>
      </Alert>
    </Box>
  );

  const renderModelConfiguration = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Model Configuration
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Configure the model details for SR 11-7 validation
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Model Name"
            value={modelConfig.model_name}
            onChange={(e) => setModelConfig({ ...modelConfig, model_name: e.target.value })}
            placeholder="e.g., US_Unsecured_Application_Scorecard_v1"
            required
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <FormControl fullWidth required>
            <InputLabel>Product Type</InputLabel>
            <Select
              value={modelConfig.product_type}
              onChange={(e) => setModelConfig({ ...modelConfig, product_type: e.target.value })}
              label="Product Type"
            >
              {options?.product_types.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={4}>
          <FormControl fullWidth required>
            <InputLabel>Scorecard Type</InputLabel>
            <Select
              value={modelConfig.scorecard_type}
              onChange={(e) => setModelConfig({ ...modelConfig, scorecard_type: e.target.value })}
              label="Scorecard Type"
            >
              {options?.scorecard_types.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={4}>
          <FormControl fullWidth required>
            <InputLabel>Model Type</InputLabel>
            <Select
              value={modelConfig.model_type}
              onChange={(e) => setModelConfig({ ...modelConfig, model_type: e.target.value })}
              label="Model Type"
            >
              {options?.model_types.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Description"
            value={modelConfig.description}
            onChange={(e) => setModelConfig({ ...modelConfig, description: e.target.value })}
            multiline
            rows={3}
            placeholder="Brief description of the model purpose and use case"
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Version"
            value={modelConfig.version}
            onChange={(e) => setModelConfig({ ...modelConfig, version: e.target.value })}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Model Owner"
            value={modelConfig.owner}
            onChange={(e) => setModelConfig({ ...modelConfig, owner: e.target.value })}
          />
        </Grid>
      </Grid>
    </Box>
  );

  const renderReviewSubmit = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Review Configuration
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Please review the model configuration before starting validation
      </Typography>

      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Typography variant="subtitle2" color="text.secondary">Model Name</Typography>
              <Typography variant="body1">{modelConfig.model_name}</Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" color="text.secondary">Product Type</Typography>
              <Typography variant="body1">
                {options?.product_types.find(o => o.value === modelConfig.product_type)?.label}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" color="text.secondary">Scorecard Type</Typography>
              <Typography variant="body1">
                {options?.scorecard_types.find(o => o.value === modelConfig.scorecard_type)?.label}
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="subtitle2" color="text.secondary">Model Type</Typography>
              <Typography variant="body1">
                {options?.model_types.find(o => o.value === modelConfig.model_type)?.label}
              </Typography>
            </Grid>
            {modelConfig.description && (
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="text.secondary">Description</Typography>
                <Typography variant="body1">{modelConfig.description}</Typography>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>

      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          The validation process will:
        </Typography>
        <ul style={{ marginTop: 8, marginBottom: 0 }}>
          <li>Generate synthetic data for testing</li>
          <li>Perform comprehensive SR 11-7 validation</li>
          <li>Generate a Word document with complete validation report</li>
          <li>Register the model in watsonx.governance</li>
        </ul>
      </Alert>
    </Box>
  );

  const renderValidationProgress = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Validation in Progress
      </Typography>
      <Typography variant="body2" color="text.secondary" paragraph>
        Validation ID: {validationId}
      </Typography>

      <Card sx={{ mt: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <CircularProgress size={24} sx={{ mr: 2 }} />
            <Typography variant="h6">
              Status: {validationStatus?.status || 'Starting...'}
            </Typography>
          </Box>

          <LinearProgress sx={{ mb: 2 }} />

          <Typography variant="body2" color="text.secondary">
            This process typically takes 2-5 minutes. The system is:
          </Typography>
          <ul>
            <li>Analyzing model requirements</li>
            <li>Generating synthetic validation data</li>
            <li>Performing data quality checks</li>
            <li>Validating model performance</li>
            <li>Testing model assumptions</li>
            <li>Analyzing stability</li>
            <li>Checking SR 11-7 compliance</li>
            <li>Generating documentation</li>
          </ul>
        </CardContent>
      </Card>
    </Box>
  );

  const renderResults = () => (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" gutterBottom>
        Validation Complete
      </Typography>

      <Alert severity="success" sx={{ mb: 3 }}>
        <Typography variant="body1">
          Validation completed successfully! The comprehensive SR 11-7 validation report is ready.
        </Typography>
      </Alert>

      {/* Use the enhanced ValidationResults component */}
      {validationResults && <ValidationResults results={validationResults} />}

      {/* Download button */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Description color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6">Validation Report</Typography>
          </Box>
          <Typography variant="body2" paragraph>
            A comprehensive Word document has been generated containing all validation results,
            statistical tests, compliance analysis, and recommendations.
          </Typography>
          <Button
            variant="contained"
            startIcon={<CloudDownload />}
            onClick={handleDownloadDocument}
            sx={{ mt: 2 }}
          >
            Download Validation Report
          </Button>
        </CardContent>
      </Card>
    </Box>
  );

  const isStepValid = () => {
    if (activeStep === 0) {
      // Document upload is REQUIRED for SR 11-7 validation
      return uploadedDocuments.length > 0;
    }
    if (activeStep === 1) {
      // Model configuration must be complete
      return modelConfig.model_name &&
             modelConfig.product_type &&
             modelConfig.scorecard_type &&
             modelConfig.model_type;
    }
    return true;
  };

  return (
    <>
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom align="center">
            Banking Model Validation System
          </Typography>
          <Typography variant="subtitle1" align="center" color="text.secondary" paragraph>
            Automated SR 11-7 Compliance Validation powered by IBM watsonx
          </Typography>

          <Divider sx={{ my: 3 }} />

          <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
            {steps.map((label) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {renderStepContent(activeStep)}

          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              disabled={activeStep === 0 || activeStep === 3}
              onClick={handleBack}
            >
              Back
            </Button>
            <Box>
              {activeStep === steps.length - 1 ? (
                <Button onClick={handleReset} variant="contained">
                  Start New Validation
                </Button>
              ) : activeStep === 2 ? (
                <Button
                  variant="contained"
                  onClick={handleSubmit}
                  disabled={loading || !isStepValid()}
                >
                  {loading ? <CircularProgress size={24} /> : 'Start Validation'}
                </Button>
              ) : (activeStep === 0 || activeStep === 1) ? (
                <Button
                  variant="contained"
                  onClick={handleNext}
                  disabled={!isStepValid()}
                >
                  Next
                </Button>
              ) : null}
            </Box>
          </Box>
        </Paper>
      </Container>
    </>
  );
}

export default App;

// Made with Bob
