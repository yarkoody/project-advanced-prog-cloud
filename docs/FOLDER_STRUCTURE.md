# Project Folder Structure

```
project/
|
|-- src/                          # Source code
|   |-- __init__.py
|   |-- domain/                   # Role 4: Entities and enums
|   |   |-- __init__.py
|   |   |-- entities.py           # Vehicle, Station, Ride, User
|   |   |-- enums.py              # VehicleType, VehicleStatus, VehicleLocation
|   |   |-- containers.py         # VehicleContainer, DegradedRepo
|   |
|   |-- services/                 # Role 3: Business logic
|   |   |-- __init__.py
|   |   |-- fleet_manager.py      # FleetManager orchestration
|   |   |-- rides_registry.py     # ActiveRidesRegistry
|   |   |-- billing.py            # BillingService
|   |
|   |-- api/                      # Role 2: REST endpoints
|   |   |-- __init__.py
|   |   |-- main.py               # FastAPI app
|   |   |-- routes.py             # Endpoint definitions
|   |   |-- schemas.py            # Request/response models
|   |
|   |-- data/                     # Role 5: Data loading and persistence
|       |-- __init__.py
|       |-- loaders.py            # StationDataLoader, VehicleDataLoader
|       |-- persistence.py        # Save/load state
|
|-- tests/                        # Test files
|   |-- __init__.py
|   |-- test_domain.py
|   |-- test_services.py
|   |-- test_api.py
|
|-- data/                         # CSV data files
|   |-- stations.csv
|   |-- vehicles.csv
|
|-- docs/                         # Documentation
|   |-- KICKOFF_PLAN.md
|   |-- WORKFLOW_SUMMARY.md
|   |-- FOLDER_STRUCTURE.md
|
|-- changelog/                    # Development log
|   |-- CHANGELOG.md
|
|-- requirements.txt              # Python dependencies
|-- pyproject.toml                # Project configuration (optional)
|-- .gitignore                    # Git ignore rules
|-- README.md                     # Project readme
```

## Layer Responsibilities

| Layer | Folder | Owner | Description |
|-------|--------|-------|-------------|
| Domain | `src/domain/` | Role 4 | Entities, enums, invariants |
| Services | `src/services/` | Role 3 | FleetManager, ActiveRidesRegistry, BillingService |
| API | `src/api/` | Role 2 | FastAPI async endpoints |
| Data | `src/data/` | Role 5 | CSV loaders, persistence |
| Tests | `tests/` | All | Unit, integration, API tests |
