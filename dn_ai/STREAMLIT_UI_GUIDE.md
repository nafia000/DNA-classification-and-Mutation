# DN-AI Web UI Guide

## Overview

The DN-AI Web UI is a modern, interactive Streamlit application that provides a user-friendly interface to the DNA Sequence Classification system without requiring Jupyter Notebook.

## Features

### 🏠 Home Page
- Welcome and quick start guide
- Project statistics overview
- System status and readiness check

### 📊 Data Explorer
- Load the synthetic DNA dataset
- View sequence statistics and distributions
- Explore class balance and sequence length patterns
- Browse sample sequences

### 🔧 Model Training
- **Step 1: Extract Features**
  - One-hot encoding
  - K-mer feature extraction
  - Hand-crafted feature generation
  
- **Step 2: Train Models**
  - SVM with hyperparameter tuning
  - Random Forest classifier
  - Automatic model optimization

- **Step 3: Evaluate Models**
  - Performance metrics calculation
  - Model comparison

### 📈 Results
- Comprehensive performance metrics
- Accuracy comparison charts
- Confusion matrices for both models
- Detailed evaluation statistics

### 🔍 XAI Analysis
- Feature importance visualization
- Top 20 important features ranking
- Mutation motif identification
- Interpretable AI insights

### 📝 About
- Project overview and technology stack
- Model performance benchmarks
- Dataset information

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Internet connection (for first-time setup)

### Step-by-Step Setup

1. **Navigate to project directory:**
   ```powershell
   cd "c:\Users\nafia\main project\dn_ai"
   ```

2. **Install required packages:**
   ```powershell
   pip install streamlit -q
   ```
   
   Or install all requirements:
   ```powershell
   pip install -r requirements.txt -q
   ```

## Running the Web UI

### Method 1: Using PowerShell (Recommended)

```powershell
cd "c:\Users\nafia\main project\dn_ai" ; python -m streamlit run app.py
```

### Method 2: Direct Command

```powershell
streamlit run "c:\Users\nafia\main project\dn_ai\app.py"
```

### What Happens Next

1. Streamlit will start a local development server
2. Your default browser will automatically open to `http://localhost:8501`
3. You'll see the DN-AI web interface

## Usage Workflow

### Quick Start (5-10 minutes)

1. **Load Data** → Go to "📊 Data Explorer" → Click "🔄 Load Data"
2. **Extract Features** → Go to "🔧 Model Training" → Click "🔄 Extract Features"
3. **Train Models** → Click "🤖 Train Models" → Wait for completion
4. **View Results** → Go to "📈 Results" → See performance metrics
5. **Explore XAI** → Go to "🔍 XAI Analysis" → Click "🔍 Generate Explanations"

### Detailed Workflow

#### Step 1: Data Exploration
- Navigate to **📊 Data Explorer**
- Click **"🔄 Load Data"** to load the synthetic DNA dataset
- Review:
  - Total number of sequences (1000+)
  - Average sequence length
  - Class distribution (Wild Type vs Mutant)
  - Sequence length distribution histogram
  - Class balance bar chart

#### Step 2: Feature Extraction
- Go to **🔧 Model Training**
- Click **"🔄 Extract Features"**
- The system will:
  - Generate one-hot encoded features
  - Extract k-mer (3-gram) features
  - Create hand-crafted features (GC content, nucleotide frequencies, etc.)
- View feature dimensions in the output

#### Step 3: Model Training
- Click **"🤖 Train Models"**
- The system trains two models:
  - **SVM**: Support Vector Machine with hyperparameter tuning
  - **Random Forest**: Ensemble learning classifier
- Training uses 5-fold cross-validation

#### Step 4: Model Evaluation
- Click **"📊 Evaluate Models"**
- Automatic evaluation metrics calculation:
  - Accuracy
  - Precision
  - Recall
  - F1-Score
  - ROC-AUC
  - Confusion Matrices

#### Step 5: Explainable AI Analysis
- Go to **🔍 XAI Analysis**
- Click **"🔍 Generate Explanations"**
- View:
  - Top 20 important features from Random Forest
  - Feature importance bar chart
  - Identified mutation motifs (up to first 10 shown)
  - Total mutation motifs count

