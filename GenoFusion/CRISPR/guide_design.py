from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction
from typing import List, Dict
import regex

class GuideRNADesigner:
    # IUPAC to regex mapping
    IUPAC_PATTERNS = {
        'N': '.', 'R': '[AG]', 'Y': '[CT]', 'S': '[GC]',
        'W': '[AT]', 'K': '[GT]', 'M': '[AC]', 'B': '[CGT]',
        'D': '[AGT]', 'H': '[ACT]', 'V': '[ACG]'
    }

    def __init__(self, pam: str = "NGG"):
        self.pam = pam.upper()
        # Convert IUPAC codes to regex
        self.regex_pam = ''.join([self.IUPAC_PATTERNS.get(c, c) for c in self.pam])
    
    def find_guides(self, sequence: str, guide_length: int = 20) -> List[Dict]:
        """Find CRISPR guide RNAs in a sequence."""
        search_pattern = f"(.{{{guide_length}}})({self.regex_pam})"
        guides = []
        pam_len = len(self.pam)
        search_pattern = f"(.{{{guide_length}}})({self.pam})"
        
        for match in regex.finditer(search_pattern, sequence, overlapped=True):
            start = match.start()
            end = start + guide_length + pam_len
            guide_seq = match.group(1)
            pam_seq = match.group(2)
            
            guides.append({
                "start": start,
                "end": end,
                "guide": guide_seq,
                "pam": pam_seq,
                "gc_content": gc_fraction(guide_seq) * 100,
                "off_target_score": self._calc_off_target_risk(guide_seq)
            })
        return guides
    
    def _calc_off_target_risk(self, guide: str) -> float:
        """Score based on GC content and repetitive elements"""
        gc_score = abs(50 - gc_fraction(guide)*100) / 50  # Penalize extremes
        repeat_score = 1 if any(base*4 in guide for base in 'ATGC') else 0
        return round(gc_score + repeat_score, 2)

class HDRTemplateDesigner:
    def design_repair_template(self, wildtype: str, edit: str, homology_arm_length: int = 50) -> Dict:
        """Design HDR template with homology arms."""
        left_arm = wildtype[-homology_arm_length:]
        right_arm = wildtype[:homology_arm_length]
        return {
            "template": f"{left_arm}{edit}{right_arm}",
            "homology_arms": {
                "left": left_arm,
                "right": right_arm
            }
        }