from __future__ import annotations

from typing import Any

AUTH_VALUES = {"public", "required", "admin", "cron", "unknown"}
JOB_AUTH_VALUES = {"cron", "admin", "required"}
HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}

MANIFEST_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://veris.kr/schemas/service-ontology-lite.manifest.json",
    "title": "service-ontology-lite manifest",
    "type": "object",
    "additionalProperties": True,
    "properties": {
        "routes": {"type": "array"},
        "entities": {"type": "array"},
        "external_services": {"type": "array"},
        "jobs": {"type": "array"},
        "agent_os": {"type": "object"},
    },
}

_AGENT_OS_LIST_SECTIONS = {
    "agents",
    "surfaces",
    "tasks",
    "skills",
    "hooks",
    "loops",
    "plugins",
    "memories",
    "relations",
}


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]

    for index, item in enumerate(_items(manifest, "routes", errors)):
        prefix = f"routes[{index}]"
        _require_string(item, "path", prefix, errors)
        _require_string(item, "handler", prefix, errors)
        auth = item.get("auth", "unknown")
        if str(auth).lower() not in AUTH_VALUES:
            errors.append(f"{prefix}.auth must be one of {', '.join(sorted(AUTH_VALUES))}")
        path = item.get("path")
        if isinstance(path, str) and not path.startswith("/"):
            errors.append(f"{prefix}.path must start with /")
        methods = item.get("methods", [])
        if methods is not None:
            _validate_string_list(methods, f"{prefix}.methods", errors, allowed=HTTP_METHODS)
        _validate_string_list(item.get("entities", []), f"{prefix}.entities", errors)
        _validate_string_list(item.get("external_services", []), f"{prefix}.external_services", errors)

    for index, item in enumerate(_items(manifest, "entities", errors)):
        prefix = f"entities[{index}]"
        _require_string(item, "name", prefix, errors)
        _validate_string_list(item.get("fields", []), f"{prefix}.fields", errors)
        _validate_string_list(item.get("exposed_at", []), f"{prefix}.exposed_at", errors)

    for index, item in enumerate(_items(manifest, "external_services", errors)):
        prefix = f"external_services[{index}]"
        _require_string(item, "name", prefix, errors)
        _validate_string_list(item.get("env", []), f"{prefix}.env", errors)
        _validate_string_list(item.get("used_by", []), f"{prefix}.used_by", errors)

    for index, item in enumerate(_items(manifest, "jobs", errors)):
        prefix = f"jobs[{index}]"
        _require_string(item, "name", prefix, errors)
        _require_string(item, "handler", prefix, errors)
        auth = item.get("auth", "cron")
        if str(auth).lower() not in JOB_AUTH_VALUES:
            errors.append(f"{prefix}.auth must be cron/admin/required")

    _validate_agent_os(manifest.get("agent_os"), errors)

    return errors


def _validate_agent_os(value: Any, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        errors.append("agent_os must be an object")
        return
    for section in _AGENT_OS_LIST_SECTIONS:
        _validate_agent_os_list(value.get(section), f"agent_os.{section}", errors)

    for index, item in enumerate(_agent_os_items(value, "agents", errors)):
        _require_string(item, "id", f"agent_os.agents[{index}]", errors)
    for index, item in enumerate(_agent_os_items(value, "surfaces", errors)):
        prefix = f"agent_os.surfaces[{index}]"
        _require_string(item, "id", prefix, errors)
        _require_string(item, "type", prefix, errors)
        _require_string(item, "project_context_id", prefix, errors)
    for index, item in enumerate(_agent_os_items(value, "tasks", errors)):
        prefix = f"agent_os.tasks[{index}]"
        _require_string(item, "id", prefix, errors)
        _require_string(item, "project_context_id", prefix, errors)
        _require_string(item, "owner_agent", prefix, errors)
    for section in ("skills", "hooks", "loops", "plugins", "memories"):
        for index, item in enumerate(_agent_os_items(value, section, errors)):
            _require_string(item, "id", f"agent_os.{section}[{index}]", errors)
    for index, item in enumerate(_agent_os_items(value, "relations", errors)):
        prefix = f"agent_os.relations[{index}]"
        _require_string(item, "source", prefix, errors)
        _require_string(item, "relation", prefix, errors)
        _require_string(item, "target", prefix, errors)


def _validate_agent_os_list(value: Any, path: str, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            errors.append(f"{path}[{index}] must be an object")


def _agent_os_items(agent_os: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    return _items(agent_os, key, errors)


def _items(manifest: dict[str, Any], key: str, errors: list[str]) -> list[dict[str, Any]]:
    value = manifest.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        errors.append(f"{key} must be an array")
        return []
    valid: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if isinstance(item, dict):
            valid.append(item)
        else:
            errors.append(f"{key}[{index}] must be an object")
    return valid


def _require_string(item: dict[str, Any], key: str, prefix: str, errors: list[str]) -> None:
    value = item.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}.{key} is required")


def _validate_string_list(value: Any, path: str, errors: list[str], allowed: set[str] | None = None) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{path} must be an array")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{path}[{index}] must be a non-empty string")
            continue
        if allowed is not None and item.upper() not in allowed:
            errors.append(f"{path}[{index}] must be one of {', '.join(sorted(allowed))}")
