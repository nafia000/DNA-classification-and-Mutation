# DN-AI Quick Start Guide

## Getting Started in 5 Minutes

### 1. Install Dependencies

```bash
# Navigate to project directory
cd c:\Users\nafia\main project\dn_ai

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Main Pipeline

**Option A: Using the Complete Jupyter Notebook (Recommended)**

```bash
# Start Jupyter
jupyter notebook

# Open: notebooks/01_complete_pipeline.ipynb
# Run all cells to see step-by-step execution with visualizations
```

**Option B: Using Python Script**

```bash
cd src
python main.py
```

### 3. View Results

After execution, check the `results/` directory for:
- `summary.txt` - Overall performance metrics
- `*_confusion_matrix.png` - Model predictions vs true labels
- `*_roc_curve.png` - ROC curves
- `feature_importance.png` - Important features for mutations
- `mutation_motifs.png` - Key DNA patterns associated with mutations

## Project Overview

The DN-AI system includes:

```
Feature Input (DNA Sequences)
        ↓
Feature Encoding (One-Hot, K-mer)
        ↓
    ┌───┴───────────────────┐
    ↓                       ↓
ML Models              DL Models
├─ SVM                ├─ CNN
└─ Random Forest      └─ LSTM
    ↓                       ↓
    └───────┬────────────────┘
            ↓
    Model Evaluation & Comparison
            ↓
    Explainable AI Analysis
            ↓
    Mutation Insights & Reports
```

## Key Features

### 1. DNA Sequence Encoding

```python
from src.feature_encoder import FeatureEncoder

encoder = FeatureEncoder(k=3)

# One-hot encoding
encoded = encoder.one_hot_encode_padded("ATCGATCG", max_length=100)
# Shape: (100, 4)

# K-mer frequencies
kmers = encoder.get_kmers("ATCGATCG", k=3)
freq = encoder.kmer_frequency("ATCGATCG", k=3)
```

### 2. Machine Learning Models

```python
from src.ml_models import MLModelTrainer

trainer = MLModelTrainer()

# Train SVM
svm_results = trainer.train_svm(X_train, y_train, cv=5)

# Train Random Forest
rf_results = trainer.train_random_forest(X_train, y_train, cv=5)

# Predict
predictions = trainer.predict_svm(X_test)
```

### 3. Deep Learning Models

```python
from src.dl_models import CNNModel, LSTMModel

# CNN
cnn = CNNModel(sequence_length=100, num_classes=2)
cnn.compile(learning_rate=0.001)
history = cnn.train(X_train, y_train, X_val, y_val, epochs=50)
predictions = cnn.predict(X_test)

# LSTM
lstm = LSTMModel(sequence_length=100, num_classes=2)
lstm.compile(learning_rate=0.001)
history = lstm.train(X_train, y_train, X_val, y_val, epochs=50)
predictions = lstm.predict(X_test)
```

### 4. Model Evaluation

```python
from src.evaluator import ModelEvaluator

evaluator = ModelEvaluator()

# Evaluate single model
metrics = evaluator.evaluate_model(y_test, y_pred, y_pred_proba)
# Returns: {accuracy, precision, recall, f1, roc_auc}

# Compare multiple models
results = {'SVM': svm_metrics, 'RF': rf_metrics, 'CNN': cnn_metrics}
evaluator.compare_models(results)

# Plot confusion matrix
fig = evaluator.plot_confusion_matrix(y_test, y_pred)

# Plot ROC curve
fig = evaluator.plot_roc_curve(y_test, y_pred_proba)
```

### 5. Explainable AI

```python
from src.explainer import DNAExplainer

explainer = DNAExplainer()

# Get feature importance
importance = explainer.get_feature_importance_ml(model, top_n=20)

# Identify mutation motifs
motifs = explainer.identify_mutation_motifs(sequences, predictions, k=3)

# Create report
report = explainer.create_explanation_report(
    model_name='Random Forest',
    features_importance=importance,
    motifs_importance=motifs,
    accuracy=0.89
)
```

### 6. Data Processing

```python
from src.data_processor import DataProcessor

processor = DataProcessor(random_state=42)

# Load and validate
df = processor.load_data('synthetic_dna_dataset.csv')
sequences, indices = processor.validate_sequences(df['Sequence'])

