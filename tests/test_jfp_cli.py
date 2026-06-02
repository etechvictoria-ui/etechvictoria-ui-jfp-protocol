"""Tests for JFP CLI module."""

import json
import tempfile
from pathlib import Path

import pytest
from tools.jfp_cli import command_parse, command_validate, command_inspect, read_spec, build_parser, main
import argparse


class TestReadSpec:
    """Test suite for read_spec function."""

    def test_read_spec_valid_file(self):
        """Test reading a valid JFP spec file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.flush()
            
            try:
                content = read_spec(f.name)
                assert "JFP_DOCUMENT" in content
                assert "VERSION" in content
            finally:
                Path(f.name).unlink()

    def test_read_spec_file_not_found(self):
        """Test reading non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_spec("/nonexistent/path/to/spec.jfp")

    def test_read_spec_is_directory(self):
        """Test reading a directory raises IsADirectoryError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(IsADirectoryError):
                read_spec(tmpdir)


class TestBuildParser:
    """Test suite for build_parser function."""

    def test_build_parser_returns_argument_parser(self):
        """Test build_parser returns ArgumentParser instance."""
        parser = build_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_build_parser_has_parse_command(self):
        """Test parser has parse subcommand."""
        parser = build_parser()
        args = parser.parse_args(['parse', 'test.jfp'])
        assert args.command == 'parse'
        assert args.spec == 'test.jfp'

    def test_build_parser_has_validate_command(self):
        """Test parser has validate subcommand."""
        parser = build_parser()
        args = parser.parse_args(['validate', 'test.jfp'])
        assert args.command == 'validate'
        assert args.spec == 'test.jfp'

    def test_build_parser_has_inspect_command(self):
        """Test parser has inspect subcommand."""
        parser = build_parser()
        args = parser.parse_args(['inspect', 'test.jfp'])
        assert args.command == 'inspect'
        assert args.spec == 'test.jfp'


class TestCommandParse:
    """Test suite for command_parse function."""

    def test_command_parse_valid_spec(self, capsys):
        """Test parse command with valid spec."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                args = argparse.Namespace(spec=f.name)
                result = command_parse(args)
                
                assert result == 0
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert "sections" in output
                assert "JFP_DOCUMENT" in output["sections"]
            finally:
                Path(f.name).unlink()


class TestCommandValidate:
    """Test suite for command_validate function."""

    def test_command_validate_valid_spec(self, capsys):
        """Test validate command with valid spec."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("F: TYPE: BUILD;\n")
            f.write("=== META ===\n")
            f.write("=== BUILD_GRAPH ===\n")
            f.write("[TASK_001]\n")
            f.write("F: ACTION: test;\n")
            f.write("F: OUTPUT: result;\n")
            f.write("=== CONSTRAINTS ===\n")
            f.write("F: RULE: no changes;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                args = argparse.Namespace(spec=f.name)
                result = command_validate(args)
                
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert "valid" in output
            finally:
                Path(f.name).unlink()

    def test_command_validate_invalid_spec(self, capsys):
        """Test validate command with invalid spec."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("")
            f.flush()
            
            try:
                args = argparse.Namespace(spec=f.name)
                result = command_validate(args)
                
                assert result == 1
            finally:
                Path(f.name).unlink()


class TestCommandInspect:
    """Test suite for command_inspect function."""

    def test_command_inspect_valid_spec(self, capsys):
        """Test inspect command with valid spec."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("F: TYPE: BUILD;\n")
            f.write("=== META ===\n")
            f.write("=== BUILD_GRAPH ===\n")
            f.write("[TASK_001]\n")
            f.write("F: ACTION: test;\n")
            f.write("F: OUTPUT: result;\n")
            f.write("=== CONSTRAINTS ===\n")
            f.write("F: RULE: no changes;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                args = argparse.Namespace(spec=f.name)
                result = command_inspect(args)
                
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert "spec" in output
                assert "valid" in output
                assert "issue_count" in output
                assert "sections" in output
                assert "task_count" in output
                assert "fact_count" in output
            finally:
                Path(f.name).unlink()

    def test_command_inspect_counts_tasks(self, capsys):
        """Test inspect command correctly counts tasks."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("F: TYPE: BUILD;\n")
            f.write("=== META ===\n")
            f.write("=== BUILD_GRAPH ===\n")
            f.write("[TASK_001]\n")
            f.write("F: ACTION: first;\n")
            f.write("F: OUTPUT: result1;\n")
            f.write("[TASK_002]\n")
            f.write("F: ACTION: second;\n")
            f.write("F: OUTPUT: result2;\n")
            f.write("=== CONSTRAINTS ===\n")
            f.write("F: RULE: safe;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                args = argparse.Namespace(spec=f.name)
                result = command_inspect(args)
                
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert output["task_count"] == 2
            finally:
                Path(f.name).unlink()

    def test_command_inspect_invalid_spec(self, capsys):
        """Test inspect command with invalid spec."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("")
            f.flush()
            
            try:
                args = argparse.Namespace(spec=f.name)
                result = command_inspect(args)
                
                assert result == 1
            finally:
                Path(f.name).unlink()


class TestMainErrorHandling:
    """Test suite for main error handling."""

    def test_main_with_missing_file(self, capsys):
        """Test main function handles missing file gracefully."""
        result = main(['parse', '/nonexistent/spec.jfp'])
        assert result == 2
        captured = capsys.readouterr()
        assert "ERROR" in captured.err

    def test_main_with_directory_instead_of_file(self, capsys):
        """Test main function handles directory instead of file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = main(['parse', tmpdir])
            assert result == 2
            captured = capsys.readouterr()
            assert "ERROR" in captured.err

    def test_main_parse_command(self, capsys):
        """Test main function with parse command."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                result = main(['parse', f.name])
                assert result == 0
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert "sections" in output
            finally:
                Path(f.name).unlink()

    def test_main_validate_command(self, capsys):
        """Test main function with validate command."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("F: TYPE: BUILD;\n")
            f.write("=== META ===\n")
            f.write("=== BUILD_GRAPH ===\n")
            f.write("[TASK_001]\n")
            f.write("F: ACTION: test;\n")
            f.write("F: OUTPUT: result;\n")
            f.write("=== CONSTRAINTS ===\n")
            f.write("F: RULE: no changes;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                result = main(['validate', f.name])
                assert result == 0
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert "valid" in output
            finally:
                Path(f.name).unlink()

    def test_main_inspect_command(self, capsys):
        """Test main function with inspect command."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jfp', delete=False) as f:
            f.write("=== JFP_DOCUMENT ===\n")
            f.write("F: VERSION: 1.0.0;\n")
            f.write("F: TYPE: BUILD;\n")
            f.write("=== META ===\n")
            f.write("=== BUILD_GRAPH ===\n")
            f.write("[TASK_001]\n")
            f.write("F: ACTION: test;\n")
            f.write("F: OUTPUT: result;\n")
            f.write("=== CONSTRAINTS ===\n")
            f.write("F: RULE: no changes;\n")
            f.write("=== END_JFP ===\n")
            f.flush()
            
            try:
                result = main(['inspect', f.name])
                assert result == 0
                captured = capsys.readouterr()
                output = json.loads(captured.out)
                assert "spec" in output
                assert "valid" in output
            finally:
                Path(f.name).unlink()
