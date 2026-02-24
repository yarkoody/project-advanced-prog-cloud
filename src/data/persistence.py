"""
Persistence layer — Role 5 (Data + Persistence).

SnapshotManager handles saving and loading the full fleet state
to/from a single JSON file so the server can restart without
losing active rides or vehicle positions.

Snapshot schema (all plain JSON-serialisable types):
{
  "stations": {<station_id>: {...station fields...}, ...},
  "vehicles": {<vehicle_id>: {...vehicle fields...}, ...},
  "users":    {<user_id>:    {...user fields...},    ...},
  "active_rides": {<ride_id>: {...ride fields...},   ...},
  "degraded_repo": [vehicle_id, ...]
}

NOTE: The methods that reconstruct domain objects from the snapshot
are scaffolded with TODO comments — wire in real constructors once
Role 4 (domain layer) is merged.
"""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# JSON helpers  (enums / dates need special treatment)
# ---------------------------------------------------------------------------

class _FleetEncoder(json.JSONEncoder):
    """Serialise date / datetime objects to ISO strings."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        # Enums: use .value so the JSON is human-readable
        if hasattr(obj, "value"):
            return obj.value
        return super().default(obj)


def _as_dict(obj: Any) -> dict:
    """Convert a domain object to a plain dict for serialisation.

    Once Role 4 merges, replace the simple __dict__ fallback with
    explicit field extraction per class if needed.
    """
    if isinstance(obj, dict):
        return obj
    return vars(obj)


# ---------------------------------------------------------------------------
# SnapshotManager
# ---------------------------------------------------------------------------

class SnapshotManager:
    """Save and load fleet state as a JSON snapshot file."""

    DEFAULT_PATH = Path("data") / "snapshot.json"

    def __init__(self, snapshot_path: str | Path | None = None) -> None:
        self.snapshot_path = Path(snapshot_path or self.DEFAULT_PATH)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(self, fleet_manager: Any) -> None:
        """Serialise the full fleet state and write it to disk.

        Args:
            fleet_manager: A FleetManager instance (or a plain dict
                           matching the snapshot schema for testing).
        """
        snapshot = self._build_snapshot(fleet_manager)
        self.snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        with self.snapshot_path.open("w", encoding="utf-8") as fh:
            json.dump(snapshot, fh, cls=_FleetEncoder, indent=2)

    def load(self) -> dict | None:
        """Load and parse the snapshot file.

        Returns:
            A dict with keys: stations, vehicles, users,
            active_rides, degraded_repo.
            Returns None if no snapshot file exists (fresh start).
        """
        if not self.snapshot_path.exists():
            return None
        with self.snapshot_path.open(encoding="utf-8") as fh:
            raw = json.load(fh)
        return self._restore_snapshot(raw)

    def exists(self) -> bool:
        """Return True if a snapshot file is present on disk."""
        return self.snapshot_path.exists()

    def delete(self) -> None:
        """Remove the snapshot file (useful in tests / hard reset)."""
        if self.snapshot_path.exists():
            self.snapshot_path.unlink()

    # ------------------------------------------------------------------
    # Internal: build snapshot dict from fleet_manager
    # ------------------------------------------------------------------

    def _build_snapshot(self, fleet_manager: Any) -> dict:
        """Extract plain-dict representation of the full fleet state."""

        # Support both a real FleetManager and a plain dict (for tests)
        if isinstance(fleet_manager, dict):
            return fleet_manager

        # TODO: once FleetManager (Role 3) is stable, extract fields
        #       explicitly here.  For now we introspect __dict__ so
        #       the persistence layer can be unit-tested with stubs.

        stations_raw = getattr(fleet_manager, "stations", {})
        vehicles_raw = getattr(fleet_manager, "vehicles", {})
        users_raw    = getattr(fleet_manager, "users", {})

        # ActiveRidesRegistry exposes active_ride_ids() + get()
        active_rides_raw: dict = {}
        registry = getattr(fleet_manager, "active_rides", None)
        if registry is not None:
            for rid in registry.active_ride_ids():
                ride = registry.get(rid)
                active_rides_raw[str(rid)] = _as_dict(ride)

        degraded_repo = getattr(fleet_manager, "degraded_repo", None)
        degraded_ids: list[str] = []
        if degraded_repo is not None:
            degraded_ids = list(degraded_repo.list_vehicle_ids())

        return {
            "stations": {
                str(k): _as_dict(v) for k, v in stations_raw.items()
            },
            "vehicles": {
                str(k): _as_dict(v) for k, v in vehicles_raw.items()
            },
            "users": {
                str(k): _as_dict(v) for k, v in users_raw.items()
            },
            "active_rides": active_rides_raw,
            "degraded_repo": degraded_ids,
        }

    # ------------------------------------------------------------------
    # Internal: restore snapshot dict → typed objects
    # ------------------------------------------------------------------

    def _restore_snapshot(self, raw: dict) -> dict:
        """Parse raw JSON back into typed Python objects.

        Currently returns plain dicts with dates parsed back to
        date/datetime objects.  Once Role 4 is merged, replace the
        dict returns with real domain constructors.
        """
        return {
            "stations":     self._restore_stations(raw.get("stations", {})),
            "vehicles":     self._restore_vehicles(raw.get("vehicles", {})),
            "users":        self._restore_users(raw.get("users", {})),
            "active_rides": self._restore_rides(raw.get("active_rides", {})),
            "degraded_repo": raw.get("degraded_repo", []),
        }

    # -- per-collection restorers ----------------------------------------

    def _restore_stations(self, raw: dict) -> dict[int, dict]:
        result = {}
        for k, v in raw.items():
            station_id = int(k)
            parsed = {**v, "station_id": station_id}
            # TODO: return Station(**parsed) once domain is available
            result[station_id] = parsed
        return result

    def _restore_vehicles(self, raw: dict) -> dict[str, dict]:
        result = {}
        for k, v in raw.items():
            parsed = {**v}
            # Parse date strings back to date objects
            if isinstance(parsed.get("last_treated_date"), str):
                parsed["last_treated_date"] = date.fromisoformat(
                    parsed["last_treated_date"]
                )
            # TODO: instantiate correct Vehicle subclass once domain is available
            result[k] = parsed
        return result

    def _restore_users(self, raw: dict) -> dict[int, dict]:
        return {int(k): {**v} for k, v in raw.items()}
        # TODO: return {int(k): User(**v) for k, v in raw.items()}

    def _restore_rides(self, raw: dict) -> dict[int, dict]:
        result = {}
        for k, v in raw.items():
            parsed = {**v}
            for field in ("start_time", "end_time"):
                if isinstance(parsed.get(field), str):
                    parsed[field] = datetime.fromisoformat(parsed[field])
            result[int(k)] = parsed
            # TODO: return Ride(**parsed) once domain is available
        return result
