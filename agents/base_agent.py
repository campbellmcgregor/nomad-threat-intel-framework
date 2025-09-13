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

class BaseAgent:
    """Base class for all NOMAD agents"""

    def __init__(self, agent_name: str):
        """Initialize base agent

        Args:
            agent_name: Name of the agent (e.g., 'rss_feed', 'orchestrator')
        """
        self.agent_name = agent_name
        self.logger = self._setup_logger()

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

    def process_with_llm(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data using LLM with agent's prompt

        This method would integrate with Claude Code's Task tool
        or an LLM API directly

        Args:
            input_data: Input data for the agent

        Returns:
            Processed output from LLM
        """
        prompt = self.load_prompt()

        # This is where Claude Code would process the data
        # For now, return a placeholder
        self.logger.info(f"Processing with LLM using prompt from {self.prompt_path}")

        # In actual implementation, this would:
        # 1. Format input_data according to prompt requirements
        # 2. Call LLM API or Claude Code Task tool
        # 3. Parse and validate the response
        # 4. Return structured output

        return {
            "status": "pending_implementation",
            "agent": self.agent_name,
            "timestamp": self.get_timestamp()
        }