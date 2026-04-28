# JFP Use Cases

JFP — JARO Flash Protocol is a protocol for controlled AI-assisted development.

It helps define what AI is allowed to change, what must stay protected, and how the result should be checked.

## Pull Request Control

JFP can define which files a pull request may change and which changes should trigger review.

Example:

```text
examples/pr-control/
```

## AI Code Generation Control

JFP can control small code generation tasks by mapping allowed outputs before code is created.

Example:

```text
examples/python-app-build-control/
```

## Documentation Change Control

JFP can protect important sections while allowing limited documentation updates.

Example:

```text
examples/readme-update-control/
```

## CI and GitHub Actions

JFP can run in GitHub Actions as an advisory validation layer.

Example:

```text
.github/workflows/jfp-check.yml
```

## Team Workflows

Teams can create their own JFP templates for:

- pull request checks
- documentation updates
- code generation tasks
- release preparation
- review reports

## Commercial Support

JFP is open source under the MIT License.

The project can be used freely under that license.

For larger projects, teams may contact the maintainer to discuss professional support, custom workflow design, integration help, training, or sponsored development.

## Summary

JFP helps answer one practical question:

```text
What exactly is AI allowed to change, and how do we prove it stayed inside that scope?
```
