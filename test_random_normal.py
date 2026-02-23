import requests
import random

# Set seed for reproducibility
random.seed(42)

sequences = [
    # Completely random sequences with balanced nucleotides
    {
        'name': 'NORMAL DNA #1 (Random Balanced - 250 bp)',
        'seq': ''.join(random.choice('ACGT') for _ in range(250))
    },
    {
        'name': 'NORMAL DNA #2 (Random Balanced - 280 bp)',
        'seq': ''.join(random.choice('ACGT') for _ in range(280))
    },
    {
        'name': 'NORMAL DNA #3 (Random Balanced - 300 bp)',
        'seq': ''.join(random.choice('ACGT') for _ in range(300))
    },
    # The problematic sequence from user
    {
        'name': 'User Test Sequence',
        'seq': 'ACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATAC'
    }
]

print("\n" + "=" * 100)
print("NORMAL DNA SEQUENCE TESTING (Updated Detection)")
print("=" * 100 + "\n")

for item in sequences:
    try:
        response = requests.post('http://localhost:8000/predict', json={'sequence': item['seq']})
        data = response.json()
        
        status = "✅ NORMAL" if not data["isMutated"] else "🔴 MUTATED"
        seq_length = len(item['seq'])
        
        print("Test: " + item['name'])
        print("Length: " + str(seq_length) + " bp")
        print("Result: " + status)
        print("Type: " + data['mutationType'])
        print("Confidence: " + "{:.2%}".format(data['confidence']))
        print("\nSequence:")
        print(item['seq'])
        print("-" * 100)
        
    except Exception as e:
        print("Error: " + str(e))
        print("-" * 100)

print("\n")
