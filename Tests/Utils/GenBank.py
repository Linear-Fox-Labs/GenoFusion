import unittest
from GenoFusion.Utils import DatabaseIntegration

class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        self.db_integration = DatabaseIntegration()

    def test_fetch_sequence_from_genbank(self):
        genbank_id = "NM_001301717.2"
        sequence = self.db_integration.fetch_sequence_from_genbank(genbank_id)
        self.assertIsNotNone(sequence)
        self.assertIsInstance(sequence, str)

    def test_fetch_sequence_from_ensembl(self):
        ensembl_id = "ENSG00000139618"
        sequence = self.db_integration.fetch_sequence_from_ensembl(ensembl_id)
        self.assertIsNotNone(sequence)
        self.assertIsInstance(sequence, str)

if __name__ == "__main__":
    unittest.main()
    