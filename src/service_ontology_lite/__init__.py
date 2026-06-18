"""service-ontology-lite package."""

from importlib.metadata import version

from .agent_os import (
    filter_project_contexts,
    load_agent_os_registry,
    normalize_agent_os_registry,
    summarize_project_contexts,
)
from .audit import audit_change_risk, audit_graph

__version__ = version("service-ontology-lite")
from .models import Finding, ServiceGraph
from .scanner import scan_project
from .schema import MANIFEST_SCHEMA, validate_manifest

__all__ = [
    "Finding",
    "MANIFEST_SCHEMA",
    "ServiceGraph",
    "__version__",
    "audit_change_risk",
    "audit_graph",
    "filter_project_contexts",
    "load_agent_os_registry",
    "normalize_agent_os_registry",
    "scan_project",
    "summarize_project_contexts",
    "validate_manifest",
]
