# Python App Build Control Example

This example demonstrates how JFP can control a small Python application build before any code is generated or written.

## Scenario

A developer wants an AI assistant to create a minimal Python CLI application.

Without a protocol, the assistant might add extra files, external dependencies, configuration files, test frameworks, folders, or modify existing repository files without being asked.

With JFP, the build request is converted into a controlled specification first.

## User request

```text
Create a minimal Python CLI app that prints a greeting message.
Use only one source file.
Do not add external dependencies.
Do not create configuration files.
Do not modify existing project files.
```

## What this example demonstrates

- defining a small application build before code generation
- mapping exactly which file may be created
- preventing dependency creep
- preventing unrequested configuration files
- protecting existing repository files from modification
- using SIGNAL_ORANGE when scope expansion is detected
- producing a reviewable execution report

## Files

| File | Purpose |
|---|---|
| `python-app-build-control.jfp` | JFP specification for the controlled Python CLI app build |
| `expected-inspect-output.json` | Expected output from `jfp_cli.py inspect` |
| `execution-report.md` | Example report after a controlled app build |

## How to run

From the repository root:

```bash
python tools/jfp_cli.py inspect examples/python-app-build-control/python-app-build-control.jfp
python tools/jfp_cli.py validate examples/python-app-build-control/python-app-build-control.jfp
python tools/jfp_cli.py parse examples/python-app-build-control/python-app-build-control.jfp
```

## Status

Planned runnable validation example.

This example demonstrates how JFP can specify, constrain, validate, and report a controlled AI-assisted code generation task.
