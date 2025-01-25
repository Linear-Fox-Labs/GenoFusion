from typing import List, Dict

def parse_bed(file_path: str) -> List[Dict]:
    """Parse BED files for genome annotations"""
    features = []
    with open(file_path) as f:
        for line in f:
            if line.startswith('#'): continue
            parts = line.strip().split('\t')
            features.append({
                "chrom": parts[0],
                "start": int(parts[1]),
                "end": int(parts[2]),
                "name": parts[3] if len(parts) > 3 else "",
                "strand": parts[5] if len(parts) > 5 else "+"
            })
    return features