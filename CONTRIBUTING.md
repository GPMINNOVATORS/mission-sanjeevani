# Contributing to Mission Sanjeevani

Thanks for helping. Clinicians, engineers, designers and field workers are all welcome.

## Setup

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## Workflow

1. Open or comment on an issue before large changes.
2. Fork, then branch: `feat/short-name` or `fix/short-name`.
3. Add tests for any behaviour change.
4. Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `test:`).
5. Open a PR and fill in the template.

## Clinical changes

Any change to triage thresholds, escalation rules or payload contents must cite its clinical source (guideline, paper or named clinician reviewer) in the PR description. PRs without this will not be merged.

## Code style

Python 3.10+, type hints on public functions, `ruff` clean, no new runtime dependencies without discussion.
