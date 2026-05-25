# Banking Model Validation System

A comprehensive, AI-powered model validation platform for banking and financial institutions, built with IBM watsonx.ai, watsonx.governance, and FastAPI.

## 🎯 Overview

This system automates the validation of banking models (credit risk, fraud detection, etc.) according to regulatory frameworks like SR 11-7, ensuring compliance, accuracy, and reliability.

### Key Features

- ✅ **Automated Model Validation** - Comprehensive validation across multiple dimensions
- 🤖 **AI-Powered Analysis** - Uses IBM watsonx.ai for intelligent document review
- 📊 **MLOps Integration** - Full model lifecycle management with watsonx.governance
- 🔄 **Workflow Orchestration** - Automated approval workflows with watsonx Orchestrate
- 📈 **Real-time Monitoring** - Continuous model performance tracking
- 📝 **Automated Documentation** - SR 11-7 compliant validation reports
- 🎨 **Modern UI** - React-based frontend with real-time updates

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │  React + Vite
│   (Port 5173)   │
└────────┬────────┘
         │
┌────────▼────────┐
│   Backend API   │  FastAPI + Python
│   (Port 8080)   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──────┐  ┌──▼────────┐
│  Cloud   │  │ watsonx   │
│  Object  │  │    AI     │
│ Storage  │  │           │
└──────────┘  └───────────┘
```

**Note:** This application uses IBM Cloud Object Storage (COS) for all data persistence. PostgreSQL is NOT required.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- IBM Cloud account with watsonx.ai access
- IBM Cloud Object Storage (COS) bucket
- Docker (optional, for containerized deployment)

**Note:** PostgreSQL is NOT required - the application uses IBM Cloud Object Storage.

### Environment Variables

Create a `.env` file in the root directory:

```bash
# IBM watsonx Configuration
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com

# IBM Cloud Object Storage Configuration
COS_API_KEY=your_cos_api_key
COS_RESOURCE_INSTANCE_ID=your_cos_resource_instance_id
COS_ENDPOINT_URL=https://s3.us-south.cloud-object-storage.appdomain.cloud
COS_BUCKET_NAME=bankvalidationapp

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Access the application at `http://localhost:5173`

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individual containers
docker build -t banking-validation-backend ./backend
docker build -t banking-validation-frontend ./frontend
```

## ☁️ IBM Cloud Code Engine Deployment

This application is **production-ready** for IBM Cloud Code Engine deployment!

### 📋 Quick Deployment Guide

**Total Time:** ~40 minutes | **Difficulty:** Intermediate

#### Required Services:
- ✅ IBM watsonx.ai (AI-powered validation)
- ✅ IBM Cloud Object Storage (Document storage)
- ✅ IBM Cloud Code Engine (Application hosting)
- ❌ PostgreSQL (NOT required)

#### Deployment Steps:

1. **Prepare Prerequisites** (5 min)
   - Create COS bucket
   - Get watsonx.ai credentials
   - Push code to GitHub

2. **Create Code Engine Project** (2 min)
   - Create project in IBM Cloud Console
   - Select region (e.g., us-south)

3. **Create Secrets** (5 min)
   - `watsonx-credentials` (API key, Project ID)
   - `cos-credentials` (API key, Instance ID, Bucket)

4. **Deploy Backend** (10 min)
   - Create application from GitHub
   - Configure build and runtime
   - Bind secrets

5. **Deploy Frontend** (10 min)
   - Create application from GitHub
   - Set backend URL as build argument
   - Deploy

6. **Configure & Test** (8 min)
   - Update CORS settings
   - Test integration
   - Verify COS storage

### 📚 Detailed Documentation

- **[Quick Start Guide](QUICK_START_DEPLOYMENT.md)** - Fast deployment in 40 minutes
- **[Comprehensive Guide](CODE_ENGINE_DEPLOYMENT_GUIDE.md)** - Detailed step-by-step instructions
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Complete verification checklist
- **[Deployment Summary](DEPLOYMENT_SUMMARY.md)** - Architecture and configuration overview

### 🔑 Key Configuration Files

- `backend/Dockerfile` - Production-ready backend container
- `frontend/Dockerfile` - Production-ready frontend container
- `.env.codeengine` - Environment variables template
- `backend/.dockerignore` - Optimized build context
- `frontend/.dockerignore` - Optimized build context

### 💡 Deployment Features

- ✅ **Stateless Architecture** - No database required
- ✅ **Auto-scaling** - Scale to zero when idle
- ✅ **Health Checks** - Built-in monitoring
- ✅ **Security** - Non-root containers, HTTPS by default
- ✅ **Cost-Optimized** - Pay only for what you use (~$0-70/month)

## 📚 API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

### Key Endpoints

- `POST /api/v1/validate` - Start model validation
- `GET /api/v1/validate/{id}` - Get validation status
- `GET /api/v1/validate/{id}/results` - Get validation results
- `GET /api/v1/validate/{id}/document` - Download validation report
- `POST /api/v1/mlops/register-model` - Register new model
- `GET /api/v1/governance/models` - List all models

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📖 Documentation

### Deployment Guides
- **[Quick Start Deployment](QUICK_START_DEPLOYMENT.md)** - Deploy in 40 minutes
- **[Comprehensive Deployment Guide](CODE_ENGINE_DEPLOYMENT_GUIDE.md)** - Detailed instructions
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Step-by-step verification
- **[Deployment Summary](DEPLOYMENT_SUMMARY.md)** - Architecture overview

### Technical Documentation
- [SR 11-7 Framework](docs/SR-11-7-FRAMEWORK.md) (if exists)
- [Supported Models](docs/SUPPORTED_MODELS.md) (if exists)
- [MCP Integration](docs/MCP_INTEGRATION.md) (if exists)

## 🔒 Security

- API key authentication for watsonx services
- Role-based access control (RBAC)
- Encrypted database connections
- Secure environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM watsonx.ai for AI capabilities
- IBM watsonx.governance for model lifecycle management
- FastAPI for the excellent web framework
- React and Vite for the frontend

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: your-email@example.com

## 🗺️ Roadmap

- [ ] Additional model types support
- [ ] Enhanced stress testing scenarios
- [ ] Integration with more data sources
- [ ] Advanced visualization dashboards
- [ ] Multi-language support

---

**Built with ❤️ using IBM watsonx and FastAPI**# bnk-ad-ce
