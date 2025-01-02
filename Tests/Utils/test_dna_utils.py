import unittest
from GenoFusion.Utils.dna_utils import (
    calculate_nucleotide_composition,
    calculate_nucleotide_percentage,
    calculate_gc_content,
    reverse_sequence,
    complement_sequence,
    reverse_complement_sequence,
    get_sequence_properties
)

class TestDNAUtils(unittest.TestCase):
    def setUp(self):
        self.test_sequence = "ATGCTAGCTA"
        self.invalid_sequence = "ATGCX"
        print(f"\nTest sequence: {self.test_sequence}")
        
    def test_calculate_nucleotide_composition(self):
        result = calculate_nucleotide_composition(self.test_sequence)
        expected = {'A': 3, 'T': 3, 'G': 2, 'C': 2}
        print(f"\nNucleotide composition: {result}")
        self.assertEqual(result, expected)
        
        # Test case insensitivity
        result_lower = calculate_nucleotide_composition(self.test_sequence.lower())
        self.assertEqual(result_lower, expected)

    def test_calculate_nucleotide_percentage(self):
        result = calculate_nucleotide_percentage(self.test_sequence)
        expected = {'A': 30.0, 'T': 30.0, 'G': 20.0, 'C': 20.0}
        print(f"\nNucleotide percentages: {result}")
        for base in expected:
            self.assertAlmostEqual(result[base], expected[base], places=1)

    def test_calculate_gc_content(self):
        result = calculate_gc_content(self.test_sequence)
        expected = 40.0  # (2 G + 2 C) / 10 total bases * 100
        print(f"\nGC content: {result}%")
        self.assertEqual(result, expected)

        # Test sequence with no GC content
        no_gc = "ATATAT"
        result_no_gc = calculate_gc_content(no_gc)
        print(f"GC content (AT only sequence): {result_no_gc}%")
        self.assertEqual(result_no_gc, 0.0)

        # Test sequence with 100% GC content
        all_gc = "GCGCGC"
        result_all_gc = calculate_gc_content(all_gc)
        print(f"GC content (GC only sequence): {result_all_gc}%")
        self.assertEqual(result_all_gc, 100.0)

    def test_reverse_sequence(self):
        result = reverse_sequence(self.test_sequence)
        expected = "ATCGATCGTA"
        print(f"\nReverse sequence: {result}")
        self.assertEqual(result, expected)

        # Test palindrome
        palindrome = "ATCGCGTA"
        result = reverse_sequence(palindrome)
        print(f"Reverse of palindrome {palindrome}: {result}")
        self.assertEqual(result, "ATGCGCTA")

    def test_complement_sequence(self):
        result = complement_sequence(self.test_sequence)
        expected = "TACGATCGAT"
        print(f"\nComplement sequence: {result}")
        self.assertEqual(result, expected)

        # Test case insensitivity
        result_lower = complement_sequence(self.test_sequence.lower())
        self.assertEqual(result_lower, expected)

    def test_reverse_complement_sequence(self):
        result = reverse_complement_sequence(self.test_sequence)
        expected = "TAGCTAGCAT"
        print(f"\nReverse complement sequence: {result}")
        self.assertEqual(result, expected)

    def test_get_sequence_properties(self):
        result = get_sequence_properties(self.test_sequence)
        print("\nSequence properties:")
        for key, value in result.items():
            print(f"{key}: {value}")
        
        # Test structure and key existence
        expected_keys = {
            'length',
            'nucleotide_composition',
            'nucleotide_percentage',
            'gc_content',
            'reverse_sequence',
            'complement_sequence',
            'reverse_complement_sequence'
        }
        self.assertEqual(set(result.keys()), expected_keys)
        
        # Test specific values
        self.assertEqual(result['length'], 10)
        self.assertEqual(result['gc_content'], 40.0)
        self.assertEqual(result['reverse_sequence'], "ATCGATCGTA")
        self.assertEqual(result['complement_sequence'], "TACGATCGAT")
        self.assertEqual(result['reverse_complement_sequence'], "TAGCTAGCAT")

    def test_empty_sequence(self):
        empty_seq = ""
        print("\nTesting empty sequence handling:")
        try:
            calculate_nucleotide_percentage(empty_seq)
        except ZeroDivisionError:
            print("Empty sequence correctly raised ZeroDivisionError for percentage calculation")
        
        try:
            calculate_gc_content(empty_seq)
        except ZeroDivisionError:
            print("Empty sequence correctly raised ZeroDivisionError for GC content calculation")

        with self.assertRaises(ZeroDivisionError):
            calculate_nucleotide_percentage(empty_seq)
        with self.assertRaises(ZeroDivisionError):
            calculate_gc_content(empty_seq)

if __name__ == '__main__':
    unittest.main(verbosity=2)