## Features in Detail

### Data Insights
- **Sequence Length Distribution**: Histogram showing the range of DNA sequence lengths
- **Class Distribution**: Bar chart showing the balance between Wild Type and Mutant samples
- **Sample Browser**: View actual DNA sequences and their labels

### Model Training Options
- **Feature Engineering**: Three complementary feature extraction methods:
  - One-hot encoding (position-specific representation)
  - K-mer frequencies (3-letter word frequencies)
  - Hand-crafted features (GC content, nucleotide ratios)

- **Model Selection**: Two state-of-the-art classifiers:
  - SVM with RBF kernel and grid search optimization
  - Random Forest with 100 trees

### Performance Evaluation
- **Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Visualizations**: 
  - Side-by-side confusion matrices
  - Accuracy comparison bar chart
  - Metric comparison table

### XAI Capabilities
- **Feature Importance**: Identify which features matter most
- **Mutation Motif Detection**: Discover DNA patterns associated with mutations
- **Interpretability**: Understand model decisions

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Make sure you're in the project directory and all dependencies are installed:
```powershell
pip install -r requirements.txt -q
```

### Issue: Port 8501 already in use
**Solution**: Run on a different port:
```powershell
streamlit run app.py --server.port 8502
```

### Issue: Browser doesn't open automatically
**Solution**: Manually open `http://localhost:8501` in your browser

### Issue: Data loading fails
**Solution**: Ensure `synthetic_dna_dataset.csv` exists in the project root directory:
```powershell
cd "c:\Users\nafia\main project"
dir *.csv
```

### Issue: Models training is slow
**Solution**: This is normal. Model training typically takes 30-60 seconds. Be patient and don't close the browser.

## Configuration

### Custom Port
```powershell
streamlit run app.py --server.port 8080
```

### Disable Browser Auto-open
```powershell
streamlit run app.py --browser.gatherUsageStats false
```

### Run in No-prompt Mode
```powershell
streamlit run app.py --logger.level=error
```

## Interface Overview

### Sidebar Navigation
Located on the left side, provides quick access to:
- 🏠 Home
- 📊 Data Explorer
- 🔧 Model Training
- 📈 Results
- 🔍 XAI Analysis
- 📝 About

### Color Scheme
- Blue (#1f77b4): Primary actions and metrics
- Orange (#ff7f0e): Secondary elements and highlights
- Green: Success messages
- Red: Error messages
- Gray: Background elements

## Advanced Usage

### Accessing Web UI from Another Computer
1. Find your computer's IP address:
   ```powershell
   ipconfig | Select-String "IPv4"
   ```

2. Share the URL with others: `http://<YOUR_IP>:8501`

3. Make sure Streamlit is accessible (may require firewall adjustment)

## System Requirements

- **Minimum RAM**: 2GB
- **CPU**: Dual-core processor
- **Storage**: 500MB free space
- **Network**: Not required (runs locally)

## Performance Tips

1. **First Run**: May be slower due to initial model training
2. **Subsequent Runs**: Use cached data if available
3. **Large Features**: Combined features may take 1-2 minutes to generate
4. **Model Training**: SVM training might take 30-60 seconds

## Keyboard Shortcuts

- **R**: Rerun the current page
- **C**: Clear cache
- **K**: Open command palette
- **I**: Show info panel

## Comparison: CLI vs Jupyter vs Web UI

| Feature | CLI | Jupyter | Web UI |
|---------|-----|---------|--------|
| Ease of Use | Moderate | Easy | Very Easy |
| Visualization | Terminal | Interactive | Interactive |
| Code Editing | Requires Editor | Inline | Not Needed |
| Learning Curve | Moderate | Low | Very Low |
| Interactivity | Low | High | High |
| Browser Access | No | Yes | Yes |
| Best For | Scripts | Learning | Exploration |

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the About page in the UI for system info
3. Check the terminal output for error messages
4. Ensure all dependencies are properly installed

## Next Steps

After running the web UI:
1. Explore the Data Explorer to understand your dataset
2. Train models with different feature combinations
3. Compare model performances
4. Use XAI Analysis to interpret results
5. Experiment with hyperparameters (if needed)

---

**Happy DNA Analyzing! 🧬**
