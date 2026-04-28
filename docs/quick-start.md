# JFP Quick Start

JFP - JARO Flash Protocol - is a specification-first protocol for controlled AI-assisted development.

This repository contains early prototype tools for parsing and validating `.jfp` specification files.

## Requirements

- Python 3.10 or newer
- Git

No external Python dependencies are required for the current prototype.

## Clone the repository

```bash
git clone https://github.com/etechvictoria-ui/etechvictoria-ui-jfp-protocol.git
cd etechvictoria-ui-jfp-protocol
```

## Parse a JFP file

```bash
python tools/parser.py specs/minimal-build-spec.jfp
```

The parser converts a `.jfp` document into structured JSON containing:

- sections
- blocks
- facts

## Validate a JFP file

```bash
python tools/validator.py specs/minimal-build-spec.jfp
```

The validator checks the document through five layers.

## L1 - Syntax

Checks basic JFP syntax:

- section markers
- fact format
- semicolons
- invalid records

## L2 - Structure

Checks whether the document contains required protocol structure:

- VERSION
- TYPE
- META
- BUILD_GRAPH or PATCH_GRAPH
- task ACTION
- task OUTPUT

## L3 - Dependency

Checks whether task dependencies refer to existing tasks.

Example:

```text
F:DEPENDENCY:TASK_01;
```

The referenced task must exist in the same document.

## L4 - Policy

Checks declared constraints and safety rules.

Example:

```text
=== CONSTRAINTS ===
F:RULE:do_not_create_unrequested_files;
```

High-risk actions should require explicit approval constraints.

## L5 - Execution Safety

Checks whether declared task outputs are mapped in `OUTPUT_MAP`.

Example:

```text
[TASK_02]
F:OUTPUT:app/main.py;

=== OUTPUT_MAP ===
[FILE_02]
F:PATH:app/main.py;
```

If a task creates an output that is not listed in `OUTPUT_MAP`, the validator raises a safety issue.

## SIGNAL_ORANGE

`SIGNAL_ORANGE` defines stop conditions.

Example:

```text
=== SIGNAL_ORANGE ===
F:TRIGGER:output_not_mapped;
F:TRIGGER:constraint_conflict;
F:ACTION:halt_and_request_human_review;
```

When a stop condition is triggered, execution should halt and request human review.

## Current workflow

1. Write a `.jfp` specification.
2. Parse it.
3. Validate it.
4. Review validation results.
5. Only then allow execution or agent-assisted implementation.

## Example

```bash
python tools/parser.py specs/minimal-build-spec.jfp
python tools/validator.py specs/minimal-build-spec.jfp
```

## Expected result

A valid spec should return:

```json
{
  "valid": true,
  "issue_count": 0,
  "issues": []
}
```

## Philosophy

AI can generate.

JFP controls.

A prompt is not a protocol.
