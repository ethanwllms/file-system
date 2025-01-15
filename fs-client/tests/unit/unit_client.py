import pytest, sys, os, json
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import WebSocketClient

class TestWebSocketClient:

    @patch('websocket.create_connection')
    def test_connect_successful(self, mock_create_connection):
        
        mock_ws = MagicMock()
        mock_create_connection.return_value = mock_ws

        client = WebSocketClient()
        client.connect()
        
        mock_create_connection.assert_called_once_with('ws://localhost:8765')
        assert client.ws == mock_ws

    @patch('websocket.create_connection', side_effect=Exception("Connection error"))
    def test_connect_failure(self, mock_create_connection):
        
        client = WebSocketClient()
        
        with pytest.raises(SystemExit):  
            client.connect()

    @patch('websocket.create_connection')
    def test_send_message(self, mock_create_connection):
        
        mock_ws = MagicMock()
        mock_ws.recv.return_value = json.dumps({"jsonrpc": "2.0", "id": 1, "result": "test response"})
        mock_create_connection.return_value = mock_ws
        client = WebSocketClient()
        client.connect()

        response = client.send({"jsonrpc": "2.0", "method": "test_method", "id": 1})
        
        mock_ws.send.assert_called_once_with(json.dumps({"jsonrpc": "2.0", "method": "test_method", "id": 1}))
        assert response == {"jsonrpc": "2.0", "id": 1, "result": "test response"}

    @patch('websocket.create_connection')
    def test_list_tools(self, mock_create_connection):
        
        mock_ws = MagicMock()
        mock_ws.recv.return_value = json.dumps({"jsonrpc": "2.0", "id": 1, "result": {"tools": []}})
        mock_create_connection.return_value = mock_ws
        client = WebSocketClient()
        client.connect()

        response = client.list_tools()
        
        expected_message = {
            "jsonrpc": "2.0",
            "method": "list_tools",
            "id": 1
        }
        mock_ws.send.assert_called_once_with(json.dumps(expected_message))
        assert response == {"jsonrpc": "2.0", "id": 1, "result": {"tools": []}}

    @patch('websocket.create_connection')
    def test_call_tool(self, mock_create_connection):
        
        mock_ws = MagicMock()
        mock_ws.recv.return_value = json.dumps({"jsonrpc": "2.0", "id": 1, "result": "tool response"})
        mock_create_connection.return_value = mock_ws
        client = WebSocketClient()
        client.connect()

        response = client.call_tool("some_tool", {"name": "some_tool", "arguments": {}})

        expected_message = {
            "jsonrpc": "2.0",
            "method": "call_tool",
            "params": {"name": "some_tool", "arguments": {}},
            "id": 1
        }
        mock_ws.send.assert_called_once_with(json.dumps(expected_message))
        assert response == {"jsonrpc": "2.0", "id": 1, "result": "tool response"}
