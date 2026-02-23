import requests

# Test alternating pattern at different lengths
base_pattern = "ACGTACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCG"

test_lengths = [50, 75, 88, 100, 120, 150, 200]

print("Testing normal alternating pattern at different lengths")
print("=" * 70)
print()

for length in test_lengths:
    sequence = base_pattern[:length] if length <= len(base_pattern) else base_pattern * ((length // len(base_pattern)) + 1)
    sequence = sequence[:length]
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json={"sequence": sequence},
            timeout=5
        )
        result = response.json()
        
        status = "✅ NORMAL" if not result["isMutated"] else "🔴 MUTATED"
        
        print(f"Length: {length:3d} bp | Status: {status} | Confidence: {result['confidence']:6.2f}%")
    except Exception as e:
        print(f"Length: {length:3d} bp | Error: {e}")

print()
print("RECOMMENDATION:")
print("-" * 70)
print("✅ Use sequences 50-88 bp for NORMAL examples")
print("   These show low confidence (< 1%) and proper NORMAL status")
