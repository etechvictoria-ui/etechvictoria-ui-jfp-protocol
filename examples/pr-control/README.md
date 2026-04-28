# Pull Request Control Example

This example demonstrates how JFP can be used as a control layer for pull request review.

## Scenario

A developer opens a pull request to add a small Python CLI feature.

Without a protocol, the pull request may include extra files, dependency changes, documentation rewrites, configuration changes, or unrelated modifications.

With JFP, the pull request is checked against a controlled specification before it is approved.

## Example PR request

```text
Add a small greeting option to the Python CLI example.
Only modify the mapped CLI file.
Do not add dependencies.
Do not change documentation.
Do not create configuration files.
```

## What this example demonstrates

- mapping which files a pull request is allowed to change
- blocking unmapped file changes
- preventing dependency creep
- preventing unrelated documentation edits
- detecting configuration changes
- using SIGNAL_ORANGE when the PR exceeds the approved scope
- producing a reviewable PR report

## Files

| File | Purpose |
|---|---|
| `pr-control.jfp` | JFP specification for pull request scope control |
| `expected-inspect-output.json` | Expected output from `jfp_cli.py inspect` |
| `pr-review-report.md` | Example PR review report generated from the JFP checks |

## How to run

From the repository root:

```bash
python tools/jfp_cli.py inspect examples/pr-control/pr-control.jfp
python tools/jfp_cli.py validate examples/pr-control/pr-control.jfp
python tools/jfp_cli.py parse examples/pr-control/pr-control.jfp
```

## Status

Planned integration example.

This example does not connect directly to GitHub Actions yet. It demonstrates the structure of a future JFP-based pull request control layer.