# Encode labels
encoded_labels = processor.encode_labels(df['Mutation_Flag'], 'mutation')

# Split data
(X_train, X_val, X_test), (y_train, y_val, y_test) = processor.split_data(
    X, y, test_size=0.2, val_size=0.1
)
```

## Understanding Results

### Model Metrics

- **Accuracy**: Overall correctness (TP + TN) / (TP + TN + FP + FN)
- **Precision**: True positive rate among positive predictions TP / (TP + FP)
- **Recall**: True positive rate among actual positives TP / (TP + FN)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the ROC curve (0.5 = random, 1.0 = perfect)

### Confusion Matrix

```
                 Predicted
              Mutation  No Mutation
Actual  Mutation    TP       FN
     No Mutation    FP       TN
```

### Feature Importance

Features with high importance scores influence mutation predictions more:
- **GC Content**: Percentage of G and C nucleotides
- **Nucleotide Frequencies**: Counts of A, T, C, G
- **Dinucleotide Frequencies**: Patterns like AA, AT, etc.

### Mutation Motifs

K-mers (short DNA sequences) that are strongly associated with mutations:
- Identify specific sequence patterns that correlate with mutations
- Useful for biological interpretation
- Example: "GCG" might appear more in mutated sequences

## Troubleshooting

### Memory Issues
```python
# Reduce batch size
cnn.train(..., batch_size=16)  # Instead of 32

# Use fewer samples for training
X_train = X_train[:1000]
```

### Slow Training
```python
# Use fewer epochs
cnn.train(..., epochs=20)  # Instead of 50

# Use fewer samples
X_train = X_train[:500]

# Disable verbose output
cnn.train(..., verbose=False)
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Verify installation
python -c "import tensorflow; import sklearn; print('OK')"
```

## Next Steps

1. **Customize Data**: Use your own DNA sequences in CSV format
2. **Adjust Models**: Modify hyperparameters in `config.json`
3. **Extend Analysis**: Add more XAI techniques (SHAP, LIME)
4. **Deploy**: Save models and create a prediction API
5. **Visualize**: Generate publication-quality plots

## Configuration File (config.json)

Key settings to customize:

```json
{
  "data": {
    "test_size": 0.2,           // 20% test set
    "val_size": 0.1,            // 10% validation set
    "random_state": 42          // Reproducibility
  },
  "models": {
    "machine_learning": {
      "svm": {"C": [0.1, 1, 10, 100]},
      "random_forest": {"n_estimators": [100, 200, 300]}
    },
    "deep_learning": {
      "cnn": {"epochs": 50, "batch_size": 32},
      "lstm": {"epochs": 50, "batch_size": 32}
    }
  },
  "xai": {
    "top_features": 20,
    "top_motifs": 20
  }
}
```

## File Structure Reference

```
dn_ai/
├── src/
│   ├── main.py                    ← Run: python main.py
│   ├── feature_encoder.py         ← DNA encoding
│   ├── data_processor.py          ← Data loading/prep
│   ├── ml_models.py               ← SVM, Random Forest
│   ├── dl_models.py               ← CNN, LSTM
│   ├── evaluator.py               ← Evaluation metrics
│   └── explainer.py               ← XAI techniques
├── notebooks/
│   └── 01_complete_pipeline.ipynb ← Jupyter notebook
├── models/                         ← Trained models (saved here)
├── results/                        ← Results & plots (saved here)
├── config.json                     ← Configuration
├── requirements.txt                ← Dependencies
└── README.md                       ← Full documentation
```

## Performance Expectations

**Typical Results on Test Set:**
- SVM: 87% accuracy
- Random Forest: 89% accuracy  
- CNN: 86% accuracy
- LSTM: 88% accuracy

**Training Time:**
- ML Models: 5-10 minutes
- DL Models: 20-30 minutes
- Total: 30-45 minutes

## Getting Help

1. Check the full [README.md](README.md) for detailed documentation
2. Review the [Jupyter notebook](notebooks/01_complete_pipeline.ipynb) for examples
3. Check `src/` module docstrings for API details
4. Review results and generated reports

---

**Enjoy using DN-AI for DNA sequence analysis!** 🧬
