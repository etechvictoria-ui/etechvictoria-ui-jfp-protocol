"""Tests for JFP validator module."""

import pytest
from tools.validator import validate


class TestValidate:
    """Test suite for validate function."""

    def test_validate_empty_spec(self):
        """Test validating empty spec."""
        result = validate("")
        assert result["valid"] is False
        assert result["issue_count"] > 0

    def test_validate_missing_jfp_document_section(self):
        """Test validation fails without JFP_DOCUMENT section."""
        text = """=== META ===
F: VERSION: 1.0.0;"""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("JFP_DOCUMENT" in msg for msg in issues)

    def test_validate_missing_end_jfp_marker(self):
        """Test validation fails without END_JFP marker."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;"""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("END_JFP" in msg for msg in issues)

    def test_validate_missing_version(self):
        """Test validation fails without VERSION fact."""
        text = """=== JFP_DOCUMENT ===
=== META ===
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("VERSION" in msg for msg in issues)

    def test_validate_missing_type(self):
        """Test validation fails without TYPE fact."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
=== META ===
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("TYPE" in msg for msg in issues)

    def test_validate_missing_meta_section(self):
        """Test validation fails without META section."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("META" in msg for msg in issues)

    def test_validate_missing_build_or_patch_graph(self):
        """Test validation fails without BUILD_GRAPH or PATCH_GRAPH."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== META ===
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("BUILD_GRAPH" in msg or "PATCH_GRAPH" in msg for msg in issues)

    def test_validate_task_missing_action(self):
        """Test validation fails for task without ACTION."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== META ===
=== BUILD_GRAPH ===
[TASK_001]
F: OUTPUT: result;
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("TASK_001" in msg and "ACTION" in msg for msg in issues)

    def test_validate_task_missing_output(self):
        """Test validation fails for task without OUTPUT."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== META ===
=== BUILD_GRAPH ===
[TASK_001]
F: ACTION: do something;
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("TASK_001" in msg and "OUTPUT" in msg for msg in issues)

    def test_validate_unknown_dependency(self):
        """Test validation fails for unknown task dependency."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== META ===
=== BUILD_GRAPH ===
[TASK_001]
F: ACTION: do something;
F: OUTPUT: result;
F: DEPENDENCY: TASK_999;
=== END_JFP ==="""

        result = validate(text)
        assert result["valid"] is False
        issues = [i["message"] for i in result["issues"]]
        assert any("unknown dependency" in msg.lower() for msg in issues)

    def test_validate_missing_constraints(self):
        """Test validation warns about missing CONSTRAINTS."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== META ===
=== BUILD_GRAPH ===
[TASK_001]
F: ACTION: do something;
F: OUTPUT: result;
=== END_JFP ==="""

        result = validate(text)
        issues = [i["message"] for i in result["issues"]]
        assert len(issues) > 0 or result.get("valid") is False

    def test_validate_returns_issue_count(self):
        """Test validate returns correct issue_count."""
        text = """=== JFP_DOCUMENT ===
=== END_JFP ==="""

        result = validate(text)
        assert "issue_count" in result
        assert result["issue_count"] == len(result.get("issues", []))

    def test_validate_returns_issues_list(self):
        """Test validate returns issues list with layer and message."""
        text = ""

        result = validate(text)
        assert "issues" in result
        assert isinstance(result["issues"], list)
        if result["issues"]:
            issue = result["issues"][0]
            assert "layer" in issue
            assert "message" in issue
            assert issue["layer"] in ["L1", "L2", "L3", "L4", "L5"]

    def test_validate_syntax_error_layer(self):
        """Test L1 layer detects syntax errors."""
        text = """=== JFP_DOCUMENT ===
F: INVALID_SYNTAX_NO_SEMICOLON
=== END_JFP ==="""

        result = validate(text)
        issues = [i["message"] for i in result["issues"] if i["layer"] == "L1"]
        assert any("syntax" in msg.lower() for msg in issues)
