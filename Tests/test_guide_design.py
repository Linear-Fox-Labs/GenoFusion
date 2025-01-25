import unittest
from GenoFusion.CRISPR import GuideRNADesigner
 
class TestGuideDesign(unittest.TestCase):
    """
    def test_guide_design(self):
        sequence = "ATGCGTAACGTACCCGGTTA" + "AGG"
        designer = GuideRNADesigner(pam="NGG")
        guides = designer.find_guides(sequence)
        self.assertEqual(len(guides), 1)
        self.assertEqual(guides[0]['guide'], "ATGCGTAACGTACCCGGTTA")
        self.assertEqual(guides[0]['pam'], "AGG")"""

    def test_no_guides(self):
        sequence = "ATGCGTAACGTACCCGGTTA"  # No PAM sequence
        designer = GuideRNADesigner(pam="NGG")
        guides = designer.find_guides(sequence)
        self.assertEqual(len(guides), 0)

    """
    def test_multiple_guides(self):
        sequence = "ATGCGTAACGTACCCGGTTA" + "AGG" + "CGTACCCGGTTA" + "TGG"  # Two guides
        designer = GuideRNADesigner(pam="NGG")
        guides = designer.find_guides(sequence)
        self.assertEqual(len(guides), 2)
        self.assertEqual(guides[0]['guide'], "ATGCGTAACGTACCCGGTTA")
        self.assertEqual(guides[0]['pam'], "AGG")
        self.assertEqual(guides[1]['guide'], "CGTACCCGGTTA")
        self.assertEqual(guides[1]['pam'], "TGG")"""

if __name__ == '__main__':
    unittest.main()