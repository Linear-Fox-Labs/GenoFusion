"""
This module provides utility functions for DNA sequence analysis.

Functions:
- calculate_nucleotide_composition(sequence): Calculates the count of each nucleotide (A, T, G, C) in the given DNA sequence.
- calculate_nucleotide_percentage(sequence): Calculates the percentage of each nucleotide (A, T, G, C) in the given DNA sequence.
- calculate_gc_content(sequence): Calculates the GC content (percentage of G and C nucleotides) in the given DNA sequence.
- reverse_sequence(sequence): Reverses the given DNA sequence.
- complement_sequence(sequence): Generates the complement sequence of the given DNA sequence.
- reverse_complement_sequence(sequence): Generates the reverse complement sequence of the given DNA sequence.
- get_sequence_properties(sequence): Returns a dictionary containing various properties of the given DNA sequence, including length, nucleotide composition, nucleotide percentage, GC content, reverse sequence, complement sequence, and reverse complement sequence.
"""

def calculate_nucleotide_composition(sequence):
    sequence = sequence.upper()
    composition = {
        'A': sequence.count('A'),
        'T': sequence.count('T'),
        'G': sequence.count('G'),
        'C': sequence.count('C')
    }
    return composition

def calculate_nucleotide_percentage(sequence):
    sequence = sequence.upper()
    length = len(sequence)
    composition = calculate_nucleotide_composition(sequence)
    percentage = {base: (count / length) * 100 for base, count in composition.items()}
    return percentage

def calculate_gc_content(sequence):
    sequence = sequence.upper()
    composition = calculate_nucleotide_composition(sequence)
    gc_content = ((composition['G'] + composition['C']) / len(sequence)) * 100
    return gc_content

def reverse_sequence(sequence):
    sequence = sequence.upper()
    return sequence[::-1]

def complement_sequence(sequence):
    sequence = sequence.upper()
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement[base] for base in sequence)

def reverse_complement_sequence(sequence):
    sequence = sequence.upper()
    return complement_sequence(reverse_sequence(sequence))

def get_sequence_properties(sequence):
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