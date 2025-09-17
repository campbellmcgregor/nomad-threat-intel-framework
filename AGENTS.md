# Repository Guidelines

## Project Structure & Modules
- `src/agents/`: Core agents (e.g., `rss_feed.py`, `base_agent.py`).
- `src/config/`: YAML config and env loader (`rss_feeds.yaml`, `environment.py`).
- `src/utils/`: Shared helpers (e.g., `workflow_validator.py`).
- `scripts/`: Entry points (`run_rss_agent.py`, `run_orchestrator.py`, `run_ciso_report.py`).
- `prompts/`, `docs/`: Prompt templates and reference docs.
- `data/`, `logs/`: Runtime artifacts (gitignored); avoid committing large/generated files.
- `tests/`: Pytest suite (add as you contribute).

## Build, Test, and Run
- Environment: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Configure: `cp .env.example .env` then update values as needed.
- Run RSS flow: `python scripts/run_rss_agent.py`
- Run orchestrator: `python scripts/run_orchestrator.py`
- Run CISO report: `python scripts/run_ciso_report.py`
- Optional dev install: `pip install -e .`
- Tests: `pytest -q` (place tests under `tests/`).

## Style & Naming
- Python, PEP 8, 4 spaces; use type hints and docstrings.
- Files/modules: `snake_case.py`; classes: `CamelCase`; functions/vars: `snake_case`; constants: `UPPER_SNAKE`.
- Keep modules cohesive; colocate agent-specific helpers under `src/agents/`.
- Store config in YAML under `src/config/`; access env via `src/config/environment.py`.

## Testing Guidelines
- Framework: `pytest`. Name tests `test_*.py` mirroring module paths (e.g., `tests/agents/test_rss_feed.py`).
- Mock network/LLM calls; cover parsing, routing decisions, and error paths.
- Include tests with new features and fixes; prioritize meaningful coverage.

## Commits & Pull Requests
- Prefer Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:` (seen in history).
- Example: `feat(agents): add vendor bulletin parser`.
- PRs: clear description, linked issue, noted config changes, test plan/output, and screenshots/log snippets when relevant.
- Keep PRs small and focused; update docs when behaviors or prompts change.

## Security & Config
- Never commit secrets. Use `.env` (copied from `.env.example`) and keep it local.
- Review `src/config/*.yaml` before running; sanitize logs to avoid sensitive data.
- Write artifacts to `data/` and `logs/` (gitignored).
