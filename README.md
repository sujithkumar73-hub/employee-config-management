# Employee Management System with Multi-Environment Configuration Management

A production-style internship project demonstrating multi-environment configuration management using Flask, Docker, Kubernetes, and GitHub Actions.

## 📌 Project Overview

This Employee Management System includes:
- Secure JWT authentication
- Employee CRUD operations
- Environment-specific behavior for DEV, QA, UAT, PROD
- Externalized configurations using Kubernetes ConfigMaps and Secrets
- Docker containerization for frontend and backend
- Kubernetes deployments with namespaces and health probes
- CI/CD automation via GitHub Actions
- SQLite database per environment

## 🧩 Problem Statement

Enterprises struggle with configuration drift when deploying across development, QA, UAT, and production. This project resolves that by externalizing environment settings, enforcing secure secret handling, and enabling automated deployment pipelines.

## 📁 Folder Structure

```
employee-config-management/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── run.py
│   ├── database/db.py
│   ├── controllers/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── tests/
│
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── employees.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
│
├── k8s/
│   ├── dev/
│   ├── qa/
│   ├── uat/
│   └── prod/
│
├── .github/workflows/deploy.yml
├── docker-compose.yml
└── README.md
```

## 🌐 Environments Supported

- `DEV` — Development environment with verbose logging and seeded sample employees.
- `QA` — Quality assurance testing environment with additional validation.
- `UAT` — User acceptance testing environment with stable dataset and near-production behavior.
- `PROD` — Production-ready environment with minimal logs and secure settings.

Each environment includes:
- Separate Kubernetes namespace
- Separate ConfigMap
- Separate Secret
- Separate Deployment
- Separate Service
- Separate environment variables

## 🛠️ Tech Stack

- Backend: Python Flask
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Authentication: Flask-JWT-Extended
- Frontend: HTML, CSS, JavaScript
- DevOps: Docker, Docker Compose, Kubernetes, GitHub Actions
- Config management: Kubernetes ConfigMap + Secret

## 🚀 Setup Instructions

### 1. Clone the repository (skip if you already have the project locally)

```bash
git clone <repository-url>
cd employee-config-management
```

If the code is already available in your local workspace, you can skip this step and continue with the backend setup.

### 2. Backend setup

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
python -m backend.run
```

If you prefer direct script execution, run from the project root as:

```bash
python backend/run.py
```

If `Flask==2.3.6` fails to install, the project uses `Flask==2.3.3` which is supported on PyPI.

### 3. Frontend setup

**Option A: Direct file access (requires backend running at `http://localhost:5000`)**

1. Open `frontend/index.html` directly in your browser
2. The frontend will automatically detect and connect to the backend at `http://localhost:5000`

**Option B: Serve via local web server (recommended)**

Install a simple HTTP server and run:

```bash
# Using Python 3
python -m http.server 8000
```

Then open `http://localhost:8000/frontend/index.html` in your browser.

**Option C: Docker Compose (full-stack local development)**

Use Docker Compose for a complete environment:

```bash
docker-compose up --build
```

This starts both backend and frontend:
- Backend: `http://localhost:5000`
- Frontend: `http://localhost:3000`

### 4. Run with Docker Compose

```bash
docker-compose up --build
```

- Backend will be available at `http://localhost:5000`
- Frontend will be available at `http://localhost:3000`

### 5. Default login credentials

- Username: `admin`
- Password: `ChangeMe123!`

## 🧪 API Documentation

### Authentication
- `POST /api/auth/login`
  - Body: `{ "username": "admin", "password": "ChangeMe123!" }`

### Employee CRUD
- `GET /api/employees/`
- `POST /api/employees/`
- `GET /api/employees/{id}`
- `PUT /api/employees/{id}`
- `DELETE /api/employees/{id}`

### Health and config
- `GET /api/health`
- `GET /api/status`
- `GET /api/config-check`

## 🐳 Docker Commands

Build containers manually:

```bash
docker build -f docker/backend.Dockerfile -t ems-backend:latest .
docker build -f docker/frontend.Dockerfile -t ems-frontend:latest .
```

Run compose:

```bash
docker-compose up --build
```

## ☸️ Kubernetes Deployment

Each environment contains manifests in:
- `k8s/dev/`
- `k8s/qa/`
- `k8s/uat/`
- `k8s/prod/`

### Apply an environment

```bash
kubectl apply -f k8s/dev/
```

### Validate manifests

```bash
kubectl apply --dry-run=client -f k8s/dev/
```

### Notes
- Frontend uses `Ingress` routing for `/` to the frontend service and `/api` to the backend service.
- Backend service exposes health probes and readiness checks.
- `ConfigMap` stores non-sensitive environment configuration.
- `Secret` stores sensitive values like JWT keys and admin password.

## ⚙️ GitHub Actions Workflow

The workflow in `.github/workflows/deploy.yml` includes:
1. Checkout source code
2. Setup Python environment
3. Install dependencies
4. Run tests
5. Build Docker images for backend and frontend
6. Push images to GitHub Container Registry
7. Validate Kubernetes manifests
8. Deploy to the correct environment based on branch

### Branch mapping
- `develop` → `DEV`
- `qa` → `QA`
- `uat` → `UAT`
- `main` → `PROD`

## 🔐 Security and Config Management

- JWT-based authentication
- Password hashing for admin account
- CORS enabled
- Input validation for employee payloads
- Environment variables for secrets and runtime settings
- Kubernetes `ConfigMap` for `APP_MODE`, `FLASK_ENV`, `API_URL`, `LOG_LEVEL`, `DATABASE_URL`
- Kubernetes `Secret` for `JWT_SECRET_KEY`, `ADMIN_PASSWORD`, `API_KEYS`

## 📚 Future Enhancements

- Add role-based access control with separate user profiles
- Add audit logs and user activity tracking
- Replace SQLite with PostgreSQL for production readiness
- Add automated UI tests and end-to-end workflows
- Add a real deployment dashboard for environment health

## 🧭 Notes for Review

- The project is built for resume-level DevOps and full-stack demonstrations.
- It exposes clean environment separation and config management.
- The architecture supports easy extension to more environments or cloud deployments.
