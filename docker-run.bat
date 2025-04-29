@echo off
REM Script to build and run the Climate Action Orchestrator Docker container on Windows

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Docker could not be found. Please install Docker before continuing.
    exit /b 1
)

REM Check if docker-compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Docker Compose could not be found. Please install Docker Compose before continuing.
    exit /b 1
)

REM Function to display help
:show_help
    echo Climate Action Orchestrator Docker Script
    echo.
    echo Usage: docker-run.bat [OPTION]
    echo.
    echo Options:
    echo   build     Build the Docker image
    echo   up        Start the services
    echo   down      Stop the services
    echo   restart   Restart the services
    echo   logs      Show logs
    echo   verify    Run the verification script
    echo   help      Show this help message
    echo.
    goto :eof

REM Create necessary directories
:create_directories
    if not exist data mkdir data
    if not exist reports mkdir reports
    if not exist logs mkdir logs
    if not exist cache\data mkdir cache\data
    if not exist azurite_data mkdir azurite_data
    echo Created necessary directories.
    goto :eof

REM Check for .env file
:check_env_file
    if not exist .env (
        echo Warning: .env file not found. Creating from .env.sample...
        if exist .env.sample (
            copy .env.sample .env
            echo Created .env file. Please edit it with your configuration.
        ) else (
            echo Error: .env.sample file not found. Please create a .env file with your configuration.
            exit /b 1
        )
    )
    goto :eof

REM Process arguments
if "%1"=="" goto :show_help
if "%1"=="build" goto :build
if "%1"=="up" goto :up
if "%1"=="down" goto :down
if "%1"=="restart" goto :restart
if "%1"=="logs" goto :logs
if "%1"=="verify" goto :verify
if "%1"=="help" goto :show_help
goto :show_help

:build
    call :create_directories
    call :check_env_file
    echo Building Docker image...
    docker-compose build
    goto :eof

:up
    call :create_directories
    call :check_env_file
    echo Starting services...
    docker-compose up -d
    goto :eof

:down
    echo Stopping services...
    docker-compose down
    goto :eof

:restart
    echo Restarting services...
    docker-compose down
    docker-compose up -d
    goto :eof

:logs
    echo Showing logs...
    docker-compose logs -f
    goto :eof

:verify
    call :create_directories
    call :check_env_file
    echo Running verification...
    docker-compose run climate-orchestrator python -m tests.verify_installation
    goto :eof
