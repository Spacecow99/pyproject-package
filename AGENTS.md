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

## Workflow artifacts live in GitHub issues

Sessions run in ephemeral containers, so local files do not survive. Specs,
plans and progress notes are stored in GitHub issues, not in the repository.
These instructions override the default save locations in the superpowers
skills.

### Do not create these local files

- `docs/superpowers/specs/*` (brainstorming design docs)
- `docs/superpowers/plans/*` (writing-plans implementation plans)
- `.superpowers/sdd/*/progress.md` (execution ledger)
- Any other planning, memory or progress markdown files.

Chat-only scratch notes are fine. Anything another session would need to
resume the work must be written to an issue.

### Issue layout

One feature maps to one parent issue plus one sub-issue per plan task.

| Artifact           | Stored in                                          | Replaces                       |
|--------------------|----------------------------------------------------|--------------------------------|
| Approved design    | Body of the feature issue                          | `docs/superpowers/specs/*.md`  |
| Implementation plan| A comment on the feature issue, headed `## Implementation plan` | `docs/superpowers/plans/*.md` |
| Plan task          | One sub-issue per task, titled `Task <N>: <summary>` | Todo list and ledger entries |
| Task progress      | Open/closed state of each sub-issue plus a closing comment | `progress.md` ledger |
| Deviations         | A comment starting `Ruling:` on the affected issue | `Ruling:` ledger lines         |

### Step by step

1. **Brainstorming.** Ask clarifying questions in chat as usual. When the
   design is approved, create (or update) the feature issue and put the design
   in its body. Use the existing issue if the work already has one. Name the
   feature branch `feature/<feature name>` and record the name in the issue.
2. **Writing plans.** Post the plan as one comment headed
   `## Implementation plan`, then create one sub-issue per task. Each
   sub-issue body holds that task's files, steps and verification commands, so
   a fresh agent can execute it from the issue alone. Link them with the
   sub-issue tool so they appear under the feature issue.
3. **Executing plans.** Work one task at a time on the feature branch. Mirror
   harness todos from the sub-issues. When a task passes its verification,
   commit, then close the sub-issue as `completed` with a comment giving the
   commit SHA and the verification command and result. Close a task only
   after its tests pass.
4. **Deviations.** If you depart from the plan, post a `Ruling:` comment
   explaining what changed and why before continuing.
5. **Finishing.** Open the pull request into `dev` per the branching model.
   Reference the feature issue with `Refs #<feature issue>` because `Closes`
   does not fire on merges into `dev`. Close the feature issue manually once
   its work reaches `main`, or earlier with a comment if the owner agrees.

### Resuming in a new session or after context compaction

Trust GitHub over memory. Read, in order: the feature issue body, the
`## Implementation plan` comment, the sub-issues' states and closing comments,
the `Ruling:` comments, and `git log` on the feature branch. Continue from the
first open sub-issue. Do not redo tasks whose sub-issues are closed.

### Conventions

- Keep one feature issue per feature branch.
- Edit the feature issue body when the design changes, and add a comment
  noting what changed. Do not leave a stale design in the body.
- Do not put secrets, credentials or customer data in issues.
- Use the GitHub MCP tools when they are available. If `gh` is available, it
  is an acceptable substitute.

## Before you open a pull request

- Re-read the template files you changed. Template variables such as
  `{{ cookiecutter.project_name }}` must stay intact.
- If you did not render the template or run its tests, say so in the pull
  request description rather than implying it was verified.
