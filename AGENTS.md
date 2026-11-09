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

Remote agent sessions are assigned a branch to develop on, for example
`claude/brave-hawking-szgbsr`, and can push only to that branch. The owner
accepts working on the assigned branch instead of a `feature/<name>` branch,
on one condition: the branch must be based on the latest `dev`, never on
`main`.

1. **Start from `dev`.** Before any work, fetch and base the assigned branch on
   `dev`:
   `git fetch origin dev && git checkout -B <assigned branch> origin/dev`
   This also applies when the session starts on a fresh clone of `main`, and
   when the assigned branch already exists and holds only work that has been
   merged. Rule 8 ("do not reuse a merged branch") does not apply to the
   assigned branch; reset it to `dev` instead.
2. **Keep unmerged work.** If the assigned branch has commits that are not in
   `dev`, keep them and merge `origin/dev` into the branch rather than
   resetting it.
3. **Never force-push.** If restarting the branch would require a force push,
   stop and ask the owner.
4. **Pull request into `dev`.** Open the pull request into `dev` unless told
   otherwise, and follow the other rules in this file for the change itself.
5. **No other branches.** Do not push to any other branch without explicit
   permission.

If a task names a different branch, follow the task's instructions for it, and
still base it on `dev`.

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

## Tooling

### AI agent tooling

Agents working in this repository use these skills and tools. Each is a
third-party project; follow its own README for installation, and treat the
rules in this file as taking precedence over a skill's defaults.

