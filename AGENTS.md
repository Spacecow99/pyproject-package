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

### Local files: `.superpowers/` is an untracked cache

- Never create or commit `docs/superpowers/specs/*` or
  `docs/superpowers/plans/*`, or any other planning, memory or progress
  markdown file inside the tracked tree.
- The superpowers skills and their scripts may read and write files under the
  repository-root `.superpowers/` folder (for example the execution ledger at
  `.superpowers/sdd/<plan>/progress.md`, task briefs, and working copies of the
  spec or plan). That folder is a disposable local cache. It is listed in
  `.gitignore` and must never be committed or force-added.
- GitHub issues are the source of truth. Every fact in `.superpowers/` must
  also be written to the matching issue, and the container may be destroyed at
  any time. If the cache and GitHub disagree, GitHub wins.
- Never treat a local file as the only record of a decision, plan or
  completed task.

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

Trust GitHub over memory and over any local cache. Read, in order: the
feature issue body, the `## Implementation plan` comment, the sub-issues'
states and closing comments, the `Ruling:` comments, and `git log` on the
feature branch.

Then rebuild `.superpowers/` before running any skill script, because the
skills trust the ledger over recollection and it will be empty or stale in a
fresh container:

1. Write the spec and plan back out as working copies under `.superpowers/`
   from the issue body and the plan comment.
2. Recreate the ledger with the header the skill expects, a
   `Task <N>: complete` line for each closed sub-issue (use the commit SHA
   from its closing comment), and a `Ruling:` line for each `Ruling:` comment.
3. If `git log` shows a task commit whose sub-issue is still open, re-run that
   task's verification and, if it passes, close the sub-issue with a comment
   before continuing.

Continue from the first open sub-issue. Do not redo tasks whose sub-issues are
closed.

Whenever a skill script appends to the ledger, make the matching GitHub update
in the same step (close the sub-issue with its comment, or post the `Ruling:`
comment). The GitHub write is the one that counts.

### Conventions

- Keep one feature issue per feature branch.
- Edit the feature issue body when the design changes, and add a comment
  noting what changed. Do not leave a stale design in the body.
- Do not put secrets, credentials or customer data in issues.
- Use the GitHub MCP tools when they are available. If `gh` is available, it
  is an acceptable substitute.

## Style guide

All code and markup in this repository, and in anything the template
generates, follows the Google style guide for its language. The full set of
guides is published at <https://google.github.io/styleguide/>. This applies to
every language, now and in the future, and it applies equally to new files and
to edits of existing files.

Rules agents must apply:

- **Identify the language first.** Before writing or editing a file, work out
  its language, then open the matching guide from the index above and follow it
  for formatting, naming, imports or includes, comments and documentation
  comments, error handling, and language features to avoid. Do not rely on
  memory of the rules; read the guide when you are unsure.
- **The Google guide wins.** If it conflicts with your habits, another
  guide, or an agent default, follow the Google guide. The only exception is a
  setting that the repository's own tool configuration (formatter, linter,
  or compiler options) explicitly sets, such as a line length. Where the
  configuration is silent, the Google guide applies.
- **No guide for the language.** If Google publishes no guide for a language,
  follow the conventions already used in the repository, and say in the pull
  request description that no Google guide applied.
- **Use the configured tooling.** Run the repository's formatter, linter and
  security checks on every change. Never loosen, disable or work around tool
  configuration to make a change pass.
- **Suppressions.** Fix findings in new code rather than suppressing them. If
  a suppression is appropriate, scope it as narrowly as the tool allows, name
  the specific rule, and add an explanation when the rule name alone does not
  make the reason clear.
- **Public interfaces.** Document every public interface using the comment or
  documentation format the guide prescribes, and follow the guide's rules on
  typing or interface declarations where the language has them.
- **TODOs.** Write TODO comments in the format the guide prescribes, with a
  link to an issue as the context. Do not put a person or team name in the
  context.
- **Focused changes.** Do not reformat or restyle unrelated code in a change.
  Existing code that deviates from the guide is not a model: do not copy the
  deviation into new code, and do not mass-fix it unless the task asks you to.
- **Tests.** Test code follows the same guide as the code it tests.

## Documentation style guide

All prose documentation follows the
[Google developer documentation style guide](https://developers.google.com/style).
This covers `README.md` files (root and template), this file, issue and pull
request text, and any docs under `docs/`. Code comments and documentation comments
follow the Style guide section above, and the rules here apply to their wording.

Rules agents must apply:

- **Voice and tone.** Write in a conversational but professional tone. Address
  the reader as "you". Use active voice and present tense. Do not
  use "please" in instructions, and avoid "easy" and "easily", because what is
  easy for you might not be easy for readers.
- **Headings.** Use sentence case, for example "Install the package", not
  "Install The Package". Start task headings with a bare infinitive ("Install
  the package") and name concepts with noun phrases ("Release process"). Use
  a heading hierarchy that does not skip levels.
- **Lists.** Use numbered lists for steps that must happen in order and
  bulleted lists otherwise. Keep items parallel in structure. Capitalize the
  first word of each item, and end items with a period when they are complete
  sentences.
- **Procedures.** Put each action in its own step, and say where the step
  happens before the action, for example "From the project root, run:".
- **Code and commands.** Put code, file names, paths, commands and
  placeholders in code formatting, and put multi-line code in fenced blocks
  with a language tag. Write placeholders in `UPPERCASE_WITH_UNDERSCORES`
  and explain each one.
- **Links.** Use descriptive link text that makes sense out of context. Never
  use "click here" or a bare "this link".
- **Wording.** Use the serial comma. Write "for example" instead of "e.g."
  and "that is" instead of "i.e.". Spell out an abbreviation on first use when readers may not know it.
  Do not use "whitelist" or "blacklist"; use terms such as "allowlist" and
  "denylist" as nouns (existing text copied from upstream tool defaults is the
  only exception). Do not use "allowlist" as a verb.
- **Consistency.** Use one term for one concept throughout a document, and
  match the capitalization of product and tool names (GitHub, Python, Flit,
  Cookiecutter).

In the template, keep Cookiecutter variables such as
`{{ cookiecutter.project_name }}` intact while editing prose around them.

## Before you open a pull request

- Check changed code against the Google style guide for its language (see the
  Style guide section) and changed prose against the Documentation style
  guide section.
- Re-read the template files you changed. Template variables such as
  `{{ cookiecutter.project_name }}` must stay intact.
- If you did not render the template or run its tests, say so in the pull
  request description rather than implying it was verified.
