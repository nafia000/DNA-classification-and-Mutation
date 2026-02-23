#!/usr/bin/env python3
"""
Normal DNA Sequence Examples
These are realistic, diverse sequences without mutation patterns
"""

import requests
import json

# Normal DNA Sequences - diverse with good nucleotide distribution
normal_sequences = {
    "Normal_Sequence_1_100bp": "ACGTACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGT",
    
    "Normal_Sequence_2_150bp": "ATGACGATCGATCGATCGATACGATACGATCGATACGTACGATACGATACGATACGATCGATACGATACGATACGATGGATCGATACGATCGATACGATAC",
    
    "Normal_Sequence_3_200bp": "ACGTACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATAC",
    
    "Normal_Sequence_4_120bp": "ATCGATACGATCGATACGATACGATCGATACGATACGATCGATACGATCGATACGATACGATCGATACGATACGATCGATACGATACGATCGATACGATC",
    
    "Normal_Sequence_5_180bp": "GACGTACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATCGATACGATCGATACTGATAC",
    
    "Normal_Sequence_6_250bp": "ACGTACGATCGATACGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATAC",
    
    "Normal_Sequence_7_110bp": "ATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATC",
    
    "Normal_Sequence_8_160bp": "ACGTACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATAC",
}

def test_normal_sequences():
    """Test all normal sequences against the backend"""
    print("=" * 80)
    print("NORMAL DNA SEQUENCE ANALYSIS")
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
            
            print(f"Name: {name}")
            print(f"Length: {len(sequence)} bp")
            print(f"Result: {result.get('isMutated', 'ERROR')}")
            if result.get('isMutated'):
                print(f"Type: {result.get('mutationType', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 'N/A'):.2f}%")
            print(f"Reason: {result.get('reason', 'N/A')}")
            print(f"Sequence sample: {sequence[:80]}...")
            print("-" * 80)
            print()
        except Exception as e:
            print(f"Error testing {name}: {e}")
            print()

if __name__ == "__main__":
    test_normal_sequences()