| Purpose                              | Tool                                                                                  | Use it for |
|--------------------------------------|---------------------------------------------------------------------------------------|------------|
| Development workflows                | [superpowers](https://github.com/obra/superpowers)                                    | Brainstorming, planning, implementing, test-driven development, code review and finishing a branch. Its outputs are redirected to GitHub issues as described in "Workflow artifacts live in GitHub issues". |
| Documentation review workflows       | [riekelt/technical-writer](https://github.com/riekelt/technical-writer)               | Reviewing and rewriting technical prose (its `reviewing-technical-prose` skill and `/prose-review` command), and drafting design docs, decision records, runbooks, changelogs and issues. |
| Google developer documentation style | [MichaelSatoshi1983/google-dev-docs-style-skill](https://github.com/MichaelSatoshi1983/google-dev-docs-style-skill/) | Applying the Google developer documentation style guide to any prose, as required by "Documentation style guide". |
| Google coding style guides           | [testdino-hq/google-styleguides-skills](https://github.com/testdino-hq/google-styleguides-skills) | Applying the Google style guide for the language of each file, as required by "Style guide". |
| Security audit and review            | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | Security audits and review workflows for generated code, run by asking the agent for a security audit of the codebase or a path. |

Rules for using them:

- **Workflow.** Use superpowers for the development workflow. Specs, plans and
  progress go to GitHub issues, with `.superpowers/` as an untracked cache.
- **Documentation precedence.** Use technical-writer for documentation review
  workflows, and the Google developer documentation style skill for the style
  itself. The Google developer documentation style guide wins when a
  technical-writer house rule conflicts with it.
- **Code style.** Load the style guide skill for each language you touch,
  and follow "Style guide" above.
- **Security reviews.** Run the security audit skill on generated code, for
  example by rendering the template into a scratch directory outside the
  repository and auditing the result. Run builds, tests and other
  target-controlled code only inside an OS-enforced sandbox with no external
  networking, because the skill's own requirements call for this. Without such
  a sandbox, leave a lead as unconfirmed and record it as needing validation
  instead of executing target code. Record audit findings in GitHub issues,
  not in committed files. The audit's working files belong in `.superpowers/`
  or in a scratch directory outside the repository.
- **Adding or updating a skill.** These skills run with an agent's
  permissions, so read a skill's files before you install or update it, install
  from the repository named above, and record any change to this table in the
  same pull request.

### Development tooling

The template configures these tools. They are declared in
`{{cookiecutter.project_name}}/pyproject.toml` and apply to projects generated
from the template. The optional dependency groups are `dev`, `test` and `docs`.

| Purpose              | Tool                                  | Configuration and use |
|----------------------|---------------------------------------|-----------------------|
| Packaging and build  | Flit (`flit_core` build backend)      | `[build-system]` and `[tool.flit.module]`. Build with `flit build`; install for development with `flit install --symlink`. Part of the `dev` group. |
| Tests                | pytest                                | Tests live in `tests/`. Run `pytest tests`. Part of the `test` group. |
| Test matrix          | Tox                                   | `[tool.tox]` runs `py37` through `py315`. Run `tox` when those interpreters are installed. Part of the `test` group. |
| Formatting           | Black                                 | `[tool.black]`: line length 80, targets `py37` through `py315`. Check with `black --check .`. Part of the `dev` group. |
| Linting              | Pylint                                | `[tool.pylint.*]`. Run `pylint <package name>`. Part of the `dev` group. |
| Security scanning    | Bandit                                | `[tool.bandit]`. Run `bandit -r <package name>`. Part of the `dev` group. |
| Documentation        | Sphinx, `sphinx-rtd-theme`, MyST      | `docs/` with a Makefile. Pages are Markdown through `myst-parser`. Part of the `docs` group. |
| Continuous integration | GitHub Actions                      | `.github/workflows/ci.yml` tests Python 3.7 through 3.15, builds with Flit, and attaches the distributions to a published GitHub Release. |
| Development environment | Dev container and VS Code workspace | `.devcontainer/devcontainer.json` (also used by GitHub Codespaces) and a `.code-workspace` file named from `project_name`. |
| Template rendering   | Cookiecutter                          | `cookiecutter.json` defines the variables. Render with `cookiecutter . --no-input --output-dir <scratch directory>`. |

Rules for using them:

- **Where the commands run.** This repository is the template, so it has no
  test suite of its own. To verify a change, render the template into a
  scratch directory outside the repository and run the commands above in the
  generated project.
- **Keep the tooling aligned.** When you change a supported Python version,
  update the Tox `envlist`, the Black `target-version`, the CI matrix and the
  `requires-python` setting together.
- **Do not weaken the configuration.** Do not loosen Black, Pylint, Bandit or
  CI settings to make a change pass; see "Style guide".
- **Keep template variables intact.** Cookiecutter variables such as
  `{{ cookiecutter.project_name }}` must survive every edit to these files.

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

## Template authoring: Jinja pitfalls

Every file under `{{cookiecutter.project_name}}/` is rendered by Cookiecutter
with Jinja, including file and directory names. Rendering fails if a file
contains Jinja syntax that Cookiecutter cannot evaluate. This already happened:
the CI workflow used GitHub Actions expressions such as
`${{ matrix.python-version }}`, Jinja treated them as variables, and the
template could not be rendered at all (`'matrix' is undefined`).

- **Wrap literal delimiters in `raw`.** Any literal `{{`, `}}`, `{%`, `%}`,
  `{#` or `#}` in a template file, such as a GitHub Actions expression, must
  sit inside a `{% raw %}` ... `{% endraw %}` block. For a whole file, use
  `{% raw -%}` at the top and `{%- endraw %}` at the bottom so no blank lines
  are added to the rendered output. The workflow
  `{{cookiecutter.project_name}}/.github/workflows/ci.yml` is the example.
- **Undefined names are errors.** An unknown variable stops rendering. Only
  use the variables defined in `cookiecutter.json`, and add new ones there
  with a default value.
- **Whole files without rendering.** If a file has too much literal Jinja
  syntax to wrap, Cookiecutter's `_copy_without_render` option in
  `cookiecutter.json` copies it unchanged. Such a file cannot use variables.
- **Variables inside string literals.** A variable that lands inside a quoted
  string in Python, TOML, YAML or JSON can break the generated file if its
  value contains a quote, a backslash or other special characters. When you
  add or change such a variable, also render once with an unusual value.
- **Format and lint the rendered output.** Formatters and linters can fail on
  or reformat Jinja syntax in the template source. Run them on a rendered
  project, then port any changes back to the template files so the rendered
  output passes. For example, the quote style in the template
  `docs/source/conf.py` had to be changed in the template to make
  `black --check .` pass on the rendered project.
- **Check for leftovers.** After rendering, the output must contain no
  unrendered template syntax. This command prints nothing when the render is
  clean:

  ```shell
  grep -rIn -E "\{\{ *cookiecutter|\{%" RENDERED_PROJECT_DIRECTORY
  ```

  Replace `RENDERED_PROJECT_DIRECTORY` with the path of the generated project.
  GitHub Actions expressions that you wrapped in `raw` are expected in the
  rendered output and do not match this pattern.

## Definition of done

A change is done only when the checks below have been run and their results
reported. "It should work" and "I read the files" are not verification.

### Changes to the template

1. **Render it.** Render with default values into a scratch directory outside
   the repository:

   ```shell
   cookiecutter . --no-input --output-dir SCRATCH_DIRECTORY
   ```

   Replace `SCRATCH_DIRECTORY` with a directory outside this repository.
   Rendering must succeed, and the leftover check in "Jinja pitfalls" must
   print nothing.
2. **Run the project checks in the generated project.** From the generated
   project root, run each of these and read the result:

   ```shell
   python -m pip install -e .
   python -m pytest tests
   black --check .
   pylint PACKAGE_NAME
   bandit -r PACKAGE_NAME
   flit build
   ```

   Replace `PACKAGE_NAME` with the generated package name. `pytest`,
   `black --check .`, `bandit` and `flit build` must pass. Pylint currently
   reports a known baseline on a fresh render: `redefined-builtin` for `sum`,
   `unused-variable` for `args`, and `unused-import` for `os` and `sys`, plus
   two `overgeneral-exceptions` configuration warnings. Your change must not
   add to that baseline. Fixing the baseline is separate work.
3. **Validate generated YAML and TOML.** If you changed a workflow or
   `pyproject.toml`, parse the rendered file with a YAML or TOML parser and
   check that the values you changed came through as intended.
4. **Say what you could not run.** Some things cannot be run here, such as a
   GitHub Actions workflow, a dev container build or a Codespaces session.
   State plainly in the pull request and in the issue that these were not
   verified. Do not describe them as working.

### Changes to `AGENTS.md` and other prose

Re-read the result against the "Documentation style guide" section. If the
change touches commands or file paths, run the commands or check the paths
exist. A prose-only change does not need a render.

### Closing issues

- Verify every acceptance criterion in the issue by running it, not by reading
  the files. If a criterion cannot be run, say so in a comment and leave the
  issue open, or ask the owner to confirm it.
- Close an issue only through a pull request into `main` that contains
  `Closes #<number>`, or manually with a comment that lists the evidence for
  each criterion. Never close an issue on the strength of reading the code.
- If a closed issue turns out not to be satisfied, reopen it and comment with
  what failed and how you found out.

### Reporting results

Report outcomes as they are. If a check fails, say so and include the relevant
output. If you skipped a step, say that you skipped it and why. When a check
passes, say so plainly without hedging.

## Before you open a pull request

- Check changed code against the Google style guide for its language (see the
  Style guide section) and changed prose against the Documentation style
  guide section.
- Re-read the template files you changed. Template variables such as
  `{{ cookiecutter.project_name }}` must stay intact, and literal Jinja
  delimiters must be wrapped in `raw` (see "Jinja pitfalls").
- Meet the "Definition of done". If you did not render the template or run its
  checks, say so in the pull request description rather than implying it was
  verified.
