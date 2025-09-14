# Using NOMAD Prompt Templates

The NOMAD framework includes comprehensive prompt templates that define the behavior of each agent. These templates can be used with any LLM (Claude, GPT-4, etc.) to implement the threat intelligence pipeline in any programming language.

## Available Prompt Templates

### Core Processing Agents

1. **rss-agent-prompt.md**
   - Parses RSS/Atom feeds for security advisories
   - Input: Feed URLs, time range
   - Output: Normalized intelligence items with CVEs, Admiralty ratings

2. **orchestrator-system-prompt.md**
   - Routes intelligence based on strict gating rules
   - Input: Intelligence items with context (asset exposure, policy)
   - Output: Routing decisions (DROP, WATCHLIST, TECHNICAL_ALERT, CISO_REPORT)

3. **vendor-parser-agent-prompt.md**
   - Parses vendor-specific security bulletins
   - Input: Advisory HTML/text
   - Output: Structured vulnerability data with patches

### Enhancement Agents

4. **enrichment-agent-prompt.md**
   - Augments items with CVSS, EPSS, KEV data
   - Input: Intelligence items with CVEs
   - Output: Enriched items with scores and exploit status

5. **dedup-agent-prompt.md**
   - Removes duplicate items
   - Input: List of intelligence items
   - Output: Deduplicated list with canonical titles

### Output Generation Agents

6. **technical-alert-prompt.md**
   - Creates actionable SOC alerts
   - Input: Routed item with context
   - Output: Technical alert with remediation steps

7. **ciso-report-generator-prompt.md**
   - Generates executive summaries
   - Input: Week's decisions and alerts
   - Output: Executive report with metrics

8. **watchlist-digest-agent-prompt.md**
   - Summarizes watchlist items
   - Input: Watchlist items
   - Output: Digest with follow-up tasks

9. **evidence-vault-writer-prompt.md**
   - Archives evidence
   - Input: Items with raw HTML
   - Output: Storage references with hashes

## Using Prompts with LLMs

### Direct LLM Implementation

Each prompt template follows a strict format:
- **SYSTEM**: Agent role and responsibilities
- **INPUT**: Expected JSON schema
- **TASKS**: Step-by-step processing instructions
- **OUTPUT**: Required JSON output format
- **CONDUCT/GUARDRAILS**: Rules and constraints

### Example: Using RSS Agent Prompt

```python
# Example with OpenAI API
import openai

# Load the prompt
with open('rss-agent-prompt.md', 'r') as f:
    system_prompt = f.read()

# Prepare input
user_input = {
    "crawl_started_utc": "2024-01-13T00:00:00Z",
    "feeds": [
        {"name": "CISA Feed", "url": "https://...", "priority": "high"}
    ],
    "since_utc": "2024-01-12T00:00:00Z",
    "until_utc": "2024-01-13T23:59:59Z"
}

# Call LLM
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": json.dumps(user_input)}
    ],
    temperature=0.1  # Low temperature for consistent outputs
)

# Parse JSON response
output = json.loads(response.choices[0].message.content)
```

### Example: Using with Claude API

```python
import anthropic

client = anthropic.Anthropic()

# Load prompt
with open('orchestrator-system-prompt.md', 'r') as f:
    system_prompt = f.read()

# Call Claude
response = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4000,
    temperature=0.1,
    system=system_prompt,
    messages=[
        {"role": "user", "content": json.dumps(input_data)}
    ]
)

# Extract JSON from response
output = json.loads(response.content[0].text)
```

## Implementing Your Own Agents

### Step 1: Choose Your Language
The prompts are language-agnostic. Implement in:
- Python
- JavaScript/TypeScript
- Go
- Java
- Any language with LLM API support

### Step 2: Core Components Needed

1. **LLM Integration**
   - API client for your chosen LLM
   - Prompt loading and formatting
   - Response parsing

