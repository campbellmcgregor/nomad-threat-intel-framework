# NOMAD Performance and Optimization Guide

Comprehensive guide for optimizing performance and scalability in the NOMAD Threat Intelligence Framework.

## Table of Contents

- [Performance Overview](#performance-overview)
- [Performance Metrics](#performance-metrics)
- [System Monitoring](#system-monitoring)
- [Application Optimization](#application-optimization)
- [Memory Management](#memory-management)
- [API Performance](#api-performance)
- [Caching Strategies](#caching-strategies)
- [Network Optimization](#network-optimization)
- [Database Optimization](#database-optimization)
- [Scaling Strategies](#scaling-strategies)
- [Resource Usage](#resource-usage)
- [Code Optimization](#code-optimization)
- [Performance Testing](#performance-testing)
- [Troubleshooting](#troubleshooting)
- [Capacity Planning](#capacity-planning)
- [Best Practices](#best-practices)

## Performance Overview

NOMAD's performance characteristics directly impact threat intelligence processing speed, system responsiveness, and operational efficiency. Optimal performance ensures timely threat detection and response.

### Performance Goals

**Processing Throughput**
- RSS feeds: 1000+ items per hour
- Intelligence routing: 500+ decisions per hour
- Report generation: Sub-minute for standard reports
- API response times: <2 seconds for typical requests

**Resource Efficiency**
- Memory usage: <2GB for standard deployments
- CPU utilization: <70% during peak processing
- Disk I/O: Minimal impact on system performance
- Network usage: Efficient API calls with proper caching

**Scalability Targets**
- Horizontal scaling: Support for 10+ concurrent agents
- Data volume: Handle 10,000+ intelligence items per day
- User load: Support 50+ concurrent users
- Geographic distribution: Multi-region deployment capability

### Performance Architecture

```
┌─────────────────────────────────────────────┐
│                Load Balancer                │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐    ┌───▼───┐    ┌───▼───┐
│Agent 1│    │Agent 2│    │Agent 3│
└───┬───┘    └───┬───┘    └───┬───┘
    │            │            │
    └─────────┬──┼──┬─────────┘
              │     │
        ┌─────▼─┐ ┌─▼──────┐
        │Cache  │ │Database│
        └───────┘ └────────┘
```

## Performance Metrics

### Key Performance Indicators (KPIs)

**Throughput Metrics**
```python
class ThroughputMetrics:
    def __init__(self):
        self.intelligence_items_per_hour = 0
        self.routing_decisions_per_hour = 0
        self.api_requests_per_minute = 0
        self.reports_generated_per_day = 0

    def calculate_hourly_throughput(self):
        """Calculate processing throughput per hour"""
        return {
            'intelligence_processing': self.intelligence_items_per_hour,
            'routing_decisions': self.routing_decisions_per_hour,
            'api_throughput': self.api_requests_per_minute * 60
        }
```

**Latency Metrics**
```python
class LatencyMetrics:
    def __init__(self):
        self.api_response_times = []
        self.agent_processing_times = {}
        self.end_to_end_latency = []

    def record_api_latency(self, endpoint: str, latency_ms: float):
        """Record API endpoint latency"""
        self.api_response_times.append({
            'endpoint': endpoint,
            'latency_ms': latency_ms,
            'timestamp': time.time()
        })

    def get_percentiles(self, metric_name: str) -> dict:
        """Calculate latency percentiles"""
        values = [m['latency_ms'] for m in self.api_response_times]
        return {
            'p50': numpy.percentile(values, 50),
            'p90': numpy.percentile(values, 90),
            'p95': numpy.percentile(values, 95),
            'p99': numpy.percentile(values, 99)
        }
```

**Resource Utilization Metrics**
```python
import psutil
import time

class ResourceMetrics:
    def __init__(self):
        self.process = psutil.Process()
        self.system_metrics = []

    def collect_system_metrics(self):
        """Collect current system resource metrics"""
        return {
            'timestamp': time.time(),
            'cpu_percent': self.process.cpu_percent(),
            'memory_mb': self.process.memory_info().rss / 1024 / 1024,
            'memory_percent': self.process.memory_percent(),
            'disk_io': psutil.disk_io_counters(),
            'network_io': psutil.net_io_counters(),
            'open_files': len(self.process.open_files()),
            'threads': self.process.num_threads()
        }

    def get_resource_trends(self, duration_hours: int = 24) -> dict:
        """Analyze resource usage trends"""
        cutoff_time = time.time() - (duration_hours * 3600)
        recent_metrics = [m for m in self.system_metrics if m['timestamp'] > cutoff_time]

        if not recent_metrics:
            return {}

        return {
            'avg_cpu': sum(m['cpu_percent'] for m in recent_metrics) / len(recent_metrics),
            'max_memory_mb': max(m['memory_mb'] for m in recent_metrics),
            'avg_memory_mb': sum(m['memory_mb'] for m in recent_metrics) / len(recent_metrics),
            'peak_threads': max(m['threads'] for m in recent_metrics)
        }
```

### Performance Benchmarking

**Agent Performance Benchmarks**
```python
import time
import statistics
from typing import List, Dict

class AgentBenchmark:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.execution_times = []
        self.memory_usage = []
        self.throughput_rates = []

    def benchmark_agent(self, agent, test_data: List[Dict], iterations: int = 10):
        """Benchmark agent performance with test data"""

        for i in range(iterations):
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss

            # Execute agent
            results = agent.run(**test_data[i % len(test_data)])

            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss

            # Record metrics
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            throughput = len(results.get('intelligence', [])) / execution_time

            self.execution_times.append(execution_time)
            self.memory_usage.append(memory_delta)
            self.throughput_rates.append(throughput)

        return self.generate_benchmark_report()

    def generate_benchmark_report(self) -> Dict:
        """Generate comprehensive benchmark report"""
        return {
            'agent_name': self.agent_name,
            'execution_time': {
                'mean': statistics.mean(self.execution_times),
                'median': statistics.median(self.execution_times),
                'std_dev': statistics.stdev(self.execution_times),
                'min': min(self.execution_times),
                'max': max(self.execution_times)
            },
            'memory_usage': {
                'mean_mb': statistics.mean(self.memory_usage) / 1024 / 1024,
                'max_mb': max(self.memory_usage) / 1024 / 1024
            },
            'throughput': {
                'mean_items_per_second': statistics.mean(self.throughput_rates),
                'max_items_per_second': max(self.throughput_rates)
            }
        }
```

## System Monitoring

### Real-Time Monitoring Setup

**Prometheus Configuration**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "nomad_performance_rules.yml"

scrape_configs:
  - job_name: 'nomad-app'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'nomad-system'
    static_configs:
      - targets: ['localhost:9100']
    scrape_interval: 30s
```

**Performance Alert Rules**
```yaml
# monitoring/nomad_performance_rules.yml
groups:
  - name: nomad_performance
    rules:
      # High CPU usage
      - alert: NomadHighCPU
        expr: nomad_cpu_usage_percent > 80
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "NOMAD CPU usage is high"
          description: "CPU usage has been above 80% for more than 2 minutes"

      # High memory usage
      - alert: NomadHighMemory
        expr: nomad_memory_usage_mb > 1500
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "NOMAD memory usage is high"
          description: "Memory usage has exceeded 1.5GB"

      # Slow API responses
      - alert: NomadSlowAPI
        expr: nomad_api_response_time_p95 > 5000
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "NOMAD API responses are slow"
          description: "95th percentile response time has exceeded 5 seconds"

      # Low throughput
      - alert: NomadLowThroughput
        expr: rate(nomad_intelligence_items_processed[5m]) < 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "NOMAD processing throughput is low"
          description: "Processing fewer than 10 items per minute for 5+ minutes"
```

**Custom Metrics Collection**
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class NomadMetrics:
    def __init__(self):
        # Counters
        self.intelligence_items_processed = Counter(
            'nomad_intelligence_items_processed_total',
            'Total intelligence items processed',
            ['agent_type', 'status']
        )

        self.api_requests = Counter(
            'nomad_api_requests_total',
            'Total API requests',
            ['endpoint', 'method', 'status']
        )

        # Histograms
        self.api_response_time = Histogram(
            'nomad_api_response_time_seconds',
            'API response time in seconds',
            ['endpoint']
        )

        self.agent_processing_time = Histogram(
            'nomad_agent_processing_time_seconds',
            'Agent processing time in seconds',
            ['agent_type']
        )

        # Gauges
        self.active_agents = Gauge(
            'nomad_active_agents',
            'Number of active agent processes'
        )

        self.memory_usage = Gauge(
            'nomad_memory_usage_mb',
            'Memory usage in MB'
        )

        self.cpu_usage = Gauge(
            'nomad_cpu_usage_percent',
            'CPU usage percentage'
        )

    def start_metrics_server(self, port: int = 8000):
        """Start Prometheus metrics server"""
        start_http_server(port)

    def update_system_metrics(self):
        """Update system resource metrics"""
        process = psutil.Process()
        self.memory_usage.set(process.memory_info().rss / 1024 / 1024)
        self.cpu_usage.set(process.cpu_percent())

    def record_api_request(self, endpoint: str, method: str,
                          response_time: float, status_code: int):
        """Record API request metrics"""
        status = 'success' if status_code < 400 else 'error'
        self.api_requests.labels(endpoint=endpoint, method=method, status=status).inc()
        self.api_response_time.labels(endpoint=endpoint).observe(response_time)

    def record_agent_execution(self, agent_type: str, processing_time: float,
                              items_processed: int, status: str):
        """Record agent execution metrics"""
        self.agent_processing_time.labels(agent_type=agent_type).observe(processing_time)
        self.intelligence_items_processed.labels(
            agent_type=agent_type, status=status
        ).inc(items_processed)
```

### Performance Dashboard

**Grafana Dashboard Configuration**
```json
{
  "dashboard": {
    "title": "NOMAD Performance Dashboard",
    "panels": [
      {
        "title": "Processing Throughput",
        "type": "stat",
        "targets": [
          {
            "expr": "rate(nomad_intelligence_items_processed_total[5m])",
            "legendFormat": "Items/sec"
          }
        ]
      },
      {
        "title": "API Response Times",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, nomad_api_response_time_seconds)",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, nomad_api_response_time_seconds)",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, nomad_api_response_time_seconds)",
            "legendFormat": "p99"
          }
        ]
      },
      {
        "title": "Resource Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "nomad_cpu_usage_percent",
            "legendFormat": "CPU %"
          },
          {
            "expr": "nomad_memory_usage_mb",
            "legendFormat": "Memory MB"
          }
        ]
      }
    ]
  }
}
```

## Application Optimization

### Agent Performance Optimization

**Asynchronous Processing**
```python
import asyncio
import aiohttp
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

class OptimizedRSSAgent:
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.session = None
        self.thread_pool = ThreadPoolExecutor(max_workers=5)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=50, limit_per_host=10)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def process_feeds_concurrent(self, feed_urls: List[str]) -> List[Dict]:
        """Process multiple RSS feeds concurrently"""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_single_feed(url: str) -> Dict:
            async with semaphore:
                try:
                    return await self._fetch_and_process_feed(url)
                except Exception as e:
                    return {
                        'url': url,
                        'error': str(e),
                        'intelligence': []
                    }

        # Process feeds concurrently
        tasks = [process_single_feed(url) for url in feed_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and combine results
        valid_results = [r for r in results if isinstance(r, dict)]
        return valid_results

    async def _fetch_and_process_feed(self, url: str) -> Dict:
        """Fetch and process single RSS feed"""
        # Fetch RSS content
        async with self.session.get(url) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status} for {url}")

            content = await response.text()

        # Parse RSS in thread pool (CPU-intensive)
        loop = asyncio.get_event_loop()
        parsed_feed = await loop.run_in_executor(
            self.thread_pool,
            self._parse_rss_content,
            content
        )

        # Process intelligence items
        intelligence_items = await self._extract_intelligence(parsed_feed)

        return {
            'url': url,
            'intelligence': intelligence_items,
            'timestamp': time.time()
        }

    def _parse_rss_content(self, content: str) -> dict:
        """Parse RSS content (runs in thread pool)"""
        import feedparser
        return feedparser.parse(content)

    async def _extract_intelligence(self, parsed_feed) -> List[Dict]:
        """Extract intelligence from parsed feed"""
        # This could also be parallelized if processing is heavy
        intelligence = []

        for entry in parsed_feed.entries:
            item = await self._process_entry(entry)
            if item:
                intelligence.append(item)

        return intelligence
```

**Batch Processing Optimization**
```python
class BatchProcessor:
    def __init__(self, batch_size: int = 50, max_workers: int = 4):
        self.batch_size = batch_size
        self.max_workers = max_workers

    async def process_intelligence_batch(self, items: List[Dict]) -> List[Dict]:
        """Process intelligence items in optimized batches"""

        # Split into batches
        batches = [
            items[i:i + self.batch_size]
            for i in range(0, len(items), self.batch_size)
        ]

        # Process batches concurrently
        semaphore = asyncio.Semaphore(self.max_workers)

        async def process_batch(batch: List[Dict]) -> List[Dict]:
            async with semaphore:
                return await self._process_single_batch(batch)

        tasks = [process_batch(batch) for batch in batches]
        batch_results = await asyncio.gather(*tasks)

        # Flatten results
        all_results = []
        for batch_result in batch_results:
            all_results.extend(batch_result)

        return all_results

    async def _process_single_batch(self, batch: List[Dict]) -> List[Dict]:
        """Process a single batch of intelligence items"""
        results = []

        # Use Claude API batch processing if available
        if len(batch) > 1 and self._supports_batch_api():
            results = await self._process_batch_with_api(batch)
        else:
            # Process individually
            for item in batch:
                result = await self._process_single_item(item)
                results.append(result)

        return results
```

### Memory Management

**Memory-Efficient Data Processing**
```python
import gc
import sys
from typing import Iterator, Dict, Any

class MemoryEfficientProcessor:
    def __init__(self, memory_limit_mb: int = 1000):
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024
        self.processed_count = 0

    def process_large_dataset(self, data_source: Iterator[Dict]) -> Iterator[Dict]:
        """Process large datasets with memory management"""

        buffer = []
        buffer_size = 0

        for item in data_source:
            # Add to buffer
            buffer.append(item)
            buffer_size += sys.getsizeof(item)

            # Check memory usage
            if buffer_size > self.memory_limit_bytes or len(buffer) >= 100:
                # Process buffer
                for result in self._process_buffer(buffer):
                    yield result

                # Clear buffer and force garbage collection
                buffer.clear()
                buffer_size = 0
                gc.collect()

        # Process remaining items
        if buffer:
            for result in self._process_buffer(buffer):
                yield result

    def _process_buffer(self, buffer: List[Dict]) -> Iterator[Dict]:
        """Process buffer of items"""
        for item in buffer:
            try:
                result = self._process_item(item)
                self.processed_count += 1
                yield result
            except Exception as e:
                yield {
                    'error': str(e),
                    'item_id': item.get('id', 'unknown')
                }

    def _process_item(self, item: Dict) -> Dict:
        """Process single item"""
        # Actual processing logic here
        return item

    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage statistics"""
        process = psutil.Process()
        return {
            'rss_mb': process.memory_info().rss / 1024 / 1024,
            'vms_mb': process.memory_info().vms / 1024 / 1024,
            'percent': process.memory_percent(),
            'processed_items': self.processed_count
        }
```

**Object Pool for Frequent Allocations**
```python
from queue import Queue
import threading

class ObjectPool:
    def __init__(self, factory_func, max_size: int = 100):
        self.factory_func = factory_func
        self.max_size = max_size
        self.pool = Queue(maxsize=max_size)
        self.lock = threading.Lock()

    def get_object(self):
        """Get object from pool or create new one"""
        try:
            return self.pool.get_nowait()
        except:
            return self.factory_func()

    def return_object(self, obj):
        """Return object to pool"""
        # Reset object state
        if hasattr(obj, 'reset'):
            obj.reset()

        try:
            self.pool.put_nowait(obj)
        except:
            # Pool is full, let object be garbage collected
            pass

# Usage example
class IntelligenceProcessor:
    def __init__(self):
        self.parser_pool = ObjectPool(
            factory_func=lambda: feedparser.FeedParserDict(),
            max_size=50
        )

    def process_rss_feed(self, content: str):
        parser = self.parser_pool.get_object()
        try:
            # Use parser
            result = parser.parse(content)
            return result
        finally:
            self.parser_pool.return_object(parser)
```

## API Performance

### Rate Limiting and Throttling

**Intelligent Rate Limiter**
```python
import time
import asyncio
from collections import defaultdict
from typing import Dict, Optional

class AdaptiveRateLimiter:
    def __init__(self):
        self.service_limits = {
            'anthropic': {'requests_per_minute': 100, 'tokens_per_minute': 50000},
            'virustotal': {'requests_per_minute': 4, 'daily_limit': 1000},
            'nvd': {'requests_per_minute': 50, 'concurrent_limit': 5}
        }

        self.service_usage = defaultdict(lambda: {
            'requests': [],
            'tokens': 0,
            'daily_requests': 0,
            'concurrent_requests': 0
        })

        self.adaptive_backoff = defaultdict(lambda: 1.0)

    async def acquire_permit(self, service: str, tokens_needed: int = 0) -> bool:
        """Acquire permit to make API call"""
        current_time = time.time()
        usage = self.service_usage[service]
        limits = self.service_limits.get(service, {})

        # Clean old requests (sliding window)
        cutoff_time = current_time - 60  # 1 minute ago
        usage['requests'] = [req_time for req_time in usage['requests']
                           if req_time > cutoff_time]

        # Check rate limits
        if len(usage['requests']) >= limits.get('requests_per_minute', float('inf')):
            # Calculate wait time
            oldest_request = min(usage['requests'])
            wait_time = 60 - (current_time - oldest_request)

            # Apply adaptive backoff
            wait_time *= self.adaptive_backoff[service]

            await asyncio.sleep(wait_time)
            return await self.acquire_permit(service, tokens_needed)

        # Check token limits
        if tokens_needed > 0:
            tokens_per_minute = limits.get('tokens_per_minute', float('inf'))
            if usage['tokens'] + tokens_needed > tokens_per_minute:
                await asyncio.sleep(2)
                return await self.acquire_permit(service, tokens_needed)

        # Check concurrent limits
        concurrent_limit = limits.get('concurrent_limit', float('inf'))
        if usage['concurrent_requests'] >= concurrent_limit:
            await asyncio.sleep(0.5)
            return await self.acquire_permit(service, tokens_needed)

        # Grant permit
        usage['requests'].append(current_time)
        usage['tokens'] += tokens_needed
        usage['concurrent_requests'] += 1

        return True

    def release_permit(self, service: str, tokens_used: int = 0):
        """Release permit after API call completion"""
        usage = self.service_usage[service]
        usage['concurrent_requests'] = max(0, usage['concurrent_requests'] - 1)

    def handle_rate_limit_error(self, service: str):
        """Handle rate limit error by increasing backoff"""
        self.adaptive_backoff[service] = min(
            self.adaptive_backoff[service] * 2,
            10.0  # Max 10x backoff
        )

    def handle_successful_request(self, service: str):
        """Handle successful request by reducing backoff"""
        self.adaptive_backoff[service] = max(
            self.adaptive_backoff[service] * 0.9,
            1.0  # Min 1x backoff
        )
```

**API Client Optimization**
```python
import aiohttp
import asyncio
from typing import Optional, Dict, Any

class OptimizedAPIClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = AdaptiveRateLimiter()
        self.connection_pool_size = 50
        self.request_timeout = 30

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(
            limit=self.connection_pool_size,
            limit_per_host=10,
            keepalive_timeout=300,
            enable_cleanup_closed=True
        )

        timeout = aiohttp.ClientTimeout(total=self.request_timeout)

        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'NOMAD-ThreatIntel/1.0',
                'Accept': 'application/json'
            }
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def make_request(self, service: str, method: str, url: str,
                          **kwargs) -> Dict[str, Any]:
        """Make optimized API request with rate limiting"""

        # Estimate token usage for request
        estimated_tokens = self._estimate_tokens(kwargs.get('json', {}))

        # Acquire rate limit permit
        await self.rate_limiter.acquire_permit(service, estimated_tokens)

        try:
            async with self.session.request(method, url, **kwargs) as response:
                if response.status == 429:  # Rate limited
                    self.rate_limiter.handle_rate_limit_error(service)
                    # Retry with backoff
                    await asyncio.sleep(2 ** self.retry_count)
                    return await self.make_request(service, method, url, **kwargs)

                elif response.status >= 400:
                    raise aiohttp.ClientError(f"HTTP {response.status}: {await response.text()}")

                else:
                    self.rate_limiter.handle_successful_request(service)
                    return await response.json()

        finally:
            self.rate_limiter.release_permit(service, estimated_tokens)

    def _estimate_tokens(self, request_data: Dict) -> int:
        """Estimate token usage for request"""
        # Simple estimation based on text length
        text_content = str(request_data)
        return len(text_content) // 4  # Rough token estimation

    async def batch_requests(self, requests: List[Dict]) -> List[Dict]:
        """Execute multiple requests with optimal batching"""

        # Group by service for better rate limiting
        service_groups = defaultdict(list)
        for req in requests:
            service_groups[req['service']].append(req)

        results = []

        for service, service_requests in service_groups.items():
            # Process service requests with appropriate concurrency
            max_concurrent = self.rate_limiter.service_limits[service].get(
                'concurrent_limit', 5
            )

            semaphore = asyncio.Semaphore(max_concurrent)

            async def process_request(request):
                async with semaphore:
                    return await self.make_request(
                        service=request['service'],
                        method=request['method'],
                        url=request['url'],
                        **request.get('kwargs', {})
                    )

            service_results = await asyncio.gather(
                *[process_request(req) for req in service_requests],
                return_exceptions=True
            )

            results.extend(service_results)

        return results
```

## Caching Strategies

### Multi-Level Caching

**Hierarchical Cache Implementation**
```python
import redis
import pickle
import hashlib
import time
from typing import Any, Optional, Union
from functools import wraps

class MultiLevelCache:
    def __init__(self, redis_url: Optional[str] = None):
        # L1: In-memory cache (fastest)
        self.memory_cache = {}
        self.memory_cache_timestamps = {}
        self.memory_cache_max_size = 1000

        # L2: Redis cache (shared across instances)
        self.redis_client = redis.from_url(redis_url) if redis_url else None

        # L3: File-based cache (persistent)
        self.file_cache_dir = "/var/cache/nomad"
        os.makedirs(self.file_cache_dir, exist_ok=True)

        self.default_ttl = 3600  # 1 hour

    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate consistent cache key"""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()

    async def get(self, key: str) -> Optional[Any]:
        """Get value from multi-level cache"""

        # L1: Check memory cache
        if key in self.memory_cache:
            timestamp = self.memory_cache_timestamps.get(key, 0)
            if time.time() - timestamp < self.default_ttl:
                return self.memory_cache[key]
            else:
                # Expired, remove from memory cache
                del self.memory_cache[key]
                del self.memory_cache_timestamps[key]

        # L2: Check Redis cache
        if self.redis_client:
            try:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    value = pickle.loads(cached_data)
                    # Store in L1 for faster access
                    self._store_in_memory(key, value)
                    return value
            except Exception as e:
                print(f"Redis cache error: {e}")

        # L3: Check file cache
        file_path = os.path.join(self.file_cache_dir, f"{key}.cache")
        if os.path.exists(file_path):
            try:
                stat = os.stat(file_path)
                if time.time() - stat.st_mtime < self.default_ttl:
                    with open(file_path, 'rb') as f:
                        value = pickle.load(f)

                    # Store in higher levels
                    self._store_in_memory(key, value)
                    if self.redis_client:
                        await self.redis_client.setex(key, self.default_ttl, pickle.dumps(value))

                    return value
            except Exception as e:
                print(f"File cache error: {e}")

        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value in all cache levels"""
        ttl = ttl or self.default_ttl

        # L1: Memory cache
        self._store_in_memory(key, value)

        # L2: Redis cache
        if self.redis_client:
            try:
                await self.redis_client.setex(key, ttl, pickle.dumps(value))
            except Exception as e:
                print(f"Redis cache set error: {e}")

        # L3: File cache
        try:
            file_path = os.path.join(self.file_cache_dir, f"{key}.cache")
            with open(file_path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            print(f"File cache set error: {e}")

    def _store_in_memory(self, key: str, value: Any):
        """Store in memory cache with size management"""
        # Remove oldest entries if cache is full
        if len(self.memory_cache) >= self.memory_cache_max_size:
            oldest_key = min(self.memory_cache_timestamps.keys(),
                           key=lambda k: self.memory_cache_timestamps[k])
            del self.memory_cache[oldest_key]
            del self.memory_cache_timestamps[oldest_key]

        self.memory_cache[key] = value
        self.memory_cache_timestamps[key] = time.time()

    def cached(self, ttl: int = None):
        """Decorator for automatic caching"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cache_key = self._generate_cache_key(func.__name__, *args, **kwargs)

                # Try to get from cache
                cached_result = await self.get(cache_key)
                if cached_result is not None:
                    return cached_result

                # Execute function
                result = await func(*args, **kwargs)

                # Store in cache
                await self.set(cache_key, result, ttl)

                return result
            return wrapper
        return decorator
```

**Intelligent Cache Warming**
```python
import asyncio
import schedule
from datetime import datetime, timedelta

class CacheWarmer:
    def __init__(self, cache: MultiLevelCache):
        self.cache = cache
        self.warming_tasks = {}

    def schedule_warming(self, cache_key: str, warm_func,
                        interval_minutes: int = 30):
        """Schedule regular cache warming"""

        async def warm_cache():
            try:
                result = await warm_func()
                await self.cache.set(cache_key, result)
                print(f"Cache warmed for key: {cache_key}")
            except Exception as e:
                print(f"Cache warming failed for {cache_key}: {e}")

        # Schedule the warming task
        schedule.every(interval_minutes).minutes.do(
            lambda: asyncio.create_task(warm_cache())
        )

        self.warming_tasks[cache_key] = warm_cache

    async def warm_critical_caches(self):
        """Warm frequently used caches"""

        critical_caches = [
            ('rss_feeds_config', self._load_rss_feeds, 60),
            ('org_context', self._load_org_context, 120),
            ('threat_intel_feeds', self._fetch_threat_feeds, 30)
        ]

        for cache_key, warm_func, interval in critical_caches:
            self.schedule_warming(cache_key, warm_func, interval)

    async def _load_rss_feeds(self):
        """Warm RSS feeds configuration"""
        # Load and return RSS feeds configuration
        pass

    async def _load_org_context(self):
        """Warm organization context"""
        # Load and return organization context
        pass

    async def _fetch_threat_feeds(self):
        """Warm threat intelligence feeds"""
        # Fetch and return latest threat feeds
        pass
```

## Network Optimization

### Connection Pooling and Optimization

**Advanced Connection Management**
```python
import aiohttp
import asyncio
from typing import Dict, Optional
import ssl

class OptimizedNetworkClient:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.connection_config = {
            'total_pool_size': 100,
            'per_host_pool_size': 20,
            'keep_alive_timeout': 300,
            'connect_timeout': 10,
            'read_timeout': 30
        }

    async def initialize(self):
        """Initialize optimized HTTP session"""

        # Create SSL context with optimizations
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED

        # Configure TCP connector
        connector = aiohttp.TCPConnector(
            limit=self.connection_config['total_pool_size'],
            limit_per_host=self.connection_config['per_host_pool_size'],
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
            keepalive_timeout=self.connection_config['keep_alive_timeout'],
            enable_cleanup_closed=True,
            ssl=ssl_context
        )

        # Configure timeout
        timeout = aiohttp.ClientTimeout(
            total=self.connection_config['read_timeout'],
            connect=self.connection_config['connect_timeout']
        )

        # Create session with optimizations
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'NOMAD-ThreatIntel/1.0',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            },
            auto_decompress=True  # Automatic gzip decompression
        )

    async def fetch_multiple_urls(self, urls: List[str],
                                 max_concurrent: int = 20) -> List[Dict]:
        """Fetch multiple URLs with optimal concurrency"""

        if not self.session:
            await self.initialize()

        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_url(url: str) -> Dict:
            async with semaphore:
                try:
                    start_time = time.time()
                    async with self.session.get(url) as response:
                        content = await response.text()

                        return {
                            'url': url,
                            'status': response.status,
                            'content': content,
                            'response_time': time.time() - start_time,
                            'content_length': len(content)
                        }
                except Exception as e:
                    return {
                        'url': url,
                        'error': str(e),
                        'status': None
                    }

        tasks = [fetch_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        return [r for r in results if isinstance(r, dict)]

    async def close(self):
        """Properly close the session"""
        if self.session:
            await self.session.close()
```

### DNS Optimization

**DNS Caching and Optimization**
```python
import aiodns
import socket
import time
from typing import Dict, Optional

class DNSOptimizer:
    def __init__(self):
        self.dns_cache: Dict[str, Dict] = {}
        self.cache_ttl = 300  # 5 minutes
        self.resolver = aiodns.DNSResolver(
            nameservers=['8.8.8.8', '8.8.4.4', '1.1.1.1'],  # Fast public DNS
            timeout=5.0,
            tries=2
        )

    async def resolve_hostname(self, hostname: str) -> Optional[str]:
        """Resolve hostname with caching"""

        # Check cache
        if hostname in self.dns_cache:
            cache_entry = self.dns_cache[hostname]
            if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                return cache_entry['ip']

        try:
            # Perform DNS lookup
            result = await self.resolver.gethostbyname(hostname, socket.AF_INET)
            ip_address = result.addresses[0]

            # Cache result
            self.dns_cache[hostname] = {
                'ip': ip_address,
                'timestamp': time.time()
            }

            return ip_address

        except Exception as e:
            print(f"DNS resolution failed for {hostname}: {e}")
            return None

    def pre_resolve_common_hosts(self):
        """Pre-resolve commonly used hostnames"""
        common_hosts = [
            'api.anthropic.com',
            'www.virustotal.com',
            'nvd.nist.gov',
            'feeds.feedburner.com',
            'www.cisa.gov'
        ]

        for host in common_hosts:
            asyncio.create_task(self.resolve_hostname(host))
```

## Database Optimization

### Query Optimization

**Efficient Data Access Patterns**
```python
import sqlite3
import asyncio
import aiosqlite
from typing import List, Dict, Optional, Any
from contextlib import asynccontextmanager

class OptimizedDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection_pool_size = 10
        self.connection_pool = asyncio.Queue(maxsize=self.connection_pool_size)

    async def initialize(self):
        """Initialize database with optimizations"""

        # Create connection pool
        for _ in range(self.connection_pool_size):
            conn = await aiosqlite.connect(self.db_path)

            # Enable SQLite optimizations
            await conn.execute("PRAGMA journal_mode = WAL")
            await conn.execute("PRAGMA cache_size = 10000")
            await conn.execute("PRAGMA temp_store = memory")
            await conn.execute("PRAGMA mmap_size = 268435456")  # 256MB
            await conn.execute("PRAGMA synchronous = NORMAL")

            await self.connection_pool.put(conn)

        # Create indexes for common queries
        await self.create_performance_indexes()

    @asynccontextmanager
    async def get_connection(self):
        """Get connection from pool"""
        conn = await self.connection_pool.get()
        try:
            yield conn
        finally:
            await self.connection_pool.put(conn)

    async def create_performance_indexes(self):
        """Create indexes for optimal query performance"""

        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_intelligence_published ON intelligence_items(published_utc)",
            "CREATE INDEX IF NOT EXISTS idx_intelligence_source ON intelligence_items(source_name)",
            "CREATE INDEX IF NOT EXISTS idx_intelligence_cves ON intelligence_items(cves)",
            "CREATE INDEX IF NOT EXISTS idx_routing_decision ON routing_decisions(routing_decision)",
            "CREATE INDEX IF NOT EXISTS idx_routing_timestamp ON routing_decisions(timestamp)",
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_dedupe_key ON intelligence_items(dedupe_key)"
        ]

        async with self.get_connection() as conn:
            for index_sql in indexes:
                await conn.execute(index_sql)
            await conn.commit()

    async def batch_insert_intelligence(self, items: List[Dict]) -> None:
        """Efficiently insert multiple intelligence items"""

        if not items:
            return

        # Prepare batch insert
        insert_sql = """
        INSERT OR REPLACE INTO intelligence_items
        (dedupe_key, source_type, source_name, title, summary,
         published_utc, cves, cvss_v3, kev_listed, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """

        async with self.get_connection() as conn:
            # Use executemany for batch insert
            batch_data = [
                (
                    item['dedupe_key'],
                    item['source_type'],
                    item['source_name'],
                    item['title'],
                    item['summary'],
                    item['published_utc'],
                    json.dumps(item.get('cves', [])),
                    item.get('cvss_v3'),
                    item.get('kev_listed'),
                )
                for item in items
            ]

            await conn.executemany(insert_sql, batch_data)
            await conn.commit()

    async def query_intelligence_optimized(self,
                                         filters: Dict[str, Any],
                                         limit: int = 100,
                                         offset: int = 0) -> List[Dict]:
        """Optimized intelligence query with filters"""

        # Build dynamic query
        where_clauses = []
        params = []

        if 'source_type' in filters:
            where_clauses.append("source_type = ?")
            params.append(filters['source_type'])

        if 'kev_listed' in filters:
            where_clauses.append("kev_listed = ?")
            params.append(filters['kev_listed'])

        if 'date_from' in filters:
            where_clauses.append("published_utc >= ?")
            params.append(filters['date_from'])

        if 'date_to' in filters:
            where_clauses.append("published_utc <= ?")
            params.append(filters['date_to'])

        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

        query_sql = f"""
        SELECT * FROM intelligence_items
        WHERE {where_clause}
        ORDER BY published_utc DESC
        LIMIT ? OFFSET ?
        """

        params.extend([limit, offset])

        async with self.get_connection() as conn:
            async with conn.execute(query_sql, params) as cursor:
                rows = await cursor.fetchall()

                # Convert to dictionaries
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]

    async def get_intelligence_stats(self) -> Dict[str, Any]:
        """Get intelligence statistics efficiently"""

        stats_queries = {
            'total_items': "SELECT COUNT(*) FROM intelligence_items",
            'high_severity': "SELECT COUNT(*) FROM intelligence_items WHERE cvss_v3 >= 7.0",
            'kev_items': "SELECT COUNT(*) FROM intelligence_items WHERE kev_listed = 1",
            'recent_items': "SELECT COUNT(*) FROM intelligence_items WHERE published_utc >= datetime('now', '-24 hours')",
            'sources': "SELECT COUNT(DISTINCT source_name) FROM intelligence_items"
        }

        async with self.get_connection() as conn:
            stats = {}
            for stat_name, query in stats_queries.items():
                async with conn.execute(query) as cursor:
                    result = await cursor.fetchone()
                    stats[stat_name] = result[0] if result else 0

            return stats
```

## Scaling Strategies

### Horizontal Scaling Architecture

**Agent Distribution System**
```python
import asyncio
import json
import redis
from typing import Dict, List, Optional, Callable
from enum import Enum

class AgentType(Enum):
    RSS_FEED = "rss_feed"
    ORCHESTRATOR = "orchestrator"
    TECHNICAL_ALERT = "technical_alert"
    CISO_REPORT = "ciso_report"

class DistributedAgentManager:
    def __init__(self, redis_url: str):
        self.redis_client = redis.from_url(redis_url)
        self.agent_registry = {}
        self.task_queues = {
            agent_type.value: f"nomad:tasks:{agent_type.value}"
            for agent_type in AgentType
        }
        self.result_queue = "nomad:results"
        self.worker_heartbeats = "nomad:workers"

    def register_agent(self, agent_type: AgentType, agent_instance):
        """Register agent for distributed execution"""
        self.agent_registry[agent_type] = agent_instance

    async def distribute_task(self, agent_type: AgentType,
                             task_data: Dict, priority: int = 1) -> str:
        """Distribute task to available worker"""

        task_id = f"{agent_type.value}:{int(time.time() * 1000)}"
        task_payload = {
            'task_id': task_id,
            'agent_type': agent_type.value,
            'data': task_data,
            'created_at': time.time(),
            'priority': priority
        }

        # Add to priority queue
        queue_name = self.task_queues[agent_type.value]
        await self.redis_client.zadd(
            queue_name,
            {json.dumps(task_payload): priority}
        )

        return task_id

    async def process_tasks(self, agent_type: AgentType, worker_id: str):
        """Process tasks for specific agent type"""

        queue_name = self.task_queues[agent_type.value]
        agent_instance = self.agent_registry.get(agent_type)

        if not agent_instance:
            raise ValueError(f"No agent registered for type: {agent_type}")

        while True:
            try:
                # Get highest priority task
                task_data = await self.redis_client.zpopmax(queue_name)

                if not task_data:
                    await asyncio.sleep(1)  # No tasks available
                    continue

                task_json, priority = task_data[0]
                task = json.loads(task_json)

                # Update worker heartbeat
                await self.redis_client.hset(
                    self.worker_heartbeats,
                    f"{worker_id}:{agent_type.value}",
                    time.time()
                )

                # Process task
                start_time = time.time()
                result = await agent_instance.run(**task['data'])
                processing_time = time.time() - start_time

                # Store result
                result_payload = {
                    'task_id': task['task_id'],
                    'result': result,
                    'worker_id': worker_id,
                    'processing_time': processing_time,
                    'completed_at': time.time()
                }

                await self.redis_client.lpush(
                    self.result_queue,
                    json.dumps(result_payload)
                )

            except Exception as e:
                # Handle task failure
                error_payload = {
                    'task_id': task.get('task_id', 'unknown'),
                    'error': str(e),
                    'worker_id': worker_id,
                    'failed_at': time.time()
                }

                await self.redis_client.lpush(
                    "nomad:errors",
                    json.dumps(error_payload)
                )

    async def get_task_result(self, task_id: str,
                             timeout_seconds: int = 300) -> Optional[Dict]:
        """Wait for and retrieve task result"""

        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            # Check for result
            result_data = await self.redis_client.brpop(
                self.result_queue,
                timeout=1
            )

            if result_data:
                result = json.loads(result_data[1])
                if result['task_id'] == task_id:
                    return result
                else:
                    # Put back result for another task
                    await self.redis_client.lpush(
                        self.result_queue,
                        result_data[1]
                    )

            await asyncio.sleep(0.1)

        return None  # Timeout

    async def scale_workers(self, agent_type: AgentType,
                           desired_workers: int):
        """Auto-scale workers based on queue depth"""

        queue_name = self.task_queues[agent_type.value]
        current_queue_size = await self.redis_client.zcard(queue_name)

        # Get current active workers
        worker_pattern = f"*:{agent_type.value}"
        active_workers = await self.redis_client.hkeys(self.worker_heartbeats)
        current_workers = len([w for w in active_workers
                             if w.decode().endswith(f":{agent_type.value}")])

        # Scale decision logic
        if current_queue_size > 10 and current_workers < desired_workers:
            # Need more workers
            return {
                'action': 'scale_up',
                'current_workers': current_workers,
                'queue_size': current_queue_size,
                'recommended_workers': min(desired_workers, current_workers + 2)
            }
        elif current_queue_size < 2 and current_workers > 1:
            # Can reduce workers
            return {
                'action': 'scale_down',
                'current_workers': current_workers,
                'queue_size': current_queue_size,
                'recommended_workers': max(1, current_workers - 1)
            }
        else:
            return {
                'action': 'maintain',
                'current_workers': current_workers,
                'queue_size': current_queue_size
            }
```

**Auto-Scaling Controller**
```python
import asyncio
import docker
import kubernetes
from typing import Dict, List

class AutoScalingController:
    def __init__(self, deployment_type: str = "docker"):
        self.deployment_type = deployment_type

        if deployment_type == "docker":
            self.docker_client = docker.from_env()
        elif deployment_type == "kubernetes":
            kubernetes.config.load_incluster_config()
            self.k8s_apps_v1 = kubernetes.client.AppsV1Api()

    async def scale_deployment(self, agent_type: str,
                              desired_replicas: int) -> bool:
        """Scale deployment based on type"""

        try:
            if self.deployment_type == "docker":
                return await self._scale_docker_service(agent_type, desired_replicas)
            elif self.deployment_type == "kubernetes":
                return await self._scale_k8s_deployment(agent_type, desired_replicas)
        except Exception as e:
            print(f"Scaling failed for {agent_type}: {e}")
            return False

    async def _scale_docker_service(self, agent_type: str,
                                   desired_replicas: int) -> bool:
        """Scale Docker Swarm service"""

        service_name = f"nomad-{agent_type.replace('_', '-')}"

        try:
            service = self.docker_client.services.get(service_name)
            service.update(
                mode={'Replicated': {'Replicas': desired_replicas}}
            )
            return True
        except docker.errors.NotFound:
            print(f"Service {service_name} not found")
            return False

    async def _scale_k8s_deployment(self, agent_type: str,
                                   desired_replicas: int) -> bool:
        """Scale Kubernetes deployment"""

        deployment_name = f"nomad-{agent_type.replace('_', '-')}"
        namespace = "nomad-system"

        try:
            # Update deployment
            body = {
                'spec': {
                    'replicas': desired_replicas
                }
            }

            self.k8s_apps_v1.patch_namespaced_deployment_scale(
                name=deployment_name,
                namespace=namespace,
                body=body
            )
            return True

        except kubernetes.client.rest.ApiException as e:
            print(f"K8s scaling error: {e}")
            return False

    async def monitor_and_scale(self, agent_manager: DistributedAgentManager):
        """Continuous monitoring and auto-scaling"""

        scaling_config = {
            AgentType.RSS_FEED: {'min': 1, 'max': 10, 'target_queue_size': 5},
            AgentType.ORCHESTRATOR: {'min': 1, 'max': 5, 'target_queue_size': 10},
            AgentType.TECHNICAL_ALERT: {'min': 1, 'max': 3, 'target_queue_size': 15},
            AgentType.CISO_REPORT: {'min': 1, 'max': 2, 'target_queue_size': 5}
        }

        while True:
            try:
                for agent_type, config in scaling_config.items():
                    scaling_recommendation = await agent_manager.scale_workers(
                        agent_type, config['max']
                    )

                    if scaling_recommendation['action'] in ['scale_up', 'scale_down']:
                        current = scaling_recommendation['current_workers']
                        recommended = scaling_recommendation['recommended_workers']

                        # Apply min/max constraints
                        desired = max(config['min'],
                                    min(config['max'], recommended))

                        if desired != current:
                            success = await self.scale_deployment(
                                agent_type.value, desired
                            )

                            if success:
                                print(f"Scaled {agent_type.value}: {current} -> {desired}")
                            else:
                                print(f"Failed to scale {agent_type.value}")

                # Wait before next check
                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                print(f"Auto-scaling error: {e}")
                await asyncio.sleep(30)
```

## Resource Usage

### Memory Optimization Strategies

**Memory Profiler and Optimizer**
```python
import tracemalloc
import psutil
import gc
import sys
from typing import Dict, List, Any, Optional

class MemoryProfiler:
    def __init__(self):
        self.snapshots = []
        self.memory_limits = {
            'warning_threshold_mb': 1000,
            'critical_threshold_mb': 1500,
            'max_allowed_mb': 2000
        }

    def start_profiling(self):
        """Start memory profiling"""
        tracemalloc.start()
        self.take_snapshot("startup")

    def take_snapshot(self, tag: str) -> Dict[str, Any]:
        """Take memory snapshot"""
        if not tracemalloc.is_tracing():
            tracemalloc.start()

        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')

        process = psutil.Process()
        memory_info = process.memory_info()

        snapshot_data = {
            'tag': tag,
            'timestamp': time.time(),
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'top_allocations': [
                {
                    'filename': stat.traceback.format()[0],
                    'size_mb': stat.size / 1024 / 1024,
                    'count': stat.count
                }
                for stat in top_stats[:10]
            ]
        }

        self.snapshots.append(snapshot_data)
        return snapshot_data

    def analyze_memory_growth(self) -> Dict[str, Any]:
        """Analyze memory growth between snapshots"""
        if len(self.snapshots) < 2:
            return {}

        latest = self.snapshots[-1]
        previous = self.snapshots[-2]

        growth_mb = latest['rss_mb'] - previous['rss_mb']
        growth_rate = growth_mb / (latest['timestamp'] - previous['timestamp'])

        return {
            'memory_growth_mb': growth_mb,
            'growth_rate_mb_per_sec': growth_rate,
            'current_memory_mb': latest['rss_mb'],
            'warning_level': self._get_warning_level(latest['rss_mb']),
            'recommendations': self._get_memory_recommendations(latest)
        }

    def _get_warning_level(self, memory_mb: float) -> str:
        """Determine warning level based on memory usage"""
        if memory_mb > self.memory_limits['critical_threshold_mb']:
            return 'critical'
        elif memory_mb > self.memory_limits['warning_threshold_mb']:
            return 'warning'
        else:
            return 'normal'

    def _get_memory_recommendations(self, snapshot: Dict) -> List[str]:
        """Generate memory optimization recommendations"""
        recommendations = []

        memory_mb = snapshot['rss_mb']

        if memory_mb > self.memory_limits['warning_threshold_mb']:
            recommendations.append("Consider garbage collection")
            recommendations.append("Review object pooling opportunities")

        if memory_mb > self.memory_limits['critical_threshold_mb']:
            recommendations.append("Immediate memory cleanup required")
            recommendations.append("Consider reducing batch sizes")
            recommendations.append("Review caching strategy")

        # Analyze top allocations
        for allocation in snapshot['top_allocations']:
            if allocation['size_mb'] > 50:  # Large allocation
                recommendations.append(
                    f"Large allocation in {allocation['filename']}: "
                    f"{allocation['size_mb']:.1f}MB"
                )

        return recommendations

    def force_cleanup(self):
        """Force memory cleanup"""
        # Clear internal caches
        if hasattr(self, '_internal_cache'):
            self._internal_cache.clear()

        # Force garbage collection
        collected = gc.collect()

        # Take snapshot after cleanup
        cleanup_snapshot = self.take_snapshot("post_cleanup")

        return {
            'objects_collected': collected,
            'memory_after_cleanup_mb': cleanup_snapshot['rss_mb']
        }
```

### CPU Optimization

**CPU Usage Monitor and Optimizer**
```python
import psutil
import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Any, List, Dict

class CPUOptimizer:
    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        self.cpu_usage_history = []
        self.thread_pool = ThreadPoolExecutor(max_workers=self.cpu_count)
        self.process_pool = ProcessPoolExecutor(max_workers=max(1, self.cpu_count - 1))

    def monitor_cpu_usage(self):
        """Monitor CPU usage continuously"""
        while True:
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage_history.append({
                'timestamp': time.time(),
                'cpu_percent': cpu_percent,
                'per_cpu': psutil.cpu_percent(percpu=True)
            })

            # Keep only last 1000 readings
            if len(self.cpu_usage_history) > 1000:
                self.cpu_usage_history.pop(0)

    def get_cpu_recommendations(self) -> Dict[str, Any]:
        """Get CPU optimization recommendations"""
        if not self.cpu_usage_history:
            return {}

        recent_usage = [entry['cpu_percent']
                       for entry in self.cpu_usage_history[-60:]]  # Last minute

        avg_cpu = sum(recent_usage) / len(recent_usage)
        max_cpu = max(recent_usage)

        recommendations = []

        if avg_cpu > 80:
            recommendations.append("High CPU usage - consider scaling horizontally")
            recommendations.append("Review algorithm efficiency")

        if max_cpu > 95:
            recommendations.append("CPU spikes detected - implement load balancing")

        if avg_cpu < 30:
            recommendations.append("Low CPU usage - consider consolidating workloads")

        return {
            'avg_cpu_percent': avg_cpu,
            'max_cpu_percent': max_cpu,
            'recommendations': recommendations,
            'optimal_worker_count': self._calculate_optimal_workers(avg_cpu)
        }

    def _calculate_optimal_workers(self, avg_cpu: float) -> int:
        """Calculate optimal number of workers based on CPU usage"""
        if avg_cpu > 80:
            return max(1, self.cpu_count - 1)  # Leave one core free
        elif avg_cpu > 60:
            return self.cpu_count
        else:
            return min(self.cpu_count + 2, self.cpu_count * 2)  # Can handle more

    async def optimize_task_execution(self, tasks: List[Callable],
                                    task_type: str = "io_bound") -> List[Any]:
        """Execute tasks with optimal CPU usage"""

        cpu_usage = self.get_cpu_recommendations()
        optimal_workers = cpu_usage.get('optimal_worker_count', self.cpu_count)

        if task_type == "cpu_bound":
            # Use process pool for CPU-bound tasks
            with ProcessPoolExecutor(max_workers=optimal_workers) as executor:
                futures = [executor.submit(task) for task in tasks]
                results = [future.result() for future in futures]
        else:
            # Use thread pool for I/O-bound tasks
            with ThreadPoolExecutor(max_workers=optimal_workers) as executor:
                futures = [executor.submit(task) for task in tasks]
                results = [future.result() for future in futures]

        return results

    def profile_function_cpu(self, func: Callable) -> Dict[str, Any]:
        """Profile function CPU usage"""
        import cProfile
        import pstats
        from io import StringIO

        profiler = cProfile.Profile()
        start_time = time.time()

        profiler.enable()
        result = func()
        profiler.disable()

        execution_time = time.time() - start_time

        # Analyze profiler results
        stats_stream = StringIO()
        stats = pstats.Stats(profiler, stream=stats_stream)
        stats.sort_stats('cumulative')
        stats.print_stats(20)  # Top 20 functions

        return {
            'execution_time': execution_time,
            'result': result,
            'profile_stats': stats_stream.getvalue(),
            'function_calls': stats.total_calls
        }
```

## Code Optimization

### Algorithm Optimization

**Common Performance Patterns**
```python
from functools import lru_cache
import bisect
from collections import defaultdict, deque
from typing import List, Dict, Set, Any

class AlgorithmOptimizations:
    """Collection of optimized algorithms for common NOMAD operations"""

    @staticmethod
    @lru_cache(maxsize=1000)
    def parse_cve_cached(text: str) -> List[str]:
        """Cached CVE parsing for repeated content"""
        import re
        cve_pattern = re.compile(r'CVE-\d{4}-\d{4,7}')
        return cve_pattern.findall(text)

    @staticmethod
    def deduplicate_intelligence_optimized(items: List[Dict]) -> List[Dict]:
        """Optimized deduplication using hash sets"""
        seen_keys = set()
        unique_items = []

        for item in items:
            dedupe_key = item.get('dedupe_key')
            if dedupe_key and dedupe_key not in seen_keys:
                seen_keys.add(dedupe_key)
                unique_items.append(item)

        return unique_items

    @staticmethod
    def merge_intelligence_sources(sources: List[List[Dict]]) -> List[Dict]:
        """Efficiently merge intelligence from multiple sources"""
        # Use heap for efficient merging of sorted sources
        import heapq

        # Assume sources are sorted by timestamp
        merged = []
        heap = []

        # Initialize heap with first item from each source
        for i, source in enumerate(sources):
            if source:
                heapq.heappush(heap, (source[0]['published_utc'], i, 0, source[0]))

        while heap:
            timestamp, source_idx, item_idx, item = heapq.heappop(heap)
            merged.append(item)

            # Add next item from same source
            next_idx = item_idx + 1
            if next_idx < len(sources[source_idx]):
                next_item = sources[source_idx][next_idx]
                heapq.heappush(heap, (
                    next_item['published_utc'],
                    source_idx,
                    next_idx,
                    next_item
                ))

        return merged

    @staticmethod
    def find_related_intelligence(target_item: Dict,
                                all_items: List[Dict],
                                similarity_threshold: float = 0.7) -> List[Dict]:
        """Find related intelligence using optimized similarity search"""
        from difflib import SequenceMatcher

        target_text = f"{target_item.get('title', '')} {target_item.get('summary', '')}"
        related_items = []

        # Pre-filter by common attributes for efficiency
        candidates = [
            item for item in all_items
            if (item.get('source_type') == target_item.get('source_type') or
                any(cve in target_item.get('cves', [])
                    for cve in item.get('cves', [])))
        ]

        for item in candidates:
            if item['dedupe_key'] == target_item['dedupe_key']:
                continue

            item_text = f"{item.get('title', '')} {item.get('summary', '')}"
            similarity = SequenceMatcher(None, target_text, item_text).ratio()

            if similarity >= similarity_threshold:
                related_items.append({
                    'item': item,
                    'similarity': similarity
                })

        # Sort by similarity
        related_items.sort(key=lambda x: x['similarity'], reverse=True)
        return [item['item'] for item in related_items[:10]]  # Top 10

    @staticmethod
    def batch_process_with_priority(items: List[Dict],
                                   batch_size: int = 50) -> List[List[Dict]]:
        """Create optimally sized batches with priority ordering"""
        # Sort by priority: KEV > High CVSS > EPSS > Others
        def priority_key(item):
            if item.get('kev_listed'):
                return (0, -(item.get('cvss_v3', 0)))
            elif item.get('cvss_v3', 0) >= 7.0:
                return (1, -(item.get('cvss_v3', 0)))
            elif item.get('epss', 0) >= 0.7:
                return (2, -(item.get('epss', 0)))
            else:
                return (3, 0)

        sorted_items = sorted(items, key=priority_key)

        # Create batches
        batches = []
        for i in range(0, len(sorted_items), batch_size):
            batch = sorted_items[i:i + batch_size]
            batches.append(batch)

        return batches

class StringOptimizations:
    """Optimized string operations for intelligence processing"""

    @staticmethod
    @lru_cache(maxsize=5000)
    def clean_text_cached(text: str) -> str:
        """Cached text cleaning for repeated content"""
        import re

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters but keep CVE format
        text = re.sub(r'[^\w\s\-\.]', '', text)

        return text.strip()

    @staticmethod
    def extract_indicators_fast(text: str) -> Dict[str, List[str]]:
        """Fast extraction of security indicators"""
        import re

        patterns = {
            'cves': re.compile(r'CVE-\d{4}-\d{4,7}'),
            'ips': re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'),
            'domains': re.compile(r'\b[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\b'),
            'hashes': re.compile(r'\b[a-fA-F0-9]{32,64}\b')
        }

        indicators = {}
        for indicator_type, pattern in patterns.items():
            indicators[indicator_type] = pattern.findall(text)

        return indicators

    @staticmethod
    def similarity_fast(text1: str, text2: str) -> float:
        """Fast similarity calculation using n-grams"""
        def get_ngrams(text: str, n: int = 3) -> Set[str]:
            return set(text[i:i+n] for i in range(len(text)-n+1))

        ngrams1 = get_ngrams(text1.lower())
        ngrams2 = get_ngrams(text2.lower())

        intersection = len(ngrams1 & ngrams2)
        union = len(ngrams1 | ngrams2)

        return intersection / union if union > 0 else 0.0
```

## Performance Testing

### Load Testing Framework

**Comprehensive Load Testing**
```python
import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

@dataclass
class LoadTestConfig:
    concurrent_users: int = 10
    duration_seconds: int = 300
    ramp_up_seconds: int = 60
    target_url: str = "http://localhost:5000"
    test_scenarios: List[Dict] = None

class LoadTestResults:
    def __init__(self):
        self.response_times: List[float] = []
        self.errors: List[str] = []
        self.status_codes: Dict[int, int] = {}
        self.start_time = time.time()
        self.end_time = None

    def add_response(self, response_time: float, status_code: int, error: str = None):
        self.response_times.append(response_time)
        self.status_codes[status_code] = self.status_codes.get(status_code, 0) + 1
        if error:
            self.errors.append(error)

    def finalize(self):
        self.end_time = time.time()

    def get_statistics(self) -> Dict[str, Any]:
        if not self.response_times:
            return {}

        total_requests = len(self.response_times)
        duration = self.end_time - self.start_time if self.end_time else 0

        return {
            'total_requests': total_requests,
            'duration_seconds': duration,
            'requests_per_second': total_requests / duration if duration > 0 else 0,
            'response_times': {
                'min': min(self.response_times),
                'max': max(self.response_times),
                'mean': statistics.mean(self.response_times),
                'median': statistics.median(self.response_times),
                'p95': self._percentile(self.response_times, 95),
                'p99': self._percentile(self.response_times, 99)
            },
            'status_codes': self.status_codes,
            'error_rate': len(self.errors) / total_requests * 100 if total_requests > 0 else 0,
            'errors': self.errors[:10]  # First 10 errors
        }

    def _percentile(self, data: List[float], percentile: int) -> float:
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]

class NomadLoadTester:
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.results = LoadTestResults()

    async def run_load_test(self) -> Dict[str, Any]:
        """Execute comprehensive load test"""

        print(f"Starting load test with {self.config.concurrent_users} users for {self.config.duration_seconds}s")

        # Create HTTP session
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        async with aiohttp.ClientSession(connector=connector) as session:

            # Start load test
            tasks = []
            for user_id in range(self.config.concurrent_users):
                task = asyncio.create_task(
                    self._simulate_user(session, user_id)
                )
                tasks.append(task)

                # Ramp up gradually
                if self.config.ramp_up_seconds > 0:
                    await asyncio.sleep(
                        self.config.ramp_up_seconds / self.config.concurrent_users
                    )

            # Wait for all tasks to complete
            await asyncio.gather(*tasks, return_exceptions=True)

        self.results.finalize()
        return self.results.get_statistics()

    async def _simulate_user(self, session: aiohttp.ClientSession, user_id: int):
        """Simulate a single user's behavior"""

        end_time = time.time() + self.config.duration_seconds

        while time.time() < end_time:
            try:
                # Select random scenario
                scenario = self._get_random_scenario()

                # Execute scenario
                start_time = time.time()

                async with session.request(
                    scenario['method'],
                    f"{self.config.target_url}{scenario['path']}",
                    json=scenario.get('data'),
                    headers=scenario.get('headers')
                ) as response:
                    await response.read()  # Consume response

                    response_time = time.time() - start_time
                    self.results.add_response(response_time, response.status)

                # Wait between requests
                await asyncio.sleep(scenario.get('think_time', 1))

            except Exception as e:
                self.results.add_response(0, 0, str(e))
                await asyncio.sleep(1)  # Wait before retry

    def _get_random_scenario(self) -> Dict[str, Any]:
        """Get random test scenario"""
        import random

        default_scenarios = [
            {
                'method': 'POST',
                'path': '/api/v1/intelligence/collect',
                'data': {
                    'since': '2024-09-13T00:00:00Z',
                    'until': '2024-09-13T23:59:59Z',
                    'priority': 'high'
                },
                'think_time': 2
            },
            {
                'method': 'GET',
                'path': '/api/v1/agents/status',
                'think_time': 1
            },
            {
                'method': 'POST',
                'path': '/api/v1/intelligence/route',
                'data': {
                    'intelligence': [
                        {
                            'source_type': 'rss',
                            'title': 'Test vulnerability',
                            'cves': ['CVE-2024-12345']
                        }
                    ]
                },
                'think_time': 3
            }
        ]

        scenarios = self.config.test_scenarios or default_scenarios
        return random.choice(scenarios)

# Usage example
async def run_performance_test():
    config = LoadTestConfig(
        concurrent_users=50,
        duration_seconds=300,  # 5 minutes
        ramp_up_seconds=60,    # 1 minute ramp up
        target_url="http://localhost:5000"
    )

    tester = NomadLoadTester(config)
    results = await tester.run_load_test()

    print("Load Test Results:")
    print(f"  Total Requests: {results['total_requests']}")
    print(f"  RPS: {results['requests_per_second']:.2f}")
    print(f"  Mean Response Time: {results['response_times']['mean']:.3f}s")
    print(f"  95th Percentile: {results['response_times']['p95']:.3f}s")
    print(f"  Error Rate: {results['error_rate']:.2f}%")

    return results
```

## Troubleshooting

### Performance Issue Diagnostics

**Automated Performance Diagnostics**
```python
import psutil
import time
import traceback
from typing import Dict, List, Any, Optional

class PerformanceDiagnostics:
    def __init__(self):
        self.diagnostic_history = []
        self.performance_thresholds = {
            'cpu_warning': 75,
            'cpu_critical': 90,
            'memory_warning_mb': 1000,
            'memory_critical_mb': 1500,
            'response_time_warning': 2.0,
            'response_time_critical': 5.0
        }

    def diagnose_performance_issue(self,
                                  symptoms: Dict[str, Any]) -> Dict[str, Any]:
        """Diagnose performance issues based on symptoms"""

        diagnosis = {
            'timestamp': time.time(),
            'symptoms': symptoms,
            'probable_causes': [],
            'recommendations': [],
            'severity': 'low'
        }

        # Analyze CPU issues
        if symptoms.get('high_cpu', False):
            diagnosis['probable_causes'].extend([
                'Inefficient algorithms or loops',
                'Too many concurrent operations',
                'CPU-bound operations not optimized'
            ])
            diagnosis['recommendations'].extend([
                'Profile CPU usage with cProfile',
                'Implement algorithm optimizations',
                'Use process pools for CPU-bound tasks'
            ])
            diagnosis['severity'] = 'high'

        # Analyze memory issues
        if symptoms.get('high_memory', False):
            diagnosis['probable_causes'].extend([
                'Memory leaks in application code',
                'Large objects not being garbage collected',
                'Inefficient caching strategies'
            ])
            diagnosis['recommendations'].extend([
                'Run memory profiler to identify leaks',
                'Implement object pooling',
                'Review caching TTL settings'
            ])
            diagnosis['severity'] = 'critical' if diagnosis['severity'] != 'critical' else 'critical'

        # Analyze slow response times
        if symptoms.get('slow_response', False):
            diagnosis['probable_causes'].extend([
                'Database query inefficiencies',
                'Network latency or timeouts',
                'Blocking I/O operations'
            ])
            diagnosis['recommendations'].extend([
                'Optimize database queries and indexes',
                'Implement connection pooling',
                'Use asynchronous I/O operations'
            ])

        # Analyze high error rates
        if symptoms.get('high_error_rate', False):
            diagnosis['probable_causes'].extend([
                'External API rate limiting',
                'Network connectivity issues',
                'Resource exhaustion'
            ])
            diagnosis['recommendations'].extend([
                'Implement exponential backoff',
                'Add circuit breaker pattern',
                'Monitor external service status'
            ])

        self.diagnostic_history.append(diagnosis)
        return diagnosis

    def run_system_health_check(self) -> Dict[str, Any]:
        """Comprehensive system health check"""

        health_check = {
            'timestamp': time.time(),
            'status': 'healthy',
            'checks': {},
            'alerts': []
        }

        # CPU Check
        cpu_percent = psutil.cpu_percent(interval=1)
        health_check['checks']['cpu'] = {
            'value': cpu_percent,
            'status': self._get_status(cpu_percent,
                                    self.performance_thresholds['cpu_warning'],
                                    self.performance_thresholds['cpu_critical'])
        }

        if cpu_percent > self.performance_thresholds['cpu_warning']:
            health_check['alerts'].append(f"High CPU usage: {cpu_percent}%")
            health_check['status'] = 'warning'

        # Memory Check
        memory = psutil.virtual_memory()
        memory_mb = memory.used / 1024 / 1024
        health_check['checks']['memory'] = {
            'value_mb': memory_mb,
            'percentage': memory.percent,
            'status': self._get_status(memory_mb,
                                    self.performance_thresholds['memory_warning_mb'],
                                    self.performance_thresholds['memory_critical_mb'])
        }

        if memory_mb > self.performance_thresholds['memory_warning_mb']:
            health_check['alerts'].append(f"High memory usage: {memory_mb:.0f}MB")
            health_check['status'] = 'warning'

        # Disk Check
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        health_check['checks']['disk'] = {
            'usage_percent': disk_percent,
            'free_gb': disk.free / 1024 / 1024 / 1024,
            'status': 'critical' if disk_percent > 90 else 'warning' if disk_percent > 80 else 'healthy'
        }

        if disk_percent > 80:
            health_check['alerts'].append(f"High disk usage: {disk_percent}%")

        # Process-specific checks
        try:
            process = psutil.Process()
            health_check['checks']['process'] = {
                'threads': process.num_threads(),
                'open_files': len(process.open_files()),
                'connections': len(process.connections()),
                'status': process.status()
            }
        except Exception as e:
            health_check['checks']['process'] = {'error': str(e)}

        return health_check

    def _get_status(self, value: float, warning_threshold: float,
                   critical_threshold: float) -> str:
        """Get status based on thresholds"""
        if value >= critical_threshold:
            return 'critical'
        elif value >= warning_threshold:
            return 'warning'
        else:
            return 'healthy'

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""

        if not self.diagnostic_history:
            return {'message': 'No diagnostic data available'}

        recent_diagnostics = self.diagnostic_history[-10:]  # Last 10 diagnostics

        # Analyze trends
        severity_counts = {}
        common_causes = {}

        for diagnostic in recent_diagnostics:
            severity = diagnostic['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            for cause in diagnostic['probable_causes']:
                common_causes[cause] = common_causes.get(cause, 0) + 1

        # Generate report
        report = {
            'report_timestamp': time.time(),
            'analysis_period': f"Last {len(recent_diagnostics)} diagnostics",
            'severity_distribution': severity_counts,
            'most_common_causes': sorted(common_causes.items(),
                                       key=lambda x: x[1], reverse=True)[:5],
            'current_system_health': self.run_system_health_check(),
            'recommendations': self._generate_consolidated_recommendations(recent_diagnostics)
        }

        return report

    def _generate_consolidated_recommendations(self,
                                            diagnostics: List[Dict]) -> List[str]:
        """Generate consolidated recommendations from multiple diagnostics"""

        all_recommendations = []
        for diagnostic in diagnostics:
            all_recommendations.extend(diagnostic.get('recommendations', []))

        # Count recommendation frequency
        rec_counts = {}
        for rec in all_recommendations:
            rec_counts[rec] = rec_counts.get(rec, 0) + 1

        # Return top recommendations
        sorted_recs = sorted(rec_counts.items(), key=lambda x: x[1], reverse=True)
        return [rec for rec, count in sorted_recs[:10]]
```

## Capacity Planning

### Capacity Planning Framework

**Resource Capacity Planner**
```python
import numpy as np
from typing import Dict, List, Tuple, Any
from datetime import datetime, timedelta
import pickle

class CapacityPlanner:
    def __init__(self):
        self.historical_data = []
        self.growth_models = {}
        self.resource_limits = {
            'cpu_cores': 16,
            'memory_gb': 32,
            'storage_gb': 1000,
            'network_mbps': 1000
        }

    def add_usage_data(self, timestamp: datetime, usage_metrics: Dict[str, float]):
        """Add usage data point for capacity planning"""
        data_point = {
            'timestamp': timestamp,
            'cpu_percent': usage_metrics.get('cpu_percent', 0),
            'memory_gb': usage_metrics.get('memory_gb', 0),
            'storage_gb': usage_metrics.get('storage_gb', 0),
            'network_mbps': usage_metrics.get('network_mbps', 0),
            'intelligence_items_per_hour': usage_metrics.get('items_per_hour', 0),
            'concurrent_users': usage_metrics.get('concurrent_users', 0)
        }
        self.historical_data.append(data_point)

    def analyze_growth_trends(self, days_back: int = 90) -> Dict[str, Dict]:
        """Analyze growth trends from historical data"""

        if len(self.historical_data) < 10:
            return {'error': 'Insufficient historical data'}

        # Filter recent data
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_data = [
            point for point in self.historical_data
            if point['timestamp'] >= cutoff_date
        ]

        trends = {}
        metrics = ['cpu_percent', 'memory_gb', 'storage_gb', 'intelligence_items_per_hour']

        for metric in metrics:
            values = [point[metric] for point in recent_data]
            timestamps = [point['timestamp'].timestamp() for point in recent_data]

            if len(values) > 1:
                # Linear regression for trend analysis
                coefficients = np.polyfit(timestamps, values, 1)
                slope = coefficients[0]

                # Convert slope to daily growth rate
                daily_growth = slope * 86400  # seconds per day

                trends[metric] = {
                    'daily_growth_rate': daily_growth,
                    'current_average': np.mean(values[-7:]) if len(values) >= 7 else np.mean(values),
                    'growth_direction': 'increasing' if slope > 0 else 'decreasing',
                    'volatility': np.std(values)
                }

        return trends

    def predict_future_usage(self, days_ahead: int = 90) -> Dict[str, Any]:
        """Predict future resource usage based on trends"""

        trends = self.analyze_growth_trends()
        if 'error' in trends:
            return trends

        predictions = {}

        for metric, trend_data in trends.items():
            current_value = trend_data['current_average']
            daily_growth = trend_data['daily_growth_rate']

            # Linear prediction with growth rate
            predicted_value = current_value + (daily_growth * days_ahead)

            # Add volatility buffer (2 standard deviations)
            buffer = trend_data['volatility'] * 2

            predictions[metric] = {
                'predicted_value': max(0, predicted_value),
                'upper_bound': max(0, predicted_value + buffer),
                'lower_bound': max(0, predicted_value - buffer),
                'confidence': self._calculate_confidence(trend_data['volatility'], len(self.historical_data))
            }

        return predictions

    def _calculate_confidence(self, volatility: float, data_points: int) -> float:
        """Calculate prediction confidence based on data quality"""

        # More data points = higher confidence
        data_confidence = min(data_points / 100, 1.0)

        # Lower volatility = higher confidence
        stability_confidence = 1.0 / (1.0 + volatility)

        return (data_confidence * stability_confidence) * 100

    def generate_capacity_recommendations(self,
                                        prediction_days: int = 180) -> Dict[str, Any]:
        """Generate capacity planning recommendations"""

        predictions = self.predict_future_usage(prediction_days)
        if 'error' in predictions:
            return predictions

        recommendations = {
            'forecast_date': (datetime.now() + timedelta(days=prediction_days)).isoformat(),
            'resource_recommendations': {},
            'scaling_timeline': {},
            'cost_implications': {},
            'risk_assessment': {}
        }

        # Analyze each resource
        for metric, prediction in predictions.items():
            resource_name = metric.replace('_percent', '').replace('_gb', '').replace('_per_hour', '')

            if metric == 'cpu_percent':
                current_limit = 100  # percentage
                recommended_action = self._get_cpu_recommendation(prediction, current_limit)
            elif metric == 'memory_gb':
                current_limit = self.resource_limits['memory_gb']
                recommended_action = self._get_memory_recommendation(prediction, current_limit)
            elif metric == 'storage_gb':
                current_limit = self.resource_limits['storage_gb']
                recommended_action = self._get_storage_recommendation(prediction, current_limit)
            else:
                recommended_action = {'action': 'monitor', 'reason': 'No specific limits defined'}

            recommendations['resource_recommendations'][resource_name] = recommended_action

            # Timeline recommendation
            if recommended_action['action'] != 'maintain':
                urgency = self._calculate_urgency(prediction, current_limit)
                recommendations['scaling_timeline'][resource_name] = {
                    'recommended_timeline': urgency['timeline'],
                    'urgency_level': urgency['level']
                }

        return recommendations

    def _get_cpu_recommendation(self, prediction: Dict, current_limit: float) -> Dict:
        """Get CPU scaling recommendations"""
        predicted_usage = prediction['upper_bound']

        if predicted_usage > 80:
            return {
                'action': 'scale_up',
                'reason': f'Predicted CPU usage ({predicted_usage:.1f}%) exceeds 80% threshold',
                'recommended_increase': 'Add 2-4 CPU cores or scale horizontally'
            }
        elif predicted_usage > 60:
            return {
                'action': 'monitor',
                'reason': f'CPU usage trending upward ({predicted_usage:.1f}%)',
                'watch_for': 'Continued growth requiring scaling'
            }
        else:
            return {
                'action': 'maintain',
                'reason': f'CPU usage stable at {predicted_usage:.1f}%'
            }

    def _get_memory_recommendation(self, prediction: Dict, current_limit: float) -> Dict:
        """Get memory scaling recommendations"""
        predicted_usage = prediction['upper_bound']
        usage_percentage = (predicted_usage / current_limit) * 100

        if usage_percentage > 85:
            return {
                'action': 'scale_up',
                'reason': f'Predicted memory usage ({predicted_usage:.1f}GB) exceeds 85% of {current_limit}GB',
                'recommended_increase': f'Increase to {int(predicted_usage * 1.5)}GB'
            }
        elif usage_percentage > 70:
            return {
                'action': 'monitor',
                'reason': f'Memory usage trending upward ({usage_percentage:.1f}%)',
                'watch_for': 'Memory pressure or performance degradation'
            }
        else:
            return {
                'action': 'maintain',
                'reason': f'Memory usage stable at {usage_percentage:.1f}%'
            }

    def _get_storage_recommendation(self, prediction: Dict, current_limit: float) -> Dict:
        """Get storage scaling recommendations"""
        predicted_usage = prediction['upper_bound']
        usage_percentage = (predicted_usage / current_limit) * 100

        if usage_percentage > 80:
            return {
                'action': 'scale_up',
                'reason': f'Predicted storage usage ({predicted_usage:.1f}GB) exceeds 80% of {current_limit}GB',
                'recommended_increase': f'Increase to {int(predicted_usage * 2)}GB'
            }
        elif usage_percentage > 60:
            return {
                'action': 'monitor',
                'reason': f'Storage usage growing ({usage_percentage:.1f}%)',
                'watch_for': 'Rapid growth or log accumulation'
            }
        else:
            return {
                'action': 'maintain',
                'reason': f'Storage usage manageable at {usage_percentage:.1f}%'
            }

    def _calculate_urgency(self, prediction: Dict, current_limit: float) -> Dict:
        """Calculate scaling urgency"""
        predicted_usage = prediction['upper_bound']

        if hasattr(current_limit, '__iter__'):  # Handle percentage metrics
            usage_ratio = predicted_usage / 100
        else:
            usage_ratio = predicted_usage / current_limit

        if usage_ratio > 0.9:
            return {'level': 'critical', 'timeline': '2-4 weeks'}
        elif usage_ratio > 0.8:
            return {'level': 'high', 'timeline': '1-2 months'}
        elif usage_ratio > 0.7:
            return {'level': 'medium', 'timeline': '3-6 months'}
        else:
            return {'level': 'low', 'timeline': '6+ months'}

    def export_capacity_plan(self, filename: str):
        """Export capacity planning data"""
        plan_data = {
            'historical_data': self.historical_data,
            'trends': self.analyze_growth_trends(),
            'predictions': self.predict_future_usage(),
            'recommendations': self.generate_capacity_recommendations(),
            'export_timestamp': datetime.now().isoformat()
        }

        with open(filename, 'wb') as f:
            pickle.dump(plan_data, f)
```

## Best Practices

### Performance Best Practices Checklist

**Development Phase**
- [ ] Profile code during development, not just in production
- [ ] Use appropriate data structures (sets for membership, deques for queues)
- [ ] Implement caching for expensive operations
- [ ] Use batch processing for database operations
- [ ] Minimize object allocation in loops
- [ ] Use connection pooling for external APIs
- [ ] Implement proper error handling with exponential backoff

**Architecture Phase**
- [ ] Design for horizontal scaling from day one
- [ ] Separate CPU-bound and I/O-bound operations
- [ ] Use asynchronous programming for I/O operations
- [ ] Implement circuit breaker pattern for external services
- [ ] Design database schema with performance in mind
- [ ] Plan for data archival and cleanup

**Deployment Phase**
- [ ] Configure appropriate resource limits
- [ ] Set up comprehensive monitoring and alerting
- [ ] Implement proper log rotation
- [ ] Use content delivery networks for static assets
- [ ] Configure database connection pooling
- [ ] Enable compression for API responses

**Operations Phase**
- [ ] Regular performance testing and benchmarking
- [ ] Continuous monitoring of key metrics
- [ ] Automated scaling based on load
- [ ] Regular capacity planning reviews
- [ ] Performance regression testing
- [ ] Documentation of performance characteristics

### Code Review Guidelines for Performance

**Algorithm Review**
```python
# Good: Efficient set operations
seen_cves = set()
new_cves = [cve for cve in all_cves if cve not in seen_cves and not seen_cves.add(cve)]

# Bad: Inefficient list operations
seen_cves = []
new_cves = [cve for cve in all_cves if cve not in seen_cves and seen_cves.append(cve)]

# Good: Use appropriate data structures
from collections import defaultdict
source_counts = defaultdict(int)

# Bad: Manual dictionary management
source_counts = {}
for source in sources:
    if source in source_counts:
        source_counts[source] += 1
    else:
        source_counts[source] = 1
```

**Memory Management Review**
```python
# Good: Generator for memory efficiency
def process_large_dataset(data_file):
    with open(data_file) as f:
        for line in f:
            yield process_line(line)

# Bad: Loading all data into memory
def process_large_dataset(data_file):
    with open(data_file) as f:
        all_data = f.readlines()
    return [process_line(line) for line in all_data]

# Good: Context managers for resource cleanup
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        return await response.json()

# Bad: Manual resource management
session = aiohttp.ClientSession()
response = await session.get(url)
data = await response.json()
# Missing cleanup!
```

---

This comprehensive performance and optimization guide provides the tools, techniques, and best practices needed to ensure NOMAD operates efficiently at scale. Regular application of these principles will maintain optimal performance as the system grows and evolves.