# 🌐 DN-AI Web UI Launch Guide

## What's New

You now have a **professional web-based user interface** for the DN-AI project! No more Jupyter or command-line needed.

## Features

✅ **Beautiful Dashboard** - Modern, responsive web interface  
✅ **No Coding Required** - Point and click navigation  
✅ **Professional Charts** - High-quality visualizations  
✅ **Complete Pipeline** - Data loading → Training → Results → XAI  
✅ **Mobile-Friendly** - Works on tablets and phones  
✅ **Auto Browser Launch** - Opens automatically on startup  

## Launch Instructions

### Quickest Way (Recommended)

**Option 1: Double-click the launcher**
```
📁 c:\Users\nafia\main project\dn_ai\
└─ run_web_ui.bat  ← Double-click this!
```

**Option 2: PowerShell command**
```powershell
cd "c:\Users\nafia\main project\dn_ai" ; python -m streamlit run app.py
```

### What Happens
1. A command prompt/PowerShell window opens
2. You'll see: "You can now view your Streamlit app in your browser"
3. Your default browser automatically opens to: **http://localhost:8501**
4. The DN-AI Web UI loads with 6 interactive sections

## Navigation Guide

### Sidebar Menu (Left Side)
```
🏠 Home               ← Welcome & Quick Stats
📊 Data Explorer      ← Load & Explore DNA Dataset
🔧 Model Training     ← Train ML Models
📈 Results            ← View Performance Metrics
🔍 XAI Analysis       ← Understand Model Decisions
📝 About              ← Project Information
```

## Quick Workflow (10-15 minutes)

### 1. Data Explorer (2 min)
- Click: **"🔄 Load Data"**
- Review: Statistics, distributions, sample sequences

### 2. Model Training (8 min)
- Click: **"🔄 Extract Features"** (2-3 min)
- Click: **"🤖 Train Models"** (3-5 min)
- Click: **"📊 Evaluate Models"** (2-3 min)

### 3. Results (2 min)
- View: Accuracy metrics, confusion matrices, performance comparison

### 4. XAI Analysis (2 min)
- Click: **"🔍 Generate Explanations"**
- View: Feature importance, mutation motifs

## System Requirements

- **OS**: Windows 7+, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Browser**: Chrome, Firefox, Edge, or Safari (modern version)
- **Internet**: Not required (runs locally)

## What You'll See

### Data Explorer
```
📊 Dataset Overview
├─ Total Sequences: 1000+
├─ Average Sequence Length: 80-120
├─ Classes: 2 (Wild Type / Mutant)
└─ Visualizations
   ├─ Sequence Length Histogram
   ├─ Class Distribution Bar Chart
   └─ Sample Sequences Table
```

### Model Training
```
🔧 Three-Step Process
├─ Step 1: Extract Features
│  ├─ One-hot Encoding
│  ├─ K-mer Features
│  └─ Hand-crafted Features
├─ Step 2: Train Models
│  ├─ SVM Classifier
│  └─ Random Forest Classifier
└─ Step 3: Evaluate
   ├─ Metrics Calculation
   └─ Performance Assessment
```

### Results
```
📈 Performance Metrics
├─ Metrics Table
│  ├─ Accuracy
│  ├─ Precision
│  ├─ Recall
│  ├─ F1-Score
│  └─ ROC-AUC
├─ Accuracy Comparison Chart
└─ Confusion Matrices (SVM & Random Forest)
```

### XAI Analysis
```
🔍 Model Explainability
├─ Feature Importance Bar Chart
├─ Top 20 Features Table
├─ Mutation Motifs List
└─ Motif Count Statistics
```

## Troubleshooting

### Issue: "Port 8501 already in use"
```powershell
streamlit run app.py --server.port 8502
# Then visit: http://localhost:8502
```

### Issue: "Module not found" error
```powershell
pip install streamlit pandas numpy scikit-learn matplotlib seaborn -q
```

### Issue: Data not loading
```powershell
# Ensure file exists:
cd "c:\Users\nafia\main project"
dir synthetic_dna_dataset.csv

# If not found, check it's in the right location:
# c:\Users\nafia\main project\synthetic_dna_dataset.csv
```

### Issue: Browser doesn't open
```
Manually visit: http://localhost:8501
```

### Issue: Very slow performance
- Close other applications
- Restart the Streamlit app
- Use a faster browser (Chrome is recommended)
- Ensure dataset is present

## File Structure

