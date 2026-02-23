import requests

# The normal sequence you should be testing
normal_seq = 'ATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATCGATACGATACGATCGATACGATCGATACGATCGATACGATCGATACGATAC'

response = requests.post('http://localhost:8000/predict', json={'sequence': normal_seq})
result = response.json()

print('NORMAL SEQUENCE TEST')
print('=' * 60)
status = "✅ NORMAL" if not result["isMutated"] else "🔴 MUTATED"
print(f'Status: {status}')
print(f'Confidence: {result["confidence"]:.2f}%')
if result.get('mutationType'):
    print(f'Type: {result["mutationType"]}')
print(f'Reason: {result.get("reason", "N/A")}')
print(f'Length: {len(normal_seq)} bp')
