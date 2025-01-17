import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import WebSocketClient, parse_arguments  # Import your refactored functions


class TestMainErrorHandling(unittest.TestCase):

    @patch('main.WebSocketClient.connect')
    def test_websocket_connection_failure(self, mock_connect):
        
        mock_connect.side_effect = Exception("Connection failed")
        
        test_args = ['program', '--host', 'localhost', '--port', '8765', 'list']
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit):  
                args = parse_arguments(sys.argv[1:])
                client = WebSocketClient(args.host, args.port)
                try:
                    client.connect()
                except Exception as e:
                    print(f"Handled exception: {e}")
                    sys.exit(1)

    @patch('main.WebSocketClient.send')
    def test_send_failure(self, mock_send):
        
        mock_send.side_effect = Exception("Send failed")
        
        client = WebSocketClient('localhost', 8765)
        client.ws = MagicMock()  

        response = None
        
        try:
            client.connect()
            test_message = {"jsonrpc": "2.0", "method": "list_tools", "id": 1}
            response = client.send(test_message)
        except Exception as e:
            print(f"Handled exception: {e}")
            self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()