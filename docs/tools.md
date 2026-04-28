# JFP Tools Reference

This document explains every tool currently included in the JFP repository.

Each tool is documented using the same pattern:

1. What it does
2. Why it exists
3. How to run it
4. Example command
5. Expected output
6. Where it fits in the JFP workflow

## Tool overview

| Tool | Purpose |
|---|---|
| `tools/parser.py` | Converts `.jfp` text into structured JSON |
| `tools/validator.py` | Validates `.jfp` files through L1-L5 checks |
| `tools/jfp_cli.py` | Provides one command-line entrypoint for parse, validate, and inspect |

---

# `tools/parser.py`

## What it does

`parser.py` reads a `.jfp` specification file and converts it into structured JSON.

It recognizes:

- sections, for example `=== META ===`
- blocks, for example `[TASK_01]`
- facts, for example `F:ACTION:fs.write_file;`

## Why it exists

A JFP file should not remain just raw text.

The parser turns a JFP document into a machine-readable structure that can be used by validators, CLIs, agents, runtimes, and future tooling.

## How to run it

From the repository root:

```bash
python tools/parser.py specs/minimal-build-spec.jfp
```

## Example command

```bash
python tools/parser.py specs/minimal-build-spec.jfp
```

## Expected output

The output is JSON containing:

- `sections`
- `blocks`
- `facts`

Example shape:

```json
{
  "sections": {},
  "blocks": {},
  "facts": []
}
```

## Where it fits in JFP

The parser is the first technical layer of JFP tooling.

It converts protocol text into data.

---

# `tools/validator.py`

## What it does

`validator.py` checks whether a `.jfp` file is structurally and operationally safe enough to continue through the workflow.

It validates the document using five layers:

- L1 - Syntax
- L2 - Structure
- L3 - Dependency
- L4 - Policy
- L5 - Execution Safety

## Why it exists

AI-assisted development often fails because instructions are vague, incomplete, or unsafe.

The validator exists to catch those problems before execution.

It helps enforce the JFP principle:

> Validate before you trust.

## How to run it

From the repository root:

```bash
python tools/validator.py specs/minimal-build-spec.jfp
```

## Example command

```bash
python tools/validator.py specs/minimal-build-spec.jfp
```

## Expected output

A valid spec returns JSON similar to:

```json
{
  "valid": true,
  "layers": {
    "L1": true,
    "L2": true,
    "L3": true,
    "L4": true,
    "L5": true
  },
  "issue_count": 0,
  "issues": []
}
```

An invalid spec returns `valid: false` and a list of issues.

## Where it fits in JFP

The validator sits after parsing and before execution.

A JFP document should be validated before any agent, script, or human team uses it to make changes.

---

# `tools/jfp_cli.py`

## What it does

`jfp_cli.py` provides a single command-line interface for the current JFP toolchain.

It supports:

- `parse`
- `validate`
- `inspect`

## Why it exists

Developers need one simple entrypoint.

Instead of remembering separate scripts, the CLI gives the user a single workflow command.

## How to run it

From the repository root:

```bash
python tools/jfp_cli.py parse specs/minimal-build-spec.jfp
python tools/jfp_cli.py validate specs/minimal-build-spec.jfp
python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp
```

## Example commands

Parse a spec:

```bash
python tools/jfp_cli.py parse specs/minimal-build-spec.jfp
```

Validate a spec:

```bash
python tools/jfp_cli.py validate specs/minimal-build-spec.jfp
```

Inspect a spec:

```bash
python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp
```

## Expected output

`parse` returns the full parsed JSON structure.

`validate` returns the L1-L5 validation report.

`inspect` returns a compact summary such as:

```json
{
  "spec": "specs/minimal-build-spec.jfp",
  "valid": true,
  "issue_count": 0,
  "sections": ["JFP_DOCUMENT", "META", "BUILD_GRAPH", "OUTPUT_MAP", "CONSTRAINTS", "SIGNAL_ORANGE", "END_JFP"],
  "task_count": 2,
  "fact_count": 20
}
```

## Where it fits in JFP

The CLI is the developer entrypoint into JFP.

It is the first step toward a full JFP runtime and future `jfp run` execution flow.

---

# Recommended workflow

Use the tools in this order:

```bash
python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp
python tools/jfp_cli.py parse specs/minimal-build-spec.jfp
python tools/jfp_cli.py validate specs/minimal-build-spec.jfp
```

For daily use, the most important command is:

```bash
python tools/jfp_cli.py validate specs/minimal-build-spec.jfp
```

If validation fails, fix the `.jfp` file before continuing.

---

# JFP rule

Do not execute what you cannot parse.

Do not trust what you cannot validate.
