# Development Changelog

## Entry 007 - Project Configuration
Date: 2026-02-08 20:27
Author: Ariel

Added pyproject.toml with pytest, ruff, and black configuration.

---

## Entry 006 - PR Template
Date: 2026-02-08 20:21
Author: Ariel

Added pull request template for consistent PR reviews.

---

## Entry 005 - Gitignore
Date: 2026-02-08 20:21
Author: Ariel

Added .gitignore to exclude Python cache, venv, IDE files.

---

## Entry 004 - CI Pipeline
Date: 2026-02-08 20:10
Author: Ariel

Set up GitHub Actions CI pipeline:
- Created `.github/workflows/ci.yml` to run tests on every PR
- Added `tests/test_smoke.py` as initial test

---

## Entry 003 - Folder Structure
Date: 2026-02-08 19:57
Author: Ariel

Created project folder hierarchy:
- `src/` with subdirectories for each layer (domain, services, api, data)
- `tests/` for test files
- `data/` for CSV files
- Added `docs/FOLDER_STRUCTURE.md` with visual overview

---

## Entry 002 - Branch Creation
Date: 2026-02-08 19:36
Author: Ariel

Created development branches for all team members:
- `feature/role1-repo-ci` - Repo/Process/CI Owner (Ariel)
- `feature/role2-api` - API Owner
- `feature/role3-services` - Core Services Owner
- `feature/role4-domain` - Domain Model Owner
- `feature/role5-data-persistence` - Data + Persistence Owner

Branch strategy: main is protected, PRs require CI green + 1 reviewer.

---

## Entry 001 - Project Initialization
Date: 2026-02-08 19:22
Author: Ariel

Initial project setup:
- Initialized Git repository
- Created requirements.txt with dependencies (FastAPI, pytest, etc.)
- Created docs/ folder with kickoff plan and workflow summary
