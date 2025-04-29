"""
Configuration utility for Climate Action Orchestrator

This module provides functions for loading, validating, and managing configuration.
"""

import os
import json
import logging
import yaml
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a file or environment variables.
    
    Args:
        config_path: Path to configuration file (JSON or YAML)
        
    Returns:
        Configuration dictionary
    """
    config = {}
    
    # Try to load from file if provided
    if config_path:
        if os.path.exists(config_path):
            try:
                file_ext = os.path.splitext(config_path)[1].lower()
                if file_ext == '.json':
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                elif file_ext in ['.yaml', '.yml']:
                    with open(config_path, 'r') as f:
                        config = yaml.safe_load(f)
                else:
                    logger.warning(f"Unsupported config file format: {file_ext}")
                    
                logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                logger.error(f"Error loading configuration from {config_path}: {str(e)}")
        else:
            logger.warning(f"Configuration file not found: {config_path}")
    
    # If no config file or it couldn't be loaded, use default config
    if not config:
        logger.info("Using default configuration")
        config = get_default_config()
    
    # Override with environment variables
    config = override_from_env(config)
    
    # Validate configuration
    validate_config(config)
    
    return config

def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration values.
    
    Returns:
        Default configuration dictionary
    """
    return {
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": None
        },
        "data_agent": {
            "sources": ["azure_blob", "csv", "api"],
            "cache_dir": "cache/data"
        },
        "carbon_agent": {
            "emissions_factors_source": "default",
            "calculation_method": "ghg_protocol"
        },
        "recommendation_agent": {
            "industry_insights_enabled": True,
            "max_recommendations": 20
        },
        "simulation_agent": {
            "models": {
                "business_growth": {"type": "linear", "params": {"default_rate": 0.03}},
                "carbon_intensity": {"type": "exponential", "params": {"default_rate": -0.01}}
            },
            "simulation_years": 10
        },
        "reporting_agent": {
            "output_dir": "reports",
            "formats": ["json", "pdf", "html"]
        }
    }

def override_from_env(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Override configuration with environment variables.
    
    Environment variables should be in the format:
    CAO_SECTION_KEY=value
    
    For example:
    CAO_LOGGING_LEVEL=DEBUG
    CAO_DATA_AGENT_CACHE_DIR=/tmp/cache
    
    Args:
        config: Base configuration to override
        
    Returns:
        Overridden configuration
    """
    # Create a copy to avoid modifying the original
    result = config.copy()
    
    # Look for environment variables with CAO_ prefix
    for env_var, value in os.environ.items():
        if env_var.startswith("CAO_"):
            parts = env_var[4:].lower().split("_")
            
            # Navigate to the right place in the config
            current = result
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Set the value, attempting to convert to appropriate type
            try:
                # Try to convert to int or float if it looks numeric
                if value.isdigit():
                    value = int(value)
                elif value.replace(".", "", 1).isdigit():
                    value = float(value)
                # Convert boolean strings
                elif value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
            except (ValueError, AttributeError):
                # If conversion fails, use the original string value
                pass
            
            current[parts[-1]] = value
            logger.debug(f"Overrode config {'.'.join(parts)} with environment variable")
    
    return result

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Validate configuration structure and values.
    
    Args:
        config: Configuration to validate
        
    Returns:
        True if valid, raises ValueError otherwise
    """
    # Check required top-level sections
    required_sections = ["data_agent", "carbon_agent", "recommendation_agent", 
                        "simulation_agent", "reporting_agent"]
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required configuration section: {section}")
    
    # Validate specific settings
    if "logging" in config:
        if "level" in config["logging"]:
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if config["logging"]["level"] not in valid_levels:
                raise ValueError(f"Invalid logging level: {config['logging']['level']}")
    
    # More validation could be added for specific agent configs
    
    logger.debug("Configuration validation passed")
    return True
