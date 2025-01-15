import unittest, subprocess, time, os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import WebSocketClient

class TestWebSocketClientIntegrationErrors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        server_script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fs-server/index.js'))
        cls.server_process = subprocess.Popen(["node", server_script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        cls.server_process.wait()

    def test_invalid_directory_error(self):
        client = WebSocketClient('localhost', 8765)
        client.connect()
        try:
            invalid_path = "/invalid/directory/path"  
            response = client.call_tool("create_directory", {"name": "create_directory", "arguments": {"path": invalid_path}})
            self.assertIn("jsonrpc", response)
            self.assertIn("id", response)
            self.assertIn("error", response)
            self.assertIn("code", response["error"])
            self.assertEqual(response["error"]["code"], -32000)  
        finally:
            client.close()

    def test_server_error_response(self):
        client = WebSocketClient('localhost', 8765)
        client.connect()
        try:
            
            response = client.call_tool("non_existent_tool", {"name": "non_existent_tool", "arguments": {}})
            self.assertIn("error", response)
            self.assertEqual(response["error"]["code"], -32000)  
        finally:
            client.close()


if __name__ == '__main__':
    unittest.main()