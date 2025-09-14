"""
Workflow validation and error recovery utilities for NOMAD Framework
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

class WorkflowValidator:
    """Validates workflow inputs, outputs, and provides error recovery"""

    def __init__(self):
        self.logger = logging.getLogger("nomad.workflow.validator")

    def validate_agent_input(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input data for a specific agent

        Args:
            agent_name: Name of the agent
            input_data: Input data to validate

        Returns:
            Validation result with errors and fixes
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "fixes_applied": [],
            "corrected_data": input_data.copy()
        }

        if agent_name == "rss_feed":
            validation_result = self._validate_rss_input(input_data, validation_result)
        elif agent_name == "orchestrator":
            validation_result = self._validate_orchestrator_input(input_data, validation_result)
        elif agent_name == "ciso_report":
            validation_result = self._validate_ciso_input(input_data, validation_result)

        return validation_result

    def validate_agent_output(self, agent_name: str, output_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate output data from an agent

        Args:
            agent_name: Name of the agent
            output_data: Output data to validate

        Returns:
            Validation result
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "schema_compliance": True
        }

        # Check basic structure
        if not isinstance(output_data, dict):
            validation_result["valid"] = False
            validation_result["errors"].append("Output must be a dictionary")
            return validation_result

        # Agent-specific validation
        if agent_name == "rss_feed":
            validation_result = self._validate_rss_output(output_data, validation_result)
        elif agent_name == "orchestrator":
            validation_result = self._validate_orchestrator_output(output_data, validation_result)
        elif agent_name == "ciso_report":
            validation_result = self._validate_ciso_output(output_data, validation_result)

        return validation_result

    def _validate_rss_input(self, input_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate RSS agent input"""
        # RSS agent typically doesn't require complex input validation
        # since it pulls from configured feeds
        return result

    def _validate_orchestrator_input(self, input_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate orchestrator input"""
        required_fields = ["received_at_utc", "items", "context"]

        for field in required_fields:
            if field not in input_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")

        # Validate items structure
        if "items" in input_data:
            items = input_data["items"]
            if not isinstance(items, list):
                result["valid"] = False
                result["errors"].append("'items' must be a list")
            else:
                for i, item in enumerate(items):
                    if not isinstance(item, dict):
                        result["errors"].append(f"Item {i} must be a dictionary")
                    elif "dedupe_key" not in item:
                        result["warnings"].append(f"Item {i} missing dedupe_key")

        return result

    def _validate_ciso_input(self, input_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate CISO report input"""
        required_fields = ["week_start", "week_end", "decisions"]

        for field in required_fields:
            if field not in input_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")

        # Validate date formats
        for date_field in ["week_start", "week_end"]:
            if date_field in input_data:
                try:
                    datetime.strptime(input_data[date_field], "%Y-%m-%d")
                except ValueError:
                    result["errors"].append(f"Invalid date format for {date_field} (expected YYYY-MM-DD)")

        return result

    def _validate_rss_output(self, output_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate RSS agent output"""
        required_fields = ["agent_type", "collected_at_utc", "intelligence"]

        for field in required_fields:
            if field not in output_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")

        # Validate intelligence items
        if "intelligence" in output_data:
            intelligence = output_data["intelligence"]
            if not isinstance(intelligence, list):
                result["valid"] = False
                result["errors"].append("'intelligence' must be a list")
            else:
                for i, item in enumerate(intelligence):
                    item_errors = self._validate_intelligence_item(item, i)
                    result["errors"].extend(item_errors)

        return result

    def _validate_orchestrator_output(self, output_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate orchestrator output"""
        required_fields = ["agent_type", "processed_at_utc", "routing_decisions"]

        for field in required_fields:
            if field not in output_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")

        return result

    def _validate_ciso_output(self, output_data: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate CISO report output"""
        required_fields = ["agent_type", "generated_at_utc", "report"]

        for field in required_fields:
            if field not in output_data:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")

        return result

    def _validate_intelligence_item(self, item: Dict[str, Any], index: int) -> List[str]:
        """Validate a single intelligence item"""
        errors = []
        required_fields = [
            "source_type", "source_name", "source_url", "title",
            "published_utc", "dedupe_key"
        ]

        for field in required_fields:
            if field not in item:
                errors.append(f"Item {index}: Missing required field '{field}'")

        # Validate CVE format
        if "cves" in item and item["cves"]:
            for cve in item["cves"]:
                if not isinstance(cve, str) or not cve.startswith("CVE-"):
                    errors.append(f"Item {index}: Invalid CVE format: {cve}")

        return errors

class ErrorRecovery:
    """Provides error recovery strategies for workflow failures"""

    def __init__(self):
        self.logger = logging.getLogger("nomad.workflow.recovery")

    def attempt_recovery(self, agent_name: str, error_type: str,
                        input_data: Dict[str, Any], error_details: str) -> Dict[str, Any]:
        """Attempt to recover from an agent error

        Args:
            agent_name: Name of the failed agent
            error_type: Type of error (api_error, timeout, validation_error, etc.)
            input_data: Original input data
            error_details: Details about the error

        Returns:
            Recovery strategy result
        """
        recovery_result = {
            "strategy": None,
            "success": False,
            "corrected_input": None,
            "retry_recommended": False,
            "fallback_available": False,
            "message": ""
        }

        self.logger.info(f"Attempting recovery for {agent_name} error: {error_type}")

        if error_type == "api_error":
            return self._recover_api_error(agent_name, input_data, error_details, recovery_result)
        elif error_type == "timeout":
            return self._recover_timeout(agent_name, input_data, recovery_result)
        elif error_type == "validation_error":
            return self._recover_validation_error(agent_name, input_data, error_details, recovery_result)
        elif error_type == "json_parse_error":
            return self._recover_json_parse_error(agent_name, recovery_result)
        else:
            recovery_result["message"] = f"No recovery strategy available for {error_type}"

        return recovery_result

    def _recover_api_error(self, agent_name: str, input_data: Dict[str, Any],
                          error_details: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from API errors"""
        result["strategy"] = "api_error_recovery"

        # Rate limit errors
        if "rate limit" in error_details.lower():
            result["retry_recommended"] = True
            result["message"] = "Rate limit hit, recommend retry with exponential backoff"
            return result

        # Authentication errors
        if "authentication" in error_details.lower() or "api key" in error_details.lower():
            result["message"] = "Authentication error, check API key configuration"
            result["fallback_available"] = True  # Could use cached data
            return result

        # Quota exceeded
        if "quota" in error_details.lower() or "usage" in error_details.lower():
            result["message"] = "API quota exceeded, consider fallback processing"
            result["fallback_available"] = True
            return result

        # General API error - retry with smaller input
        if isinstance(input_data, dict) and "items" in input_data:
            items = input_data["items"]
            if isinstance(items, list) and len(items) > 10:
                # Split into smaller batches
                result["strategy"] = "batch_splitting"
                result["corrected_input"] = input_data.copy()
                result["corrected_input"]["items"] = items[:5]  # Process smaller batch
                result["retry_recommended"] = True
                result["success"] = True
                result["message"] = f"Splitting large input ({len(items)} items) into smaller batches"

        return result

    def _recover_timeout(self, agent_name: str, input_data: Dict[str, Any],
                        result: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from timeout errors"""
        result["strategy"] = "timeout_recovery"
        result["retry_recommended"] = True

        # Reduce input size for timeout recovery
        if isinstance(input_data, dict) and "items" in input_data:
            items = input_data["items"]
            if isinstance(items, list) and len(items) > 5:
                result["corrected_input"] = input_data.copy()
                result["corrected_input"]["items"] = items[:3]  # Much smaller batch
                result["success"] = True
                result["message"] = "Timeout occurred, reducing batch size for retry"

        return result

    def _recover_validation_error(self, agent_name: str, input_data: Dict[str, Any],
                                 error_details: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from validation errors"""
        result["strategy"] = "validation_recovery"

        # Try to fix common validation issues
        validator = WorkflowValidator()
        validation_result = validator.validate_agent_input(agent_name, input_data)

        if validation_result["fixes_applied"]:
            result["corrected_input"] = validation_result["corrected_data"]
            result["retry_recommended"] = True
            result["success"] = True
            result["message"] = f"Applied {len(validation_result['fixes_applied'])} fixes to input data"
        else:
            result["message"] = f"Validation errors cannot be automatically fixed: {error_details}"

        return result

    def _recover_json_parse_error(self, agent_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Recover from JSON parsing errors"""
        result["strategy"] = "json_recovery"
        result["retry_recommended"] = True
        result["message"] = "JSON parse error, recommend retry with explicit JSON format instruction"

        # Could implement JSON repair strategies here
        return result

    def save_recovery_log(self, workflow_name: str, agent_name: str,
                         recovery_attempt: Dict[str, Any]):
        """Save recovery attempt to log file"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "workflow": workflow_name,
            "agent": agent_name,
            "recovery_attempt": recovery_attempt
        }

        log_dir = Path("data/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"recovery_log_{datetime.now().strftime('%Y%m%d')}.jsonl"

        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")

        self.logger.info(f"Recovery attempt logged to {log_file}")

def create_checkpoint(workflow_name: str, step: int, agent_name: str,
                     input_data: Dict[str, Any], output_data: Dict[str, Any]):
    """Create a checkpoint for workflow recovery

    Args:
        workflow_name: Name of the workflow
        step: Current step number
        agent_name: Name of the agent
        input_data: Input data for the step
        output_data: Output data from the step
    """
    checkpoint = {
        "workflow": workflow_name,
        "step": step,
        "agent": agent_name,
        "timestamp": datetime.utcnow().isoformat(),
        "input_data": input_data,
        "output_data": output_data
    }

    checkpoint_dir = Path("data/checkpoints")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_file = checkpoint_dir / f"{workflow_name}_step_{step}_{agent_name}.json"

    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint, f, indent=2, default=str)

    print(f"💾 Checkpoint saved: {checkpoint_file}")

def load_checkpoint(workflow_name: str, step: int, agent_name: str) -> Optional[Dict[str, Any]]:
    """Load a checkpoint for workflow recovery

    Args:
        workflow_name: Name of the workflow
        step: Step number
        agent_name: Name of the agent

    Returns:
        Checkpoint data or None if not found
    """
    checkpoint_file = Path(f"data/checkpoints/{workflow_name}_step_{step}_{agent_name}.json")

    if checkpoint_file.exists():
        with open(checkpoint_file, 'r') as f:
            return json.load(f)

    return None