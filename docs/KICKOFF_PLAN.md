# Final Project Kickoff Plan

> Meeting-ready breakdown for a 5-person team (supports staggered availability)

---

## 1. Goal for Today's Meeting

- Agree on the architecture split (Domain / Services / API / Data / Quality).
- Assign 5 owners with clear handoffs.
- Set up GitHub repo, branching, PR rules, and a minimal CI pipeline.
- Define a "thin slice" milestone: load CSV → register → start ride → end ride.

---

## 2. What the System Must Support

- Async REST backend that manages stations, vehicles, users, rides, degradation, and treatment.
- Initial data loaded from `data/stations.csv` and `data/vehicles.csv`.
- **Rules:** eligibility, degradation, treatment, deterministic vehicle selection, nearest-station logic, fixed pricing, free ride when user reports degraded.
- **Engineering:** validation, tests, GitHub workflow/automation, and a short design document.

---

## 3. Architecture (So We Don't Block Each Other)

### 3.1 Domain Layer (pure logic, no I/O)

- Entities and enums (Vehicle hierarchy, Station/VehicleContainer, Ride, User, DegradedRepo, etc.).
- Local rules + invariants (eligibility, state transitions).

### 3.2 Services Layer (orchestration)

- `FleetManager` as the coordinator.
- `ActiveRidesRegistry` to track active rides.
- `BillingService` for pricing/payment (mock token).

### 3.3 Data Layer (loading + persistence)

- CSV loaders build initial objects.
- Persistence strategy so restart does not lose state (simple snapshot acceptable).

### 3.4 API Layer (async REST)

- Async endpoints call FleetManager and return structured responses.
- Validation via request/response schemas; consistent errors.

### 3.5 Quality Layer

- Unit + integration + API tests.
- CI runs lint + tests on every PR.

---

## 4. Work Sequencing (Designed for Staggered Availability)

### Phase 1: Start Now (does not depend on late joiners)

- Repo skeleton + CI green.
- Domain/services skeletons (interfaces decided early).
- Thin slice working end-to-end (minimal happy path).
- Basic unit tests for core rules.

### Phase 2: Next Week (build on stable core)

- Full API coverage + edge cases.
- Maintenance/treatment flows finalized.
- Persistence + restart behavior tested.
- More tests (integration + API).
- Finalize design document (PDF).

---

## 5. Team Split (5 People)

> Pick owners today. If someone is only available next week, assign them to roles 4–5.

### Role 1 — Repo / Process / CI Owner ⭐ (ASSIGNED: ME)

| | |
|---|---|
| **Start now** | ✅ YES (best first task) |

**Responsibilities:**
- Create repo structure (`src/`, `tests/`, `data/`, `docs/`).
- Branch strategy + PR template + required reviewers.
- CI pipeline: install deps → run lint/format check → run pytest.
- Add basic pre-commit hooks (optional).

**Deliverables:**
- CI green on main.
- Everyone can branch and open PRs safely.
- One "smoke test" in CI (e.g., `pytest -q`).

**Key interfaces / dependencies:**
- Coordinates with all owners for folder naming and test command.

---

### Role 2 — API Owner (Async REST)

| | |
|---|---|
| **Start now** | ✅ YES |

**Responsibilities:**
- Scaffold async API (recommended: FastAPI).
- Define request/response schemas, consistent error format.
- Implement endpoints for thin slice (register, start ride, end ride).
- Add 1–2 API smoke tests (TestClient / httpx).

**Deliverables:**
- Server runs locally.
- Thin slice endpoints wired to FleetManager.
- At least one API test passes in CI.

**Key interfaces / dependencies:**
- Depends on FleetManager service interface (`start_ride`/`end_ride`).

---

### Role 3 — Core Services Owner (FleetManager + ActiveRidesRegistry)

| | |
|---|---|
| **Start now** | ✅ YES |

**Responsibilities:**
- Implement orchestration rules: prevent multiple active rides per user, prevent using a vehicle already in ride.
- Deterministic vehicle selection among eligible vehicles (define rule clearly).
- Nearest-station selection + free-slot logic for docking.
- Unit tests for start/end ride behavior.

**Deliverables:**
- Thin slice logic works in-memory.
- Unit tests cover happy path + 2–3 key failures.

**Key interfaces / dependencies:**
- Coordinates with Domain owner for entities/enums; with API owner for signatures.

---

### Role 4 — Domain Model Owner (Vehicles/Stations/Ride/User)

| | |
|---|---|
| **Start now** | ⏳ CAN START LATER (next week is fine) |

**Responsibilities:**
- Implement domain entities cleanly with enums and invariants.
- Vehicle hierarchy + eligibility rules; state transitions (docked/in_ride/in_repo).
- Station/VehicleContainer add/remove operations and capacity checks.
- Unit tests for domain rules.

**Deliverables:**
- Domain layer complete and tested.
- Clear, stable class APIs used by Services.

**Key interfaces / dependencies:**
- Should align with the UML you already prepared.

---

### Role 5 — Data + Persistence Owner (CSV + restart behavior)

| | |
|---|---|
| **Start now** | ⏳ CAN START LATER (next week is fine) |

**Responsibilities:**
- Implement CSV loaders (`StationDataLoader`, `VehicleDataLoader`) and bootstrap wiring.
- Initial placement of vehicles into stations based on CSV mapping.
- Implement simple persistence (e.g., JSON snapshot) and reload on startup.
- Integration test: load → do one ride → save → reload → state consistent.

**Deliverables:**
- Loaders work with provided CSVs.
- Persistence save/load works; restart behavior tested.

**Key interfaces / dependencies:**
- Depends on stable domain model (Station/Vehicle constructors + ids).

---

## 6. Thin Slice Definition (First Milestone)

1. Load CSV → in-memory state created.
2. Register user (stores payment token).
3. Start ride (choose deterministic eligible vehicle, create active ride).
4. End ride (dock at nearest station with free slot, compute price, update counters).
5. Minimal validation + at least one test per layer (domain/service/api).

---

## 7. Jira / GitHub Workflow (Simple Rules)

- Create epics: `Setup/CI`, `Domain`, `Services`, `API`, `Data+Persistence`, `Testing`, `Docs`.
- Branch per ticket: `feature/PROJ-12-ride-start`.
- PR title starts with Jira ID: `PROJ-12: Implement ride start`.
- Require CI green + at least 1 reviewer to merge.

---

## 8. Meeting Agenda (Suggested 60 Minutes)

1. Confirm tooling: Python version, async API framework, pytest, linting.
2. Write the deterministic selection rule in one sentence (freeze it).
3. Assign owners for the 5 roles; note who starts now vs next week.
4. Create initial tickets (10–15) and assign.
5. Repo/CI owner creates skeleton; API/services owners create scaffolds.
6. Schedule next sync focused on the thin slice + blockers.

---

## Next Steps for Role 1 (Repo/CI Owner)

- [ ] Create GitHub repository
- [ ] Set up folder structure (`src/`, `tests/`, `data/`, `docs/`)
- [ ] Configure linting (ruff/flake8/black)
- [ ] Set up GitHub Actions CI pipeline
- [ ] Add PR template and branch protection rules
- [ ] Create initial smoke test
