# Maintainer Notes

These notes are written for the project maintainer and future contributors.

The goal is to keep the project clear, honest, and easy to maintain.

## What JFP is

JFP — JARO Flash Protocol is a specification-first protocol for controlled AI-assisted development.

It helps define:

- what AI is allowed to do
- which files may be created or changed
- which files or sections must stay protected
- what constraints apply
- when work should stop for human review
- what report should be produced after execution

In simple words:

```text
JFP controls the scope of AI-assisted work before execution.
```

## What JFP is not

JFP is not:

- a finished enterprise platform
- a replacement for developers
- a replacement for code review
- a replacement for testing
- a security certification system
- an autonomous decision system
- a collection of random prompts

The current repository is an early open-source prototype and documentation companion.

## Repository map

```text
assets/        Visual references, wallpapers, and media assets
case-studies/  Existing prototype systems and application patterns
docs/          Documentation, notes, and guides
examples/      Example JFP workflows and validation demos
specs/         Example JFP specification files
templates/     Reusable JFP templates
tools/         Parser, validator, and CLI prototypes
```

## How to run basic checks

From the repository root, run:

```bash
python tools/jfp_cli.py inspect specs/minimal-build-spec.jfp
python tools/jfp_cli.py validate specs/minimal-build-spec.jfp
python tools/jfp_cli.py parse specs/minimal-build-spec.jfp
```

You can also run example specs:

```bash
python tools/jfp_cli.py inspect examples/pr-control/pr-control.jfp
python tools/jfp_cli.py validate examples/pr-control/pr-control.jfp
python tools/jfp_cli.py parse examples/pr-control/pr-control.jfp
```

## How to add a new example

A good example should usually include:

```text
examples/example-name/
├── README.md
├── example-name.jfp
├── expected-inspect-output.json
└── execution-report.md
```

Each example should explain:

- what the example does
- why it exists
- how to run it
- what output to expect
- what constraints are being demonstrated

## How to review changes

Before accepting or publishing a change, check:

- does the change match the purpose of JFP?
- does it explain what it does?
- does it explain how to run it?
- does it avoid false claims?
- does it avoid pretending the project is more mature than it is?
- does it keep examples clear and controlled?

## Safe public wording

Good wording:

```text
JFP is an early-stage protocol for controlled AI-assisted development.
```

```text
JFP helps make AI-assisted work more explicit, bounded, reviewable, and auditable.
```

```text
The current tools are prototypes for experimentation, documentation, and workflow design.
```

Avoid wording like:

```text
JFP is an industry standard.
```

```text
JFP guarantees safe AI output.
```

```text
JFP replaces developers or security review.
```

```text
JFP is a complete enterprise platform.
```

## Commercial conversations

JFP is open source under the MIT License.

Commercial conversations should stay simple and honest.

Safe wording:

```text
For larger projects, custom integrations, workflow design, training, or professional support can be discussed with the maintainer.
```

Do not promise features that do not exist yet.

Possible future commercial paths:

- consulting
- GitHub Actions integration support
- custom JFP templates
- workflow design for teams
- training for controlled AI-assisted development
- sponsored development

## Current project status

Current status:

```text
early-stage open-source prototype
```

The project already includes:

- JFP specification examples
- parser prototype
- validator prototype
- CLI prototype
- templates
- example workflows
- GitHub Actions integration
- PR control example
- documentation and use cases

The project does not yet include:

- full production platform
- hosted service
- enterprise dashboard
- official package release
- formal standard body approval

## Maintainer principle

When unsure, keep the project:

```text
clear, honest, controlled, and useful
```

Do not overpromise.

Explain what each file does, how to run it, and why it exists.
