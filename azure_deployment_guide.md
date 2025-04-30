# Deploying Climate Action Orchestrator Dashboard to Azure App Service

This guide will walk you through deploying your Climate Action Orchestrator dashboard to Azure App Service using GitHub deployment.

## Prerequisites

- An Azure account with an active subscription
- Your GitHub repository with the Climate Action Orchestrator code
- Git installed on your local machine

## Step 1: Configure Deployment Files

Before deploying, we need to ensure only production code is deployed, not demo files. I've added a `.gitignore` file that excludes all demo-specific files from deployment.

Files that will NOT be deployed:
- `run_agent_demo.py`
- `agent_realtime_demo.py`
- `demo_commands.ps1`
- `demo_commands.bat`
- `demo_script.md`
- `demo_video_script.md`
- `azure_demo_script.md`
- `azure_agent_architecture.md`
- `run_demo.py`
- `dashboard_requirements.txt`
- `run_dashboard.bat`

These files are useful for your local development and demo preparation but aren't needed in the production environment.

## Step 2: Commit Your Latest Changes to GitHub

Make sure all your changes are committed to your GitHub repository:

```bash
git add .
git commit -m "Prepared dashboard for Azure deployment"
git push origin main
```

## Step 3: Create an Azure App Service Web App

1. **Go to the Azure Portal**: Sign in to [portal.azure.com](https://portal.azure.com)

2. **Create a New Web App**:
   - Click on "Create a resource"
   - Search for "Web App" and select it
   - Click "Create"

3. **Configure the Web App**:
   - **Project Details**:
     - **Subscription**: Select your subscription
     - **Resource Group**: Use your existing resource group (`ClimateActionOrch-RG`) or create a new one
   
   - **Instance Details**:
     - **Name**: Enter a unique name (e.g., `climate-action-dashboard`)
     - **Publish**: Select "Code"
     - **Runtime stack**: Python 3.9
     - **Operating System**: Linux
     - **Region**: Select a region close to you (e.g., Central US)
   
   - **App Service Plan**:
     - Create a new plan or select your existing one
     - For testing, you can use the Basic (B1) tier

4. **Click "Review + create"** and then **"Create"** to provision the web app

## Step 4: Set Up Deployment from GitHub

1. **Go to your new Web App**:
   - Once deployment is complete, click "Go to resource"
   - Or find your web app in the resource list

2. **Set up Deployment Center**:
   - In the left menu, under "Deployment", click on "Deployment Center"
   - For Source, select "GitHub"

3. **Connect to GitHub**:
   - Click "Authorize" if needed to connect your GitHub account
   - Select your organization, repository, and branch (main)
   - For build provider, select "GitHub Actions"

4. **Configure GitHub Actions**:
   - Choose "Workflow Configuration"
   - Select "Add a workflow configuration"
   
5. **Review and Finish**:
   - Review the settings
   - Click "Save"

This will create a GitHub Actions workflow file in your repository and trigger an initial build and deployment.

## Step 5: Monitor the Deployment

1. **Check Deployment Status**:
   - In the Azure Portal, go to your web app's "Deployment Center"
   - You should see a deployment in progress
   - Click on it to see more details

2. **Check GitHub Actions**:
   - Go to your GitHub repository
   - Click on the "Actions" tab
   - You should see a workflow running

3. **Wait for Deployment to Complete**:
   - The initial deployment may take a few minutes
   - The workflow will clone your repository, build the application, and deploy it to Azure App Service

## Step 6: Verify Your Dashboard is Working

1. **Access Your Dashboard**:
   - Once deployment is complete, go to your web app URL
   - It will be something like `https://climate-action-dashboard.azurewebsites.net`
   - You should see your Climate Action Orchestrator dashboard

2. **Test Different Pages**:
   - Navigate through the different pages (Dashboard, AI Agents, Recommendations, etc.)
   - Ensure all pages and functionality work as expected

3. **Use This URL in Your Demo**:
   - Update your demo script to use this live URL instead of the local version
   - This will make your demo more professional and impressive

## Troubleshooting

If you encounter issues with your deployment:

1. **Check Logs**:
   - In Azure Portal, go to your web app
   - Under "Monitoring", click on "Log stream" to see real-time logs

2. **Check GitHub Actions Logs**:
   - On GitHub, go to the Actions tab
   - Click on the failed workflow run
   - Examine the logs for errors

3. **Common Issues**:
   - **Application Startup Errors**: Check that your application.py file is correctly configured
   - **Missing Dependencies**: Ensure all required packages are in requirements.txt
   - **File Permissions**: Ensure the startup.txt file has the correct permissions

## Making Updates

To update your dashboard after it's deployed:

1. Make changes to your code locally
2. Commit and push to GitHub
3. The GitHub Actions workflow will automatically deploy the changes to Azure

## Using in Your Demo

When demonstrating your Climate Action Orchestrator:

1. Show the Azure Portal with your deployed web app
2. Navigate to your live dashboard at the Azure URL
3. Explain that this is running in Azure, powered by Azure AI Agent Service
4. Highlight the multi-agent architecture and real-time collaboration

This approach showcases both your technical implementation and the user experience of your solution.
