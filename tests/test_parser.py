import unittest
from datetime import datetime
from unittest.mock import MagicMock
from dataclasses import dataclass
from src.core.Parser import NEM12DataParser

'''
    Unit tests for the NEM12 parser.
    Run: python3 -m unittest test_parser.py
'''

class TestNEM12DataParser(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock()
        self.parser = NEM12DataParser(config=self.mock_config)

    def test_parse_nmi_batch_success(self):
        """Test parsing a valid batch containing 200 and 300 records."""
        fake_batch = {
            "input": [[
                ['100', 'NEM12', '20230101'],
                ['200', 'NMI12345', 'E1', '1', 'E1', 'N1', '01009', 'kWh', '30', '20230101'],
                ['300', '20230101', '0.5', '1.2'],
                ['300', '20230102', '0.8', '2.2']
            ]]
        }

        records = self.parser.parse_nmi_batch(fake_batch)

        self.assertEqual(len(records), 4)
        
        # Check first record
        self.assertEqual(records[0].nmi, 'NMI12345')
        self.assertEqual(records[0].consumption, 0.5)
        self.assertEqual(records[0].timestamp, datetime(2023, 1, 1, 0, 0))

        # Check second record (should be 30 mins later)
        self.assertEqual(records[1].consumption, 1.2)
        self.assertEqual(records[1].timestamp, datetime(2023, 1, 1, 0, 30))

        # Check third record (should be on the next day)
        self.assertEqual(records[2].consumption, 0.8)
        self.assertEqual(records[2].timestamp, datetime(2023, 1, 2, 0, 0))

        # Check forth record (should be 30 mins later on the next day)
        self.assertEqual(records[3].consumption, 2.2)
        self.assertEqual(records[3].timestamp, datetime(2023, 1, 2, 0, 30))

    def test_invalid_date_format(self):
        """Test how the parser handles a malformed date string."""
        bad_batch = {
            "input": [[
                ['200', 'NMI123', 'E1', '1', 'E1', 'N1', '01', 'kWh', '30', '20230101'],
                ['300', 'NOT_A_DATE', '0.5']
            ]]
        }
        # TODO: Should handle exception gracefully, log error and skip bad records
        with self.assertRaises(ValueError):
            self.parser.parse_nmi_batch(bad_batch)

    def test_empty_input(self):
        """Ensure an empty input list returns an empty records list."""
        empty_batch = {"input": [[]]}
        records = self.parser.parse_nmi_batch(empty_batch)
        self.assertEqual(records, [])
