"""
Data Connectors Utility for Climate Action Orchestrator

This module provides functions to connect to various data sources
for gathering operational data used in emissions calculations.
"""

import logging
import os
from typing import Dict, Any, List, Optional
import pandas as pd
import json
import csv
import requests
from datetime import datetime

# Import Azure-specific utilities
from utils.azure_client import get_azure_client

logger = logging.getLogger(__name__)

def connect_to_data_source(source_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Connect to a specific data source and retrieve client/connection.
    
    Args:
        source_type: Type of data source (azure_blob, csv, api, etc.)
        config: Connection configuration
    
    Returns:
        Dictionary with connection details
    """
    try:
        if source_type == 'azure_blob':
            return connect_to_azure_blob(config)
        elif source_type == 'csv':
            return connect_to_csv_files(config)
        elif source_type == 'api':
            return connect_to_api(config)
        elif source_type == 'database':
            return connect_to_database(config)
        else:
            logger.warning(f"Unsupported data source type: {source_type}")
            return {"error": f"Unsupported data source type: {source_type}"}
    except Exception as e:
        logger.error(f"Error connecting to {source_type} data source: {e}")
        return {"error": str(e)}

def connect_to_azure_blob(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Connect to Azure Blob Storage.
    
    Args:
        config: Azure connection configuration
    
    Returns:
        Dictionary with Azure Blob client and connection details
    """
    try:
        # Get Azure client
        azure_client = get_azure_client(config)
        
        # Check if blob client was created
        if 'blob' not in azure_client:
            raise Exception("Failed to create Azure Blob client")
        
        # Return client and account info
        blob_client = azure_client['blob']
        return {
            "client": blob_client,
            "account_name": blob_client.account_name,
            "status": "connected"
        }
    except Exception as e:
        logger.error(f"Error connecting to Azure Blob Storage: {e}")
        raise

def connect_to_csv_files(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set up connection to CSV files.
    
    Args:
        config: Configuration including directory or file paths
    
    Returns:
        Dictionary with file paths and connection details
    """
    try:
        # Get directory or file paths
        directory = config.get("directory")
        files = config.get("files", [])
        
        # If directory is provided, scan for CSV files
        if directory and os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.lower().endswith('.csv'):
                    file_path = os.path.join(directory, filename)
                    files.append(file_path)
        
        # Validate files exist
        valid_files = []
        for file_path in files:
            if os.path.isfile(file_path):
                valid_files.append(file_path)
            else:
                logger.warning(f"CSV file not found: {file_path}")
        
        if not valid_files:
            raise Exception("No valid CSV files found")
        
        return {
            "files": valid_files,
            "count": len(valid_files),
            "status": "connected"
        }
    except Exception as e:
        logger.error(f"Error setting up CSV files connection: {e}")
        raise

def connect_to_api(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Connect to a REST API data source.
    
    Args:
        config: API connection configuration
    
    Returns:
        Dictionary with API connection details
    """
    try:
        # Get API configuration
        base_url = config.get("base_url")
        headers = config.get("headers", {})
        auth_type = config.get("auth_type")
        
        if not base_url:
            raise Exception("API base URL not provided")
        
        # Set up authentication
        auth = None
        if auth_type == "basic":
            username = config.get("username")
            password = config.get("password")
            if username and password:
                auth = (username, password)
            else:
                raise Exception("Username and password required for basic authentication")
        elif auth_type == "token":
            token = config.get("token")
            if token:
                headers["Authorization"] = f"Bearer {token}"
            else:
                raise Exception("Token required for token authentication")
        
        # Test connection with a simple request
        try:
            test_endpoint = config.get("test_endpoint", "")
            url = f"{base_url.rstrip('/')}/{test_endpoint.lstrip('/')}" if test_endpoint else base_url
            response = requests.get(url, headers=headers, auth=auth, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.warning(f"API connection test failed: {e}")
        
        return {
            "base_url": base_url,
            "headers": headers,
            "auth": auth is not None,
            "auth_type": auth_type,
            "status": "connected"
        }
    except Exception as e:
        logger.error(f"Error connecting to API: {e}")
        raise

def connect_to_database(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Connect to a database.
    
    Args:
        config: Database connection configuration
    
    Returns:
        Dictionary with database connection details
    """
    try:
        # Get database configuration
        db_type = config.get("type", "").lower()
        connection_string = config.get("connection_string")
        
        if not db_type:
            raise Exception("Database type not provided")
        
        # Connect based on database type
        if db_type == "cosmos":
            # Use the Azure client utility to connect to Cosmos DB
            azure_config = {
                "cosmos_endpoint": config.get("endpoint"),
                "cosmos_key": config.get("key"),
                "cosmos_database": config.get("database")
            }
            azure_client = get_azure_client(azure_config)
            
            if 'cosmos' not in azure_client:
                raise Exception("Failed to create Cosmos DB client")
            
            return {
                "client": azure_client['cosmos'],
                "database": config.get("database"),
                "type": "cosmos",
                "status": "connected"
            }
        
        elif db_type in ["sql", "postgresql", "mysql", "oracle"]:
            # For SQL databases, just validate configuration
            # In a real implementation, this would create and return a connection
            if not connection_string:
                raise Exception(f"Connection string required for {db_type} database")
            
            return {
                "type": db_type,
                "has_connection_string": True,
                "status": "configured"
            }
        
        else:
            raise Exception(f"Unsupported database type: {db_type}")
    
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def read_data_from_source(connection: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read data from a connected data source.
    
    Args:
        connection: Connection details from connect_to_data_source
        query: Query/request parameters
    
    Returns:
        Dictionary with retrieved data
    """
    try:
        # Determine source type
        if "client" in connection and "account_name" in connection:
            # Azure Blob
            return read_from_azure_blob(connection, query)
        elif "files" in connection:
            # CSV files
            return read_from_csv_files(connection, query)
        elif "base_url" in connection:
            # API
            return read_from_api(connection, query)
        elif "type" in connection and connection["type"] in ["cosmos", "sql", "postgresql", "mysql", "oracle"]:
            # Database
            return read_from_database(connection, query)
        else:
            raise Exception("Unknown data source type in connection")
    
    except Exception as e:
        logger.error(f"Error reading data from source: {e}")
        return {"error": str(e)}

def read_from_azure_blob(connection: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read data from Azure Blob Storage.
    
    Args:
        connection: Azure Blob connection details
        query: Query parameters including container and blob names
    
    Returns:
        Dictionary with retrieved data
    """
    try:
        client = connection["client"]
        container_name = query.get("container")
        blob_name = query.get("blob")
        format_type = query.get("format", "").lower()
        
        if not container_name or not blob_name:
            raise Exception("Container name and blob name required")
        
        # Download blob content
        container_client = client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        
        # Download as text
        download_stream = blob_client.download_blob()
        content = download_stream.readall().decode('utf-8')
        
        # Parse based on format
        data = None
        if format_type == "csv":
            # Parse CSV
            lines = content.strip().split('\n')
            reader = csv.reader(lines)
            headers = next(reader)
            rows = list(reader)
            
            # Convert to list of dicts
            data = []
            for row in rows:
                data.append(dict(zip(headers, row)))
        
        elif format_type == "json":
            # Parse JSON
            data = json.loads(content)
        
        else:
            # Return raw content
            data = content
        
        return {
            "data": data,
            "source": f"azure_blob:{container_name}/{blob_name}",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error reading from Azure Blob: {e}")
        raise

def read_from_csv_files(connection: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read data from CSV files.
    
    Args:
        connection: CSV connection details
        query: Query parameters including file selection and filters
    
    Returns:
        Dictionary with retrieved data
    """
    try:
        files = connection["files"]
        file_pattern = query.get("file_pattern", "")
        columns = query.get("columns")
        filters = query.get("filters", {})
        
        # Select files based on pattern
        selected_files = []
        if file_pattern:
            for file_path in files:
                if file_pattern in os.path.basename(file_path):
                    selected_files.append(file_path)
        else:
            selected_files = files
        
        if not selected_files:
            raise Exception("No matching CSV files found")
        
        # Read and process each file
        all_data = []
        for file_path in selected_files:
            # Read CSV into DataFrame
            df = pd.read_csv(file_path)
            
            # Filter columns if specified
            if columns:
                df = df[columns]
            
            # Apply filters if specified
            for column, value in filters.items():
                if column in df.columns:
                    df = df[df[column] == value]
            
            # Convert DataFrame to list of dictionaries
            file_data = df.to_dict('records')
            all_data.extend(file_data)
        
        return {
            "data": all_data,
            "count": len(all_data),
            "files": selected_files,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error reading from CSV files: {e}")
        raise

def read_from_api(connection: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read data from an API.
    
    Args:
        connection: API connection details
        query: Query parameters including endpoint and parameters
    
    Returns:
        Dictionary with retrieved data
    """
    try:
        base_url = connection["base_url"]
        headers = connection.get("headers", {})
        auth = connection.get("auth")
        
        endpoint = query.get("endpoint", "")
        params = query.get("params", {})
        method = query.get("method", "GET").upper()
        body = query.get("body")
        
        # Construct URL
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}" if endpoint else base_url
        
        # Make request based on method
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, auth=auth, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, params=params, json=body, auth=auth, timeout=30)
        else:
            raise Exception(f"Unsupported HTTP method: {method}")
        
        # Check for errors
        response.raise_for_status()
        
        # Parse response
        try:
            data = response.json()
        except ValueError:
            data = response.text
        
        return {
            "data": data,
            "status_code": response.status_code,
            "url": url,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error reading from API: {e}")
        raise

def read_from_database(connection: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read data from a database.
    
    Args:
        connection: Database connection details
        query: Query parameters
    
    Returns:
        Dictionary with retrieved data
    """
    try:
        db_type = connection.get("type")
        
        if db_type == "cosmos":
            return read_from_cosmos_db(connection, query)
        else:
            # For other database types
            # In a real implementation, this would execute the query
            # and return results
            return {
                "message": f"Reading from {db_type} database not implemented",
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Error reading from database: {e}")
        raise

def read_from_cosmos_db(connection: Dict[str, Any], query: Dict[str, Any]) -> Dict[str, Any]:
    """
    Read data from Azure Cosmos DB.
    
    Args:
        connection: Cosmos DB connection details
        query: Query parameters including container and query string
    
    Returns:
        Dictionary with retrieved data
    """
    try:
        client = connection["client"]
        container_name = query.get("container")
        query_str = query.get("query", "SELECT * FROM c")
        params = query.get("params", [])
        
        if not container_name:
            raise Exception("Container name required for Cosmos DB query")
        
        # Get container client
        container = client.get_container_client(container_name)
        
        # Execute query
        items = list(container.query_items(
            query=query_str,
            parameters=params,
            enable_cross_partition_query=True
        ))
        
        return {
            "data": items,
            "count": len(items),
            "container": container_name,
            "query": query_str,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error reading from Cosmos DB: {e}")
        raise

def write_data_to_source(connection: Dict[str, Any], data: Any, 
                        destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write data to a connected data source.
    
    Args:
        connection: Connection details from connect_to_data_source
        data: Data to write
        destination: Destination parameters
    
    Returns:
        Dictionary with write operation result
    """
    try:
        # Determine source type
        if "client" in connection and "account_name" in connection:
            # Azure Blob
            return write_to_azure_blob(connection, data, destination)
        elif "files" in connection:
            # CSV files
            return write_to_csv_file(data, destination)
        elif "type" in connection and connection["type"] == "cosmos":
            # Cosmos DB
            return write_to_cosmos_db(connection, data, destination)
        else:
            raise Exception("Writing to this source type not supported")
    
    except Exception as e:
        logger.error(f"Error writing data to source: {e}")
        return {"error": str(e)}

def write_to_azure_blob(connection: Dict[str, Any], data: Any, 
                       destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write data to Azure Blob Storage.
    
    Args:
        connection: Azure Blob connection details
        data: Data to write
        destination: Destination parameters including container and blob names
    
    Returns:
        Dictionary with write operation result
    """
    try:
        client = connection["client"]
        container_name = destination.get("container")
        blob_name = destination.get("blob")
        content_type = destination.get("content_type", "application/json")
        
        if not container_name or not blob_name:
            raise Exception("Container name and blob name required")
        
        # Ensure container exists
        container_client = client.get_container_client(container_name)
        try:
            container_client.get_container_properties()
        except Exception:
            container_client = client.create_container(container_name)
        
        # Format data based on content type
        if content_type == "application/json" and isinstance(data, (dict, list)):
            blob_data = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            blob_data = data.encode('utf-8')
        else:
            # Assume bytes or serializable
            blob_data = data
        
        # Upload blob
        blob_client = container_client.upload_blob(
            name=blob_name,
            data=blob_data,
            overwrite=True,
            content_settings={"content_type": content_type}
        )
        
        # Get URL
        account_name = client.account_name
        url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
        
        return {
            "status": "success",
            "url": url,
            "container": container_name,
            "blob": blob_name,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error writing to Azure Blob: {e}")
        raise

def write_to_csv_file(data: Any, destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write data to a CSV file.
    
    Args:
        data: Data to write (list of dictionaries or pandas DataFrame)
        destination: Destination parameters including file path
    
    Returns:
        Dictionary with write operation result
    """
    try:
        file_path = destination.get("file_path")
        mode = destination.get("mode", "w")  # 'w' for overwrite, 'a' for append
        index = destination.get("index", False)
        
        if not file_path:
            raise Exception("File path required")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Convert data to DataFrame if needed
        if isinstance(data, pd.DataFrame):
            df = data
        else:
            df = pd.DataFrame(data)
        
        # Write to CSV
        if mode == "a" and os.path.exists(file_path):
            # Append without headers if file exists
            df.to_csv(file_path, mode='a', header=False, index=index)
        else:
            # Create new file with headers
            df.to_csv(file_path, index=index)
        
        return {
            "status": "success",
            "file_path": file_path,
            "rows": len(df),
            "columns": len(df.columns),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error writing to CSV file: {e}")
        raise

def write_to_cosmos_db(connection: Dict[str, Any], data: Any, 
                     destination: Dict[str, Any]) -> Dict[str, Any]:
    """
    Write data to Azure Cosmos DB.
    
    Args:
        connection: Cosmos DB connection details
        data: Data to write (document or list of documents)
        destination: Destination parameters including container
    
    Returns:
        Dictionary with write operation result
    """
    try:
        client = connection["client"]
        container_name = destination.get("container")
        partition_key = destination.get("partition_key")
        
        if not container_name:
            raise Exception("Container name required")
        
        # Get container client
        container = client.get_container_client(container_name)
        
        # Determine if single document or batch
        if isinstance(data, dict):
            # Single document
            # Ensure it has an id
            if 'id' not in data:
                from uuid import uuid4
                data['id'] = str(uuid4())
            
            # Insert document
            if not partition_key:
                pk_value = data['id']
            else:
                pk_value = data.get(partition_key, data['id'])
            
            result = container.upsert_item(body=data, partition_key=pk_value)
            
            return {
                "status": "success",
                "operation": "upsert",
                "document_id": result['id'],
                "count": 1,
                "timestamp": datetime.now().isoformat()
            }
        
        elif isinstance(data, list):
            # Batch of documents
            results = []
            count = 0
            
            for item in data:
                # Ensure each item has an id
                if 'id' not in item:
                    from uuid import uuid4
                    item['id'] = str(uuid4())
                
                # Get partition key value
                if not partition_key:
                    pk_value = item['id']
                else:
                    pk_value = item.get(partition_key, item['id'])
                
                # Insert document
                result = container.upsert_item(body=item, partition_key=pk_value)
                results.append(result['id'])
                count += 1
            
            return {
                "status": "success",
                "operation": "batch_upsert",
                "document_ids": results,
                "count": count,
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            raise Exception(f"Unsupported data type for Cosmos DB: {type(data)}")
    
    except Exception as e:
        logger.error(f"Error writing to Cosmos DB: {e}")
        raise
