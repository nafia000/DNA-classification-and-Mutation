import requests
import json

sequences = [
    {
        'name': 'Simple Diverse',
        'seq': 'ACGTACGACGATAGTACGATACGATACGACACGTACGACTGATCTGACTGATCGATACGATCGATCGATCGATACGATCGATCGATCG'
    },
    {
        'name': 'User Sequence',
        'seq': 'ACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATACGATACGATACTAGATACTGATGATAC'
    },
    {
        'name': 'Mutated Example',
        'seq': 'ACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGTCGACGT'
    }
]

print("\n" + "=" * 100)
print("MUTATION DETECTION ANALYSIS")
print("=" * 100 + "\n")

for item in sequences:
    try:
        response = requests.post('http://localhost:8000/predict', json={'sequence': item['seq']})
        data = response.json()
        
        status = "NORMAL" if not data["isMutated"] else "MUTATED"
        seq_length = len(item['seq'])
        
        print("Name: " + item['name'])
        print("Length: " + str(seq_length) + " bp")
        print("Result: " + status)
        print("Type: " + data['mutationType'])
        print("Confidence: " + "{:.2%}".format(data['confidence']))
        print("\nReason: " + data['reasons'])
        print("\nSequence: " + item['seq'][:80] + "...")
        print("-" * 100)
        
    except Exception as e:
        print("Error: " + str(e))
        print("-" * 100)
