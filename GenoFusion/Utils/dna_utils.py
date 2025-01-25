# GenoFusion/Utils/dna_utils.py

"""
This module provides utility functions for DNA sequence analysis with support for IUPAC ambiguity codes.
"""

from typing import Dict, List
import regex

def calculate_nucleotide_composition(sequence):
    """
    Calculate the count of each nucleotide in the sequence.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        dict: Count of each nucleotide
    """
    sequence = sequence.upper()
    return {base: sequence.count(base) for base in set(sequence)}

def calculate_nucleotide_percentage(sequence):
    """
    Calculate the percentage of each nucleotide in the sequence.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        dict: Percentage of each nucleotide
    """
    sequence = sequence.upper()
    length = len(sequence)
    if length == 0:
        raise ZeroDivisionError("Cannot calculate percentages for empty sequence")
    composition = calculate_nucleotide_composition(sequence)
    return {base: (count / length) * 100 for base, count in composition.items()}

def calculate_gc_content(sequence):
    """
    Calculate GC content percentage.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        float: GC content percentage
    """
    sequence = sequence.upper()
    gc_bases = sum(sequence.count(base) for base in ['G', 'C'])
    total_bases = sum(1 for base in sequence if base in 'ATGCN')
    return (gc_bases / total_bases) * 100 if total_bases > 0 else 0.0

def reverse_sequence(sequence):
    """
    Reverse the sequence.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        str: Reversed sequence
    """
    sequence = sequence.upper()
    return sequence[::-1]

def complement_sequence(sequence):
    """
    Generate complement sequence with IUPAC ambiguity code support.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        str: Complement sequence
    """
    sequence = sequence.upper()
    complement = {
        'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
        'N': 'N', 'R': 'Y', 'Y': 'R', 'K': 'M',
        'M': 'K', 'S': 'S', 'W': 'W', 'B': 'V',
        'V': 'B', 'D': 'H', 'H': 'D', '-': '-',
        '.': '.'
    }
    return ''.join(complement.get(base, base) for base in sequence)

def reverse_complement_sequence(sequence):
    """
    Generate reverse complement sequence.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        str: Reverse complement sequence
    """
    sequence = sequence.upper()
    return complement_sequence(reverse_sequence(sequence))

def get_sequence_properties(sequence):
    """
    Get comprehensive sequence properties.
    
    Args:
        sequence (str): DNA sequence
        
    Returns:
        dict: Dictionary containing sequence properties
    """
    sequence = sequence.upper()
    properties = {
        'length': len(sequence),
        'nucleotide_composition': calculate_nucleotide_composition(sequence),
        'nucleotide_percentage': calculate_nucleotide_percentage(sequence),
        'gc_content': calculate_gc_content(sequence),
        'reverse_sequence': reverse_sequence(sequence),
        'complement_sequence': complement_sequence(sequence),
        'reverse_complement_sequence': reverse_complement_sequence(sequence)
    }
    return properties

def validate_sequence(sequence, alphabet='ATGCN'):
    """
    Validate sequence contains only allowed characters.
    
    Args:
        sequence (str): DNA sequence
        alphabet (str): Allowed characters
        
    Returns:
        bool: True if valid, False otherwise
    """
    return all(base in alphabet for base in sequence.upper())

 
def find_crispr_offtargets(guide_seq: str, genome_sequence: str, mismatches: int = 3) -> List[Dict]:
    """Find potential off-target sites using fuzzy matching"""
    pattern = f"(?b)({guide_seq}){{s<={mismatches}}}"
    matches = []
    for match in regex.finditer(pattern, genome_sequence, regex.IGNORECASE):
        matches.append({
            "start": match.start(),
            "end": match.end(),
            "sequence": match.group(),
            "mismatches": match.fuzzy_counts[0]
        })
    return matches

def _check_secondary_structure(sequence: str) -> bool:
    """Placeholder function to check for secondary structure"""
    return False

def validate_grna(sequence: str) -> Dict:
    """Comprehensive CRISPR guide validation"""
    return {
        "valid": len(sequence) == 20,
        "gc_warning": not (40 <= calculate_gc_content(sequence) <= 60),
        "polyT": "TTTT" in sequence,
        "secondary_structure": _check_secondary_structure(sequence)
    }