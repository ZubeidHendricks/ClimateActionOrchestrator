#!/usr/bin/env python
"""
Verification script for Climate Action Orchestrator installation.

This script checks that all components are properly installed and configured,
and that the system can connect to required services.
"""

import os
import sys
import importlib
import logging

# Setup simple logging for this script
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("verification")

def check_python_version():
    """Check that Python version is 3.8 or higher."""
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        logger.error(f"Python version {major}.{minor} is not supported. Please use Python 3.8 or higher.")
        return False
    logger.info(f"Python version {major}.{minor} is supported.")
    return True

def check_dependencies():
    """Check that all required packages are installed."""
    required_packages = [
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "azure-cosmos",
        "azure-storage-blob",
        "azure-identity",
        "python-dotenv",
        "requests"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace("-", "_"))
            logger.info(f"Package {package} is installed.")
        except ImportError:
            missing_packages.append(package)
            logger.error(f"Package {package} is not installed.")
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.error("Please install them with: pip install -r requirements.txt")
        return False
    return True

def check_environment_variables():
    """Check that required environment variables are set."""
    required_variables = [
        "AZURE_STORAGE_CONNECTION_STRING",
        "AZURE_COSMOS_ENDPOINT",
        "AZURE_COSMOS_KEY",
        "AZURE_COSMOS_DATABASE"
    ]
    
    missing_variables = []
    for variable in required_variables:
        if not os.environ.get(variable):
            missing_variables.append(variable)
            logger.error(f"Environment variable {variable} is not set.")
    
    if missing_variables:
        logger.error(f"Missing environment variables: {', '.join(missing_variables)}")
        logger.error("Please set them in your .env file or environment.")
        return False
    
    logger.info("All required environment variables are set.")
    return True

def check_data_directories():
    """Check that required data directories exist."""
    required_directories = [
        "data",
        "reports",
        "logs"
    ]
    
    missing_directories = []
    for directory in required_directories:
        if not os.path.isdir(directory):
            missing_directories.append(directory)
            logger.error(f"Directory {directory} does not exist.")
    
    if missing_directories:
        logger.error(f"Missing directories: {', '.join(missing_directories)}")
        logger.error("Please create them before running the application.")
        return False
    
    logger.info("All required directories exist.")
    return True

def check_emissions_factors():
    """Check that emissions factors file exists."""
    emissions_factors_path = os.path.join("data", "emissions_factors.json")
    if not os.path.isfile(emissions_factors_path):
        logger.error(f"Emissions factors file {emissions_factors_path} does not exist.")
        return False
    
    logger.info("Emissions factors file exists.")
    return True

def check_agent_modules():
    """Check that all agent modules can be imported."""
    agent_modules = [
        "agents.data_collection_agent",
        "agents.carbon_calculation_agent",
        "agents.recommendation_agent",
        "agents.simulation_agent",
        "agents.reporting_agent"
    ]
    
    missing_modules = []
    for module in agent_modules:
        try:
            importlib.import_module(module)
            logger.info(f"Module {module} can be imported.")
        except ImportError as e:
            missing_modules.append(module)
            logger.error(f"Module {module} cannot be imported: {e}")
    
    if missing_modules:
        logger.error(f"Missing modules: {', '.join(missing_modules)}")
        return False
    return True

def verify_installation():
    """Run all verification checks."""
    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment variables", check_environment_variables),
        ("Data directories", check_data_directories),
        ("Emissions factors", check_emissions_factors),
        ("Agent modules", check_agent_modules)
    ]
    
    results = []
    
    logger.info("Starting Climate Action Orchestrator verification...")
    for name, check_func in checks:
        logger.info(f"Checking {name}...")
        result = check_func()
        results.append((name, result))
    
    # Print summary
    logger.info("\n=== Verification Summary ===")
    all_passed = True
    for name, result in results:
        status = "PASSED" if result else "FAILED"
        if not result:
            all_passed = False
        logger.info(f"{name}: {status}")
    
    if all_passed:
        logger.info("\n✅ All checks passed! Climate Action Orchestrator is ready to use.")
        return 0
    else:
        logger.error("\n❌ Some checks failed. Please fix the issues above before using the application.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_installation())
