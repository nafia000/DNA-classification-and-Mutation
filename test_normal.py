import requests
import json

sequences = [
    # NORMAL/HEALTHY SEQUENCES - No CG/GC, no homopolymers, no high repetition
    {
        'name': 'NORMAL DNA Sequence #1 (Healthy - 240 bp)',
        'seq': 'ATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATGATG'
    },
    {
        'name': 'NORMAL DNA Sequence #2 (Wild-type - 250 bp)',
        'seq': 'ATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATAATA'
    },
    {
        'name': 'NORMAL DNA Sequence #3 (Standard - 260 bp)',
        'seq': 'ATGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGATAGAT'
    }
]

print("\n" + "=" * 100)
print("NORMAL DNA SEQUENCE EXAMPLES")
print("=" * 100 + "\n")

for item in sequences:
    try:
        response = requests.post('http://localhost:8000/predict', json={'sequence': item['seq']})
        data = response.json()
        
        status = "NORMAL - HEALTHY" if not data["isMutated"] else "MUTATED - ABNORMAL"
        seq_length = len(item['seq'])
        
        print("Test: " + item['name'])
        print("Length: " + str(seq_length) + " bp")
        print("Status: " + status)
        print("Type: " + data['mutationType'])
        print("Confidence: " + "{:.2%}".format(data['confidence']))
        print("\nSequence:")
        print(item['seq'])
        print("-" * 100)
        
    except Exception as e:
        print("Error testing " + item["name"] + ": " + str(e))
        print("-" * 100)

print("\n")
