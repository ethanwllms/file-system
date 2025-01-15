import unittest, subprocess, time, sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import WebSocketClient  

class TestWebSocketClientIntegration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        server_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fs-server/index.js'))
        
        cls.server_process = subprocess.Popen(["node", server_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
    
        cls.server_process.terminate()
        cls.server_process.wait()

    def test_list_tools(self):
    
        client = WebSocketClient('localhost', 8765)
        client.connect()
        try:
            response = client.list_tools()
            expected_keys = ["jsonrpc", "id", "result"]
            for key in expected_keys:
                self.assertIn(key, response)
            self.assertIn("tools", response["result"])
        finally:
            client.close()

    def test_create_directory(self):
    
        client = WebSocketClient('localhost', 8765)
        client.connect()
        try:
            response = client.call_tool("create_directory", {"name": "create_directory", "arguments": {"path": "/users/ethanwilliams/documents/code/serverfarm/file-system-ws/fs-test/"}})
            expected_keys = ["jsonrpc", "id", "result"]
            for key in expected_keys:
                self.assertIn(key, response)
            self.assertIn("content", response["result"])
            print(response)
        finally:
            client.close()

if __name__ == '__main__':
    unittest.main()
