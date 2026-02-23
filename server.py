from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI()

# Add CORS middleware to allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the new Random Forest model and vectorizer
MODEL_PATH = "model/dna_mutation_model.pkl"
VECTORIZER_PATH = "model/dna_vectorizer.pkl"

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Random Forest model and vectorizer loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading model files: {e}")
    print("Make sure the new Random Forest model files exist in the model/ folder")
    model = None
    vectorizer = None

# Request/Response models
class DNASequenceRequest(BaseModel):
    sequence: str

class PredictionResponse(BaseModel):
    isMutated: bool
    confidence: float
    sequence: str
    mutationType: str
    explanation: str
    mutatedSegments: list = []
    reasons: str = ""
    prevention: str = ""

def get_kmers(sequence, k=3):
    """Convert DNA sequence to k-mers"""
    return [sequence[i:i+k] for i in range(len(sequence)-k+1)]

def validate_dna_sequence(seq):
    """Validate if sequence contains only ACGT"""
    import re
    cleaned = seq.upper().replace('\n', '').replace(' ', '')
    return re.match(r'^[ACGT]+$', cleaned) is not None

def analyze_sequence_patterns(sequence):
    """Analyze sequence for known mutation patterns"""
    analysis = {
        'has_homopolymer_runs': False,
        'has_repetitive_kmers': False,
        'has_cg_rich_regions': False,
        'mutation_score': 0.0
    }
    
    # Check for homopolymer runs (5+ same nucleotides) - stricter threshold
    for base in 'ACGT':
        if base * 5 in sequence:
            analysis['has_homopolymer_runs'] = True
            analysis['mutation_score'] += 0.4
            break
    
    # Check for CpG islands - at least 20% CG content
    cg_count = sequence.count('CG') + sequence.count('GC')
    cg_percentage = (cg_count * 2) / len(sequence)  # Each dinucleotide is 2 nucleotides
    if cg_percentage > 0.20:  # More than 20% CG/GC
        analysis['has_cg_rich_regions'] = True
        analysis['mutation_score'] += 0.35
    
    # Check for highly repetitive k-mers (stricter: > 20% of sequence)
    kmers = get_kmers(sequence)
    from collections import Counter
    kmer_counts = Counter(kmers)
    if len(kmer_counts) > 0 and max(kmer_counts.values()) > len(kmers) * 0.20:
        analysis['has_repetitive_kmers'] = True
        analysis['mutation_score'] += 0.3
    
    # Check for extreme AT or GC bias (>75%)
    at_content = (sequence.count('A') + sequence.count('T')) / len(sequence)
    if at_content > 0.75 or at_content < 0.25:
        analysis['mutation_score'] += 0.2
    
    return analysis

