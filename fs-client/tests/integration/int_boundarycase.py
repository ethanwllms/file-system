import os
import subprocess
import sys
import time
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import WebSocketClient


class TestWebSocketClientBoundaryCases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        server_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fs-server/index.js'))
        
        cls.server_process = subprocess.Popen(["node", server_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        
        cls.server_process.terminate()
        cls.server_process.wait()

    def test_maximum_path_length(self):
        client = WebSocketClient('localhost', 8765)
        client.connect()

        try:
            max_path = "/a" * 255  # Example of large path length, adjust as needed for your operating system limits
            response = client.call_tool("create_directory", {"name": "create_directory", "arguments": {"path": max_path}})
            self.assertIn("jsonrpc", response)
            if "error" in response:
                print("Error:", response["error"]["message"])
            else:
                self.assertIn("result", response)
                print("Result:", response["result"]["content"])
        finally:
            client.close()

    def test_large_content_size(self):
        client = WebSocketClient('localhost', 8765)
        client.connect()

        try:
            large_content = "x" * (10**6)  # 1 MB of data, BIG DATA
            path = "/tmp/large_test_file.txt"
            response = client.call_tool("write_file", {"name": "write_file", "arguments": {"path": path, "content": large_content}})
            self.assertIn("jsonrpc", response)
            if "error" in response:
                print("Error:", response["error"]["message"])
            else:
                self.assertIn("result", response)
                print("Result:", response["result"]["content"])
        finally:
            client.close()

if __name__ == '__main__':
    unittest.main()