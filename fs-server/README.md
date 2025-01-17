# WebSocket File Operations API Documentation

## Overview

The WebSocket File Operations API allows clients to interact with a server for various file management operations. It supports reading, writing, listing directories, searching for files, and creating new directories.

## Authentication

This API does not require authentication. Access is controlled through allowed directories configured on the server.

## Endpoints

### 1. List Tools

#### Request Example
{
  "jsonrpc": "2.0",
  "method": "list_tools",
  "id": 1
}

#### Reponse Example
{
  "jsonrpc": "2.0",
  "result": {
    "tools": [
      {"name": "read_file", "description": "Read file contents"},
      {"name": "write_file", "description": "Write to file"},
      {"name": "list_directory", "description": "List directory contents"},
      {"name": "search_files", "description": "Search for files"},
      {"name": "create_directory", "description": "Create new directory"}
    ]
  },
  "id": 1
}


### 2. Call Tools

#### read_file example
{
  "jsonrpc": "2.0",
  "method": "call_tool",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/path/to/your/file.txt"
    }
  },
  "id": 2
}

#### Response Example
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "File content goes here"}]
  },
  "id": 2
}

#### write_file example
{
  "jsonrpc": "2.0",
  "method": "call_tool",
  "params": {
    "name": "write_file",
    "arguments": {
      "path": "/path/to/your/file.txt",
      "content": "This is the new file content."
    }
  },
  "id": 3
}

#### Response Example
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "Successfully wrote to /path/to/your/file.txt"}]
  },
  "id": 3
}

#### list_directory example
{
  jsonrpc: '2.0',
  method: 'call_tool',
  params: {
    name: 'list_directory',
    arguments: { path: '/path/to/files/within/allowed/dirs/fs-test' }
  },
  id: 1
}

#### Response Example
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "Dir contents go here."}]
  },
  "id": 2
}

#### search_files example
{
  "jsonrpc": "2.0",
  "method": "call_tool",
  "params": {
    "name": "search_file",
    "arguments": {
      "path": "/path/to/your/dir",
      "pattern": ".txt"
    }
  },
  "id": 3
}

#### Response Example
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "[FILE] file.txt ..."}]
  },
  "id": 3
}

#### create_directory example
{
  "jsonrpc": "2.0",
  "method": "call_tool",
  "params": {
    "name": "create_directory",
    "arguments": {
      "path": "/path/to/your/dir"
    }
  },
  "id": 3
}

#### Response Example
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "Successfully created directory at: /path/to/your/dir"}]
  },
  "id": 3
}

## Error Handling

When an error occurs, the response will include an error object.
Common error codes include:

-32000: Invalid parameters or request format.

-32601: Method not found.


## Rate Limits

Currently, there are no rate limits imposed on the API. However, abuse of the service may result in throttling.