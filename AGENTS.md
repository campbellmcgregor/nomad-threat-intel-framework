# Repository Guidelines

## Project Structure & Module Organization
Source lives under `src/`, with agents in `src/agents/`, shared helpers in `src/utils/`, and configuration loaders and YAML under `src/config/`. Entry scripts such as `scripts/run_rss_agent.py` and `scripts/run_orchestrator.py` are the supported CLIs. Prompts and docs sit in `prompts/` and `docs/`. Runtime artifacts belong in `data/` and `logs/` (both gitignored). Tests mirror the module tree inside `tests/` (for example `tests/agents/test_rss_feed.py`).

## Build, Test, and Development Commands
Create an isolated environment before work: `python -m venv .venv && source .venv/bin/activate`. Install dependencies with `pip install -r requirements.txt` or use `pip install -e .` for editable mode. Replicate prod settings via `cp .env.example .env` and update secrets locally. Run agents through their scripts (`python scripts/run_rss_agent.py`, `python scripts/run_ciso_report.py`). Execute the full suite with `pytest -q`.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation, descriptive docstrings, and type hints on public interfaces. Use `snake_case.py` file names, `CamelCase` classes, and `snake_case` functions and variables; promote constants to `UPPER_SNAKE`. Keep agent-specific helpers close to their agent modules to ease discovery and reuse.

## Testing Guidelines
Pytest is the standard. Name new tests `test_*.py`, colocated with their target modules. Mock network calls or LLM responses so tests stay deterministic. Cover workflow routing, parsing logic, and error branches before merging. Run `pytest -q` locally and ensure failures are triaged or skipped intentionally.

## Commit & Pull Request Guidelines
Adopt Conventional Commit prefixes (`feat:`, `fix:`, `docs:`, `chore:`); scope components when helpful, e.g. `feat(agents): add vendor bulletin parser`. Each PR should link to its issue, describe behavioral changes, call out config edits, and attach relevant logs or screenshots. Keep changesets focused and update prompts or docs when behavior shifts.

## Security & Configuration Tips
Never commit credentials. Rely on `.env` for secrets and audit `src/config/*.yaml` before distribution. Sanitize logs prior to sharing and store generated reports under `data/` for traceability.
