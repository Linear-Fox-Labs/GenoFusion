import random
from Bio.Seq import Seq
from Bio.Restriction import AllEnzymes, CommOnly

# Define groups of enzymes
NEB_enzymes = ['EcoRI', 'BamHI', 'HindIII']
Fermentas_enzymes = ['BglII', 'EcoRV', 'HindIII']

# Functions to categorize enzymes
def is_unique(enzyme):
    """Check if an enzyme recognizes a unique sequence in a 10kb sequence of 'A's."""
    return len(enzyme.search(Seq("A" * 10000))) == 1

def is_double_cutter(enzyme):
    """Check if an enzyme recognizes exactly two sites in a 10kb sequence of 'A's."""
    return len(enzyme.search(Seq("A" * 10000))) == 2

def is_type_iis(enzyme):
    """Check if an enzyme is a Type IIS enzyme."""
    return enzyme.elucidate().startswith("^") or enzyme.elucidate().endswith("^")

def is_nicking(enzyme):
    """Check if an enzyme is a nicking endonuclease."""
    return "Nicking" in enzyme.__class__.__name__

enzyme_groups = {
    "All Commercial": CommOnly,
    "Nonredundant Commercial": CommOnly,  # This should be updated with a proper list if available
    "New England Biolabs": [enzyme for enzyme in AllEnzymes if enzyme.__name__ in NEB_enzymes],
    "Fermentas": [enzyme for enzyme in AllEnzymes if enzyme.__name__ in Fermentas_enzymes],
    "Unique Cutters": [enzyme for enzyme in AllEnzymes if is_unique(enzyme)],
    "Unique Dual Cutters": [enzyme for enzyme in AllEnzymes if is_double_cutter(enzyme)],
    "6+ Cutters": [enzyme for enzyme in AllEnzymes if len(enzyme.site) >= 6],
    "Unique 6+ Cutters": [enzyme for enzyme in AllEnzymes if is_unique(enzyme) and len(enzyme.site) >= 6],
    "Type IIS Enzymes": [enzyme for enzyme in AllEnzymes if is_type_iis(enzyme)],
    "Golden Gate Enzymes": [enzyme for enzyme in AllEnzymes if is_type_iis(enzyme)],  # Typically Type IIS enzymes are used
    "Nicking Endonucleases": [enzyme for enzyme in AllEnzymes if is_nicking(enzyme)]
}

colors = [
    "red", "green", "blue", "yellow", "orange", "purple", "cyan", "magenta", "lime", "pink",
    "teal", "lavender", "brown", "beige", "maroon", "mint", "olive", "coral", "navy", "grey"
]

enzyme_colors = {}

def get_color_for_enzyme(enzyme_name):
    if enzyme_name not in enzyme_colors:
        enzyme_colors[enzyme_name] = random.choice(colors)
    return enzyme_colors[enzyme_name]

def get_enzyme_sites(sequence, enzymes):
    enzyme_sites = []
    for enzyme in enzymes:
        for site in enzyme.search(sequence):
            enzyme_sites.append((enzyme, site, site + len(enzyme.site)))
    enzyme_sites.sort(key=lambda x: x[1])
    return enzyme_sites

def translate_sequence(nucleotide_sequence):
    sequence = Seq(nucleotide_sequence)
    return str(sequence.translate())

def find_enzyme_sites(sequence_str, selected_group):
    if selected_group in enzyme_groups:
        enzymes = enzyme_groups[selected_group]
    else:
        enzymes = AllEnzymes

    enzyme_sites = get_enzyme_sites(Seq(sequence_str), enzymes)
    highlighted_sequence = ""
    last_end = 0

    for enzyme, start, end in enzyme_sites:
        highlighted_sequence += sequence_str[last_end:start]
        highlighted_sequence += f'<span class="enzyme" data-enzyme="{enzyme}" style="background-color:{get_color_for_enzyme(enzyme.__name__)}">{sequence_str[start:end]}</span>'
        last_end = end

    highlighted_sequence += sequence_str[last_end:]

    return highlighted_sequence, enzyme_sites

def get_sequence_properties(sequence_str):
    sequence = Seq(sequence_str)
    gc_content = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
    return {
        "length": len(sequence),
        "gc_content": gc_content
    }

""" Example usage:
sequence = "ATGCGTACG"
selected_group = "Fermentas"

highlighted_sequence, enzyme_sites = find_enzyme_sites(sequence, selected_group)
sequence_properties = get_sequence_properties(sequence)

print("Highlighted Sequence:")
print(highlighted_sequence)
print("\nEnzyme Sites:")
for enzyme, start, end in enzyme_sites:
    print(f"{enzyme.__name__} cuts at position {start}-{end}")

print("\nSequence Properties:")
print(sequence_properties)
"""