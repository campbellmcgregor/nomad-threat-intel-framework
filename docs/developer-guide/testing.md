# NOMAD Testing Guide

Comprehensive guide for testing the NOMAD Threat Intelligence Framework, covering unit tests, integration tests, and quality assurance practices.

## Table of Contents

- [Testing Philosophy](#testing-philosophy)
- [Testing Strategy](#testing-strategy)
- [Test Environment Setup](#test-environment-setup)
- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)
- [End-to-End Testing](#end-to-end-testing)
- [API Testing](#api-testing)
- [Performance Testing](#performance-testing)
- [Security Testing](#security-testing)
- [Test Data Management](#test-data-management)
- [Mocking and Fixtures](#mocking-and-fixtures)
- [Test Coverage](#test-coverage)
- [Continuous Integration](#continuous-integration)
- [Testing Best Practices](#testing-best-practices)

## Testing Philosophy

NOMAD follows a comprehensive testing strategy to ensure reliability, security, and performance of threat intelligence processing:

### Core Testing Principles

- **Test-Driven Development**: Write tests before implementing features
- **Fail-Fast**: Tests should catch issues early in development
- **Comprehensive Coverage**: Test all critical paths and edge cases
- **Realistic Data**: Use representative threat intelligence data
- **Automated Testing**: All tests run automatically in CI/CD
- **Security-First**: Every component tested for security vulnerabilities

### Quality Gates

Code must pass these quality gates before deployment:
- ✅ All unit tests pass (100% critical path coverage)
- ✅ Integration tests pass with real API responses
- ✅ Security tests identify no high/critical vulnerabilities
- ✅ Performance tests meet latency/throughput requirements
- ✅ Code style and linting checks pass

## Testing Strategy

### Test Pyramid

```
    /\
   /  \   E2E Tests
  /____\   (Workflow Integration)
 /      \
/  I&T   \ Integration Tests
\________/  (Agent Integration)
/        \
/ Unit    \ Unit Tests
\________/  (Function/Class Level)
```

**Distribution:**
- 70% Unit Tests: Fast, isolated component testing
- 20% Integration Tests: Agent and API integration
- 10% End-to-End Tests: Complete workflow validation

### Test Categories

**Functional Tests**
- Agent logic and data processing
- Workflow orchestration
- Configuration management
- Data validation and sanitization

**Non-Functional Tests**
- Performance and load testing
- Security vulnerability testing
- Reliability and error recovery
- Resource usage and memory leaks

**Compatibility Tests**
- Python version compatibility
- OS platform compatibility
- External API version compatibility
- Configuration format compatibility

## Test Environment Setup

### Dependencies

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock pytest-asyncio
pip install requests-mock responses factory-boy
pip install selenium webdriver-manager  # For E2E tests
pip install bandit safety  # Security testing
pip install locust  # Performance testing
```

### Test Configuration

**pytest.ini**
```ini
[tool:pytest]
minversion = 6.0
addopts =
    -ra
    --strict-markers
    --strict-config
    --cov=agents
    --cov=config
    --cov=utils
    --cov-report=term-missing:skip-covered
    --cov-report=html:htmlcov
    --cov-fail-under=80
testpaths = tests
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    security: Security tests
    performance: Performance tests
```

**conftest.py**
```python
import pytest
import os
import tempfile
from unittest.mock import MagicMock
from agents.base_agent import BaseAgent
from config.environment import EnvironmentConfig

@pytest.fixture(scope="session")
def test_config():
    """Test environment configuration"""
    return {
        'ANTHROPIC_API_KEY': 'test-key-12345',
        'ORG_NAME': 'Test Organization',
        'CROWN_JEWELS': 'Test Server,Test Database',
        'BUSINESS_SECTORS': 'Technology',
        'LOG_LEVEL': 'DEBUG'
    }

@pytest.fixture(scope="session")
def temp_data_dir():
    """Temporary directory for test data"""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ['NOMAD_DATA_DIR'] = tmpdir
        yield tmpdir

@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic Claude client"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock()]
    mock_response.content[0].text = '{"test": "response"}'
    mock_client.messages.create.return_value = mock_response
    return mock_client

@pytest.fixture
def sample_intelligence_item():
    """Sample intelligence item for testing"""
    return {
        "source_type": "rss",
        "source_name": "Test Security Blog",
        "source_url": "https://example.com/feed.xml",
        "title": "Critical Vulnerability in Test Software",
        "summary": "A critical vulnerability affects Test Software versions 1.0-2.0",
        "published_utc": "2025-09-13T10:00:00Z",
        "cves": ["CVE-2025-12345"],
        "cvss_v3": 9.8,
        "kev_listed": True,
        "admiralty_source_reliability": "A",
        "admiralty_info_credibility": 1,
        "admiralty_reason": "Official vendor advisory",
        "dedupe_key": "test-hash-12345"
    }

@pytest.fixture
def sample_rss_feed():
    """Sample RSS feed content"""
    return """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Test Security Feed</title>
            <item>
                <title>Critical Vulnerability CVE-2025-12345</title>
                <description>Critical vulnerability in test software</description>
                <pubDate>Wed, 13 Sep 2025 10:00:00 GMT</pubDate>
                <link>https://example.com/vuln/2025-12345</link>
            </item>
        </channel>
    </rss>"""
```

### Environment Isolation

**Test Environment Variables**
```bash
# .env.test
ANTHROPIC_API_KEY=test-key-12345
NOMAD_ENV=test
LOG_LEVEL=DEBUG
CACHE_ENABLED=false
RATE_LIMITING_ENABLED=false
```

**Environment Setup Script**
```python
# scripts/setup_test_env.py
import os
import shutil
from pathlib import Path

def setup_test_environment():
    """Set up isolated test environment"""

    # Create test directories
    test_dirs = ['data/test', 'logs/test', 'cache/test']
    for directory in test_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Set test environment variables
    os.environ.update({
        'NOMAD_ENV': 'test',
        'NOMAD_DATA_DIR': 'data/test',
        'NOMAD_LOG_DIR': 'logs/test',
        'NOMAD_CACHE_DIR': 'cache/test'
    })

    print("Test environment set up successfully")

if __name__ == "__main__":
    setup_test_environment()
```

## Unit Testing

### Agent Unit Tests

**Example: RSS Feed Agent Tests**
```python
# tests/src/agents/test_rss_feed_agent.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from agents.rss_feed_agent import RSSFeedAgent
from agents.exceptions import ValidationError

class TestRSSFeedAgent:

    @pytest.fixture
    def rss_agent(self, mock_anthropic_client):
        """Initialize RSS agent with mocked dependencies"""
        with patch('agents.base_agent.anthropic.Anthropic') as mock_anthropic:
            mock_anthropic.return_value = mock_anthropic_client
            agent = RSSFeedAgent()
            return agent

    def test_init_agent(self, rss_agent):
        """Test agent initialization"""
        assert rss_agent.agent_name == "rss_feed"
        assert rss_agent.client is not None
        assert hasattr(rss_agent, 'rss_feeds')

    def test_validate_input_valid(self, rss_agent):
        """Test input validation with valid parameters"""
        valid_input = {
            'since': '2025-09-12T00:00:00Z',
            'until': '2025-09-13T00:00:00Z',
            'priority': 'high'
        }
        assert rss_agent.validate_input(valid_input) is True

    def test_validate_input_invalid_date(self, rss_agent):
        """Test input validation with invalid date format"""
        invalid_input = {
            'since': 'invalid-date',
            'until': '2025-09-13T00:00:00Z',
            'priority': 'high'
        }
        with pytest.raises(ValidationError, match="Invalid date format"):
            rss_agent.validate_input(invalid_input)

    def test_validate_input_missing_required(self, rss_agent):
        """Test input validation with missing required fields"""
        invalid_input = {
            'since': '2025-09-12T00:00:00Z'
            # Missing 'until'
        }
        with pytest.raises(ValidationError, match="Missing required field"):
            rss_agent.validate_input(invalid_input)

    def test_extract_cves(self, rss_agent):
        """Test CVE extraction from text"""
        text = "Critical vulnerability CVE-2025-12345 and CVE-2025-67890 found"
        cves = rss_agent._extract_cves(text)
        assert cves == ["CVE-2025-12345", "CVE-2025-67890"]

    def test_extract_cves_no_matches(self, rss_agent):
        """Test CVE extraction with no CVEs in text"""
        text = "No vulnerabilities found in this text"
        cves = rss_agent._extract_cves(text)
        assert cves == []

    def test_assign_admiralty_rating(self, rss_agent):
        """Test Admiralty rating assignment"""
        # Test official source
        rating = rss_agent._assign_admiralty_rating("https://www.cisa.gov/feed")
        assert rating['source_reliability'] == 'A'
        assert rating['info_credibility'] == 1

        # Test community source
        rating = rss_agent._assign_admiralty_rating("https://random-blog.com/feed")
        assert rating['source_reliability'] == 'C'
        assert rating['info_credibility'] >= 2

    @patch('requests.get')
    def test_fetch_rss_feed(self, mock_get, rss_agent, sample_rss_feed):
        """Test RSS feed fetching"""
        mock_response = Mock()
        mock_response.text = sample_rss_feed
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        feed_data = rss_agent._fetch_rss_feed("https://example.com/feed.xml")
        assert 'entries' in feed_data
        assert len(feed_data.entries) == 1
        assert 'CVE-2025-12345' in feed_data.entries[0].title

    @patch('requests.get')
    def test_fetch_rss_feed_error(self, mock_get, rss_agent):
        """Test RSS feed fetching with network error"""
        mock_get.side_effect = Exception("Network error")

        with pytest.raises(Exception, match="Network error"):
            rss_agent._fetch_rss_feed("https://example.com/feed.xml")

    def test_deduplicate_intelligence(self, rss_agent):
        """Test intelligence deduplication"""
        items = [
            {'title': 'Test Alert', 'source_url': 'https://example.com/1', 'dedupe_key': 'hash1'},
            {'title': 'Test Alert', 'source_url': 'https://example.com/1', 'dedupe_key': 'hash1'},
            {'title': 'Different Alert', 'source_url': 'https://example.com/2', 'dedupe_key': 'hash2'}
        ]

        deduped = rss_agent._deduplicate_intelligence(items)
        assert len(deduped) == 2
        assert deduped[0]['dedupe_key'] == 'hash1'
        assert deduped[1]['dedupe_key'] == 'hash2'

    def test_generate_dedupe_key(self, rss_agent):
        """Test dedupe key generation"""
        item = {
            'title': 'Test Alert',
            'source_url': 'https://example.com/alert'
        }

        key1 = rss_agent._generate_dedupe_key(item)
        key2 = rss_agent._generate_dedupe_key(item)

        # Same input should generate same key
        assert key1 == key2
        assert len(key1) == 64  # SHA-256 hex length

    @patch('agents.rss_feed_agent.RSSFeedAgent._fetch_rss_feed')
    def test_run_success(self, mock_fetch, rss_agent, sample_intelligence_item):
        """Test successful agent run"""
        # Mock feed data
        mock_feed = Mock()
        mock_feed.entries = [Mock()]
        mock_feed.entries[0].title = "Critical Vulnerability CVE-2025-12345"
        mock_feed.entries[0].description = "Test description"
        mock_feed.entries[0].published_parsed = None
        mock_feed.entries[0].link = "https://example.com/alert"
        mock_fetch.return_value = mock_feed

        result = rss_agent.run(
            since="2025-09-12T00:00:00Z",
            until="2025-09-13T00:00:00Z",
            priority="high"
        )

        assert result['agent_type'] == 'rss_feed'
        assert 'intelligence' in result
        assert 'stats' in result
        assert isinstance(result['intelligence'], list)

    def test_run_dry_run(self, rss_agent):
        """Test dry run mode"""
        result = rss_agent.run(
            since="2025-09-12T00:00:00Z",
            until="2025-09-13T00:00:00Z",
            dry_run=True
        )

        assert result['status'] == 'dry_run'
        assert result['agent_type'] == 'rss_feed'
        assert 'validation_passed' in result
```

### Configuration Unit Tests

**Example: Environment Configuration Tests**
```python
# tests/src/config/test_environment.py
import pytest
import os
from unittest.mock import patch, MagicMock
from config.environment import EnvironmentConfig
from config.exceptions import ConfigurationError

class TestEnvironmentConfig:

    @pytest.fixture
    def config(self, test_config):
        """Create test configuration"""
        with patch.dict(os.environ, test_config):
            return EnvironmentConfig()

    def test_init_config(self, config):
        """Test configuration initialization"""
        assert config.anthropic_api_key == 'test-key-12345'
        assert config.org_name == 'Test Organization'
        assert config.environment == 'test'

    def test_missing_api_key(self):
        """Test behavior with missing API key"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ConfigurationError, match="ANTHROPIC_API_KEY"):
                EnvironmentConfig()

    def test_validate_api_key_format(self, config):
        """Test API key format validation"""
        # Valid key
        assert config._validate_api_key('sk-ant-api03-' + 'x' * 95) is True

        # Invalid keys
        assert config._validate_api_key('invalid-key') is False
        assert config._validate_api_key('sk-ant-wrong-format') is False

    @patch('anthropic.Anthropic')
    def test_validate_api_access_success(self, mock_anthropic, config):
        """Test successful API access validation"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client

        result = config.validate_api_access()
        assert result['anthropic'] is True

    @patch('anthropic.Anthropic')
    def test_validate_api_access_failure(self, mock_anthropic, config):
        """Test API access validation failure"""
        mock_anthropic.side_effect = Exception("Authentication failed")

        result = config.validate_api_access()
        assert result['anthropic'] is False

    def test_get_organization_context(self, config):
        """Test organization context retrieval"""
        context = config.get_organization_context()

        assert context['name'] == 'Test Organization'
        assert 'Test Server' in context['crown_jewels']
        assert 'Technology' in context['business_sectors']

    def test_get_rss_feeds(self, config):
        """Test RSS feeds configuration"""
        feeds = config.get_rss_feeds()

        assert isinstance(feeds, list)
        assert len(feeds) > 0

        for feed in feeds:
            assert 'name' in feed
            assert 'url' in feed
            assert 'priority' in feed
```

### Utility Function Tests

**Example: Data Validation Tests**
```python
# tests/src/utils/test_validation.py
import pytest
from datetime import datetime
from utils.validation import DataValidator
from utils.exceptions import ValidationError

class TestDataValidator:

    @pytest.fixture
    def validator(self):
        return DataValidator()

    def test_validate_cve_format_valid(self, validator):
        """Test valid CVE format validation"""
        valid_cves = [
            "CVE-2025-12345",
            "CVE-2024-0001",
            "CVE-2023-1234567"
        ]

        for cve in valid_cves:
            assert validator.validate_cve_format(cve) is True

    def test_validate_cve_format_invalid(self, validator):
        """Test invalid CVE format validation"""
        invalid_cves = [
            "CVE-25-12345",      # Wrong year format
            "CVE-2025-123",      # Too few digits
            "CVE-2025-12345678", # Too many digits
            "cve-2025-12345",    # Wrong case
            "CVE-2025-ABCD"      # Non-numeric ID
        ]

        for cve in invalid_cves:
            assert validator.validate_cve_format(cve) is False

    def test_validate_timestamp_valid(self, validator):
        """Test valid timestamp validation"""
        valid_timestamps = [
            "2025-09-13T10:00:00Z",
            "2025-09-13T10:00:00+00:00",
            "2025-09-13T10:00:00.123Z"
        ]

        for timestamp in valid_timestamps:
            assert validator.validate_timestamp(timestamp) is True

    def test_validate_timestamp_invalid(self, validator):
        """Test invalid timestamp validation"""
        invalid_timestamps = [
            "2025-09-13",           # No time
            "2025-13-01T10:00:00Z", # Invalid month
            "invalid-timestamp",     # Not a timestamp
            "2025-09-13 10:00:00"   # Wrong format
        ]

        for timestamp in invalid_timestamps:
            assert validator.validate_timestamp(timestamp) is False

    def test_validate_admiralty_rating_valid(self, validator):
        """Test valid Admiralty rating validation"""
        for rating in ['A', 'B', 'C', 'D', 'E', 'F']:
            assert validator.validate_admiralty_source(rating) is True

        for rating in [1, 2, 3, 4, 5, 6]:
            assert validator.validate_admiralty_info(rating) is True

    def test_validate_admiralty_rating_invalid(self, validator):
        """Test invalid Admiralty rating validation"""
        invalid_sources = ['G', 'a', '1', None, '']
        for rating in invalid_sources:
            assert validator.validate_admiralty_source(rating) is False

        invalid_info = [0, 7, 'A', None, '']
        for rating in invalid_info:
            assert validator.validate_admiralty_info(rating) is False

    def test_sanitize_string(self, validator):
        """Test string sanitization"""
        test_cases = [
            ("Normal text", "Normal text"),
            ("<script>alert('xss')</script>", "[FILTERED]"),
            ("SELECT * FROM users", "[FILTERED]"),
            ("Mixed content <b>bold</b>", "Mixed content &lt;b&gt;bold&lt;/b&gt;")
        ]

        for input_text, expected in test_cases:
            result = validator.sanitize_string(input_text)
            assert expected in result
```

## Integration Testing

### Agent Integration Tests

**Example: RSS Agent Integration Test**
```python
# tests/integration/test_rss_agent_integration.py
import pytest
import responses
from agents.rss_feed_agent import RSSFeedAgent

@pytest.mark.integration
class TestRSSAgentIntegration:

    @responses.activate
    def test_real_feed_processing(self):
        """Test processing real RSS feed with mocked HTTP responses"""

        # Mock RSS feed response
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Security Advisories</title>
                <item>
                    <title>Critical Vulnerability CVE-2025-12345 in Test Software</title>
                    <description>A critical vulnerability has been discovered...</description>
                    <pubDate>Wed, 13 Sep 2025 10:00:00 GMT</pubDate>
                    <link>https://security.example.com/advisory/2025-12345</link>
                </item>
            </channel>
        </rss>"""

        responses.add(
            responses.GET,
            "https://security.example.com/feed.xml",
            body=rss_content,
            status=200,
            content_type='application/rss+xml'
        )

        # Initialize agent
        agent = RSSFeedAgent()

        # Run agent with single feed
        result = agent.run(
            since="2025-09-12T00:00:00Z",
            until="2025-09-14T00:00:00Z",
            single_feed="https://security.example.com/feed.xml",
            use_llm=False  # Skip LLM for integration test
        )

        # Verify results
        assert result['status'] == 'success'
        assert len(result['intelligence']) > 0

        intelligence = result['intelligence'][0]
        assert intelligence['source_type'] == 'rss'
        assert 'CVE-2025-12345' in intelligence['cves']
        assert intelligence['admiralty_source_reliability'] in ['A', 'B', 'C', 'D']

    @responses.activate
    def test_network_timeout_handling(self):
        """Test handling of network timeouts"""
        import requests

        # Mock timeout response
        def timeout_callback(request):
            raise requests.exceptions.Timeout("Request timed out")

        responses.add_callback(
            responses.GET,
            "https://slow-server.example.com/feed.xml",
            callback=timeout_callback
        )

        agent = RSSFeedAgent()

        # Should handle timeout gracefully
        result = agent.run(
            since="2025-09-12T00:00:00Z",
            until="2025-09-14T00:00:00Z",
            single_feed="https://slow-server.example.com/feed.xml"
        )

        assert 'errors' in result
        assert any('timeout' in error['message'].lower() for error in result['errors'])

    @pytest.mark.slow
    def test_large_feed_processing(self):
        """Test processing large RSS feed (performance test)"""

        # Generate large RSS feed
        large_feed = self._generate_large_rss_feed(1000)  # 1000 items

        responses.add(
            responses.GET,
            "https://large-feed.example.com/feed.xml",
            body=large_feed,
            status=200
        )

        agent = RSSFeedAgent()

        import time
        start_time = time.time()

        result = agent.run(
            since="2025-09-12T00:00:00Z",
            until="2025-09-14T00:00:00Z",
            single_feed="https://large-feed.example.com/feed.xml",
            use_llm=False
        )

        processing_time = time.time() - start_time

        # Performance assertions
        assert processing_time < 30  # Should complete in under 30 seconds
        assert len(result['intelligence']) <= 1000
        assert result['status'] == 'success'

    def _generate_large_rss_feed(self, item_count):
        """Generate large RSS feed for testing"""
        items = []
        for i in range(item_count):
            items.append(f"""
                <item>
                    <title>Security Alert {i}: CVE-2025-{10000 + i}</title>
                    <description>Security alert number {i}</description>
                    <pubDate>Wed, 13 Sep 2025 {i % 24:02d}:00:00 GMT</pubDate>
                    <link>https://alerts.example.com/{i}</link>
                </item>
            """)

        return f"""<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Large Security Feed</title>
                {''.join(items)}
            </channel>
        </rss>"""
```

### Workflow Integration Tests

**Example: End-to-End Workflow Test**
```python
# tests/integration/test_workflow_integration.py
import pytest
import tempfile
import json
from pathlib import Path
from nomad_workflow_enhanced import NomadWorkflowEnhanced

@pytest.mark.integration
class TestWorkflowIntegration:

    @pytest.fixture
    def workflow_engine(self, temp_data_dir):
        """Create workflow engine with test configuration"""
        return NomadWorkflowEnhanced(data_dir=temp_data_dir)

    def test_morning_check_workflow(self, workflow_engine):
        """Test complete morning check workflow"""

        # Execute morning check workflow
        result = workflow_engine.execute_workflow(
            'morning_check',
            date_range_days=1,
            priority='medium',
            use_test_mode=True  # Use test data sources
        )

        # Verify workflow completion
        assert result['status'] == 'success'
        assert 'rss_feed_result' in result
        assert 'orchestrator_result' in result

        # Check file outputs
        data_dir = Path(workflow_engine.data_dir)
        output_files = list(data_dir.glob('output/*.json'))
        assert len(output_files) > 0

        # Verify data flow
        rss_output = result['rss_feed_result']
        orchestrator_input = result['orchestrator_result']

        assert len(rss_output['intelligence']) > 0
        assert len(orchestrator_input['decisions']) > 0

    def test_workflow_error_recovery(self, workflow_engine):
        """Test workflow error recovery mechanisms"""

        # Introduce deliberate error (invalid API key)
        with pytest.MonkeyPatch().context() as mp:
            mp.setenv('ANTHROPIC_API_KEY', 'invalid-key')

            result = workflow_engine.execute_workflow(
                'morning_check',
                date_range_days=1
            )

            # Should handle error gracefully
            assert 'errors' in result
            assert result['status'] in ['partial', 'failure']

            # Check recovery actions
            if 'recovery_actions' in result:
                assert len(result['recovery_actions']) > 0

    @pytest.mark.slow
    def test_weekly_report_workflow(self, workflow_engine):
        """Test weekly report generation workflow"""

        # Create sample decision data
        sample_decisions = self._create_sample_decisions()
        decisions_file = Path(workflow_engine.data_dir) / 'test_decisions.json'

        with open(decisions_file, 'w') as f:
            json.dump(sample_decisions, f)

        # Execute weekly report workflow
        result = workflow_engine.execute_workflow(
            'weekly_report',
            week_start='2025-09-07',
            week_end='2025-09-13',
            decisions_file=str(decisions_file)
        )

        assert result['status'] == 'success'
        assert 'ciso_report' in result

        # Verify report content
        report = result['ciso_report']
        assert 'executive_summary' in report
        assert 'threat_landscape' in report
        assert 'recommendations' in report

    def _create_sample_decisions(self):
        """Create sample routing decisions for testing"""
        return {
            'decisions': [
                {
                    'intelligence_id': 'test-001',
                    'routing_decision': 'TECHNICAL_ALERT',
                    'reasoning': 'KEV-listed vulnerability',
                    'owner_team': 'SOC',
                    'sla_hours': 24,
                    'priority': 'P1'
                },
                {
                    'intelligence_id': 'test-002',
                    'routing_decision': 'CISO_REPORT',
                    'reasoning': 'High business impact',
                    'owner_team': 'CISO',
                    'sla_hours': 48,
                    'priority': 'P2'
                }
            ]
        }
```

## End-to-End Testing

### Workflow E2E Tests

**Example: Complete Intelligence Pipeline Test**
```python
# tests/e2e/test_intelligence_pipeline.py
import pytest
import os
import time
from pathlib import Path

@pytest.mark.e2e
class TestIntelligencePipelineE2E:

    @pytest.mark.slow
    def test_complete_pipeline(self, temp_data_dir):
        """Test complete intelligence processing pipeline"""

        # Set up test environment
        os.environ['NOMAD_DATA_DIR'] = temp_data_dir
        os.environ['NOMAD_ENV'] = 'test'

        # Import modules after environment setup
        from nomad_workflow_enhanced import NomadWorkflowEnhanced

        workflow = NomadWorkflowEnhanced()

        # Step 1: Collect intelligence
        print("Step 1: Collecting intelligence...")
        rss_result = workflow.execute_agent_direct(
            'rss_feed',
            since='2025-09-12T00:00:00Z',
            until='2025-09-13T00:00:00Z',
            priority='high',
            use_llm=True
        )

        assert rss_result['status'] == 'success'
        assert len(rss_result['intelligence']) > 0

        # Step 2: Route intelligence
        print("Step 2: Routing intelligence...")
        orchestrator_result = workflow.execute_agent_direct(
            'orchestrator',
            input_data=rss_result['intelligence']
        )

        assert orchestrator_result['status'] == 'success'
        assert len(orchestrator_result['decisions']) > 0

        # Step 3: Generate outputs
        print("Step 3: Generating outputs...")

        # Technical alerts
        tech_alert_result = workflow.execute_agent_direct(
            'technical_alert',
            input_data=[d for d in orchestrator_result['decisions']
                       if d['routing_decision'] == 'TECHNICAL_ALERT']
        )

        # CISO report (if applicable)
        ciso_decisions = [d for d in orchestrator_result['decisions']
                         if d['routing_decision'] == 'CISO_REPORT']

        if ciso_decisions:
            ciso_result = workflow.execute_agent_direct(
                'ciso_report',
                week_start='2025-09-07',
                week_end='2025-09-13',
                decisions=ciso_decisions
            )
            assert ciso_result['status'] == 'success'

        # Verify outputs
        data_dir = Path(temp_data_dir)
        output_files = list(data_dir.glob('output/*.json'))
        assert len(output_files) >= 2  # At least RSS and orchestrator outputs

        print(f"E2E test completed successfully. Generated {len(output_files)} output files.")

    def test_error_scenarios(self):
        """Test pipeline behavior under error conditions"""

        from nomad_workflow_enhanced import NomadWorkflowEnhanced
        workflow = NomadWorkflowEnhanced()

        # Test with invalid date range
        result = workflow.execute_agent_direct(
            'rss_feed',
            since='invalid-date',
            until='2025-09-13T00:00:00Z'
        )

        assert result['status'] == 'failure'
        assert 'errors' in result

        # Test with missing required parameters
        result = workflow.execute_agent_direct(
            'orchestrator'
            # Missing input_data
        )

        assert result['status'] == 'failure'
        assert 'validation' in str(result.get('errors', [])).lower()
```

## API Testing

### REST API Testing

**Example: API Endpoint Tests**
```python
# tests/api/test_api_endpoints.py
import pytest
import json
from unittest.mock import patch
from flask import Flask
from api.nomad_api import create_app

@pytest.fixture
def client():
    """Create test Flask client"""
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_headers():
    """Authentication headers for API requests"""
    return {
        'Authorization': 'Bearer test-api-key',
        'Content-Type': 'application/json'
    }

class TestIntelligenceAPI:

    def test_collect_intelligence_endpoint(self, client, auth_headers):
        """Test intelligence collection endpoint"""

        request_data = {
            'since': '2025-09-12T00:00:00Z',
            'until': '2025-09-13T00:00:00Z',
            'priority': 'high'
        }

        with patch('agents.rss_feed_agent.RSSFeedAgent.run') as mock_run:
            mock_run.return_value = {
                'status': 'success',
                'intelligence': [
                    {
                        'source_type': 'rss',
                        'title': 'Test Alert',
                        'cves': ['CVE-2025-12345']
                    }
                ]
            }

            response = client.post(
                '/api/v1/intelligence/collect',
                data=json.dumps(request_data),
                headers=auth_headers
            )

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert len(data['intelligence']) > 0

    def test_collect_intelligence_validation_error(self, client, auth_headers):
        """Test API validation error handling"""

        # Invalid request (missing required fields)
        request_data = {
            'since': '2025-09-12T00:00:00Z'
            # Missing 'until'
        }

        response = client.post(
            '/api/v1/intelligence/collect',
            data=json.dumps(request_data),
            headers=auth_headers
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] is True
        assert 'validation' in data['message'].lower()

    def test_unauthorized_access(self, client):
        """Test API access without authentication"""

        request_data = {
            'since': '2025-09-12T00:00:00Z',
            'until': '2025-09-13T00:00:00Z'
        }

        response = client.post(
            '/api/v1/intelligence/collect',
            data=json.dumps(request_data),
            headers={'Content-Type': 'application/json'}
        )

        assert response.status_code == 401

    def test_rate_limiting(self, client, auth_headers):
        """Test API rate limiting"""

        request_data = {
            'since': '2025-09-12T00:00:00Z',
            'until': '2025-09-13T00:00:00Z'
        }

        # Make multiple rapid requests
        for i in range(10):
            response = client.post(
                '/api/v1/intelligence/collect',
                data=json.dumps(request_data),
                headers=auth_headers
            )

            if response.status_code == 429:  # Too Many Requests
                data = json.loads(response.data)
                assert 'rate limit' in data['message'].lower()
                break
        else:
            pytest.skip("Rate limiting not triggered in test environment")
```

## Performance Testing

### Load Testing with Locust

**Example: Load Test Configuration**
```python
# tests/performance/locustfile.py
from locust import HttpUser, task, between
import json
import random

class NomadAPIUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Set up authentication"""
        self.headers = {
            'Authorization': 'Bearer test-api-key',
            'Content-Type': 'application/json'
        }

    @task(3)
    def collect_intelligence(self):
        """Test intelligence collection endpoint (most common operation)"""
        request_data = {
            'since': '2025-09-12T00:00:00Z',
            'until': '2025-09-13T00:00:00Z',
            'priority': random.choice(['low', 'medium', 'high'])
        }

        self.client.post(
            '/api/v1/intelligence/collect',
            data=json.dumps(request_data),
            headers=self.headers
        )

    @task(1)
    def route_intelligence(self):
        """Test intelligence routing endpoint"""
        # Sample intelligence data
        intelligence_data = [
            {
                'source_type': 'rss',
                'title': f'Test Alert {random.randint(1, 1000)}',
                'cves': [f'CVE-2025-{random.randint(10000, 99999)}']
            }
        ]

        self.client.post(
            '/api/v1/intelligence/route',
            data=json.dumps({'intelligence': intelligence_data}),
            headers=self.headers
        )

    @task(1)
    def get_agent_status(self):
        """Test agent status endpoint"""
        self.client.get(
            '/api/v1/src/agents/status',
            headers=self.headers
        )

# Run with: locust -f locustfile.py --host=http://localhost:5000
```

### Performance Benchmarks

**Example: Agent Performance Tests**
```python
# tests/performance/test_agent_performance.py
import pytest
import time
import psutil
import os
from agents.rss_feed_agent import RSSFeedAgent

@pytest.mark.performance
class TestAgentPerformance:

    def test_rss_agent_processing_speed(self):
        """Test RSS agent processing performance"""
        agent = RSSFeedAgent()

        # Monitor resource usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        start_time = time.time()

        # Process large dataset
        result = agent.run(
            since='2025-09-01T00:00:00Z',
            until='2025-09-13T00:00:00Z',
            priority='all',
            use_llm=False  # Skip LLM for pure processing test
        )

        end_time = time.time()
        processing_time = end_time - start_time
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_usage = final_memory - initial_memory

        # Performance assertions
        items_processed = len(result['intelligence'])
        items_per_second = items_processed / processing_time

        assert items_per_second > 10, f"Too slow: {items_per_second:.2f} items/sec"
        assert memory_usage < 100, f"Memory usage too high: {memory_usage:.2f} MB"
        assert processing_time < 30, f"Processing too slow: {processing_time:.2f} seconds"

        print(f"Performance metrics:")
        print(f"  Items processed: {items_processed}")
        print(f"  Processing time: {processing_time:.2f} seconds")
        print(f"  Items per second: {items_per_second:.2f}")
        print(f"  Memory usage: {memory_usage:.2f} MB")

    def test_concurrent_agent_execution(self):
        """Test multiple agents running concurrently"""
        import concurrent.futures
        import threading

        def run_agent(agent_id):
            agent = RSSFeedAgent()
            start_time = time.time()

            result = agent.run(
                since='2025-09-12T00:00:00Z',
                until='2025-09-13T00:00:00Z',
                use_llm=False
            )

            end_time = time.time()
            return {
                'agent_id': agent_id,
                'processing_time': end_time - start_time,
                'items_processed': len(result['intelligence']),
                'status': result['status']
            }

        # Run 5 agents concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(run_agent, i) for i in range(5)]
            results = [future.result() for future in futures]

        # All agents should complete successfully
        for result in results:
            assert result['status'] == 'success'
            assert result['processing_time'] < 60  # Each should complete within 60 seconds

        # Total processing time should be less than sequential
        total_concurrent_time = max(r['processing_time'] for r in results)
        assert total_concurrent_time < 120, "Concurrent execution too slow"

        print(f"Concurrent execution results:")
        for result in results:
            print(f"  Agent {result['agent_id']}: {result['processing_time']:.2f}s, "
                  f"{result['items_processed']} items")
```

## Security Testing

### Security Vulnerability Tests

**Example: Security Test Suite**
```python
# tests/security/test_security_vulnerabilities.py
import pytest
import os
import subprocess
import json
from agents.rss_feed_agent import RSSFeedAgent
from utils.validation import DataValidator

@pytest.mark.security
class TestSecurityVulnerabilities:

    def test_sql_injection_protection(self):
        """Test protection against SQL injection attacks"""
        validator = DataValidator()

        # Test SQL injection payloads
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM passwords --",
            "'; INSERT INTO admin VALUES ('hacker', 'password'); --"
        ]

        for payload in sql_injection_payloads:
            # Should sanitize or reject malicious input
            sanitized = validator.sanitize_string(payload)
            assert '[FILTERED]' in sanitized or payload != sanitized

    def test_xss_protection(self):
        """Test protection against XSS attacks"""
        validator = DataValidator()

        xss_payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>"
        ]

        for payload in xss_payloads:
            sanitized = validator.sanitize_string(payload)
            assert '<script>' not in sanitized.lower()
            assert 'javascript:' not in sanitized.lower()
            assert 'onerror=' not in sanitized.lower()

    def test_api_key_exposure(self):
        """Test that API keys are not exposed in logs or outputs"""
        agent = RSSFeedAgent()

        # Run agent and check output
        result = agent.run(
            since='2025-09-12T00:00:00Z',
            until='2025-09-13T00:00:00Z',
            dry_run=True
        )

        # Convert result to string for inspection
        result_str = json.dumps(result, indent=2)

        # Should not contain actual API keys
        assert 'sk-ant-api03-' not in result_str
        assert os.getenv('ANTHROPIC_API_KEY', '') not in result_str

    def test_path_traversal_protection(self):
        """Test protection against path traversal attacks"""
        from utils.file_handler import FileHandler

        handler = FileHandler()

        # Test path traversal payloads
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "/etc/shadow",
            "../../../../root/.ssh/id_rsa"
        ]

        for path in malicious_paths:
            with pytest.raises(ValueError, match="Invalid path"):
                handler.safe_read(path)

    def test_command_injection_protection(self):
        """Test protection against command injection"""
        from utils.command_executor import SafeCommandExecutor

        executor = SafeCommandExecutor()

        # Test command injection payloads
        malicious_commands = [
            "ls; rm -rf /",
            "cat /etc/passwd",
            "python -c 'import os; os.system(\"rm -rf /\")'",
            "ping google.com && cat /etc/shadow"
        ]

        for command in malicious_commands:
            with pytest.raises(ValueError, match="Command not allowed|Invalid command"):
                executor.execute_safe_command(command)

    def test_secrets_in_logs(self, caplog):
        """Test that secrets are not logged"""
        import logging

        # Set up logging capture
        caplog.set_level(logging.DEBUG)

        # Initialize agent (which might log configuration)
        agent = RSSFeedAgent()

        # Check all log messages
        for record in caplog.records:
            message = record.getMessage()

            # Should not contain API keys
            assert 'sk-ant-api03-' not in message
            assert 'password' not in message.lower()
            assert 'secret' not in message.lower()

    def test_file_permissions(self):
        """Test that sensitive files have correct permissions"""
        import stat

        sensitive_files = [
            '.env',
            'src/config/secrets.yml',
            'logs/security_audit.log'
        ]

        for file_path in sensitive_files:
            if os.path.exists(file_path):
                file_stat = os.stat(file_path)
                permissions = oct(file_stat.st_mode)[-3:]

                # Should not be world-readable
                assert permissions[2] != '7'  # No world write/execute
                assert permissions[2] not in ['4', '5', '6', '7']  # No world read

    @pytest.mark.skipif(not os.path.exists('requirements.txt'),
                       reason="requirements.txt not found")
    def test_dependency_vulnerabilities(self):
        """Test for known vulnerabilities in dependencies"""

        # Run safety check on dependencies
        result = subprocess.run(
            ['safety', 'check', '--json'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("No known vulnerabilities found in dependencies")
        else:
            # Parse safety output
            if result.stdout:
                try:
                    vulnerabilities = json.loads(result.stdout)
                    if vulnerabilities:
                        pytest.fail(f"Found {len(vulnerabilities)} dependency vulnerabilities")
                except json.JSONDecodeError:
                    # safety might return non-JSON output
                    if 'vulnerabilities found' in result.stdout.lower():
                        pytest.fail("Dependency vulnerabilities found (check safety output)")

    def test_static_code_analysis(self):
        """Run static security analysis with bandit"""

        # Run bandit security analysis
        result = subprocess.run(
            ['bandit', '-r', 'src/agents/', 'src/config/', 'src/utils/', '-f', 'json'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("No security issues found in static analysis")
        else:
            try:
                bandit_output = json.loads(result.stdout)

                # Filter out low confidence issues
                high_severity_issues = [
                    issue for issue in bandit_output.get('results', [])
                    if issue['issue_severity'] in ['HIGH', 'MEDIUM']
                ]

                if high_severity_issues:
                    issue_summary = "\n".join([
                        f"  {issue['filename']}:{issue['line_number']} - {issue['issue_text']}"
                        for issue in high_severity_issues
                    ])
                    pytest.fail(f"Security issues found:\n{issue_summary}")

            except json.JSONDecodeError:
                if 'issue' in result.stdout.lower():
                    pytest.fail("Security analysis failed (check bandit output)")
```

## Test Data Management

### Test Data Factories

**Example: Intelligence Data Factory**
```python
# tests/factories/intelligence_factory.py
import factory
import random
from datetime import datetime, timedelta
from factory import Faker, LazyAttribute

class IntelligenceItemFactory(factory.Factory):
    """Factory for generating test intelligence items"""

    class Meta:
        model = dict

    source_type = factory.Iterator(['rss', 'vendor', 'cert'])
    source_name = Faker('company')
    source_url = Faker('url')
    title = LazyAttribute(lambda obj: f"Security Alert: CVE-{random.randint(2020, 2025)}-{random.randint(1000, 99999)}")
    summary = Faker('text', max_nb_chars=200)
    published_utc = LazyAttribute(lambda obj:
        (datetime.utcnow() - timedelta(days=random.randint(0, 30))).isoformat() + 'Z')

    cves = LazyAttribute(lambda obj: [f"CVE-{random.randint(2020, 2025)}-{random.randint(1000, 99999)}"])
    cvss_v3 = LazyAttribute(lambda obj: round(random.uniform(0.1, 10.0), 1))
    epss = LazyAttribute(lambda obj: round(random.uniform(0.0, 1.0), 3))
    kev_listed = Faker('boolean')

    admiralty_source_reliability = factory.Iterator(['A', 'B', 'C', 'D'])
    admiralty_info_credibility = factory.Iterator([1, 2, 3, 4])
    admiralty_reason = Faker('sentence')

    dedupe_key = Faker('sha256')

# Usage in tests
def test_with_sample_data():
    # Generate single item
    item = IntelligenceItemFactory()

    # Generate multiple items
    items = IntelligenceItemFactory.create_batch(10)

    # Generate with specific attributes
    high_severity_item = IntelligenceItemFactory(cvss_v3=9.5, kev_listed=True)
```

### Test Data Sets

**Example: Predefined Test Data**
```python
# tests/data/sample_data.py
SAMPLE_RSS_FEEDS = [
    {
        "name": "Test Security Blog",
        "url": "https://test-security.example.com/feed.xml",
        "content": """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Test Security Blog</title>
                <item>
                    <title>Critical Vulnerability CVE-2025-12345</title>
                    <description>A critical vulnerability has been discovered...</description>
                    <pubDate>Wed, 13 Sep 2025 10:00:00 GMT</pubDate>
                    <link>https://test-security.example.com/cve-2025-12345</link>
                </item>
            </channel>
        </rss>"""
    }
]

SAMPLE_INTELLIGENCE_ITEMS = [
    {
        "source_type": "rss",
        "source_name": "CISA Known Exploited Vulnerabilities",
        "source_url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "title": "CISA Adds CVE-2025-12345 to Known Exploited Vulnerabilities Catalog",
        "summary": "CISA has added CVE-2025-12345 affecting Windows systems to the KEV catalog",
        "published_utc": "2025-09-13T08:00:00Z",
        "cves": ["CVE-2025-12345"],
        "cvss_v3": 9.8,
        "epss": 0.85,
        "kev_listed": True,
        "kev_date_added": "2025-09-13",
        "exploit_status": "ITW",
        "admiralty_source_reliability": "A",
        "admiralty_info_credibility": 1,
        "admiralty_reason": "Official CISA advisory",
        "dedupe_key": "sha256_hash_of_title_and_url"
    }
]

SAMPLE_ROUTING_DECISIONS = [
    {
        "intelligence_id": "test-001",
        "routing_decision": "TECHNICAL_ALERT",
        "reasoning": "KEV-listed vulnerability with active exploitation",
        "owner_team": "SOC",
        "sla_hours": 24,
        "priority": "P0",
        "business_impact": "Critical"
    }
]
```

## Mocking and Fixtures

### External API Mocks

**Example: Anthropic API Mock**
```python
# tests/mocks/anthropic_mock.py
import json
from unittest.mock import MagicMock

class MockAnthropicClient:
    """Mock Anthropic Claude client for testing"""

    def __init__(self):
        self.messages = MagicMock()
        self.usage_stats = {
            'total_requests': 0,
            'total_tokens': 0
        }

    def create_message_response(self, content_text):
        """Create mock response with specified content"""
        response = MagicMock()
        response.content = [MagicMock()]
        response.content[0].text = content_text
        response.usage = MagicMock()
        response.usage.input_tokens = 100
        response.usage.output_tokens = 50

        # Track usage
        self.usage_stats['total_requests'] += 1
        self.usage_stats['total_tokens'] += 150

        return response

    def setup_rss_agent_response(self):
        """Set up mock response for RSS agent"""
        mock_response = {
            "agent_type": "rss_feed",
            "timestamp": "2025-09-13T10:00:00Z",
            "intelligence": [
                {
                    "source_type": "rss",
                    "title": "Mock Security Alert",
                    "cves": ["CVE-2025-12345"],
                    "admiralty_source_reliability": "B",
                    "admiralty_info_credibility": 2
                }
            ]
        }

        self.messages.create.return_value = self.create_message_response(
            json.dumps(mock_response, indent=2)
        )

    def setup_orchestrator_response(self):
        """Set up mock response for orchestrator"""
        mock_response = {
            "decisions": [
                {
                    "intelligence_id": "mock-001",
                    "routing_decision": "TECHNICAL_ALERT",
                    "reasoning": "Mock reasoning",
                    "owner_team": "SOC",
                    "sla_hours": 24
                }
            ]
        }

        self.messages.create.return_value = self.create_message_response(
            json.dumps(mock_response, indent=2)
        )

    def simulate_api_error(self, error_type='rate_limit'):
        """Simulate API errors for testing"""
        if error_type == 'rate_limit':
            from anthropic import RateLimitError
            self.messages.create.side_effect = RateLimitError("Rate limit exceeded")
        elif error_type == 'auth':
            from anthropic import AuthenticationError
            self.messages.create.side_effect = AuthenticationError("Invalid API key")
        elif error_type == 'network':
            self.messages.create.side_effect = Exception("Network error")
```

### Response Fixtures

**Example: HTTP Response Fixtures**
```python
# tests/fixtures/http_fixtures.py
import responses
import json

class HTTPFixtures:
    """HTTP response fixtures for testing"""

    @staticmethod
    def setup_rss_feed_responses():
        """Set up RSS feed HTTP responses"""

        # CISA KEV feed
        responses.add(
            responses.GET,
            "https://www.cisa.gov/known-exploited-vulnerabilities-catalog.xml",
            body="""<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
                <channel>
                    <title>CISA KEV Catalog</title>
                    <item>
                        <title>CISA Adds CVE-2025-12345</title>
                        <description>Critical Windows vulnerability</description>
                        <pubDate>Wed, 13 Sep 2025 08:00:00 GMT</pubDate>
                    </item>
                </channel>
            </rss>""",
            status=200,
            content_type='application/rss+xml'
        )

        # NVD CVE feed
        responses.add(
            responses.GET,
            "https://nvd.nist.gov/vuln/data-feeds/xml/cve/misc/nvd-rss.xml",
            body="""<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
                <channel>
                    <title>NVD - Recent CVE</title>
                    <item>
                        <title>CVE-2025-67890</title>
                        <description>Remote code execution vulnerability</description>
                        <pubDate>Wed, 13 Sep 2025 12:00:00 GMT</pubDate>
                    </item>
                </channel>
            </rss>""",
            status=200
        )

    @staticmethod
    def setup_api_error_responses():
        """Set up error responses for testing"""

        # Timeout simulation
        responses.add(
            responses.GET,
            "https://slow-server.example.com/feed.xml",
            body=responses.ConnectionError("Request timed out")
        )

        # 404 Not Found
        responses.add(
            responses.GET,
            "https://missing-feed.example.com/feed.xml",
            status=404,
            body="Not Found"
        )

        # 500 Server Error
        responses.add(
            responses.GET,
            "https://broken-server.example.com/feed.xml",
            status=500,
            body="Internal Server Error"
        )
```

## Test Coverage

### Coverage Configuration

**Example: Coverage Settings**
```ini
# .coveragerc
[run]
source = agents, config, utils
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

show_missing = True
skip_covered = False
precision = 2

[html]
directory = htmlcov
```

### Coverage Analysis

**Example: Coverage Analysis Script**
```python
# scripts/analyze_coverage.py
import subprocess
import json
import sys

def run_coverage_analysis():
    """Run coverage analysis and generate report"""

    print("Running test suite with coverage...")

    # Run tests with coverage
    result = subprocess.run([
        'pytest',
        '--cov=agents',
        '--cov=config',
        '--cov=utils',
        '--cov-report=json:coverage.json',
        '--cov-report=html:htmlcov',
        '--cov-report=term-missing',
        'tests/'
    ], capture_output=True, text=True)

    print(result.stdout)

    # Load coverage data
    try:
        with open('coverage.json', 'r') as f:
            coverage_data = json.load(f)

        total_coverage = coverage_data['totals']['percent_covered']

        print(f"\nOverall Coverage: {total_coverage:.1f}%")

        # Analyze by module
        print("\nCoverage by Module:")
        for filename, data in coverage_data['files'].items():
            coverage_percent = (data['summary']['covered_lines'] /
                              data['summary']['num_statements'] * 100)
            print(f"  {filename}: {coverage_percent:.1f}%")

        # Check coverage threshold
        if total_coverage < 80:
            print(f"\nWARNING: Coverage {total_coverage:.1f}% is below 80% threshold")
            sys.exit(1)
        else:
            print(f"\nSUCCESS: Coverage {total_coverage:.1f}% meets requirements")

    except FileNotFoundError:
        print("ERROR: Coverage data not found")
        sys.exit(1)

if __name__ == "__main__":
    run_coverage_analysis()
```

## Continuous Integration

### GitHub Actions Workflow

**Example: CI/CD Pipeline**
```yaml
# .github/workflows/tests.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y libxml2-dev libxslt-dev

    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Lint with flake8
      run: |
        flake8 agents config utils --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 agents config utils --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

    - name: Type checking with mypy
      run: |
        mypy agents config utils

    - name: Security analysis with bandit
      run: |
        bandit -r agents config utils

    - name: Test with pytest
      env:
        ANTHROPIC_API_KEY: ${{ secrets.TEST_ANTHROPIC_API_KEY }}
        NOMAD_ENV: test
      run: |
        pytest tests/ -v --cov=agents --cov=config --cov=utils --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  integration-tests:
    runs-on: ubuntu-latest
    needs: test

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Run integration tests
      env:
        ANTHROPIC_API_KEY: ${{ secrets.TEST_ANTHROPIC_API_KEY }}
        NOMAD_ENV: test
      run: |
        pytest tests/integration/ -v -m integration

  security-tests:
    runs-on: ubuntu-latest
    needs: test

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install safety bandit

    - name: Run security tests
      run: |
        safety check
        bandit -r agents config utils -f json -o bandit-report.json

    - name: Upload security report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-report
        path: bandit-report.json

  performance-tests:
    runs-on: ubuntu-latest
    needs: test

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install locust pytest-benchmark

    - name: Run performance tests
      env:
        ANTHROPIC_API_KEY: ${{ secrets.TEST_ANTHROPIC_API_KEY }}
        NOMAD_ENV: test
      run: |
        pytest tests/performance/ -v -m performance --benchmark-only
```

## Testing Best Practices

### Test Organization

**Directory Structure**
```
tests/
├── unit/                   # Unit tests
│   ├── src/agents/
│   ├── src/config/
│   └── src/utils/
├── integration/            # Integration tests
│   ├── test_agent_integration.py
│   └── test_workflow_integration.py
├── e2e/                    # End-to-end tests
│   └── test_complete_pipeline.py
├── performance/            # Performance tests
│   ├── locustfile.py
│   └── test_benchmarks.py
├── security/               # Security tests
│   └── test_vulnerabilities.py
├── api/                    # API tests
│   └── test_api_endpoints.py
├── fixtures/               # Test fixtures
│   ├── sample_data.py
│   └── http_fixtures.py
├── mocks/                  # Mock objects
│   └── anthropic_mock.py
└── factories/              # Data factories
    └── intelligence_factory.py
```

### Test Naming Conventions

```python
def test_<unit_under_test>_<scenario>_<expected_behavior>():
    """
    Examples:
    - test_rss_agent_valid_input_returns_intelligence()
    - test_validator_invalid_cve_format_raises_error()
    - test_orchestrator_kev_vulnerability_routes_to_technical_alert()
    """
    pass
```

### Test Documentation

```python
def test_complex_scenario(self):
    """
    Test Description:
    Verify that the RSS agent correctly processes intelligence items
    when multiple CVEs are present in a single RSS entry.

    Test Steps:
    1. Create RSS feed with multi-CVE entry
    2. Process feed through RSS agent
    3. Verify all CVEs are extracted
    4. Verify deduplication works correctly

    Expected Results:
    - All CVEs should be extracted
    - Each CVE should have proper formatting
    - Deduplication should preserve unique items
    """
    pass
```

### Common Testing Patterns

**Arrange-Act-Assert Pattern**
```python
def test_agent_processing():
    # Arrange
    agent = RSSFeedAgent()
    test_data = create_test_intelligence_item()

    # Act
    result = agent.process_intelligence(test_data)

    # Assert
    assert result['status'] == 'success'
    assert len(result['intelligence']) > 0
```

**Test Fixtures for Common Setup**
```python
@pytest.fixture
def configured_agent():
    """Common agent setup used across multiple tests"""
    with patch.dict(os.environ, TEST_CONFIG):
        agent = RSSFeedAgent()
        agent.setup_test_mode()
        return agent

def test_with_fixture(configured_agent):
    result = configured_agent.run(test_parameters)
    assert result['status'] == 'success'
```

**Parameterized Tests**
```python
@pytest.mark.parametrize("cve,expected", [
    ("CVE-2025-12345", True),
    ("CVE-25-12345", False),
    ("cve-2025-12345", False),
    ("CVE-2025-ABCD", False),
])
def test_cve_validation(cve, expected):
    validator = DataValidator()
    assert validator.validate_cve_format(cve) == expected
```

---

This comprehensive testing guide provides the framework and examples needed to thoroughly test the NOMAD Threat Intelligence Framework. Regular execution of these tests ensures system reliability, security, and performance as the framework evolves.