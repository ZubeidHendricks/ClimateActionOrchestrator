"""
Azure Client Utility for Climate Action Orchestrator

This module provides helper functions to interact with Azure services
including Azure AI, Azure Storage, Azure Cosmos DB, etc.
"""

import logging
import os
from typing import Dict, Any, Optional
import json
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from azure.ai.ml import MLClient

logger = logging.getLogger(__name__)

def get_azure_client(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get Azure clients based on configuration.
    
    Args:
        config: Azure configuration including connection strings, 
               endpoints, and other settings
    
    Returns:
        Dictionary of initialized Azure clients
    """
    # If no config provided, try to use environment variables
    if not config:
        config = {
            "use_credential": os.environ.get("AZURE_USE_CREDENTIAL", "false").lower() == "true",
            "storage_connection_string": os.environ.get("AZURE_STORAGE_CONNECTION_STRING", ""),
            "cosmos_endpoint": os.environ.get("AZURE_COSMOS_ENDPOINT", ""),
            "cosmos_key": os.environ.get("AZURE_COSMOS_KEY", ""),
            "cosmos_database": os.environ.get("AZURE_COSMOS_DATABASE", "climate_action"),
            "ai_endpoint": os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
            "ai_key": os.environ.get("AZURE_OPENAI_KEY", ""),
            "ml_workspace": os.environ.get("AZURE_ML_WORKSPACE", ""),
            "ml_resource_group": os.environ.get("AZURE_ML_RESOURCE_GROUP", ""),
            "ml_subscription_id": os.environ.get("AZURE_ML_SUBSCRIPTION_ID", "")
        }
    
    clients = {}
    
    # Get credential if needed
    credential = None
    if config.get("use_credential", False):
        try:
            credential = DefaultAzureCredential()
            logger.info("Successfully created DefaultAzureCredential")
        except Exception as e:
            logger.error(f"Error creating DefaultAzureCredential: {e}")
    
    # Initialize Blob Storage client
    try:
        connection_string = config.get("storage_connection_string", "")
        if connection_string:
            blob_client = BlobServiceClient.from_connection_string(connection_string)
            clients["blob"] = blob_client
            logger.info("Successfully initialized Blob Storage client")
        elif credential:
            account_name = config.get("storage_account_name", "")
            if account_name:
                blob_url = f"https://{account_name}.blob.core.windows.net"
                blob_client = BlobServiceClient(blob_url, credential=credential)
                clients["blob"] = blob_client
                logger.info("Successfully initialized Blob Storage client with credential")
    except Exception as e:
        logger.error(f"Error initializing Blob Storage client: {e}")
    
    # Initialize Cosmos DB client
    try:
        cosmos_endpoint = config.get("cosmos_endpoint", "")
        cosmos_key = config.get("cosmos_key", "")
        
        if cosmos_endpoint and cosmos_key:
            cosmos_client = CosmosClient(cosmos_endpoint, credential=cosmos_key)
            database_name = config.get("cosmos_database", "climate_action")
            database = cosmos_client.get_database_client(database_name)
            clients["cosmos"] = database
            logger.info("Successfully initialized Cosmos DB client")
        elif cosmos_endpoint and credential:
            cosmos_client = CosmosClient(cosmos_endpoint, credential=credential)
            database_name = config.get("cosmos_database", "climate_action")
            database = cosmos_client.get_database_client(database_name)
            clients["cosmos"] = database
            logger.info("Successfully initialized Cosmos DB client with credential")
    except Exception as e:
        logger.error(f"Error initializing Cosmos DB client: {e}")
    
    # Initialize Azure AI client
    try:
        ai_endpoint = config.get("ai_endpoint", "")
        ai_key = config.get("ai_key", "")
        
        if ai_endpoint and ai_key:
            clients["ai"] = {
                "endpoint": ai_endpoint,
                "key": ai_key
            }
            logger.info("Successfully initialized Azure AI client")
    except Exception as e:
        logger.error(f"Error initializing Azure AI client: {e}")
    
    # Initialize Azure ML client
    try:
        workspace_name = config.get("ml_workspace", "")
        resource_group = config.get("ml_resource_group", "")
        subscription_id = config.get("ml_subscription_id", "")
        
        if workspace_name and resource_group and subscription_id and credential:
            ml_client = MLClient(
                credential=credential,
                subscription_id=subscription_id,
                resource_group_name=resource_group,
                workspace_name=workspace_name
            )
            clients["ml"] = ml_client
            logger.info("Successfully initialized Azure ML client")
    except Exception as e:
        logger.error(f"Error initializing Azure ML client: {e}")
    
    return clients

def upload_blob(client: BlobServiceClient, container_name: str, blob_name: str, 
              data: Any, content_type: str = "application/json") -> str:
    """
    Upload data to Azure Blob Storage.
    
    Args:
        client: BlobServiceClient
        container_name: Name of the container
        blob_name: Name of the blob
        data: Data to upload (string, dict, or bytes)
        content_type: Content type of the data
    
    Returns:
        URL of the uploaded blob
    """
    try:
        # Get or create container
        try:
            container_client = client.get_container_client(container_name)
            container_client.get_container_properties()  # Check if exists
        except Exception:
            container_client = client.create_container(container_name)
        
        # Convert data to appropriate format
        if isinstance(data, dict):
            upload_data = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            upload_data = data.encode('utf-8')
        else:
            upload_data = data  # Assume bytes
        
        # Upload data
        blob_client = container_client.upload_blob(
            name=blob_name,
            data=upload_data,
            overwrite=True,
            content_settings={"content_type": content_type}
        )
        
        # Get URL
        account_name = client.account_name
        url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        
        logger.info(f"Successfully uploaded blob: {url}")
        return url
    
    except Exception as e:
        logger.error(f"Error uploading blob: {e}")
        raise
    
def download_blob(client: BlobServiceClient, container_name: str, blob_name: str, 
                as_text: bool = True) -> Any:
    """
    Download data from Azure Blob Storage.
    
    Args:
        client: BlobServiceClient
        container_name: Name of the container
        blob_name: Name of the blob
        as_text: Whether to return the data as text
    
    Returns:
        Downloaded data as text or bytes
    """
    try:
        # Get container client
        container_client = client.get_container_client(container_name)
        
        # Download blob
        blob_client = container_client.get_blob_client(blob_name)
        download_stream = blob_client.download_blob()
        
        if as_text:
            data = download_stream.readall().decode('utf-8')
        else:
            data = download_stream.readall()
        
        logger.info(f"Successfully downloaded blob: {container_name}/{blob_name}")
        return data
    
    except Exception as e:
        logger.error(f"Error downloading blob: {e}")
        raise
    
def save_to_cosmos(client: Any, container_name: str, item: Dict[str, Any], 
                 partition_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Save an item to Cosmos DB.
    
    Args:
        client: Cosmos DB database client
        container_name: Name of the container
        item: Item to save
        partition_key: Partition key value (if None, will use item['id'])
    
    Returns:
        The saved item as returned by Cosmos DB
    """
    try:
        # Get or create container
        try:
            container = client.get_container_client(container_name)
            container.read()  # Check if exists
        except Exception:
            # Create with default partition key
            partition_key_path = "/id" if not partition_key else f"/{partition_key}"
            container = client.create_container(
                id=container_name,
                partition_key=partition_key_path
            )
        
        # Ensure item has an id
        if 'id' not in item:
            import uuid
            item['id'] = str(uuid.uuid4())
        
        # Save item
        if not partition_key:
            pk_value = item['id']
        else:
            pk_value = item.get(partition_key, item['id'])
        
        result = container.upsert_item(body=item, partition_key=pk_value)
        
        logger.info(f"Successfully saved item to Cosmos DB: {container_name}/{item['id']}")
        return result
    
    except Exception as e:
        logger.error(f"Error saving to Cosmos DB: {e}")
        raise

def query_cosmos(client: Any, container_name: str, query: str, 
               params: Optional[Dict[str, Any]] = None) -> list:
    """
    Query items from Cosmos DB.
    
    Args:
        client: Cosmos DB database client
        container_name: Name of the container
        query: SQL query string
        params: Query parameters
    
    Returns:
        List of queried items
    """
    try:
        # Get container
        container = client.get_container_client(container_name)
        
        # Execute query
        if params:
            items = list(container.query_items(
                query=query,
                parameters=params,
                enable_cross_partition_query=True
            ))
        else:
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
        
        logger.info(f"Successfully queried items from Cosmos DB: {container_name}")
        return items
    
    except Exception as e:
        logger.error(f"Error querying Cosmos DB: {e}")
        raise
