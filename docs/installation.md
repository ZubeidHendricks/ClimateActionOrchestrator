# Installation Guide for Climate Action Orchestrator

This guide will walk you through the process of setting up the Climate Action Orchestrator on your system.

## Prerequisites

Before installing the Climate Action Orchestrator, ensure you have the following:

- Python 3.8 or higher
- An Azure account with appropriate permissions
- The following Azure services:
  - Azure Blob Storage
  - Azure Cosmos DB
  - Azure AI services (formerly Azure OpenAI Service)
  - Azure Active Directory (for authentication)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/your-organization/ClimateActionOrchestrator.git
cd ClimateActionOrchestrator
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Azure Resources

The Climate Action Orchestrator relies on several Azure services. You'll need to:

1. **Set up an Azure Blob Storage account** for storing operational data and reports
2. **Create an Azure Cosmos DB database** for storing emissions data and calculations
3. **Set up Azure AI services** for recommendations and scenario modeling
4. **Configure Azure Active Directory** for authentication

### 5. Create Configuration Files

Create a `.env` file in the root directory with the following environment variables:

```
# Azure Storage
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string

# Azure Cosmos DB
AZURE_COSMOS_ENDPOINT=your_cosmos_endpoint
AZURE_COSMOS_KEY=your_cosmos_key
AZURE_COSMOS_DATABASE=climate_action

# Azure AI
AZURE_OPENAI_ENDPOINT=your_openai_endpoint
AZURE_OPENAI_KEY=your_openai_key

# Logging
CAO_LOGGING_LEVEL=INFO
CAO_LOGGING_FILE=logs/climate_action.log
```

### 6. Initialize Data Stores

Create the necessary data directories:

```bash
mkdir -p data/emissions_factors
mkdir -p reports
mkdir -p logs
```

### 7. Verify Installation

Run the verification script to ensure everything is set up correctly:

```bash
python tests/verify_installation.py
```

If successful, you should see a message indicating that the installation is complete and all components are functioning properly.

## Troubleshooting

### Azure Connection Issues

If you encounter connection issues with Azure services:

1. Verify that your Azure credentials are correct and have appropriate permissions
2. Check that your IP address is allowed in Azure firewall settings
3. Ensure that the required Azure services are provisioned in your subscription

### Package Dependency Issues

If you encounter dependency conflicts:

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Data Storage Issues

If you encounter issues with data storage:

1. Ensure that your Azure Blob Storage containers are properly configured
2. Check that your Cosmos DB database and containers are created with appropriate throughput

## Next Steps

Once you've successfully installed the Climate Action Orchestrator, proceed to the [Quick Start Tutorial](quickstart.md) to begin using the system.

For more advanced configuration options, see the [Configuration Guide](configuration.md).
