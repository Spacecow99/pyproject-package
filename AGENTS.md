# Agent instructions

This repository is a Cookiecutter template for a Python package. The template
lives in `{{cookiecutter.project_name}}/`. Files in that directory are rendered
into generated projects; this root `AGENTS.md` is for work on the template
itself and is not part of generated projects.

## Branching model

| Branch             | Purpose                                              | Branches from | Merges into |
|--------------------|------------------------------------------------------|---------------|-------------|
| `main`             | Stable, released state of the template.              | n/a           | n/a         |
| `dev`              | Integration branch. All feature work lands here.     | `main`        | `main`      |
| `feature/<name>`   | One feature, fix or documentation change.            | `dev`         | `dev`       |

### Rules

1. `dev` is created from `main` and is the base for all new work.
2. Every change is made on a feature branch named `feature/<feature name>`.
   Use lowercase words separated by hyphens, for example
   `feature/add-pre-commit-config`.
3. Create feature branches from the latest `dev`, never from `main` and never
   from another feature branch:
   `git fetch origin dev && git checkout -b feature/<name> origin/dev`
4. Never commit directly to `main` or `dev`. Open a pull request from the
   feature branch into `dev`.
5. Changes reach `main` only through a pull request from `dev` into `main`.
6. Never open a pull request from a feature branch directly into `main`.
7. Keep each feature branch focused on one change. If the change references a
   GitHub issue, put `Closes #<number>` in the pull request description. Note
   that GitHub only auto-closes issues when the pull request merges into the
   default branch (`main`), so issues resolved on `dev` stay open until `dev`
   is merged; close them manually with a comment if they must be closed sooner.
8. After a feature branch is merged into `dev`, delete it. Do not reuse a
   merged branch for new work; create a new `feature/<name>` branch from the
   latest `dev`.
9. Do not rewrite history on `main` or `dev`. Never force-push to them.

### Session branch override

If a task or the environment names a specific branch to develop on (for
example an automatically assigned `claude/...` branch), push only to that
branch and follow the task's instructions for it. Open the pull request into
`dev` unless told otherwise. Do not push to any other branch without explicit
permission.

## Before you open a pull request

- Re-read the template files you changed. Template variables such as
  `{{ cookiecutter.project_name }}` must stay intact.
- If you did not render the template or run its tests, say so in the pull
  request description rather than implying it was verified.
