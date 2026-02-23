import requests

# The "Simple Diverse" sequence that showed NORMAL before
simple_diverse = 'ACGTACGACGATAGTACGATACGATACGACACGTACGACTGATCTGACTGATCGATACGATCGATCGATCGATACGATCGATCGATCG'

print("Testing 'Simple Diverse' sequence")
print("=" * 60)
print(f"Sequence: {simple_diverse}")
print(f"Length: {len(simple_diverse)} bp")
print()

try:
    response = requests.post('http://localhost:8000/predict', json={'sequence': simple_diverse})
    result = response.json()
    
    status = "✅ NORMAL" if not result["isMutated"] else "🔴 MUTATED"
    print(f'Status: {status}')
    print(f'Confidence: {result["confidence"]:.2f}%')
    if result.get('mutationType') != 'None':
        print(f'Type: {result["mutationType"]}')
    print(f'Reason: {result.get("reasons", "N/A")}')
except Exception as e:
    print(f'Error: {e}')
