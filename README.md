

# Genome-X: DNA Analysis Platform with ML Integration

A clinical-grade genomic analysis platform combining a React/TypeScript UI with a machine learning backend for mutation detection.

## Architecture

- **Frontend**: React + Vite + TypeScript - Beautiful clinical interface for DNA sequence analysis
- **Backend**: Python FastAPI server - Serves pre-trained SVM ML model for mutation classification
- **ML Model**: Scikit-learn LinearSVC trained on DNA sequences with k-mer feature extraction

## Setup & Installation

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- pip (Python package manager)

### 1. Install Frontend Dependencies

```bash
npm install
```

### 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Step 1: Start the Python ML Backend

Open a terminal in the project directory and run:

```bash
python server.py
```

The backend will start on `http://localhost:8000`

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Start the Frontend in a New Terminal

```bash
npm run dev
```

The UI will be available at `http://localhost:5173`

## How It Works

1. **User Input**: DNA sequences are entered in the UI (ACGT format)
2. **Validation**: Frontend validates sequence format
3. **API Call**: Sequence is sent to the Python backend
4. **ML Processing**: 
   - Backend converts DNA sequence to k-mers (3-character substrings: ACG, CGT, etc.)
   - Uses CountVectorizer to convert k-mers to numeric features
   - Runs through trained LinearSVC model
   - Generates confidence score via decision function
5. **Results Display**: 
   - UI displays mutation status, confidence, and detailed explanation
   - XAI (Explainable AI) interface shows model reasoning

## Model Details

The ML model (`dna_mutation_model.pkl`) was trained on:
- DNA sequences with labeled mutation status
- k-mer feature extraction (k=3)
- LinearSVC classifier with balanced class weights
- Achieved high accuracy on test set

### Model Files
- `model/dna_mutation_model.pkl` - Trained SVM classifier
- `model/dna_vectorizer.pkl` - Fitted CountVectorizer for k-mer conversion

## API Endpoints

### POST `/predict`
Analyzes a DNA sequence for mutations.

**Request:**
```json
{
  "sequence": "ACGTACGTACGTACGT"
}
```

**Response:**
```json
{
  "isMutated": false,
  "confidence": 0.92,
  "sequence": "ACGTACGTACGTACGT",
  "mutationType": "None",
  "explanation": "The DNA sequence appears normal with no significant mutation indicators detected..."
}
```

### GET `/health`
Health check endpoint.

## Environment Variables

For future Gemini API integration (currently using local ML model):
- Create a `.env.local` file
- Add: `API_URL=http://localhost:8000`

## Troubleshooting

**"Connection refused" error in UI:**
- Make sure backend is running on port 8000
- Check firewall settings
- Verify Python server output shows "Uvicorn running..."

**"Model files not found" error:**
- Ensure `model/` folder contains both `.pkl` files
- Run the Jupyter notebook in `model/model.ipynb` to regenerate models if needed

**Port conflicts:**
- Backend uses port 8000 (changeable in `server.py`)
- Frontend uses port 5173 (managed by Vite)

## Development

### Build for Production
```bash
npm run build
```

### Project Structure
```
├── index.tsx              # Main React app
├── index.html             # HTML entry point
├── server.py              # FastAPI backend
├── model/
│   ├── model.ipynb        # Jupyter notebook with ML code
│   ├── dna_mutation_model.pkl    # Trained SVM model
│   └── dna_vectorizer.pkl        # Vectorizer for k-mer conversion
├── package.json           # Frontend dependencies
├── requirements.txt       # Python dependencies
└── tsconfig.json          # TypeScript config
```

## License & Attribution

This project integrates a pre-trained ML model for DNA mutation detection with a clinical-grade user interface for genomic analysis.