```
c:\Users\nafia\main project\dn_ai\
├─ app.py                          ← 🌐 Web UI (Main File)
├─ run_web_ui.bat                  ← 🔘 Windows Launcher
├─ run_web_ui.ps1                  ← 🔘 PowerShell Launcher
├─ requirements.txt                ← 📦 Dependencies
├─ WEB_UI_QUICKSTART.md            ← 📖 Detailed Guide
├─ STREAMLIT_UI_GUIDE.md           ← 📖 Complete Documentation
├─ INTERFACE_GUIDE.md              ← 📖 Interface Comparison
├─ notebooks/
│  └─ 01_complete_pipeline.ipynb   ← 📓 Jupyter Notebook
├─ src/
│  ├─ main.py                      ← 💻 CLI Pipeline
│  ├─ data_processor.py
│  ├─ feature_encoder.py
│  ├─ ml_models.py
│  ├─ evaluator.py
│  └─ explainer.py
└─ data/
   └─ (model files and results)
```

## Performance Tips

⚡ **Fast Load**: First time is slower (installing dependencies)  
⚡ **Subsequent Runs**: Much faster (cached dependencies)  
⚡ **Model Training**: Takes 30-60 seconds (normal)  
⚡ **Use Chrome**: Fastest browser for Streamlit  
⚡ **Close Other Apps**: More resources available  

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **R** | Refresh current page |
| **C** | Clear cache |
| **K** | Open command palette |

## Available Options

### Three Ways to Run DN-AI

```
1. 🌐 WEB UI (This One!)
   ├─ Easiest to use
   ├─ Most beautiful interface
   ├─ Best for exploration
   └─ Recommended for most users
   └─ Command: python -m streamlit run app.py

2. 📓 JUPYTER NOTEBOOK
   ├─ Interactive learning
   ├─ Edit code inline
   ├─ See results step-by-step
   └─ Command: python -m notebook
   
3. 💻 COMMAND-LINE (CLI)
   ├─ Fastest execution
   ├─ Automated workflows
   ├─ Server-friendly
   └─ Command: python src/main.py
```

## What's Installed

```
✅ Streamlit 1.52.2       ← Web UI Framework
✅ Pandas 2.3.3           ← Data Processing
✅ NumPy 1.26.4           ← Numerical Computing
✅ scikit-learn 1.8.0     ← Machine Learning
✅ Matplotlib 3.10.8      ← Visualization
✅ Seaborn 0.13+          ← Statistical Visualization
✅ Plotly 5.0+            ← Interactive Charts
```

## Next Steps

1. **Launch the App**:
   ```powershell
   cd "c:\Users\nafia\main project\dn_ai" ; python -m streamlit run app.py
   ```

2. **Follow the Workflow**:
   - Load Data → Extract Features → Train Models → View Results → Explore XAI

3. **Explore Features**:
   - Try different data views
   - Review model comparisons
   - Understand feature importance

4. **Share Results**:
   - Take screenshots of charts
   - Export metrics from results page
   - Share with collaborators

## Advanced Usage

### Run on Different Port
```powershell
streamlit run app.py --server.port 9000
# Visit: http://localhost:9000
```

### Run on Network
```powershell
# Find your IP:
ipconfig | findstr "IPv4"

# Share: http://<YOUR_IP>:8501
```

### Run Without Browser Auto-open
```powershell
streamlit run app.py --logger.level=error
```

## Need Help?

Check these files:
- 📖 **WEB_UI_QUICKSTART.md** - Step-by-step guide
- 📖 **STREAMLIT_UI_GUIDE.md** - Comprehensive documentation
- 📖 **INTERFACE_GUIDE.md** - Comparison with other interfaces
- 📖 **README.md** - General project information

## Success Indicators

✅ Browser opens automatically  
✅ You see the DN-AI logo and title  
✅ Left sidebar shows 6 menu items  
✅ "Load Data" button is clickable  
✅ No red error messages  

If you see all these, the web UI is working correctly!

---

## Quick Reference

| Task | Command |
|------|---------|
| Launch Web UI | `python -m streamlit run app.py` |
| Launch Jupyter | `python -m notebook` |
| Run CLI Pipeline | `python src/main.py` |
| Stop Server | Press **Ctrl+C** in terminal |
| Clear Cache | Press **C** in web UI |
| Refresh Page | Press **R** in web UI |

---

**Ready to explore? Launch the Web UI now! 🚀🧬**

Simply run:
```powershell
cd "c:\Users\nafia\main project\dn_ai" ; python -m streamlit run app.py
```

Or double-click: `run_web_ui.bat`
