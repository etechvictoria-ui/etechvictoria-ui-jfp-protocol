# JFP — JARO Flash Protocol

**A specification-first protocol for controlled AI-assisted development.**

AI can generate.  
JFP controls.

JFP is a protocol layer for designing, validating, and reviewing AI-assisted systems before execution.
It helps developers move from vague prompts to structured specifications, explicit constraints, validation layers, and traceable delivery.

## Why JFP matters

AI coding tools can generate code quickly, but speed without control creates risk:

- unclear scope
- unrequested files
- hidden assumptions
- unsafe changes
- missing validation
- difficult code review
- weak execution traceability

JFP introduces a protocol layer between human intention and AI execution.

## Core idea

A prompt is not a protocol.

JFP replaces vague instruction with:

- facts
- BUILD_GRAPH
- OUTPUT_MAP
- CONSTRAINTS
- SIGNAL_ORANGE
- validation
- dry-run
- execution reports

## JFP operating rules

1. Define before you generate  
2. Map before you create  
3. Constrain before you execute  
4. Validate before you trust  
5. Dry-run before you change  
6. Stop before you guess  
7. Verify before you deliver  
8. Report before you ask for trust  

## Quick Start

See: [`docs/quick-start.md`](docs/quick-start.md)

Run locally:

```bash
python tools/parser.py specs/minimal-build-spec.jfp
python tools/validator.py specs/minimal-build-spec.jfp
python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp
```

## Tools

| Tool | What it does | How to run |
|---|---|---|
| `tools/parser.py` | Parses `.jfp` files into structured JSON | `python tools/parser.py specs/minimal-build-spec.jfp` |
| `tools/validator.py` | Validates `.jfp` files through L1-L5 checks | `python tools/validator.py specs/minimal-build-spec.jfp` |
| `tools/jfp_cli.py` | CLI entrypoint for parse, validate, and inspect | `python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp` |

Full reference: [`docs/tools.md`](docs/tools.md)

## Real systems and case studies

JFP is not only a document format. The repository also documents existing prototype systems that demonstrate JFP-inspired design patterns.

| Case study | What it demonstrates |
|---|---|
| [`VIKI Vision UEACT`](case-studies/viki-vision-ueact/) | Visual decision-support workflow using structured AI perception output, uncertainty, correction layers, and human review |
| [`VIKI VIPER Command Center`](case-studies/viki-viper-command-center/) | Operational monitoring, anomaly analysis, proof tracking, blackbox logging, degraded states, and operator-controlled safety actions |

These case studies are included as architectural references and demonstrations of structured AI-assisted systems.
They are not provided as real emergency, tactical, medical, police, military, or autonomous decision systems.

The case studies are description-only architectural references. Full source code and private implementation details are not included in this repository.

See all case studies: [`case-studies/`](case-studies/)

## Repository structure

```text
case-studies/  Existing prototype systems and application patterns
docs/          Quick start and tool documentation
specs/         Example JFP specification files
templates/     Reusable JFP templates
tools/         Parser, validator, and CLI prototypes
examples/      Example workflows and future demos
```

## Status

JFP version: **v13.0.0**

This repository is an early open-source companion for the JFP ecosystem.
The current tools are prototypes intended for education, experimentation, and structured AI-assisted workflow design.

## Book

**JFP — How to Design, Control, and Deliver Systems in the Age of Artificial Intelligence**

## Author

Jaroslaw Kuchta  
Creator of JFP — JARO Flash Protocol
