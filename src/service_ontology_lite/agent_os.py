from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_AGENT_OS_SECTIONS = ("agents", "surfaces", "tasks", "skills", "hooks", "loops", "plugins", "memories", "relations")


def load_agent_os_registry(root: str | Path) -> dict[str, Any]:
    """Load normalized Agent OS registry data from a service-ontology manifest."""
    project_root = Path(root).resolve()
    manifest = _load_manifest(project_root)
    registry = manifest.get("agent_os", {}) if isinstance(manifest, dict) else {}
    if not isinstance(registry, dict):
        registry = {}

    normalized: dict[str, Any] = {section: _list_of_dicts(registry.get(section)) for section in _AGENT_OS_SECTIONS}
    normalized["counts"] = {section: len(normalized[section]) for section in _AGENT_OS_SECTIONS}
    return normalized


def normalize_agent_os_registry(manifest: dict[str, Any]) -> dict[str, Any]:
    registry = manifest.get("agent_os", {}) if isinstance(manifest, dict) else {}
    if not isinstance(registry, dict):
        registry = {}
    normalized: dict[str, Any] = {section: _list_of_dicts(registry.get(section)) for section in _AGENT_OS_SECTIONS}
    normalized["counts"] = {section: len(normalized[section]) for section in _AGENT_OS_SECTIONS}
    return normalized


def _load_manifest(root: Path) -> dict[str, Any]:
    path = root / "service-ontology.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]
