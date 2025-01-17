import json
import sys
import argparse
import websocket

class WebSocketClient:
    def __init__(self, host='localhost', port=8765):
        self.url = f"ws://{host}:{port}"
        self.ws = None

    def connect(self):
        try:
            self.ws = websocket.create_connection(self.url)
            print(f"Connected to {self.url}")
        except Exception as e:
            print(f"Connection error: {e}")
            sys.exit(1)

    def send(self, message):
        try:
            # print("Sending message:", json.dumps(message, indent=2))
            self.ws.send(json.dumps(message))
            response = self.ws.recv()
            return json.loads(response)
        except Exception as e:
            print(f"Error sending message: {e}")
            return None

    def close(self):
        if self.ws:
            self.ws.close()

    def list_tools(self):
        message = {
            "jsonrpc": "2.0",
            "method": "list_tools",
            "id": 1
        }
        response = self.send(message)
        return response

    def call_tool(self, method, params):
        message = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": params,
            "id": 1
        }
        response = self.send(message)
        return response
    
def parse_arguments(args):
    parser = argparse.ArgumentParser(description="WebSocket client for file operations")
    
    parser.add_argument('--host', type=str, default='localhost', help='Server hostname')
    parser.add_argument('--port', type=int, default=8765, help='Server port')
    parser.add_argument('command', type=str, help='Command to execute (list, read, write, search, create_dir)')
    
    # Optional arguments for the commands
    parser.add_argument('--path', type=str, help='File or directory path')
    parser.add_argument('--pattern', type=str, help='Search pattern')
    parser.add_argument('--content', type=str, help='Content to write')

    return parser.parse_args(args)

def main():
    args = parse_arguments(sys.argv[1:])

    client = WebSocketClient(host=args.host, port=args.port)
    client.connect()

    try:
        if args.command == 'list':
            if args.path is None:
                result = client.list_tools()
                print("Available tools:", result)
            else:
                # print(type({args.path}))
                result = client.call_tool("list_directory", {"name": "list_directory", "arguments": {"path": args.path}})
                # print(type(result))
                contents = result['result']['content'][0]['text']
                # print(type(contents))
                print("Directory contents:\n", contents)

        elif args.command == 'read':
            if args.path is None:
                print("Error: --path is required for read command.")
            else:
                result = client.call_tool("read_file", {"name": "read_file", "arguments": {"path": args.path}})
                contents = result['result']['content'][0]['text']
                print("File contents:\n", contents)

        elif args.command == 'write':
            if args.path is None or args.content is None:
                print("Error: --path and --content are required for write command.")
            else:
                result = client.call_tool("write_file", {"name": "write_file", "arguments": {"path": args.path, "content": args.content}})
                contents = result['result']['content'][0]['text']
                print(contents)

        elif args.command == 'search':
            if args.path is None or args.pattern is None:
                print("Error: --path and --pattern are required for search command.")
            else:
                result = client.call_tool("search_files", {"name": "search_files", "arguments": {"path": args.path, "pattern": str(args.pattern)}})
                contents = result['result']['content'][0]['text']

                print("Search results:\n", contents)

        elif args.command == 'create_dir':
            if args.path is None:
                print("Error: --path is required for create_dir command.")
            else:
                result = client.call_tool("create_directory", {"name": "create_directory", "arguments": {"path": args.path}})  # Assuming this method is implemented
                contents = result['result']['content'][0]['text']
                print(contents)

        else:
            print("Error: Invalid command.")
    finally:
        client.close()

if __name__ == "__main__":
    main()
