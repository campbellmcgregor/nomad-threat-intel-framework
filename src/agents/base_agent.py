"""
Base Agent class for NOMAD framework
Provides common functionality for all agents
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from dotenv import load_dotenv
import anthropic
from anthropic import Anthropic
import time

class BaseAgent:
    """Base class for all NOMAD agents"""

    def __init__(self, agent_name: str):
        """Initialize base agent

        Args:
            agent_name: Name of the agent (e.g., 'rss_feed', 'orchestrator')
        """
        # Load environment variables
        load_dotenv()

        self.agent_name = agent_name
        self.logger = self._setup_logger()

        # Initialize Claude client if API key is available
        self.claude_client = None
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            try:
                self.claude_client = Anthropic(api_key=api_key)
                self.logger.info("Claude API client initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize Claude client: {e}")
        else:
            self.logger.warning("No ANTHROPIC_API_KEY found - LLM processing will use placeholder mode")

        # Look for prompt in root directory first, then prompts folder
        root_prompt = Path(__file__).parent.parent / f"{agent_name}-prompt.md"
        prompts_folder = Path(__file__).parent.parent / "prompts" / f"{agent_name}-prompt.md"

        if root_prompt.exists():
            self.prompt_path = root_prompt
        elif prompts_folder.exists():
            self.prompt_path = prompts_folder
        else:
            # Default to root location
            self.prompt_path = root_prompt

        self.data_dir = Path(__file__).parent.parent / "data"
        self.config = self._load_config()

    def _setup_logger(self) -> logging.Logger:
        """Setup agent-specific logger"""
        logger = logging.getLogger(f"nomad.{self.agent_name}")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML files"""
        config = {}
        config_dir = Path(__file__).parent.parent / "config"

        # Load RSS feeds config
        feeds_file = config_dir / "rss_feeds.yaml"
        if feeds_file.exists():
            with open(feeds_file, 'r') as f:
                config['feeds'] = yaml.safe_load(f)

        # Load general config if exists
        general_config = config_dir / "config.yaml"
        if general_config.exists():
            with open(general_config, 'r') as f:
                config.update(yaml.safe_load(f))

        return config

    def load_prompt(self) -> str:
        """Load the agent's prompt template"""
        if self.prompt_path.exists():
            with open(self.prompt_path, 'r') as f:
                return f.read()
        else:
            self.logger.warning(f"Prompt file not found: {self.prompt_path}")
            return ""

    def validate_json(self, data: Dict[str, Any], schema: Optional[Dict] = None) -> bool:
        """Validate JSON data against schema

        Args:
            data: JSON data to validate
            schema: Optional JSON schema to validate against

        Returns:
            Boolean indicating if data is valid
        """
        # Basic validation - can be extended with jsonschema library
        if not isinstance(data, dict):
            return False

        # Add schema validation here if needed
        return True

    def save_output(self, data: Dict[str, Any], filename: str) -> str:
        """Save agent output to file

        Args:
            data: Data to save
            filename: Output filename

        Returns:
            Path to saved file
        """
        output_path = self.data_dir / "output" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        self.logger.info(f"Output saved to: {output_path}")
        return str(output_path)

    def load_input(self, filename: str) -> Dict[str, Any]:
        """Load input data from file

        Args:
            filename: Input filename

        Returns:
            Loaded JSON data
        """
        input_path = self.data_dir / "input" / filename

        if not input_path.exists():
            # Try looking in output directory
            input_path = self.data_dir / "output" / filename

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {filename}")

        with open(input_path, 'r') as f:
            return json.load(f)

    def get_timestamp(self) -> str:
        """Get current UTC timestamp in standard format"""
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    def run(self, **kwargs) -> Dict[str, Any]:
        """Run the agent - to be implemented by subclasses

        Args:
            **kwargs: Agent-specific arguments

        Returns:
            Agent output as dictionary
        """
        raise NotImplementedError("Subclasses must implement run() method")

    def process_with_llm(self, input_data: Dict[str, Any], max_retries: int = 3) -> Dict[str, Any]:
        """Process data using LLM with agent's prompt

        Args:
            input_data: Input data for the agent
            max_retries: Maximum number of API call retries

        Returns:
            Processed output from LLM
        """
        prompt_template = self.load_prompt()

        if not prompt_template:
            self.logger.error(f"No prompt template found for {self.agent_name}")
            return {"error": "No prompt template available", "agent": self.agent_name}

        # Format the full prompt with input data
        full_prompt = self._format_prompt(prompt_template, input_data)

        if not self.claude_client:
            self.logger.warning("No Claude client available - returning placeholder")
            return {
                "status": "no_api_key",
                "agent": self.agent_name,
                "timestamp": self.get_timestamp(),
                "input_received": bool(input_data)
            }

        # Process with Claude API
        return self._call_claude_api(full_prompt, max_retries)

    def _format_prompt(self, template: str, input_data: Dict[str, Any]) -> str:
        """Format prompt template with input data

        Args:
            template: The prompt template
            input_data: Data to insert into template

        Returns:
            Formatted prompt string
        """
        # For NOMAD agents, input data is typically JSON that should be inserted
        # into the INPUT section of the prompt
        if input_data:
            input_json = json.dumps(input_data, indent=2, default=str)
            # Look for INPUT section and replace or append
            if "INPUT" in template and "{" in template:
                # Replace placeholder JSON in template
                import re
                # Find JSON blocks in template and replace with actual data
                json_pattern = r'\{[\s\S]*?\}'
                template = re.sub(json_pattern, input_json, template, count=1)
            else:
                # Append input data to template
                template += f"\n\nINPUT:\n{input_json}"

        return template

    def _call_claude_api(self, prompt: str, max_retries: int) -> Dict[str, Any]:
        """Make API call to Claude with retry logic

        Args:
            prompt: Formatted prompt to send
            max_retries: Maximum retry attempts

        Returns:
            Parsed response from Claude
        """
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Calling Claude API (attempt {attempt + 1}/{max_retries})")

                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=4096,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                # Extract response content
                response_text = response.content[0].text if response.content else ""

                # Try to parse JSON response
                parsed_response = self._parse_response(response_text)

                self.logger.info(f"Successfully processed with Claude API")
                return {
                    "status": "success",
                    "agent": self.agent_name,
                    "timestamp": self.get_timestamp(),
                    "response": parsed_response,
                    "raw_response": response_text
                }

            except anthropic.APITimeoutError as e:
                self.logger.warning(f"Claude API timeout (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue

            except anthropic.APIError as e:
                self.logger.error(f"Claude API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            except Exception as e:
                self.logger.error(f"Unexpected error calling Claude API: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue

        # All retries failed
        return {
            "status": "api_error",
            "agent": self.agent_name,
            "timestamp": self.get_timestamp(),
            "error": "Failed to get response from Claude API after all retries"
        }

    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Claude's response, handling both JSON and text

        Args:
            response_text: Raw response from Claude

        Returns:
            Parsed response data
        """
        # Try to extract JSON from response
        try:
            # Look for JSON blocks in markdown code fences
            import re
            json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
                return json.loads(json_text)

            # Try to parse the entire response as JSON
            return json.loads(response_text)

        except json.JSONDecodeError:
            # If not valid JSON, look for JSON-like content
            json_start = response_text.find('{')
            json_end = response_text.rfind('}')

            if json_start >= 0 and json_end > json_start:
                try:
                    json_content = response_text[json_start:json_end + 1]
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    pass

            # Return as text if no JSON found
            return {
                "text_response": response_text,
                "parsed": False
            }