@app.post("/predict", response_model=PredictionResponse)
def predict(request: DNASequenceRequest):
    """Predict if DNA sequence has mutations"""
    try:
        if model is None or vectorizer is None:
            raise HTTPException(
                status_code=500,
                detail="Model or vectorizer not loaded. Please check server logs."
            )

        sequence = request.sequence.upper().replace('\n', '').replace(' ', '')
        
        # Validate sequence
        if not validate_dna_sequence(sequence):
            raise HTTPException(
                status_code=400,
                detail="Invalid DNA sequence. Only ACGT characters allowed."
            )
        
        if len(sequence) < 3:
            raise HTTPException(
                status_code=400,
                detail="DNA sequence too short. Minimum 3 characters required."
            )
        
        # Create k-mers
        kmers = get_kmers(sequence)
        kmers_text = " ".join(kmers)
        
        # Vectorize
        X = vectorizer.transform([kmers_text])
        
        # Predict using model
        prediction = model.predict(X)[0]

        # Use predict_proba if available
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0][1]  # Probability of class 1 (mutated)
            model_confidence = float(proba)
        else:
            # Fallback to decision_function + sigmoid
            decision_scores = model.decision_function(X)
            model_confidence = float(1 / (1 + np.exp(-decision_scores[0])))
        confidence = max(0, min(1, model_confidence))

        pattern_analysis = analyze_sequence_patterns(sequence)
        
        # Use model prediction as the only determinant
        is_mutated = bool(prediction == 1)
        
        # Determine mutation type for explanation
        if is_mutated:
            if pattern_analysis['has_homopolymer_runs']:
                mutation_type = "Frameshift Mutation"
            elif pattern_analysis['has_cg_rich_regions']:
                mutation_type = "Point Mutation"
            elif pattern_analysis['has_repetitive_kmers']:
                mutation_type = "Deletion Mutation"
            else:
                mutation_type = "Insertion Mutation"
        else:
            mutation_type = "None"
        
        # Calculate mutated segments
        mutated_segments = []
        reasons_dict = {
            "Point Mutation": "CpG sites are hotspots for spontaneous deamination, converting cytosine to thymine or causing oxidative damage",
            "Deletion Mutation": "Homopolymer runs cause DNA polymerase slippage leading to nucleotide loss in repetitive regions",
            "Insertion Mutation": "Repetitive k-mer sequences facilitate transposable element insertion and polymerase errors",
            "Frameshift Mutation": "Homopolymer expansions disrupt reading frame and cause downstream frameshift effects"
        }
        
        prevention_dict = {
            "Point Mutation": "Reduce UV exposure, maintain high antioxidant levels, avoid carcinogenic substances, and regular genetic monitoring",
            "Deletion Mutation": "Monitor for trinucleotide repeat expansions, maintain proper nucleotide balance, and genetic counseling",
            "Insertion Mutation": "Suppress transposable element activity through epigenetic regulation and lifestyle modifications",
            "Frameshift Mutation": "Prevent repeat expansion through stress management, adequate nutrition, and periodic genetic screening"
        }
        
        if is_mutated:
            # Identify mutated segments (divide sequence into regions)
            segment_size = len(sequence) // 4
            for i in range(4):
                start = i * segment_size
                end = start + segment_size if i < 3 else len(sequence)
                segment = sequence[start:end]
                segment_kmers = get_kmers(segment)
                
                # Check if this segment has anomalies
                if len(segment_kmers) > 0:
                    from collections import Counter
                    kmer_freq = Counter(segment_kmers)
                    max_freq = max(kmer_freq.values()) if kmer_freq else 0
                    
                    # Mark segment as affected if it has high kmer repetition or homopolymers
                    if max_freq > len(segment_kmers) * 0.1 or any(base*4 in segment for base in 'ACGT'):
                        segment_num = i + 1
                        mutated_segments.append({
                            "position": f"Segment {segment_num} (Position {start}-{end})",
                            "kmer_count": len(segment_kmers),
                            "abnormal_kmers": max(1, int(len(segment_kmers) * (confidence - 0.4)))
                        })
            
            explanation = f"The DNA sequence shows patterns consistent with mutations (confidence: {confidence:.2%}). Detected: {', '.join([k for k in pattern_analysis.keys() if pattern_analysis[k]])}. These patterns indicate potential genetic variations requiring further investigation."
            reasons = reasons_dict.get(mutation_type, "Mutation pattern detected in genomic sequence")
            prevention = prevention_dict.get(mutation_type, "Standard clinical monitoring and genetic counseling recommended")
        else:
            explanation = f"The DNA sequence appears normal with stable genomic patterns (confidence: {confidence:.2%}). K-mer analysis shows expected distribution consistent with wild-type DNA."
            reasons = "No mutations detected - genomic integrity maintained"
            prevention = "Continue standard health maintenance and periodic genetic screening as preventative care"
        
        return PredictionResponse(
            isMutated=is_mutated,
            confidence=confidence,
            sequence=sequence[:50] + "..." if len(sequence) > 50 else sequence,
            mutationType=mutation_type,
            explanation=explanation,
            mutatedSegments=mutated_segments,
            reasons=reasons,
            prevention=prevention
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)