# Python WebSocket Client for File Operations

This Python client allows you to interact with a WebSocket server designed for file operations, including reading, writing, listing directories, searching for files, and creating directories.

## Features

- List available tools on the server
- Read the contents of a file
- Write content to a file
- List the contents of a directory
- Search for files by pattern
- Create new directories

## Requirements

- Python 3.x
- [websocket-client](https://pypi.org/project/websocket-client/)
- Node.js v22.x

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Change directory to fs-server:
   ```bash
   npm install
   npm start ../fs-test
   ```
3. Open new tab in terminal, change directory to fs-client:
   ```bash
   ./setup.sh
   ```

4. You are ready to use the client!

## Usage

Run the client from the command line with the following syntax:

```
python client.py [options] command [arguments]
```

### Commands
- list: List available tools or the contents of a directory

- read: Read a file

- write: Write content to a file

- search: Search for files matching a pattern

- create_dir: Create a new directory

### Options
--host: Specify the server hostname (default: localhost)

--port: Specify the server port (default: 8765)

--path: Specify the file or directory path

--pattern: Specify the pattern to search for files

--content: Specify the content to write to a file


## Examples

- List contents in allowed directory:
  ```
  python client.py --host localhost --port 8765 list --path /path/to/allowed/dirs/
  ```
- Read contents of a file within allowed directory:
  ```
  python client.py --host localhost --port 8765 read --path /path/to/allowed/dirs/file.txt
  ```
- Write contents to a file within allowed directory:
  ```
  python client.py --host localhost --port 8765 write --path /path/to/allowed/dirs/file.txt --content "Your text here"
  ```
- Search for file within allowed directory:
  ```
  python client.py --host localhost --port 8765 search --path /path/to/allowed/dirs/ --pattern "search_term"
  ```
- Create sub-directory within allowed directory:
  ```
  python client.py --host localhost --port 8765 create_dir --path /path/to/allowed/dirs/new_directory
  ```

## Troubleshooting
- Ensure the WebSocket server is running and accessible at the specified host and port.

- Check permissions on directories and files to ensure that your user has access.

- Verify that the required Python packages are installed correctly.

  - If you receive `Connection error: module 'websocket' has no attribute 'create_connection'` you may need to uninstall/re-install websocket-client via pip