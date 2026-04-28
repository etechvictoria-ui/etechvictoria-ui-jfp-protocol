# JFP Templates

This folder will contain reusable JFP specification templates.

Templates are intended to help developers start from a known structure instead of writing every `.jfp` file from scratch.

## Purpose

Templates should provide repeatable structures for common JFP workflows, such as:

- build specifications
- patch specifications
- validation workflows
- output maps
- constraint sets
- SIGNAL_ORANGE stop rules

## How to use this folder

Copy a template, rename it, and adjust the facts, tasks, outputs, and constraints for your project.

Example future usage:

```bash
cp templates/build-spec-template.jfp specs/my-project-build.jfp
python tools/jfp_cli.py validate specs/my-project-build.jfp
```

## Status

Early placeholder.

Reusable `.jfp` templates will be added here as the protocol evolves.
