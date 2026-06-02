"""Tests for JFP parser module."""

import pytest
from tools.parser import parse_jfp, Fact


class TestParseJFP:
    """Test suite for parse_jfp function."""

    def test_parse_empty_content(self):
        """Test parsing empty JFP content."""
        result = parse_jfp("")
        assert result["facts"] == []
        assert result["sections"] == {}
        assert result["blocks"] == {}

    def test_parse_jfp_document_section(self):
        """Test parsing basic JFP_DOCUMENT section."""
        text = """=== JFP_DOCUMENT ===
F: TITLE: Test Spec;
F: VERSION: 1.0.0;"""

        result = parse_jfp(text)
        assert "JFP_DOCUMENT" in result["sections"]
        assert len(result["facts"]) == 2
        assert result["facts"][0]["key"] == "TITLE"
        assert result["facts"][0]["value"] == "Test Spec"

    def test_parse_multiple_sections(self):
        """Test parsing multiple sections."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
=== META ===
F: TYPE: BUILD;"""

        result = parse_jfp(text)
        assert "JFP_DOCUMENT" in result["sections"]
        assert "META" in result["sections"]
        assert len(result["sections"]) == 2

    def test_parse_fact_with_syntax_error(self):
        """Test parsing fact with missing semicolon."""
        text = "F: KEY: value"  # Missing semicolon
        result = parse_jfp(text)
        assert result["facts"][0]["key"] == "__SYNTAX_ERROR__"

    def test_parse_fact_with_malformed_key_value(self):
        """Test parsing fact with malformed key-value pair."""
        text = "F: ONLYKEY;"
        result = parse_jfp(text)
        assert result["facts"][0]["key"] == "__SYNTAX_ERROR__"

    def test_parse_block_definition(self):
        """Test parsing block definitions."""
        text = """=== BUILD_GRAPH ===
[TASK_001]
F: ACTION: create file;
F: OUTPUT: file.txt;"""

        result = parse_jfp(text)
        assert "TASK_001" in result["blocks"]
        assert result["blocks"]["TASK_001"]["section"] == "BUILD_GRAPH"
        assert len(result["blocks"]["TASK_001"]["facts"]) == 2

    def test_parse_line_numbers(self):
        """Test that line numbers are correctly tracked."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;"""

        result = parse_jfp(text)
        assert result["facts"][0]["line"] == 2
        assert result["facts"][1]["line"] == 3

    def test_parse_ignores_blank_lines(self):
        """Test that blank lines are ignored."""
        text = """=== JFP_DOCUMENT ===

F: VERSION: 1.0.0;

F: TYPE: BUILD;"""

        result = parse_jfp(text)
        assert len(result["facts"]) == 2

    def test_parse_fact_object(self):
        """Test Fact dataclass."""
        fact = Fact(
            key="TEST_KEY",
            value="test_value",
            line=1,
            section="TEST_SECTION",
            block="TEST_BLOCK"
        )
        assert fact.key == "TEST_KEY"
        assert fact.value == "test_value"
        assert fact.line == 1
        assert fact.section == "TEST_SECTION"
        assert fact.block == "TEST_BLOCK"

    def test_parse_complex_spec(self):
        """Test parsing a complete minimal spec."""
        text = """=== JFP_DOCUMENT ===
F: VERSION: 1.0.0;
F: TYPE: BUILD;
=== META ===
[TASK_001]
F: ACTION: initialize;
F: OUTPUT: initialized;
=== BUILD_GRAPH ===
[TASK_002]
F: ACTION: execute;
F: OUTPUT: result;
F: DEPENDENCY: TASK_001;
=== END_JFP ==="""

        result = parse_jfp(text)
        assert "JFP_DOCUMENT" in result["sections"]
        assert "META" in result["sections"]
        assert "BUILD_GRAPH" in result["sections"]
        assert "END_JFP" in result["sections"]
        assert len(result["blocks"]) == 2
        assert len(result["facts"]) >= 7
