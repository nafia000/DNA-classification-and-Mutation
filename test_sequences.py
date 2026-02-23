import requests
import json

sequences = [
    # Example 1: Point Mutation - Contains CpG rich region (mutation hotspot)
    {
        'name': 'Point Mutation (CpG-rich)',
        'seq': 'ACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGT'
    },
    # Example 2: Frameshift Mutation - Contains homopolymer runs
    {
        'name': 'Frameshift Mutation (Homopolymer)',
        'seq': 'ACGTTTTTTACGTTTTTTACGTTTTTTACGTTTTTTACGTTTTTTACGT'
    },
    # Example 3: Deletion - Contains AT-rich region (70%+ AT)
    {
        'name': 'Deletion Mutation (AT-rich)',
        'seq': 'ATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATATAA'
    },
    # Example 4: Insertion - Highly repetitive k-mers
    {
        'name': 'Insertion Mutation (Repetitive)',
        'seq': 'ACGACGACGACGACGACGACGACGACGACGACGACGACGACGACGACGACG'
    },
    # Example 5: Normal sequence - Balanced distribution
    {
        'name': 'Normal Sequence (Balanced)',
        'seq': 'ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT'
    }
]

print("\n" + "=" * 80)
print("DNA MUTATION DETECTION TEST RESULTS")
print("=" * 80 + "\n")

for item in sequences:
    try:
        response = requests.post('http://localhost:8000/predict', json={'sequence': item['seq']})
        data = response.json()
        
        status = "🔴 MUTATED" if data["isMutated"] else "✅ NORMAL"
        print(f"Test: {item['name']}")
        print(f"Sequence: {item['seq']}")
        print(f"Result: {status}")
        print(f"Type: {data['mutationType']}")
        print(f"Confidence: {data['confidence']:.2%}")
        print(f"Reason: {data['reasons']}")
        print("-" * 80)
        
    except Exception as e:
        print(f'Error testing {item["name"]}: {e}')
        print("-" * 80)

print("\n✅ Copy any MUTATED sequence above to test in the UI!\n")

