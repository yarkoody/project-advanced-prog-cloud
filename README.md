# Vehicle Sharing API — Advanced Programming Final Project + Cloud Deployment Extension

A backend system for a vehicle-sharing service, implementing ride lifecycle management including user registration, ride handling, vehicle allocation, and maintenance flows.

This repository includes the cloud deployment extension: Docker-based packaging, GitHub Actions CI/CD, Google Artifact Registry publishing, and Cloud Run deployment.

## Tech Stack
- Python 3.12
- FastAPI
- Pytest
- Docker
- GitHub Actions (CI/CD)
- Google Artifact Registry
- Google Cloud Run
- Jira for planning and traceability

## Repository Structure
- src/        → application code
- tests/      → test suite
- data/       → input CSV files (stations, vehicles)
- docs/       → documentation
- .github/    → CI configuration

## Local Setup

Run the project locally with Python 3.12:

1. Create and activate a virtual environment:
    python3.12 -m venv .venv
    source .venv/bin/activate

2. Install dependencies:
    python -m pip install -r requirements.txt

3. Run tests:
    python -m pytest -q

4. Start the API server:
    uvicorn src.main:app --reload

5. Open the API in your browser:
    http://127.0.0.1:8000/docs

## API Usage

After starting the server, the main endpoints are available through the API documentation page (`/docs`).

Main endpoints:
- POST /register
- POST /ride/start
- POST /ride/end
- POST /vehicle/treat
- POST /vehicle/report-degraded
- GET /stations/nearest
- GET /rides/active-users

### Example Requests

Register a user:
POST /register
{
  "payment_token": "token_123"
}

Start a ride:
POST /ride/start
{
  "user_id": 1,
  "lat": 32.0853,
  "lon": 34.7818
}

## Notes

- Initial system data is loaded from the CSV files in the `data/` directory.
- Runtime state is persisted in `state.json`.

## Supported Features

The system supports the following core functionalities:

- User registration with unique payment token
- Starting a ride with deterministic vehicle selection
- Ending a ride with automatic station selection and billing
- Reporting a vehicle as degraded during a ride
- Vehicle treatment and reintegration into stations
- Retrieval of nearest station based on location
- Retrieval of currently active users

The API uses structured error handling with appropriate HTTP status codes (400, 404, 409).

## Architecture

The system follows a layered architecture:

- API Layer  
  Handles HTTP requests, validation, and response mapping using FastAPI.

- Service Layer  
  Contains business logic and orchestrates workflows such as ride start/end, pricing, and vehicle treatment.

- Domain Layer  
  Defines core entities (Vehicle, Ride, User, Station) and enforces invariants.

- Data Layer  
  Responsible for CSV loading and state persistence (state.json).


## Workflow

Branch per Jira ticket:
    feature/KAN-XX-description

PR to main requires:
- 1 approval
- CI passing
- branch up to date

Definition of IN REVIEW:
- PR opened
- CI running or green

Definition of DONE:
- PR merged to main
- CI green on main

## Cloud Extension Workflow

The cloud extension is implemented as a multi-stage CI/CD flow:

1. Validate image build
  - Workflow: `.github/workflows/docker-validate.yml`
  - Purpose: verify Docker image build succeeds

2. Publish image to Artifact Registry
  - Workflow: `.github/workflows/image-publish.yml`
  - Purpose: build and push image to GCP Artifact Registry

3. Deploy image to Cloud Run
  - Workflow: `.github/workflows/cloudrun-deploy.yml`
  - Purpose: deploy a chosen image tag to Cloud Run

WIF-based alternatives for cloud auth are also provided:
- `.github/workflows/eden-wif-gcp-deployment.yml`
- `.github/workflows/eden-wif-deploy-cloudrun.yml`

## Deployment Notes

- Region is set to `us-central1` to stay aligned with course cost guidelines.
- Sensitive values are passed via GitHub Secrets.
- Deployment is done to a public Cloud Run service endpoint.
- API behavior in cloud is expected to match local behavior.