from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_AGENT_OS_SECTIONS = (
    "projects",
    "agents",
    "surfaces",
    "tasks",
    "skills",
    "hooks",
    "loops",
    "plugins",
    "artifacts",
    "memories",
    "relations",
)
_CONTEXT_SECTIONS = ("surfaces", "tasks", "artifacts", "memories")
_UNDECLARED_CONTEXT_WARNING = "project_context_id is referenced but not declared in agent_os.projects"


def load_agent_os_registry(root: str | Path) -> dict[str, Any]:
    """Load normalized Agent OS registry data from a service-ontology manifest."""
    project_root = Path(root).resolve()
    manifest = _load_manifest(project_root)
    registry = manifest.get("agent_os", {}) if isinstance(manifest, dict) else {}
    if not isinstance(registry, dict):
        registry = {}

    normalized: dict[str, Any] = {section: _list_of_dicts(registry.get(section)) for section in _AGENT_OS_SECTIONS}
    normalized["counts"] = {section: len(normalized[section]) for section in _AGENT_OS_SECTIONS}
    normalized["project_contexts"] = summarize_project_contexts(normalized)
    return normalized


def normalize_agent_os_registry(manifest: dict[str, Any]) -> dict[str, Any]:
    registry = manifest.get("agent_os", {}) if isinstance(manifest, dict) else {}
    if not isinstance(registry, dict):
        registry = {}
    normalized: dict[str, Any] = {section: _list_of_dicts(registry.get(section)) for section in _AGENT_OS_SECTIONS}
    normalized["counts"] = {section: len(normalized[section]) for section in _AGENT_OS_SECTIONS}
    normalized["project_contexts"] = summarize_project_contexts(normalized)
    return normalized


def summarize_project_contexts(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Group Agent OS surfaces, tasks, artifacts, memories, and relation edges by project_context_id."""
    projects = _list_of_dicts(registry.get("projects"))
    declared_project_ids = sorted({item["id"] for item in projects if isinstance(item.get("id"), str) and item["id"]})
    summary: dict[str, dict[str, Any]] = {
        project_id: _empty_project_context(declared=True) for project_id in declared_project_ids
    }

    entity_to_context: dict[str, str] = {}
    owner_agents_by_context: dict[str, set[str]] = {project_id: set() for project_id in declared_project_ids}

    for section in _CONTEXT_SECTIONS:
        for item in _list_of_dicts(registry.get(section)):
            project_context_id = item.get("project_context_id")
            if not isinstance(project_context_id, str) or not project_context_id:
                continue
            context = summary.setdefault(project_context_id, _empty_project_context(declared=False))
            context[section].append(item)
            item_id = item.get("id")
            if isinstance(item_id, str) and item_id:
                entity_to_context[item_id] = project_context_id
            if section == "tasks":
                owner_agent = item.get("owner_agent")
                if isinstance(owner_agent, str) and owner_agent:
                    owner_agents_by_context.setdefault(project_context_id, set()).add(owner_agent)

    for relation in _list_of_dicts(registry.get("relations")):
        context_ids = {
            entity_to_context[value]
            for value in (relation.get("source"), relation.get("target"))
            if isinstance(value, str) and value in entity_to_context
        }
        for context_id in context_ids:
            summary.setdefault(context_id, _empty_project_context(declared=False))["relations"].append(relation)

    for context_id, context in summary.items():
        context["counts"] = {section: len(context[section]) for section in (*_CONTEXT_SECTIONS, "relations")}
        context["agents"] = sorted(owner_agents_by_context.get(context_id, set()))
        context["warnings"] = [] if context["declared"] else [_UNDECLARED_CONTEXT_WARNING]

    return dict(sorted(summary.items()))


def _empty_project_context(*, declared: bool) -> dict[str, Any]:
    return {
        "declared": declared,
        "surfaces": [],
        "tasks": [],
        "artifacts": [],
        "memories": [],
        "relations": [],
        "counts": {},
        "agents": [],
        "warnings": [],
    }


def _load_manifest(root: Path) -> dict[str, Any]:
    path = root / "service-ontology.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]
