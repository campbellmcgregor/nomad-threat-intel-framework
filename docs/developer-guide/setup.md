# NOMAD Developer Setup Guide

Complete guide to setting up a development environment for the NOMAD Threat Intelligence Framework.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Environment Setup](#development-environment-setup)
- [IDE Configuration](#ide-configuration)
- [Development Tools](#development-tools)
- [Code Quality Setup](#code-quality-setup)
- [Testing Environment](#testing-environment)
- [Debugging Setup](#debugging-setup)
- [Contribution Workflow](#contribution-workflow)

## Prerequisites

### System Requirements

- **Python**: 3.8+ (3.9 or 3.10 recommended)
- **Git**: Latest version
- **Operating System**: macOS, Linux, or Windows (WSL2 recommended)
- **Memory**: Minimum 4GB RAM, 8GB+ recommended
- **Storage**: 2GB free space for development environment

### Required Accounts and Keys

- **GitHub Account**: For code contributions
- **Anthropic Account**: API key for Claude integration
- **Development API Keys**: Separate keys for development/testing

### Software Installation

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.9+
brew install python@3.9

# Install Git
brew install git

# Optional: Development tools
brew install jq yq curl wget
```

#### Ubuntu/Debian Linux
```bash
# Update package list
sudo apt update

# Install Python 3.9+
sudo apt install python3.9 python3.9-dev python3.9-venv python3-pip

# Install Git
sudo apt install git

# Install development tools
sudo apt install curl wget jq build-essential

# Install yq (YAML processor)
sudo wget -qO /usr/local/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod +x /usr/local/bin/yq
```

#### Windows (WSL2 recommended)
```bash
# Install WSL2 and Ubuntu distribution first
# Then follow Ubuntu instructions above

# Alternative: Use Windows Python
# Download from https://www.python.org/downloads/
# Ensure "Add Python to PATH" is checked during installation
```

## Development Environment Setup

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/your-org/nomad-threat-intel-framework.git
cd nomad-threat-intel-framework

# Set up remote for contributions (if forking)
git remote add upstream https://github.com/original-org/nomad-threat-intel-framework.git

# Create and switch to development branch
git checkout -b dev-setup
```

### 2. Python Environment

```bash
# Create virtual environment
python3.9 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Development Dependencies

Create `requirements-dev.txt`:

```txt
# Development and testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Code quality
black>=23.12.0
isort>=5.13.0
flake8>=6.1.0
mypy>=1.7.0
pylint>=3.0.0

# Development tools
ipython>=8.18.0
jupyter>=1.0.0
pre-commit>=3.6.0

# Documentation
mkdocs>=1.5.3
mkdocs-material>=9.4.0
mkdocs-mermaid2-plugin>=1.1.0

# API testing
httpx>=0.25.0
responses>=0.24.0

# Database tools (if using)
sqlite-utils>=3.35.0

# Performance profiling
py-spy>=0.3.14
memory-profiler>=0.61.0
```

### 4. Environment Configuration

```bash
# Copy development environment template
cp .env.example .env.dev

# Edit development configuration
nano .env.dev
```

Development `.env.dev` example:
```bash
# Development API keys (separate from production)
ANTHROPIC_API_KEY=dev_sk-your-dev-key-here

# Development settings
DEV_MODE=true
USE_TEST_DATA=false
MOCK_APIS=false  # Set to true for offline development
VERBOSE_LOGGING=true
LOG_LEVEL=DEBUG

# Reduced rate limits for development
RATE_LIMIT_RPM=30
API_TIMEOUT=120

# Development directories
OUTPUT_DIR=data/dev-output
INPUT_DIR=data/dev-input
CACHE_DIR=data/dev-cache

# Organization settings for testing
ORG_NAME=DevCorp Test Environment
CROWN_JEWELS=Test Exchange,Test AD,Test Database
BUSINESS_SECTORS=Technology,Testing

# Enable development features
COLLECT_METRICS=true
ENABLE_CACHE=true
CACHE_TTL=1800  # 30 minutes for faster development iteration
```

### 5. Directory Structure Setup

```bash
# Create development directories
mkdir -p {data/{dev-output,dev-input,dev-cache,logs,checkpoints},tests/{unit,integration,fixtures},docs/developer-guide}

# Set up test data directory
mkdir -p tests/fixtures/{rss-feeds,api-responses,sample-data}

# Create development utility directories
mkdir -p utils/{dev-tools,test-helpers,mock-servers}
```

## IDE Configuration

### Visual Studio Code Setup

#### Extensions
```bash
# Install recommended extensions
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-toolsai.jupyter
code --install-extension yzhang.markdown-all-in-one
code --install-extension redhat.vscode-yaml
```

#### VS Code Settings (.vscode/settings.json)
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.envFile": "${workspaceFolder}/.env.dev",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.sorting.provider": "isort",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/venv": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true
    },
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "yaml.schemas": {
        "./schema/rss-feeds-schema.json": "config/rss_feeds.yaml",
        "./schema/agent-config-schema.json": "config/claude_agent_config.yaml"
    }
}
```

#### Launch Configuration (.vscode/launch.json)
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug RSS Agent",
            "type": "python",
            "request": "launch",
            "program": "scripts/run_rss_agent.py",
            "args": ["--single-feed", "https://feeds.feedburner.com/eset/blog", "--verbose", "--use-llm"],
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env.dev"
        },
        {
            "name": "Debug Orchestrator",
            "type": "python",
            "request": "launch",
            "program": "scripts/run_orchestrator.py",
            "args": ["--input", "tests/fixtures/sample-data/rss_output.json", "--verbose"],
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env.dev"
        },
        {
            "name": "Debug Workflow",
            "type": "python",
            "request": "launch",
            "program": "nomad_workflow_enhanced.py",
            "args": ["execute", "morning_check"],
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env.dev"
        },
        {
            "name": "Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"],
            "console": "integratedTerminal",
            "envFile": "${workspaceFolder}/.env.dev"
        }
    ]
}
```

### PyCharm Setup

#### Project Configuration
1. Open PyCharm and create new project from existing sources
2. Select the NOMAD directory
3. Configure Python interpreter:
   - File → Settings → Project → Python Interpreter
   - Add new interpreter → Existing environment
   - Select `venv/bin/python`

#### Environment Variables
1. Run/Debug Configurations
2. Edit configurations
3. Add environment file: `.env.dev`
4. Set working directory to project root

#### Code Style
1. File → Settings → Editor → Code Style → Python
2. Import black configuration or set manually:
   - Line length: 88
   - Use tabs: No
   - Tab size: 4

### Vim/Neovim Setup (for vim users)

#### Basic Configuration
```vim
" Add to .vimrc or init.vim

" Python settings
autocmd FileType python setlocal expandtab shiftwidth=4 softtabstop=4

" Plugin recommendations (using vim-plug)
Plug 'psf/black', { 'branch': 'stable' }
Plug 'fisadev/vim-isort'
Plug 'nvie/vim-flake8'
Plug 'davidhalter/jedi-vim'
Plug 'tpope/vim-fugitive'  " Git integration

" YAML settings
autocmd FileType yaml setlocal expandtab shiftwidth=2 softtabstop=2
```

## Development Tools

### Code Formatting and Linting Setup

#### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
EOF

# Install hooks
pre-commit install
```

#### Configuration Files

**pyproject.toml**:
```toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
  | venv
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["agents", "config", "utils"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = [
    "feedparser.*",
    "anthropic.*",
    "yaml.*",
    "dotenv.*",
    "tabulate.*"
]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
    "api: Tests that require API access"
]
```

**setup.cfg**:
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    build,
    dist,
    .eggs,
    *.egg

[pylint]
max-line-length = 88
disable =
    C0114,  # missing-module-docstring
    C0115,  # missing-class-docstring
    C0116,  # missing-function-docstring
    R0903,  # too-few-public-methods
```

### Development Scripts

Create `scripts/dev-setup.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 NOMAD Development Environment Setup"
echo "======================================"

# Check Python version
python_version=$(python --version 2>&1 | cut -d' ' -f2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version+ required, found $python_version"
    exit 1
fi

echo "✓ Python version OK: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
fi

# Set up pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

# Create development environment file
if [ ! -f ".env.dev" ]; then
    echo "⚙️ Creating development environment file..."
    cp .env.example .env.dev
    echo "✏️ Please edit .env.dev with your development API keys"
fi

# Create development directories
echo "📁 Creating development directories..."
mkdir -p data/{dev-output,dev-input,dev-cache,logs,checkpoints}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p utils/{dev-tools,test-helpers}

# Test basic functionality
echo "🧪 Testing basic functionality..."
if python -c "from agents.rss_feed import RSSFeedAgent; print('✓ RSS Agent import OK')"; then
    echo "✅ Basic import test passed"
else
    echo "❌ Basic import test failed"
    exit 1
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env.dev with your development API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python scripts/run_rss_agent.py --help"
echo "4. Start developing!"
```

Make it executable:
```bash
chmod +x scripts/dev-setup.sh
./scripts/dev-setup.sh
```

## Code Quality Setup

### Automated Quality Checks

Create `scripts/quality-check.sh`:
```bash
#!/bin/bash
set -e

echo "🔍 Running code quality checks..."

# Format code
echo "🎨 Formatting code with black..."
black .

# Sort imports
echo "📦 Sorting imports with isort..."
isort .

# Lint code
echo "🔬 Linting with flake8..."
flake8 .

# Type checking
echo "📝 Type checking with mypy..."
mypy agents/ config/ utils/ --ignore-missing-imports

# Security check (optional)
if command -v bandit &> /dev/null; then
    echo "🔒 Security check with bandit..."
    bandit -r agents/ config/ utils/ -x tests/
fi

echo "✅ All quality checks passed!"
```

### Code Review Checklist

Create `.github/pull_request_template.md`:
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Code Quality
- [ ] Code formatted with black
- [ ] Imports sorted with isort
- [ ] Linting passes (flake8)
- [ ] Type hints added where appropriate
- [ ] Documentation updated

## Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation added where needed
- [ ] Error handling doesn't expose sensitive information

## Checklist
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or they are documented)
- [ ] Backward compatibility maintained
```

## Testing Environment

### Test Data Setup

Create test fixtures:
```bash
# Create sample RSS feed data
mkdir -p tests/fixtures/rss-feeds

cat > tests/fixtures/rss-feeds/sample_feed.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Security Feed</title>
    <description>Sample RSS feed for testing</description>
    <item>
      <title>Critical VMware vCenter Vulnerability CVE-2025-1234</title>
      <link>https://example.com/vuln/1</link>
      <description>A critical vulnerability affecting VMware vCenter Server...</description>
      <pubDate>Fri, 13 Sep 2025 10:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
EOF

# Create sample API responses
mkdir -p tests/fixtures/api-responses

cat > tests/fixtures/api-responses/claude_response.json << 'EOF'
{
  "response": {
    "agent_type": "rss",
    "collected_at_utc": "2025-09-13T10:00:00Z",
    "intelligence": [
      {
        "source_type": "rss",
        "source_name": "Test Feed",
        "title": "Test Vulnerability",
        "cves": ["CVE-2025-1234"],
        "cvss_v3": 9.8,
        "admiralty_source_reliability": "A",
        "admiralty_info_credibility": 2
      }
    ]
  }
}
EOF
```

### Mock Services

Create `tests/fixtures/mock_server.py`:
```python
"""Mock server for testing API integrations."""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import threading
import time
from typing import Dict, Any


class MockAPIHandler(SimpleHTTPRequestHandler):
    """Handler for mock API responses."""

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/v1/messages':
            # Mock Claude API response
            response = {
                "content": [
                    {
                        "text": json.dumps({
                            "agent_type": "test",
                            "processed_at_utc": "2025-09-13T10:00:00Z",
                            "intelligence": []
                        })
                    }
                ]
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


class MockServer:
    """Mock server for testing."""

    def __init__(self, port: int = 8000):
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        """Start the mock server."""
        self.server = HTTPServer(('localhost', self.port), MockAPIHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(0.1)  # Give server time to start

    def stop(self):
        """Stop the mock server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join()
```

### Test Configuration

Create `tests/conftest.py`:
```python
"""Pytest configuration and fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

from config.environment import EnvironmentConfig
from agents.base_agent import BaseAgent


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_env(temp_dir):
    """Mock environment configuration."""
    with patch.dict('os.environ', {
        'ANTHROPIC_API_KEY': 'test-key',
        'OUTPUT_DIR': str(temp_dir / 'output'),
        'INPUT_DIR': str(temp_dir / 'input'),
        'CACHE_DIR': str(temp_dir / 'cache'),
        'LOG_LEVEL': 'DEBUG',
        'DEV_MODE': 'true'
    }):
        config = EnvironmentConfig()
        config.ensure_directories()
        yield config


@pytest.fixture
def mock_claude_api():
    """Mock Claude API client."""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text='{"test": "response"}')]
    mock_client.messages.create.return_value = mock_response

    with patch('anthropic.Anthropic', return_value=mock_client):
        yield mock_client


@pytest.fixture
def sample_rss_data():
    """Sample RSS feed data for testing."""
    return {
        "agent_type": "rss",
        "collected_at_utc": "2025-09-13T10:00:00Z",
        "intelligence": [
            {
                "source_type": "rss",
                "source_name": "Test Feed",
                "source_url": "https://example.com/feed",
                "title": "Test Vulnerability CVE-2025-1234",
                "summary": "A test vulnerability for unit testing",
                "published_utc": "2025-09-13T09:00:00Z",
                "cves": ["CVE-2025-1234"],
                "cvss_v3": 8.5,
                "admiralty_source_reliability": "A",
                "admiralty_info_credibility": 2,
                "dedupe_key": "test-dedupe-key"
            }
        ]
    }
```

## Debugging Setup

### Logging Configuration for Development

Create `utils/dev_logging.py`:
```python
"""Development logging configuration."""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_dev_logging(level: str = "DEBUG", log_to_file: bool = True):
    """Set up enhanced logging for development."""

    # Create formatter with more detail for development
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler with colors (if colorama is available)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File handler for persistent logs
    if log_to_file:
        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"dev_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    root_logger.addHandler(console_handler)

    if log_to_file:
        root_logger.addHandler(file_handler)

    # Configure specific loggers
    logging.getLogger("anthropic").setLevel(logging.INFO)  # Less verbose API logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)  # Even less verbose HTTP

    return root_logger


def debug_agent_execution(agent_name: str, input_data: dict, output_data: dict):
    """Debug helper for agent execution."""
    logger = logging.getLogger(f"nomad.debug.{agent_name}")

    logger.debug(f"Agent {agent_name} starting execution")
    logger.debug(f"Input keys: {list(input_data.keys()) if isinstance(input_data, dict) else type(input_data)}")

    if isinstance(input_data, dict) and 'items' in input_data:
        logger.debug(f"Processing {len(input_data['items'])} items")

    logger.debug(f"Output keys: {list(output_data.keys()) if isinstance(output_data, dict) else type(output_data)}")
    logger.debug(f"Agent {agent_name} completed execution")
```

### Debug Utilities

Create `utils/debug_helpers.py`:
```python
"""Debugging utilities for development."""

import json
import pprint
from typing import Any, Dict
from pathlib import Path


def save_debug_data(data: Any, filename: str, pretty: bool = True):
    """Save data for debugging inspection."""
    debug_dir = Path("data/debug")
    debug_dir.mkdir(parents=True, exist_ok=True)

    file_path = debug_dir / filename

    if isinstance(data, (dict, list)):
        with open(file_path, 'w') as f:
            if pretty:
                json.dump(data, f, indent=2, default=str)
            else:
                json.dump(data, f, default=str)
    else:
        with open(file_path, 'w') as f:
            f.write(str(data))

    print(f"Debug data saved to: {file_path}")


def inspect_data_structure(data: Any, max_depth: int = 3):
    """Inspect and print data structure for debugging."""
    def _inspect(obj, depth=0, max_items=5):
        indent = "  " * depth

        if depth >= max_depth:
            return f"{indent}... (max depth reached)"

        if isinstance(obj, dict):
            result = f"{indent}dict ({len(obj)} items):\n"
            for i, (key, value) in enumerate(obj.items()):
                if i >= max_items:
                    result += f"{indent}  ... ({len(obj) - max_items} more items)\n"
                    break
                result += f"{indent}  {key}: {_inspect(value, depth + 1)}\n"
            return result.rstrip()

        elif isinstance(obj, list):
            result = f"{indent}list ({len(obj)} items):\n"
            for i, item in enumerate(obj[:max_items]):
                result += f"{indent}  [{i}]: {_inspect(item, depth + 1)}\n"
            if len(obj) > max_items:
                result += f"{indent}  ... ({len(obj) - max_items} more items)\n"
            return result.rstrip()

        else:
            return f"{type(obj).__name__}: {str(obj)[:100]}{'...' if len(str(obj)) > 100 else ''}"

    print(_inspect(data))


def compare_agent_outputs(before: Dict, after: Dict, agent_name: str):
    """Compare agent outputs for debugging."""
    print(f"\n=== {agent_name} Output Comparison ===")

    before_keys = set(before.keys()) if isinstance(before, dict) else set()
    after_keys = set(after.keys()) if isinstance(after, dict) else set()

    # Check for new/removed keys
    new_keys = after_keys - before_keys
    removed_keys = before_keys - after_keys

    if new_keys:
        print(f"New keys: {new_keys}")
    if removed_keys:
        print(f"Removed keys: {removed_keys}")

    # Compare common keys
    common_keys = before_keys & after_keys
    for key in common_keys:
        if before[key] != after[key]:
            print(f"Changed: {key}")
            print(f"  Before: {type(before[key]).__name__} = {str(before[key])[:100]}")
            print(f"  After:  {type(after[key]).__name__} = {str(after[key])[:100]}")

    print("=" * 50)
```

## Contribution Workflow

### Git Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-agent-type

# 2. Make changes and commit frequently
git add .
git commit -m "Add new agent type with basic functionality"

# 3. Run quality checks before pushing
scripts/quality-check.sh

# 4. Push to remote
git push origin feature/new-agent-type

# 5. Create pull request on GitHub
# 6. Address review feedback
# 7. Merge after approval
```

### Development Best Practices

1. **Write Tests First**: Use TDD approach when possible
2. **Small Commits**: Make frequent, focused commits
3. **Code Review**: Always get code reviewed before merging
4. **Documentation**: Update docs with new features
5. **Backward Compatibility**: Maintain compatibility when possible

### Release Process

```bash
# 1. Update version
echo "v1.2.0" > VERSION

# 2. Update changelog
git log --oneline v1.1.0..HEAD > CHANGELOG.md

# 3. Run full test suite
pytest tests/ --cov=agents --cov=config --cov=utils

# 4. Tag release
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# 5. Create release notes on GitHub
```

---

## Next Steps

After completing the development setup:

1. **📖 Read [Architecture Overview](architecture.md)** to understand the system design
2. **🧪 Review [Testing Guide](testing.md)** for testing best practices
3. **🏗️ Check [Agent Development Guide](agent-development.md)** to create new agents
4. **📚 Explore [API Documentation](api.md)** for integration details

Your development environment is now ready for contributing to NOMAD!