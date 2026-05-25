"""
Banking Model Validation System - Enhanced Main API
FastAPI application with MLOps, watsonx.governance, and watsonx Orchestrate integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
import asyncio
import json

from wxo.watsonx_client import WatsonxClient
from watsonx.governance_client import WatsonxGovernanceClient
from wxo.orchestrate_client import WatsonxOrchestrateClient
from agents.validation_orchestrator import ValidationOrchestratorAgent
from agents.mlops_agent import MLOpsAgent
from validation.document_generator import SR117DocumentGenerator

# Initialize FastAPI app
app = FastAPI(
    title="Banking Model Validation System - Enhanced",
    description="Automated model validation with MLOps, governance, and orchestration",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
watsonx_client = None
governance_client = None
orchestrate_client = None
mlops_agent = None
orchestrator = None

# WebSocket connections for real-time updates
active_connections: List[WebSocket] = []

# ==================== Pydantic Models ====================

class ModelConfig(BaseModel):
    """Model configuration for validation"""
    model_name: str = Field(..., description="Name of the model")
    product_type: str = Field(..., description="Product type: secured, unsecured, revolving")
    scorecard_type: str = Field(..., description="Scorecard type: application, behavioral, collections_early, collections_late")
    model_type: str = Field(..., description="Model type: GLM, GAM, ANN, XGBoost, RandomForest, etc.")
    description: Optional[str] = Field(None, description="Model description")
    version: Optional[str] = Field("1.0", description="Model version")
    owner: Optional[str] = Field("Model Risk Management", description="Model owner")
    features: Optional[List[str]] = Field(None, description="List of model features")
    data_version: Optional[str] = Field("1.0", description="Training data version")


class UseCaseRequest(BaseModel):
    """Use case onboarding request"""
    product_type: str
    scorecard_type: str
    business_objective: str
    risk_level: str = "high"


class ModelRegistrationRequest(BaseModel):
    """Model registration request"""
    model_name: str
    use_case_id: str
    model_type: str
    product_type: str
    scorecard_type: str
    features: List[str]
    data_version: str
    performance_metrics: Dict[str, float]
    validation_results: Dict[str, Any]
    description: Optional[str] = None


class MonitoringRequest(BaseModel):
    """Production monitoring request"""
    model_id: str
    version_id: str
    current_metrics: Dict[str, float]


class DeploymentRequest(BaseModel):
    """Model deployment request"""
    model_id: str
    version_id: str
    deployment_environment: str = "production"
    approvers: List[str] = ["mrm@bank.com"]


class ApprovalRequest(BaseModel):
    """Task approval/rejection request"""
    task_id: str
    approver: str
    action: str  # "approve" or "reject"
    comments: Optional[str] = None
    reason: Optional[str] = None


class StressTestRequest(BaseModel):
    """Stress testing request"""
    model_id: str
    test_type: str  # "adverse", "severely_adverse", "custom"
    scenarios: List[Dict[str, Any]]


class CustomTestRequest(BaseModel):
    """Custom validation test request"""
    model_id: str
    test_name: str
    test_description: str
    test_parameters: Dict[str, Any]


# ==================== Startup and Shutdown ====================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global watsonx_client, governance_client, orchestrate_client, mlops_agent, orchestrator
    
    try:
        # Initialize watsonx client
        watsonx_client = WatsonxClient()
        
        # Initialize governance client
        governance_client = WatsonxGovernanceClient()
        
        # Initialize orchestrate client
        orchestrate_client = WatsonxOrchestrateClient()
        
        # Initialize MLOps agent
        mlops_agent = MLOpsAgent(governance_client, watsonx_client)
        
        # Initialize orchestrator
        orchestrator = ValidationOrchestratorAgent(watsonx_client)
        
        print("✓ Banking Model Validation System (Enhanced) initialized successfully")
        print("  - watsonx.ai: Connected")
        print("  - watsonx.governance: Connected")
        print("  - watsonx Orchestrate: Connected")
        print("  - MLOps Agent: Ready")
        
    except Exception as e:
        print(f"✗ Failed to initialize system: {e}")
        print("  Note: Set WATSONX_API_KEY environment variable to enable watsonx features")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Banking Model Validation System shutting down...")


# ==================== WebSocket for Real-time Updates ====================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_update(message: Dict[str, Any]):
    """Broadcast update to all connected clients"""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            pass


# ==================== Basic Endpoints ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Banking Model Validation System - Enhanced",
        "version": "2.0.0",
        "status": "operational",
        "framework": "SR 11-7",
        "powered_by": "IBM watsonx",
        "features": [
            "MLOps Automation",
            "watsonx.governance Integration",
            "watsonx Orchestrate Workflows",
            "Real-time Monitoring",
            "Stress Testing",
            "Custom Validation Tests"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "watsonx_ai": watsonx_client is not None,
            "governance": governance_client is not None,
            "orchestrate": orchestrate_client is not None,
            "mlops_agent": mlops_agent is not None
        }
    }


@app.get("/api/v1/options")
async def get_options():
    """Get available options for model configuration"""
    return {
        "product_types": [
            {"value": "secured", "label": "Secured Loans"},
            {"value": "unsecured", "label": "Unsecured Loans"},
            {"value": "revolving", "label": "Revolving Credit"}
        ],
        "scorecard_types": [
            {"value": "application", "label": "Application Scorecard"},
            {"value": "behavioral", "label": "Behavioral Scorecard"},
            {"value": "collections_early", "label": "Early Stage Collections"},
            {"value": "collections_late", "label": "Late Stage Collections"}
        ],
        "model_types": [
            {"value": "GLM", "label": "Generalized Linear Model"},
            {"value": "GAM", "label": "Generalized Additive Model"},
            {"value": "ANN", "label": "Artificial Neural Network"},
            {"value": "XGBoost", "label": "XGBoost"},
            {"value": "RandomForest", "label": "Random Forest"},
            {"value": "LightGBM", "label": "LightGBM"},
            {"value": "LogisticRegression", "label": "Logistic Regression"},
            {"value": "DecisionTree", "label": "Decision Tree"}
        ],
        "risk_levels": [
            {"value": "low", "label": "Low Risk"},
            {"value": "medium", "label": "Medium Risk"},
            {"value": "high", "label": "High Risk"},
            {"value": "critical", "label": "Critical Risk"}
        ]
    }


# ==================== MLOps Endpoints ====================

@app.post("/api/v1/mlops/onboard-use-case")
async def onboard_use_case(request: UseCaseRequest):
    """Onboard a new model use case"""
    if not mlops_agent:
        raise HTTPException(status_code=503, detail="MLOps agent not initialized")
    
    try:
        result = await mlops_agent.onboard_use_case(
            product_type=request.product_type,
            scorecard_type=request.scorecard_type,
            business_objective=request.business_objective,
            risk_level=request.risk_level
        )
        
        await broadcast_update({
            "type": "use_case_onboarded",
            "data": result
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/mlops/check-existing-models")
async def check_existing_models(
    product_type: str,
    scorecard_type: str,
    model_type: Optional[str] = None
):
    """Check for existing models before building new one"""
    if not mlops_agent:
        raise HTTPException(status_code=503, detail="MLOps agent not initialized")
    
    try:
        result = await mlops_agent.check_existing_models(
            product_type=product_type,
            scorecard_type=scorecard_type,
            model_type=model_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/mlops/register-model")
async def register_model(request: ModelRegistrationRequest):
    """Register a new model with initial version"""
    if not mlops_agent:
        raise HTTPException(status_code=503, detail="MLOps agent not initialized")
    
    try:
        result = await mlops_agent.register_new_model(
            model_name=request.model_name,
            use_case_id=request.use_case_id,
            model_type=request.model_type,
            product_type=request.product_type,
            scorecard_type=request.scorecard_type,
            features=request.features,
            data_version=request.data_version,
            performance_metrics=request.performance_metrics,
            validation_results=request.validation_results,
            description=request.description
        )
        
        await broadcast_update({
            "type": "model_registered",
            "data": result
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/mlops/monitor")
async def monitor_model(request: MonitoringRequest):
    """Monitor model performance in production"""
    if not mlops_agent:
        raise HTTPException(status_code=503, detail="MLOps agent not initialized")
    
    try:
        result = await mlops_agent.monitor_production_model(
            model_id=request.model_id,
            version_id=request.version_id,
            current_metrics=request.current_metrics
        )
        
        # Broadcast alert if critical
        if result["status"] == "critical":
            await broadcast_update({
                "type": "monitoring_alert",
                "severity": "critical",
                "data": result
            })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/mlops/deploy")
async def deploy_model(request: DeploymentRequest):
    """Deploy model to production"""
    if not mlops_agent or not orchestrate_client:
        raise HTTPException(status_code=503, detail="Services not initialized")
    
    try:
        # Create deployment workflow
        workflow_id = orchestrate_client.create_model_deployment_workflow(
            model_name=f"Model_{request.model_id}",
            model_id=request.model_id,
            version_id=request.version_id,
            deployment_environment=request.deployment_environment,
            approvers=request.approvers
        )
        
        return {
            "workflow_id": workflow_id,
            "status": "approval_pending",
            "message": "Deployment workflow created. Awaiting approval.",
            "approvers": request.approvers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/mlops/documentation/{model_id}")
async def get_model_documentation(model_id: str, version_id: Optional[str] = None):
    """Generate comprehensive model documentation"""
    if not mlops_agent:
        raise HTTPException(status_code=503, detail="MLOps agent not initialized")
    
    try:
        documentation = await mlops_agent.generate_model_documentation(
            model_id=model_id,
            version_id=version_id
        )
        return documentation
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Governance Endpoints ====================

@app.get("/api/v1/governance/use-cases")
async def list_use_cases():
    """List all use cases"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        use_cases = governance_client.list_use_cases()
        return {"use_cases": use_cases}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/governance/models")
