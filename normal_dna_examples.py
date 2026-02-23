#!/usr/bin/env python3
"""
Normal DNA Sequences - Best Examples
These work well and show as NORMAL because they have high diversity
"""

import requests

# These sequences work well - high diversity, frequent base transitions
normal_sequences = {
    "Normal_Alternating_88bp": "ACGTACGACGATAGTACGATACGATACGACACGTACGACTGATCTGACTGATCGATACGATCGATCGATCGATACGATCGATCGATCG",
    
    "Normal_Alternating_150bp": "ACGTACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATAC",
    
    "Normal_Alternating_200bp": "ATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATAC",
    
    "Normal_Alternating_250bp": "ACGTACGATCGATACGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACTGATAC",
    
    "Normal_Alternating_300bp": "ATCGACGTACGATCGATCGATACGATACGATACGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATAC"
}

print("=" * 80)
print("NORMAL DNA SEQUENCE EXAMPLES (High Diversity Pattern)")
print("=" * 80)
print()

for name, sequence in normal_sequences.items():
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"sequence": sequence},
            timeout=5
        )
        result = response.json()
        
        status = "✅ NORMAL" if not result["isMutated"] else "🔴 MUTATED"
        
        print(f"Name: {name}")
        print(f"Length: {len(sequence)} bp")
        print(f"Status: {status}")
        print(f"Confidence: {result['confidence']:.2f}%")
        if result.get('mutationType') != 'None':
            print(f"Type: {result['mutationType']}")
        print(f"Pattern: Alternating ACGT with high diversity")
        print(f"Sequence: {sequence[:70]}...")
        print("-" * 80)
        print()
    except Exception as e:
        print(f"Error testing {name}: {e}")
        print()
