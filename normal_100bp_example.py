import requests

# Additional 100 bp normal DNA sequence
normal_100bp = "ATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATAC"

print("Testing Additional 100 bp Normal DNA Sequence")
print("=" * 70)
print()
print(f"Sequence: {normal_100bp}")
print(f"Length: {len(normal_100bp)} bp")
print()

try:
    response = requests.post(
        "http://localhost:8000/predict",
        json={"sequence": normal_100bp},
        timeout=5
    )
    result = response.json()
    
    status = "✅ NORMAL" if not result["isMutated"] else "🔴 MUTATED"
    
    print(f"Status: {status}")
    print(f"Confidence: {result['confidence']:.2f}%")
    if result.get('mutationType') != 'None':
        print(f"Type: {result['mutationType']}")
    print(f"Reason: {result.get('reasons', 'Normal sequence')}")
    print()
    print("-" * 70)
    print("✅ Ready to use in your project!")
    
except Exception as e:
    print(f"Error: {e}")