async def list_models(use_case_id: Optional[str] = None):
    """List all models"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        models = governance_client.list_models(use_case_id=use_case_id)
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/governance/models/{model_id}")
async def get_model(model_id: str):
    """Get model details"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        model = governance_client.get_model(model_id)
        return model
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/governance/models/{model_id}/versions")
async def get_model_versions(model_id: str):
    """Get all versions of a model"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        versions = governance_client.get_model_versions(model_id)
        return {"versions": versions}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/governance/models/{model_id}/monitoring")
async def get_monitoring_metrics(
    model_id: str,
    version_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get monitoring metrics for a model version"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        metrics = governance_client.get_monitoring_metrics(
            model_id=model_id,
            version_id=version_id,
            start_date=start_date,
            end_date=end_date
        )
        return {"metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/governance/models/{model_id}/compliance")
async def get_compliance_report(
    model_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Generate compliance report for a model"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        report = governance_client.generate_compliance_report(
            model_id=model_id,
            start_date=start_date,
            end_date=end_date
        )
        return report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/governance/models/{model_id}/card")
async def get_model_card(model_id: str):
    """Get model card"""
    if not governance_client:
        raise HTTPException(status_code=503, detail="Governance client not initialized")
    
    try:
        card = governance_client.generate_model_card(model_id)
        return card
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Orchestrate Endpoints ====================

@app.get("/api/v1/orchestrate/workflows")
async def list_workflows(
    workflow_type: Optional[str] = None,
    status: Optional[str] = None
):
    """List workflows"""
    if not orchestrate_client:
        raise HTTPException(status_code=503, detail="Orchestrate client not initialized")
    
    try:
        workflows = orchestrate_client.list_workflows(
            workflow_type=workflow_type,
            status=status
        )
        return {"workflows": workflows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/orchestrate/workflows/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get workflow details"""
    if not orchestrate_client:
        raise HTTPException(status_code=503, detail="Orchestrate client not initialized")
    
    try:
        workflow = orchestrate_client.get_workflow(workflow_id)
        return workflow
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/orchestrate/tasks")
async def list_tasks(
    assignee: Optional[str] = None,
    status: Optional[str] = None
):
    """List tasks"""
    if not orchestrate_client:
        raise HTTPException(status_code=503, detail="Orchestrate client not initialized")
    
    try:
        tasks = orchestrate_client.list_tasks(assignee=assignee, status=status)
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/orchestrate/tasks/action")
async def handle_task_action(request: ApprovalRequest):
    """Approve or reject a task"""
    if not orchestrate_client:
        raise HTTPException(status_code=503, detail="Orchestrate client not initialized")
    
    try:
        if request.action == "approve":
            result = await orchestrate_client.approve_task(
                task_id=request.task_id,
                approver=request.approver,
                comments=request.comments
            )
        elif request.action == "reject":
            result = await orchestrate_client.reject_task(
                task_id=request.task_id,
                approver=request.approver,
                reason=request.reason or "No reason provided"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'approve' or 'reject'")
        
        await broadcast_update({
            "type": "task_action",
            "action": request.action,
            "data": result
        })
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Stress Testing Endpoints ====================

@app.post("/api/v1/stress-test")
async def run_stress_test(request: StressTestRequest):
    """Run stress testing on a model"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        # This would integrate with the validation orchestrator
        # For now, return a placeholder
        result = {
            "test_id": f"STRESS_{datetime.utcnow().timestamp()}",
            "model_id": request.model_id,
            "test_type": request.test_type,
            "status": "running",
            "scenarios": len(request.scenarios),
            "started_at": datetime.utcnow().isoformat()
        }
        
        await broadcast_update({
            "type": "stress_test_started",
            "data": result
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/stress-test/{test_id}")
async def get_stress_test_results(test_id: str):
    """Get stress test results"""
    # Placeholder for stress test results
    return {
        "test_id": test_id,
        "status": "completed",
        "results": {
            "baseline_performance": {"AUC": 0.75, "KS": 0.35},
            "adverse_scenario": {"AUC": 0.72, "KS": 0.32},
            "severely_adverse_scenario": {"AUC": 0.68, "KS": 0.28},
            "recommendation": "Model shows acceptable resilience under stress"
        }
    }


# ==================== Custom Test Endpoints ====================

@app.post("/api/v1/custom-test")
async def run_custom_test(request: CustomTestRequest):
    """Run custom validation test"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    try:
        test_id = f"CUSTOM_{datetime.utcnow().timestamp()}"
        
        result = {
            "test_id": test_id,
            "model_id": request.model_id,
            "test_name": request.test_name,
            "status": "running",
            "started_at": datetime.utcnow().isoformat()
        }
        
        await broadcast_update({
            "type": "custom_test_started",
            "data": result
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/custom-test/{test_id}")
async def get_custom_test_results(test_id: str):
    """Get custom test results"""
    # Placeholder for custom test results
    return {
        "test_id": test_id,
        "status": "completed",
        "results": {
            "test_passed": True,
            "details": "Custom test completed successfully"
        }
    }


# ==================== Document Upload Endpoints ====================

from fastapi import UploadFile, File
from validation.document_analyzer import DocumentAnalyzer
import shutil
from pathlib import Path

# Initialize document analyzer
document_analyzer = DocumentAnalyzer()

# Create uploads directory
UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Store uploaded documents metadata
uploaded_documents = {}


@app.post("/api/v1/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    model_id: Optional[str] = None,
    document_type: Optional[str] = None
):
    """
    Upload and analyze a document (PDF, DOCX, or CSV)
    
    Args:
        file: The file to upload
        model_id: Optional model ID to associate with the document
        document_type: Optional document type (e.g., 'model_documentation', 'validation_report')
    
    Returns:
        Document metadata and analysis results
    """
    try:
        # Validate file
        validation_result = document_analyzer.validate_file(file.filename, file.size)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # Generate unique document ID
        doc_id = f"DOC_{datetime.utcnow().timestamp()}"
        
        # Save file
        file_path = UPLOAD_DIR / f"{doc_id}_{file.filename}"
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Analyze document
        analysis = document_analyzer.analyze_document(str(file_path))
        
        # Extract metadata
        metadata = document_analyzer.extract_metadata(str(file_path))
        
        # Store document info
        doc_info = {
            "document_id": doc_id,
            "filename": file.filename,
            "file_path": str(file_path),
            "file_size": file.size,
            "file_type": validation_result["file_type"],
            "model_id": model_id,
            "document_type": document_type,
            "uploaded_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "analysis": analysis
        }
        
        uploaded_documents[doc_id] = doc_info
        
        # Broadcast update
        await broadcast_update({
            "type": "document_uploaded",
            "data": {
                "document_id": doc_id,
                "filename": file.filename,
                "analysis_summary": {
                    "sr_11_7_coverage": analysis.get("sr_11_7_sections", {}).get("overall_coverage", 0),
                    "sections_found": len(analysis.get("sr_11_7_sections", {}).get("sections_found", [])),
                    "model_info_extracted": bool(analysis.get("model_info"))
                }
            }
        })
        
        return {
            "success": True,
            "document_id": doc_id,
            "filename": file.filename,
            "file_type": validation_result["file_type"],
            "analysis": analysis,
            "metadata": metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@app.post("/api/upload-documents")
async def upload_documents_batch(
    files: List[UploadFile] = File(...)
):
    """
    Upload multiple documents at once (batch upload)
    
    Args:
        files: List of files to upload
    
    Returns:
        Upload results with document metadata and datasets info
    """
    try:
        uploaded_docs = []
        datasets = {
            "train": None,
            "test": None,
            "oot": None
        }
        errors = []
        
        for file in files:
            try:
                # Validate file
                validation_result = document_analyzer.validate_file(file.filename, file.size)
                if not validation_result["valid"]:
                    errors.append(f"{file.filename}: {validation_result['error']}")
                    continue
                
                # Generate unique document ID
                doc_id = f"DOC_{datetime.utcnow().timestamp()}_{file.filename}"
                
                # Save file
                file_path = UPLOAD_DIR / f"{doc_id}_{file.filename}"
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Analyze document
                analysis = document_analyzer.analyze_document(str(file_path))
                
                # Extract metadata
                metadata = document_analyzer.extract_metadata(str(file_path))
                
                # Store document info
                doc_info = {
                    "document_id": doc_id,
                    "filename": file.filename,
                    "file_path": str(file_path),
                    "file_size": file.size,
                    "file_type": validation_result["file_type"],
                    "upload_time": datetime.utcnow().isoformat(),
                    "metadata": metadata,
                    "analysis": analysis
                }
                
                uploaded_documents[doc_id] = doc_info
                uploaded_docs.append(doc_info)
                
                # Identify dataset type from filename
                filename_lower = file.filename.lower()
                if 'train' in filename_lower:
                    datasets["train"] = doc_id
                elif 'test' in filename_lower:
                    datasets["test"] = doc_id
                elif 'oot' in filename_lower:
                    datasets["oot"] = doc_id
                
            except Exception as e:
                errors.append(f"{file.filename}: {str(e)}")
        
        # Broadcast update
        await broadcast_update({
            "type": "documents_uploaded",
            "data": {
                "count": len(uploaded_docs),
                "documents": [{"document_id": d["document_id"], "filename": d["filename"]} for d in uploaded_docs]
            }
        })
        
        return {
            "success": True,
            "documents": uploaded_docs,
            "datasets": datasets,
            "errors": errors if errors else None,
            "message": f"Successfully uploaded {len(uploaded_docs)} of {len(files)} files"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading documents: {str(e)}")



@app.get("/api/v1/documents")
async def list_documents(
    model_id: Optional[str] = None,
    document_type: Optional[str] = None
):
    """
    List all uploaded documents
    
    Args:
        model_id: Filter by model ID
        document_type: Filter by document type
    
    Returns:
        List of documents with metadata
    """
    try:
        documents = list(uploaded_documents.values())
        
        # Apply filters
        if model_id:
            documents = [d for d in documents if d.get("model_id") == model_id]
        if document_type:
            documents = [d for d in documents if d.get("document_type") == document_type]
        
        # Return summary (without full analysis)
        return {
            "documents": [
                {
                    "document_id": d["document_id"],
                    "filename": d["filename"],
                    "file_type": d["file_type"],
                    "file_size": d["file_size"],
                    "model_id": d.get("model_id"),
                    "document_type": d.get("document_type"),
                    "uploaded_at": d["uploaded_at"],
                    "sr_11_7_coverage": d["analysis"].get("sr_11_7_sections", {}).get("overall_coverage", 0)
                }
                for d in documents
            ],
            "total": len(documents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/{document_id}")
async def get_document(document_id: str):
    """
    Get document details and analysis
    
    Args:
        document_id: Document ID
    
    Returns:
        Complete document information including analysis
    """
    try:
        if document_id not in uploaded_documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return uploaded_documents[document_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/v1/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete an uploaded document
    
    Args:
        document_id: Document ID
    
    Returns:
        Success message
    """
    try:
        if document_id not in uploaded_documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc_info = uploaded_documents[document_id]
        
        # Delete file
        file_path = Path(doc_info["file_path"])
        if file_path.exists():
            file_path.unlink()
        
        # Remove from storage
        del uploaded_documents[document_id]
        
        # Broadcast update
        await broadcast_update({
            "type": "document_deleted",
            "data": {"document_id": document_id}
        })
        
        return {
            "success": True,
            "message": f"Document {document_id} deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/{document_id}/download")
async def download_document(document_id: str):
    """
    Download an uploaded document
    
    Args:
        document_id: Document ID
    
    Returns:
        File response
    """
    try:
        if document_id not in uploaded_documents:
            raise HTTPException(status_code=404, detail="Document not found")
        
        doc_info = uploaded_documents[document_id]
        file_path = Path(doc_info["file_path"])
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Determine media type
        media_types = {
            "pdf": "application/pdf",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "csv": "text/csv"
        }
        media_type = media_types.get(doc_info["file_type"], "application/octet-stream")
        
        return FileResponse(
            str(file_path),
            media_type=media_type,
            filename=doc_info["filename"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Validation Endpoints (Original) ====================

@app.post("/api/v1/validate")
async def start_validation(
    request: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Start model validation process"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")
    
    try:
        model_request = request.get("model_config", request)
        generate_document = request.get("generate_document", True)

        validation_id = f"VAL_{datetime.utcnow().timestamp()}"

        background_tasks.add_task(
            run_validation,
            validation_id,
            model_request,
            generate_document
        )
        
        return {
            "validation_id": validation_id,
            "status": "started",
            "started_at": datetime.utcnow().isoformat(),
            "model_name": model_request.get("model_name", "Unknown")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def run_validation(validation_id: str, request: Dict[str, Any], generate_document: bool = True):
    """Run validation workflow in background"""
    try:
        await broadcast_update({
            "type": "validation_started",
            "validation_id": validation_id
        })
        
        results = await orchestrator.orchestrate_validation(request)

        internal_validation_id = results["validation_id"]
        if internal_validation_id != validation_id and internal_validation_id in orchestrator.validation_state:
            orchestrator.validation_state[validation_id] = orchestrator.validation_state.pop(internal_validation_id)

        if generate_document:
            doc_generator = SR117DocumentGenerator()
            output_dir = "/app/output/documents"
            os.makedirs(output_dir, exist_ok=True)

            doc_path = os.path.join(
                output_dir,
                f"{request.get('model_name', 'model')}_validation_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.docx"
            )

            doc_generator.generate_validation_report(
                model_config=request,
                validation_results=results["results"],
                output_path=doc_path
            )

            orchestrator.validation_state[validation_id]["results"]["documentation"] = {
                **orchestrator.validation_state[validation_id]["results"].get("documentation", {}),
                "document_path": doc_path
            }

        await broadcast_update({
            "type": "validation_completed",
            "validation_id": validation_id,
            "results": orchestrator.validation_state.get(validation_id, {})
        })
        
    except Exception as e:
        if validation_id in orchestrator.validation_state:
            orchestrator.validation_state[validation_id]["status"] = "failed"
            orchestrator.validation_state[validation_id]["error"] = str(e)
        await broadcast_update({
            "type": "validation_failed",
            "validation_id": validation_id,
            "error": str(e)
        })


@app.get("/api/v1/validate/{validation_id}")
async def get_validation_status(validation_id: str):
    """Get validation status"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        status = orchestrator.get_validation_status(validation_id)
        return {
            "validation_id": validation_id,
            "status": status["status"],
            "started_at": status["started_at"],
            "completed_at": status.get("completed_at"),
            "model_name": status["model_config"].get("model_name", "Unknown"),
            "progress": status.get("results", {}),
            "error": status.get("error")
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/validate/{validation_id}/results")
async def get_validation_results(validation_id: str):
    """Get complete validation results"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        status = orchestrator.get_validation_status(validation_id)

        if status["status"] != "completed":
            raise HTTPException(
                status_code=400,
                detail=f"Validation not completed. Current status: {status['status']}"
            )

        return {
            "validation_id": validation_id,
            "model_config": status["model_config"],
            "results": status["results"],
            "completed_at": status.get("completed_at")
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/validate/{validation_id}/document")
async def download_validation_document(validation_id: str):
    """Download validation document"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        status = orchestrator.get_validation_status(validation_id)

        if status["status"] != "completed":
            raise HTTPException(status_code=400, detail="Validation not completed")

        doc_path = status["results"].get("documentation", {}).get("document_path")

        if not doc_path or not os.path.exists(doc_path):
            raise HTTPException(status_code=404, detail="Document not found")

        return FileResponse(
            doc_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=os.path.basename(doc_path)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/validations")
async def list_validations():
    """List all validations"""
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Validation service not initialized")

    try:
        return {"validations": orchestrator.list_validations()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Made with ❤️ by Bob

# Made with Bob
