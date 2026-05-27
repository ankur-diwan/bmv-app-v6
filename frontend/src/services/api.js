/**
 * API Client for Banking Model Validation System
 * Handles all backend communication
 */

import axios from 'axios';

// API Base URL configuration
// In production (Code Engine), requests go through nginx proxy at /api/
// In development, use VITE_API_URL environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens if needed
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ==================== Basic Endpoints ====================

export const getHealth = () => apiClient.get('/health');

export const getOptions = () => apiClient.get('/api/v1/options');

// ==================== MLOps Endpoints ====================

export const mlopsAPI = {
  // Onboard use case
  onboardUseCase: (data) => 
    apiClient.post('/api/v1/mlops/onboard-use-case', data),
  
  // Check existing models
  checkExistingModels: (productType, scorecardType, modelType = null) => 
    apiClient.get('/api/v1/mlops/check-existing-models', {
      params: { product_type: productType, scorecard_type: scorecardType, model_type: modelType }
    }),
  
  // Register new model
  registerModel: (data) => 
    apiClient.post('/api/v1/mlops/register-model', data),
  
  // Monitor model
  monitorModel: (data) => 
    apiClient.post('/api/v1/mlops/monitor', data),
  
  // Deploy model
  deployModel: (data) => 
    apiClient.post('/api/v1/mlops/deploy', data),
  
  // Get model documentation
  getDocumentation: (modelId, versionId = null) => 
    apiClient.get(`/api/v1/mlops/documentation/${modelId}`, {
      params: versionId ? { version_id: versionId } : {}
    }),
};

// ==================== Governance Endpoints ====================

export const governanceAPI = {
  // List use cases
  listUseCases: () => 
    apiClient.get('/api/v1/governance/use-cases'),
  
  // List models
  listModels: (useCaseId = null) => 
    apiClient.get('/api/v1/governance/models', {
      params: useCaseId ? { use_case_id: useCaseId } : {}
    }),
  
  // Get model details
  getModel: (modelId) => 
    apiClient.get(`/api/v1/governance/models/${modelId}`),
  
  // Get model versions
  getModelVersions: (modelId) => 
    apiClient.get(`/api/v1/governance/models/${modelId}/versions`),
  
  // Get monitoring metrics
  getMonitoringMetrics: (modelId, versionId, startDate = null, endDate = null) => 
    apiClient.get(`/api/v1/governance/models/${modelId}/monitoring`, {
      params: { version_id: versionId, start_date: startDate, end_date: endDate }
    }),
  
  // Get compliance report
  getComplianceReport: (modelId, startDate = null, endDate = null) => 
    apiClient.get(`/api/v1/governance/models/${modelId}/compliance`, {
      params: { start_date: startDate, end_date: endDate }
    }),
  
  // Get model card
  getModelCard: (modelId) => 
    apiClient.get(`/api/v1/governance/models/${modelId}/card`),
};

// ==================== Orchestrate Endpoints ====================

export const orchestrateAPI = {
  // List workflows
  listWorkflows: (workflowType = null, status = null) => 
    apiClient.get('/api/v1/orchestrate/workflows', {
      params: { workflow_type: workflowType, status }
    }),
  
  // Get workflow details
  getWorkflow: (workflowId) => 
    apiClient.get(`/api/v1/orchestrate/workflows/${workflowId}`),
  
  // List tasks
  listTasks: (assignee = null, status = null) => 
    apiClient.get('/api/v1/orchestrate/tasks', {
      params: { assignee, status }
    }),
  
  // Approve task
  approveTask: (taskId, approver, comments = null) => 
    apiClient.post('/api/v1/orchestrate/tasks/action', {
      task_id: taskId,
      approver,
      action: 'approve',
      comments
    }),
  
  // Reject task
  rejectTask: (taskId, approver, reason) => 
    apiClient.post('/api/v1/orchestrate/tasks/action', {
      task_id: taskId,
      approver,
      action: 'reject',
      reason
    }),
};

// ==================== Stress Testing Endpoints ====================

export const stressTestAPI = {
  // Run stress test
  runStressTest: (data) => 
    apiClient.post('/api/v1/stress-test', data),
  
  // Get stress test results
  getStressTestResults: (testId) => 
    apiClient.get(`/api/v1/stress-test/${testId}`),
};

// ==================== Custom Test Endpoints ====================

export const customTestAPI = {
  // Run custom test
  runCustomTest: (data) => 
    apiClient.post('/api/v1/custom-test', data),
  
  // Get custom test results
  getCustomTestResults: (testId) => 
    apiClient.get(`/api/v1/custom-test/${testId}`),
};

// ==================== Validation Endpoints (Original) ====================

export const validationAPI = {
  // Start validation
  startValidation: (data) => 
    apiClient.post('/api/v1/validate', data),
  
  // Get validation status
  getValidationStatus: (validationId) => 
    apiClient.get(`/api/v1/validate/${validationId}`),
  
  // Get validation results
  getValidationResults: (validationId) => 
    apiClient.get(`/api/v1/validate/${validationId}/results`),
  
  // Download validation document
  downloadDocument: (validationId) => 
    apiClient.get(`/api/v1/validate/${validationId}/document`, {
      responseType: 'blob'
    }),
};

// ==================== WebSocket Connection ====================

export const createWebSocketConnection = (onMessage) => {
  const wsUrl = API_BASE_URL.replace('http', 'ws') + '/ws';
  const ws = new WebSocket(wsUrl);
  
  ws.onopen = () => {
    console.log('WebSocket connected');
  };
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  ws.onclose = () => {
    console.log('WebSocket disconnected');
  };
  
  return ws;
};

// Export default client for custom requests
export default apiClient;

// Made with ❤️ by Bob

// Made with Bob
