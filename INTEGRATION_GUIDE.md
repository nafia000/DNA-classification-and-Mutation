# Genome-X: ML Model Integration Guide

## Overview

Your DNA analysis UI has been successfully integrated with the ML model from the `model/` folder. The system now uses a trained SVM classifier instead of the Google Gemini API.

## What Changed

### Frontend (React/TypeScript)
- **Removed**: Google Genai API integration
- **Added**: FastAPI backend client
- **Updated**: `runAnalysis()` function to call the local ML backend
- **File**: `index.tsx`

### Backend (New)
- **Created**: `server.py` - FastAPI server that serves the ML model
- **Features**:
  - Loads pre-trained SVM model and vectorizer from `model/` folder
  - Accepts DNA sequences via REST API
  - Performs k-mer conversion and vectorization
  - Returns mutation predictions with confidence scores
  - CORS enabled for frontend communication

### Dependencies
- **Python**: FastAPI, Uvicorn, joblib, scikit-learn, numpy
- **Frontend**: Already had React, no new JS dependencies needed

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (Port 5173)                │
│  - Beautiful clinical interface                              │
│  - DNA sequence input                                        │
│  - Results display & XAI visualization                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP POST /predict
                       │ (DNA sequence)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Port 8000)                 │
│  - Model loading (dna_mutation_model.pkl)                    │
│  - Vectorizer loading (dna_vectorizer.pkl)                   │
│  - K-mer feature extraction                                  │
│  - SVM prediction                                            │
│  - Confidence calculation                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ JSON Response
                       │ {isMutated, confidence, explanation}
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Display                          │
│  - Mutation status                                           │
│  - Confidence score                                          │
│  - XAI interpretation                                        │
└─────────────────────────────────────────────────────────────┘
```

## How to Run

### Quick Start (Windows)
Simply run the setup script:
```batch
setup.bat
```

This will install all dependencies. Then follow the on-screen instructions.

### Manual Start

**Terminal 1 - Start Backend:**
```bash
python server.py
```
Expected: `INFO: Uvicorn running on http://0.0.0.0:8000`

**Terminal 2 - Start Frontend:**
```bash
npm run dev
```
Expected: Frontend available at `http://localhost:5173`

## ML Model Details

### Training Process (from model.ipynb)
1. **Data Loading**: Combines two DNA datasets with mutation labels
2. **Feature Engineering**: 
   - Converts DNA sequences to k-mers (3-character substrings)
   - Uses CountVectorizer for numeric feature extraction
3. **Data Balancing**: SMOTE (Synthetic Minority Over-sampling)
4. **Model**: LinearSVC classifier with balanced class weights
5. **Evaluation**: Achieved high accuracy on test set

### Input Format
- **Accepts**: DNA sequences with ACGT characters
- **Ignores**: Whitespace and newlines
- **Minimum**: 3 characters
- **Example**: `ACGTACGTACGT`

### Output Format
```json
{
  "isMutated": true/false,
  "confidence": 0.0-1.0,
  "sequence": "truncated_sequence",
  "mutationType": "Point Mutation/Deletion/Insertion/Frameshift/None",
  "explanation": "Detailed explanation of model reasoning"
}
```

## Customization

### Change Backend Port
Edit `server.py` line 75:
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # Change 8000 to desired port
```

Then update `index.tsx` line 42:
```typescript
const API_BASE_URL = 'http://localhost:YOUR_PORT';
```

### Use Environment Variable
Create `.env.local` in project root:
```
API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Won't Start
```
FileNotFoundError: model/dna_mutation_model.pkl not found
```
**Solution**: Ensure both `.pkl` files exist in `model/` folder. Run the Jupyter notebook to regenerate them.

### Frontend Can't Connect to Backend
```
Network Error: Failed to fetch from http://localhost:8000
```
**Solutions**:
1. Verify backend is running (`python server.py`)
2. Check firewall isn't blocking port 8000
3. Verify API_BASE_URL is correct in `index.tsx`

### Invalid Sequence Error
```json
{"detail": "Invalid DNA sequence. Only ACGT characters allowed."}
```
**Solution**: Only enter ACGT characters (case-insensitive). Remove spaces, numbers, or special characters.

## API Reference

### POST /predict
Analyzes a DNA sequence for mutations.

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"sequence": "ACGTACGTACGT"}'
```

**Success Response (200):**
```json
{
  "isMutated": false,
  "confidence": 0.92,
  "sequence": "ACGTACGTACGT",
  "mutationType": "None",
  "explanation": "The DNA sequence appears normal..."
}
```

**Error Response (400):**
```json
{"detail": "Invalid DNA sequence. Only ACGT characters allowed."}
```

### GET /health
Health check endpoint.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{"status": "ok", "model_loaded": true}
```

## Future Enhancements

1. **Authentication**: Add user authentication to backend
2. **Database**: Store analysis history in database
3. **Model Improvements**: Retrain with more data or try different algorithms
4. **Deployment**: Deploy to cloud (AWS, Google Cloud, Azure)
5. **ONNX Export**: Convert model to ONNX for edge inference
6. **Real-time Analysis**: WebSocket support for streaming DNA sequences

## Project Structure

```
c:\Users\nafia\DNA\
├── index.tsx                    # Main React component
├── index.html                   # HTML entry point
├── server.py                    # FastAPI backend ⭐ NEW
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
├── package.json                 # Node dependencies
├── requirements.txt             # Python dependencies ⭐ NEW
├── setup.bat                    # Setup script (Windows) ⭐ NEW
├── .env.example                 # Environment variables example ⭐ NEW
├── README.md                    # Updated documentation
└── model/
    ├── model.ipynb              # Jupyter notebook with ML code
    ├── dna_mutation_model.pkl    # Trained SVM model
    └── dna_vectorizer.pkl       # Vectorizer for k-mer conversion
```

## Summary

Your UI is now fully integrated with your ML model! The React frontend communicates with the Python backend via REST API. The pipeline handles:
- Sequence validation
- K-mer feature extraction
- ML model inference
- Confidence calculation
- XAI-ready explanations

Simply run the backend and frontend in separate terminals, and you're ready to analyze DNA sequences with your trained model!
