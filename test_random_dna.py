import random
import requests

# Generate truly random diverse DNA sequence (no patterns)
random.seed(42)
dna_chars = ['A', 'C', 'G', 'T']

# Create 300bp of truly random DNA
random_seq = ''.join(random.choice(dna_chars) for _ in range(300))

print("Generated Random DNA Sequence (300bp)")
print("=" * 60)
print(random_seq)
print()
print("Testing against backend...")
print("=" * 60)

try:
    response = requests.post('http://localhost:8000/predict', json={'sequence': random_seq})
    result = response.json()
    
    status = "✅ NORMAL" if not result["isMutated"] else "🔴 MUTATED"
    print(f'Status: {status}')
    print(f'Confidence: {result["confidence"]:.2f}%')
    if result.get('mutationType') != 'None':
        print(f'Type: {result["mutationType"]}')
    print(f'Reason: {result.get("reason", "Normal sequence")}')
    print(f'Length: {len(random_seq)} bp')
except Exception as e:
    print(f'Error: {e}')
