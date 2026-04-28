# Minimal Python App Example

This example demonstrates a small end-to-end JFP workflow for creating a minimal Python application structure.

## Purpose

The goal is to show how a `.jfp` file can describe a controlled build before any files are created.

This example focuses on:

- defining intent before execution
- mapping outputs before creation
- declaring constraints
- using SIGNAL_ORANGE stop rules
- validating the specification before implementation

## Files

| File | Purpose |
|---|---|
| `minimal-python-app.jfp` | JFP build specification for a tiny Python app |
| `expected-inspect-output.json` | Example output from `python tools/jfp_cli.py inspect ...` |

## How to run

From the repository root:

```bash
python tools/jfp_cli.py inspect examples/minimal-python-app/minimal-python-app.jfp
python tools/jfp_cli.py validate examples/minimal-python-app/minimal-python-app.jfp
python tools/jfp_cli.py parse examples/minimal-python-app/minimal-python-app.jfp
```

## What this example teaches

A JFP build should not begin with generated code.

It should begin with a specification that answers:

- What is being created?
- Which tasks are allowed?
- Which files or folders may be produced?
- Which constraints must be respected?
- When should execution stop for human review?

## Status

Runnable validation example.

This example does not execute file creation. It demonstrates specification, inspection, parsing, and validation only.
