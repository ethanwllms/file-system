import json
import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from main import parse_arguments


class TestArgumentParsing(unittest.TestCase):

    def test_default_values(self):
        test_args = ['list']
        with patch('sys.argv', ['program'] + test_args):
            args = parse_arguments(sys.argv[1:])
            self.assertEqual(args.host, 'localhost')
            self.assertEqual(args.port, 8765)
            self.assertEqual(args.command, 'list')

    def test_custom_host_and_port(self):
        test_args = ['--host', '0.0.0.0', '--port', '8000', 'list']
        with patch('sys.argv', ['program'] + test_args):
            args = parse_arguments(sys.argv[1:])
            self.assertEqual(args.host, '0.0.0.0')
            self.assertEqual(args.port, 8000)
            self.assertEqual(args.command, 'list')

    def test_path_argument(self):
        test_args = ['list', '--path', '/some/directory']
        with patch('sys.argv', ['program'] + test_args):
            args = parse_arguments(sys.argv[1:])
            self.assertEqual(args.command, 'list')
            self.assertEqual(args.path, '/some/directory')

    def test_missing_command(self):
        test_args = [] 
        with self.assertRaises(SystemExit):  
            with patch('sys.argv', ['program'] + test_args):
                parse_arguments(sys.argv[1:])