2. **Data Validation**
   - JSON schema validation
   - Input/output validation per prompt specs

3. **Agent Orchestration**
   - Pipeline to chain agents
   - State management between agents

### Step 3: Follow the Schemas

Each prompt defines strict JSON schemas. Example from RSS Agent:

**Input Schema:**
```json
{
  "crawl_started_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "feeds": [{"name": "...", "url": "...", "priority": "..."}],
  "since_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "until_utc": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**Output Schema:**
```json
{
  "agent_type": "rss",
  "collected_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "intelligence": [
    {
      "source_type": "rss",
      "source_name": "...",
      "cves": ["CVE-YYYY-XXXX"],
      // ... full schema in prompt
    }
  ]
}
```

## Admiralty Grading System

All prompts use the Admiralty grading system:

### Source Reliability
- **A**: Official vendor/CERT advisory
- **B**: Major security organization
- **C**: Reputable media/researcher
- **D**: Community/unverified
- **E-F**: Unreliable (auto-DROP)

### Information Credibility
- **1**: Primary evidence confirmed
- **2**: Advisory with evidence
- **3**: Research report
- **4**: Unverified
- **5-6**: Unreliable (auto-DROP)

## Best Practices

1. **Temperature Settings**: Use low temperature (0.1-0.3) for consistent outputs
2. **JSON Validation**: Always validate LLM outputs against schemas
3. **Error Handling**: LLMs may occasionally produce invalid JSON
4. **Rate Limiting**: Implement appropriate delays between API calls
5. **Caching**: Cache enrichment data to reduce API calls
6. **Logging**: Log all agent inputs/outputs for debugging

## Integration Examples

### Pipeline Example
```python
def run_pipeline(feeds_data):
    # Step 1: RSS Collection
    rss_output = call_llm_agent("rss-agent-prompt.md", feeds_data)

    # Step 2: Deduplication
    dedup_output = call_llm_agent("dedup-agent-prompt.md", rss_output)

    # Step 3: Enrichment
    enriched = call_llm_agent("enrichment-agent-prompt.md", dedup_output)

    # Step 4: Orchestration
    routing = call_llm_agent("orchestrator-system-prompt.md", enriched)

    # Step 5: Generate outputs based on routing
    for decision in routing['decisions']:
        if decision['route'] == 'TECHNICAL_ALERT':
            alert = call_llm_agent("technical-alert-prompt.md", decision)
            send_to_soc(alert)
```

### Standalone Agent Usage
```python
# Use individual agents as needed
vendor_data = fetch_vendor_advisory("https://...")
parsed = call_llm_agent("vendor-parser-agent-prompt.md", {
    "fetched_at_utc": "2024-01-13T00:00:00Z",
    "advisory": vendor_data
})
```

## Customization

You can modify the prompts for your organization:

1. **Adjust Thresholds**: Modify EPSS/CVSS thresholds in orchestrator
2. **Add Products**: Extend product patterns in RSS agent
3. **Custom Routing**: Add organization-specific routing rules
4. **Output Formats**: Adapt output schemas to your tools

## Testing Prompts

Test prompts with sample data:

```bash
# Test with Claude CLI
cat sample_input.json | claude --system-prompt rss-agent-prompt.md

# Test with OpenAI CLI
openai api chat.completions.create \
  -m gpt-4 \
  -s "$(cat rss-agent-prompt.md)" \
  -u "$(cat sample_input.json)"
```

## Advantages of Prompt-Based Approach

1. **Language Agnostic**: Implement in any language
2. **LLM Flexible**: Use any capable LLM
3. **Easy Updates**: Modify behavior by editing prompts
4. **Transparent Logic**: Clear rules in human-readable format
5. **Testable**: Each agent can be tested independently

## Next Steps

1. Choose your implementation language
2. Set up LLM API access
3. Implement core agent wrapper
4. Test with individual prompts
5. Build pipeline orchestration
6. Deploy and monitor