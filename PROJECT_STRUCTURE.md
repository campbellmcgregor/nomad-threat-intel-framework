# NOMAD Project Structure

This document describes the organized directory structure of the NOMAD Threat Intelligence Framework.

## Directory Layout

```
nomad-threat-intel-framework/
├── README.md                     # Main project README
├── setup.py                      # Python package setup
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignore rules
├── PROJECT_STRUCTURE.md          # This file
├── nomad_workflow_enhanced.py    # Main workflow runner
├── weekly-threat-report-*.json   # Sample outputs
│
├── src/                          # Source code
│   ├── agents/                   # Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Base agent class
│   │   ├── rss_feed.py          # RSS feed agent
│   │   └── ...
│   ├── config/                   # Configuration modules
│   │   ├── __init__.py
│   │   └── environment.py        # Environment configuration
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       └── workflow_validator.py
│
├── scripts/                      # CLI execution scripts
│   ├── run_rss_agent.py         # Direct RSS agent execution
│   ├── run_orchestrator.py      # Direct orchestrator execution
│   └── run_ciso_report.py       # Direct CISO report generation
│
├── prompts/                      # AI prompt templates
│   ├── agents/                   # Agent-specific prompts
│   │   ├── rss-agent-prompt.md
│   │   ├── orchestrator-system-prompt.md
│   │   ├── ciso-report-generator-prompt.md
│   │   └── ...
│   └── archived/                 # Archived/old prompts
│
├── docs/                         # Comprehensive documentation
│   ├── README.md                 # Documentation hub
│   ├── user-guide/               # User documentation
│   │   ├── quick-start.md
│   │   ├── user-manual.md
│   │   ├── configuration.md
│   │   ├── workflows.md
│   │   └── troubleshooting.md
│   ├── developer-guide/          # Developer documentation
│   │   ├── setup.md
│   │   ├── architecture.md
│   │   ├── agent-development.md
│   │   ├── testing.md
│   │   └── deployment.md
│   └── reference/                # Reference documentation
│       ├── api.md
│       ├── schemas.md
│       ├── security.md
│       ├── prompts.md
│       └── performance.md
│
├── data/                         # Data directories
│   ├── input/                    # Input data files
│   ├── output/                   # Generated output files
│   └── cache/                    # Cached data
│
├── logs/                         # Application logs
│
├── tests/                        # Test files (to be created)
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── examples/                     # Usage examples (to be created)
│
└── archive/                      # Archived files
    ├── old-docs/                 # Old documentation files
    └── old-scripts/              # Old script files
```

## Key Components

### Source Code (`src/`)
- **agents/**: Core agent implementations inheriting from BaseAgent
- **config/**: Configuration management and environment setup
- **utils/**: Shared utility functions and classes

### Scripts (`scripts/`)
- Standalone execution scripts for each agent
- Allow direct Python execution without Claude Code
- Include argument parsing and output formatting

### Prompts (`prompts/`)
- AI prompt templates organized by agent type
- Markdown format for easy editing and version control
- Archived older versions for reference

### Documentation (`docs/`)
- Comprehensive documentation for all audiences
- User guides for operators and administrators
- Developer guides for contributors and integrators
- Reference documentation for APIs and schemas

### Data Directories
- **data/input/**: Raw input files and configurations
- **data/output/**: Generated reports and processed intelligence
- **data/cache/**: Temporary cached data for performance
- **logs/**: Application and error logs

## Import Structure

With the reorganized structure, imports follow this pattern:

```python
# Agent imports
from src.agents.base_agent import BaseAgent
from src.agents.rss_feed import RSSFeedAgent

# Configuration imports
from src.config.environment import config

# Utility imports
from src.utils.workflow_validator import WorkflowValidator
```

## Installation

With the new structure, install as a Python package:

```bash
# Development installation
pip install -e .

# Production installation
pip install .

# With optional dependencies
pip install .[dev]
pip install .[production]
```

## Entry Points

The setup.py provides command-line entry points:

```bash
nomad list                    # List workflows
nomad execute morning_check   # Execute workflow
nomad-rss --help             # RSS agent help
nomad-orchestrator --help    # Orchestrator help
nomad-ciso --help            # CISO report help
```

This organized structure provides clear separation of concerns, easier maintenance, and better scalability as the project grows.