# README Update Control Example

This example demonstrates how JFP can control a simple documentation change before the change is executed.

## Scenario

A developer wants an AI assistant to update a project README.

Without a protocol, the assistant might rewrite too much, add unrequested sections, remove important context, or change files outside the requested scope.

With JFP, the request is converted into a controlled specification first.

## User request

```text
Update the README with a short "Getting Started" section, but do not change the project description, author section, or existing tool table.
```

## What this example demonstrates

- defining the requested change before execution
- mapping the only file that may be modified
- protecting sections that must not change
- using constraints to prevent scope creep
- stopping when the requested output is unclear
- producing a reviewable execution report

## Files

| File | Purpose |
|---|---|
| `readme-update-control.jfp` | JFP specification for the README update request |
| `expected-inspect-output.json` | Expected output from `jfp_cli.py inspect` |
| `execution-report.md` | Example report after a controlled documentation update |

## How to run

From the repository root:

```bash
python tools/jfp_cli.py inspect examples/readme-update-control/readme-update-control.jfp
python tools/jfp_cli.py validate examples/readme-update-control/readme-update-control.jfp
python tools/jfp_cli.py parse examples/readme-update-control/readme-update-control.jfp
```

## Status

Runnable validation example.

This example does not edit the real repository README. It demonstrates how JFP can specify, constrain, validate, and report a controlled documentation update.
