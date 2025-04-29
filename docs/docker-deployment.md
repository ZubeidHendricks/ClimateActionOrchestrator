# Docker Deployment Guide for Climate Action Orchestrator

This guide provides instructions for deploying the Climate Action Orchestrator using Docker containers, making it easy to set up and run in any environment.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system
- Basic familiarity with Docker concepts

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/ClimateActionOrchestrator.git
   cd ClimateActionOrchestrator
   ```

2. Create and configure environment variables:
   ```bash
   cp .env.sample .env
   # Edit .env with your configuration
   ```

3. Build and run with Docker Compose:
   ```bash
   # On Linux/macOS
   ./docker-run.sh up
   
   # On Windows
   docker-run.bat up
   ```

## Configuration

### Environment Variables

The `.env` file contains all the configuration needed for the Docker deployment. Key variables include:

- `AZURE_STORAGE_CONNECTION_STRING`: Connection string for Azure Blob Storage
- `AZURE_COSMOS_ENDPOINT`: Endpoint URL for Azure Cosmos DB
- `AZURE_COSMOS_KEY`: Access key for Azure Cosmos DB
- `AZURE_COSMOS_DATABASE`: Database name for Azure Cosmos DB
- `CAO_LOGGING_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Local Development with Azurite

For local development, you can use Azurite to emulate Azure Blob Storage:

```bash
# Start only the Azurite container
docker-compose up -d azurite
```

The default connection string for Azurite is already configured in the `.env.sample` file.

## Using the Docker Helper Scripts

We provide helper scripts to simplify Docker operations:

### Linux/macOS (`docker-run.sh`)

```bash
# Build the Docker image
./docker-run.sh build

# Start the services
./docker-run.sh up

# Stop the services
./docker-run.sh down

# Restart the services
./docker-run.sh restart

# View logs
./docker-run.sh logs

# Run verification
./docker-run.sh verify

# Display help
./docker-run.sh help
```

### Windows (`docker-run.bat`)

```bash
# Build the Docker image
docker-run.bat build

# Start the services
docker-run.bat up

# Stop the services
docker-run.bat down

# Restart the services
docker-run.bat restart

# View logs
docker-run.bat logs

# Run verification
docker-run.bat verify

# Display help
docker-run.bat help
```

## Docker Compose Configuration

The `docker-compose.yml` file defines the following services:

- `climate-orchestrator`: The main application
- `azurite`: Azure Storage emulator for local development

You can customize the Docker Compose configuration by editing the `docker-compose.yml` file.

## Production Deployment

For production deployment, make the following changes:

1. Update the `.env` file with production Azure credentials
2. Modify the command in `docker-compose.yml` to run the actual application:
   ```yaml
   command: ["python", "orchestrator.py"]
   ```
3. Consider using Docker Swarm or Kubernetes for orchestration in production environments

## Data Persistence

The following volumes are created to persist data:

- `./data:/app/data`: Application data directory
- `./reports:/app/reports`: Generated reports
- `./logs:/app/logs`: Application logs
- `./.env:/app/.env`: Environment configuration
- `./azurite_data:/data`: Azurite storage data (local development only)

## Troubleshooting

### Container fails to start

Check the container logs:
```bash
docker-compose logs climate-orchestrator
```

### Connection issues with Azure services

- Verify your environment variables in the `.env` file
- Check your network connection and firewall settings
- For local development, ensure Azurite is running

### Permission issues with volumes

Ensure the directory permissions are set correctly:
```bash
chmod -R 777 data reports logs cache
```

## Advanced Configuration

### Custom Dockerfile

You can customize the `Dockerfile` to add additional dependencies or configurations:

1. Edit the `Dockerfile` in the project root
2. Rebuild the Docker image:
   ```bash
   ./docker-run.sh build
   ```

### Adding Web Interface

To expose a web interface through the container:

1. Create a web application (e.g., using Flask or FastAPI)
2. Update the `Dockerfile` to install web dependencies
3. Update the `CMD` in the `Dockerfile` to run the web server
4. Map the container port in `docker-compose.yml`

## Security Considerations

- Do not store sensitive credentials directly in the Dockerfile
- Use environment variables or Docker secrets for sensitive information
- Regularly update the base Docker image to get security patches
- Run containers with non-root users when possible (already configured)

## Next Steps

After successfully deploying with Docker, consider:

1. Setting up CI/CD pipelines for automated deployments
2. Implementing monitoring and alerting
3. Setting up automated backups of your data volumes
4. Creating a web interface for easier interaction with the application
