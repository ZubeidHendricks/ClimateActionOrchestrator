"""
Logging setup utility for Climate Action Orchestrator

This module provides functions for configuring logging.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
import sys
from typing import Dict, Any, Optional

def setup_logging(config: Optional[Dict[str, Any]] = None) -> None:
    """
    Set up logging configuration based on settings.
    
    Args:
        config: Logging configuration dictionary
    """
    if config is None:
        config = {}
    
    # Get logging settings
    log_level_str = config.get("level", os.environ.get("CAO_LOGGING_LEVEL", "INFO"))
    log_format = config.get("format", os.environ.get("CAO_LOGGING_FORMAT", 
                                                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    log_file = config.get("file", os.environ.get("CAO_LOGGING_FILE", None))
    log_max_size = int(config.get("max_size", os.environ.get("CAO_LOGGING_MAX_SIZE", 10 * 1024 * 1024)))  # 10MB default
    log_backup_count = int(config.get("backup_count", os.environ.get("CAO_LOGGING_BACKUP_COUNT", 5)))
    
    # Convert log level string to logging constant
    log_level_str = log_level_str.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to prevent duplicate logs
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Create file handler if log file is specified
    if log_file:
        # Create directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=log_max_size, 
            backupCount=log_backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set library loggers to WARNING level to reduce noise
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    
    # Log configuration information
    logging.info(f"Logging initialized at level {log_level_str}")
    if log_file:
        logging.info(f"Logging to file: {log_file}")
