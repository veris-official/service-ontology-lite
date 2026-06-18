from __future__ import annotations

import service_ontology_lite as sol


def test_agent_os_helpers_are_exported_from_public_api():
    assert callable(sol.load_agent_os_registry)
    assert callable(sol.normalize_agent_os_registry)
    assert callable(sol.summarize_project_contexts)
    assert callable(sol.filter_project_contexts)

    for name in (
        "load_agent_os_registry",
        "normalize_agent_os_registry",
        "summarize_project_contexts",
        "filter_project_contexts",
    ):
        assert name in sol.__all__
