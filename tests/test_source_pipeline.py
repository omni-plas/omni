import pytest

from omni.backend import BackendRegistry, GenericArtifactBackend
from omni.frontend import FrontendRegistry
from omni.source_pipeline import SourcePipelineError, compile_source


class DemoFrontend:
    language = "demo"

    def supports(self, language):
        return language == self.language

    def parse(self, source, *, filename="<source>"):
        return {
            "version": "1",
            "entity": {"kind": "application", "name": filename},
            "source": {"language": self.language, "version": "1"},
            "target": {"platform": "future-os", "capabilities": {"semantic-artifact": True}},
            "semantics": {"program": {"source": source}},
        }


def test_compile_source_connects_frontend_and_backend():
    frontends = FrontendRegistry((DemoFrontend(),))
    backends = BackendRegistry().register(GenericArtifactBackend())
    result = compile_source("main", language="demo", filename="demo.src", frontends=frontends, backends=backends)
    assert result.frontend_language == "demo"
    assert result.compilation.backend_name == "generic-semantic-artifact"
    assert result.compilation.artifact.target.platform == "future-os"


def test_compile_source_reports_unknown_language():
    with pytest.raises(SourcePipelineError, match="language"):
        compile_source("x", language="unknown", frontends=FrontendRegistry(), backends=BackendRegistry())
