#!/bin/bash

# Script to build and run the Climate Action Orchestrator Docker container

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker before continuing."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose could not be found. Please install Docker Compose before continuing."
    exit 1
fi

# Function to display help
show_help() {
    echo "Climate Action Orchestrator Docker Script"
    echo ""
    echo "Usage: ./docker-run.sh [OPTION]"
    echo ""
    echo "Options:"
    echo "  build     Build the Docker image"
    echo "  up        Start the services"
    echo "  down      Stop the services"
    echo "  restart   Restart the services"
    echo "  logs      Show logs"
    echo "  verify    Run the verification script"
    echo "  help      Show this help message"
    echo ""
}

# Create necessary directories
create_directories() {
    mkdir -p data reports logs cache/data azurite_data
    echo "Created necessary directories."
}

# Check for .env file
check_env_file() {
    if [ ! -f .env ]; then
        echo "Warning: .env file not found. Creating from .env.sample..."
        if [ -f .env.sample ]; then
            cp .env.sample .env
            echo "Created .env file. Please edit it with your configuration."
        else
            echo "Error: .env.sample file not found. Please create a .env file with your configuration."
            exit 1
        fi
    fi
}

# Process arguments
case "$1" in
    build)
        create_directories
        check_env_file
        echo "Building Docker image..."
        docker-compose build
        ;;
    up)
        create_directories
        check_env_file
        echo "Starting services..."
        docker-compose up -d
        ;;
    down)
        echo "Stopping services..."
        docker-compose down
        ;;
    restart)
        echo "Restarting services..."
        docker-compose down
        docker-compose up -d
        ;;
    logs)
        echo "Showing logs..."
        docker-compose logs -f
        ;;
    verify)
        create_directories
        check_env_file
        echo "Running verification..."
        docker-compose run climate-orchestrator python -m tests.verify_installation
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac

exit 0
