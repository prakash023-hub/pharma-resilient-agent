"""Offline tests — no TrueFoundry API key required."""

from __future__ import annotations

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.guardrails import local_pii_check
from src.mcp_tools import extract_drug_name


class OfflineTests(unittest.TestCase):
    def test_extract_drug_name(self):
        query = "Amoxicillin for UTI in 65yo patient with CrCl 45"
        self.assertEqual(extract_drug_name(query), "Amoxicillin")

    def test_local_pii_blocks_ssn(self):
        self.assertIsNotNone(local_pii_check("patient SSN 123-45-6789"))

    def test_local_pii_allows_clinical_query(self):
        self.assertIsNone(
            local_pii_check("Amoxicillin for UTI in 65yo patient with CrCl 45")
        )


if __name__ == "__main__":
    unittest.main()
