# DN-AI Interface Guide: Choose Your Way to Use DN-AI

## Overview: 3 Ways to Use DN-AI

The DN-AI DNA Sequence Classification System can be used in three different ways:

1. **🌐 Web UI (NEW!)** - Beautiful, interactive web interface with Streamlit
2. **📓 Jupyter Notebook** - Interactive notebook for learning and exploration
3. **💻 Command-Line Interface (CLI)** - Direct Python script execution

Choose the one that fits your needs best!

---

## 1. 🌐 Web User Interface (RECOMMENDED FOR MOST USERS)

### When to Use
✅ Want the easiest experience  
✅ Non-technical users  
✅ Want beautiful visualizations  
✅ Prefer clicking buttons over typing commands  
✅ Want a professional-looking interface  

### Advantages
- **Zero coding required** - Just click buttons
- **Auto-opening browser** - Launches automatically
- **Beautiful UI** - Professional charts and layouts
- **Mobile-friendly** - Works on tablets and phones
- **Fast interactions** - No cell execution delays
- **Session memory** - Remembers your progress

### Quick Start

**One-click launch:**
```powershell
cd "c:\Users\nafia\main project\dn_ai" ; python -m streamlit run app.py
```

Or double-click: `run_web_ui.bat`

**Browser opens automatically to:** `http://localhost:8501`

### Features Available
- 📊 Data Explorer (load & visualize dataset)
- 🔧 Model Training (extract features & train models)
- 📈 Results (performance metrics & visualizations)
- 🔍 XAI Analysis (feature importance & mutation motifs)
- 📝 About (system information)

### Typical Workflow (10-15 min)
1. Click "Load Data" in Data Explorer
2. Click "Extract Features" in Model Training
3. Click "Train Models"
4. Click "Evaluate Models"
5. View results in Results page
6. Click "Generate Explanations" in XAI Analysis

### System Requirements
- Python 3.8+
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Edge)

**👉 BEST FOR: First-time users, exploratory analysis, presentations**

---

## 2. 📓 Jupyter Notebook

### When to Use
✅ Want to learn step-by-step  
✅ Like interactive code cells  
✅ Want to modify code inline  
✅ Learning about DNA classification  
✅ Want detailed annotations  

### Advantages
- **Interactive learning** - See code and results together
- **Cell-by-cell execution** - Control workflow step by step
- **Code visibility** - See and modify code directly
- **Rich documentation** - Mix code with markdown explanations
- **Flexible** - Add your own cells for experiments

### Quick Start

**Install Jupyter (if not already installed):**
```powershell
pip install notebook -q
```

**Start Jupyter Notebook:**
```powershell
cd "c:\Users\nafia\main project\dn_ai" ; python -m notebook
```

**Then:**
1. Browser opens to `http://localhost:8888`
2. Click on `notebooks/01_complete_pipeline.ipynb`
3. Run cells with **Shift+Enter**

### Notebook Structure
```
Notebook: 01_complete_pipeline.ipynb
├─ Cell 1: Import Libraries
├─ Cell 2: Load DNA Dataset
├─ Cell 3: Explore Data Statistics
├─ Cell 4: Extract Features (One-hot, K-mer, Hand-crafted)
├─ Cell 5: Train SVM Model
├─ Cell 6: Train Random Forest Model
├─ Cell 7: Evaluate Models
├─ Cell 8: Generate Confusion Matrices
├─ Cell 9: Extract Feature Importance
└─ Cell 10: Identify Mutation Motifs
```

### Typical Workflow (15-20 min)
1. Run cells sequentially from top to bottom
2. Review output after each cell
3. Modify code in cells as desired
4. Add new cells for custom analysis

### System Requirements
- Python 3.8+
- Jupyter/IPython installed
- 2GB RAM minimum

**👉 BEST FOR: Learning, code experimentation, detailed analysis**

---

## 3. 💻 Command-Line Interface (CLI)

### When to Use
✅ Want fastest execution  
✅ Running automated scripts  
✅ Integration with other tools  
✅ Server/headless environments  
✅ Batch processing  

### Advantages
- **Fastest** - No UI overhead
- **Scriptable** - Easy to automate
- **Minimal dependencies** - Just core packages
- **Server-friendly** - No browser required
- **Detailed logging** - See everything happening

### Quick Start

```powershell
cd "c:\Users\nafia\main project\dn_ai"
python src/main.py
```

### Output Example
```
====================================
DN-AI: DNA Sequence Classification
====================================

[1/6] Loading dataset...
✓ Loaded 1000 sequences
  - Sequence length: 50-150 nucleotides
  - Classes: 2 (Wild Type, Mutant)

[2/6] Encoding sequences...
✓ One-hot encoded: shape (1000, 150, 4)
✓ K-mer features: shape (1000, 64)
✓ Hand-crafted features: shape (1000, 5)

[3/6] Training ML models...
✓ SVM training complete
✓ Random Forest training complete

[4/6] Evaluating models...
✓ SVM Accuracy: 52.67%, ROC-AUC: 52.49%
✓ RF Accuracy: 49.83%, ROC-AUC: 49.34%

[5/6] Extracting feature importance...
✓ 20 top features identified

[6/6] Identifying mutation motifs...
✓ 64 mutation motifs found

====================================
Pipeline completed successfully!
====================================
```

### Output Files Generated
```
results/
├─ confusion_matrix_svm.csv
├─ confusion_matrix_rf.csv
├─ feature_importance.csv
├─ metrics_summary.json
├─ model_evaluation.txt
└─ top_mutations.csv
```

### Typical Workflow (3-5 min)
```powershell
# Simply run:
python src/main.py

# Done! All steps executed automatically
```

### System Requirements
- Python 3.8+
- Core ML packages installed
- ~500MB disk space

### Customization
To customize, edit `src/main.py`:
```python
# Example: Change dataset path
processor = DataProcessor()
df = processor.load_data('path/to/your/data.csv')

# Example: Train only SVM
ml_models = MLModels()
svm = ml_models.train_svm(X, y)

# Example: Get specific metrics
evaluator = Evaluator()
metrics = evaluator.calculate_metrics(y_true, y_pred)
```

**👉 BEST FOR: Batch processing, automation, production pipelines**

---

## Comparison Table

| Feature | Web UI 🌐 | Jupyter 📓 | CLI 💻 |
|---------|----------|-----------|--------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Learning Curve** | Very Easy | Easy | Moderate |
| **Visualization** | Excellent | Good | Basic |
| **Interactivity** | High | Very High | None |
| **Speed** | Medium | Medium | Fast |
| **Code Editing** | No | Yes | Yes |
| **Coding Knowledge** | None | Basic | Moderate |
| **Setup Time** | 2 min | 3 min | 1 min |
| **Best For** | Exploration | Learning | Automation |
| **Mobile-Friendly** | Yes | Limited | No |
| **Browser Required** | Yes | Yes | No |
| **Installation** | `pip install streamlit` | `pip install notebook` | Already included |

---

## Installation & Setup Summary

### Prerequisite (Same for All)
```powershell
cd "c:\Users\nafia\main project\dn_ai"
pip install -r requirements.txt -q
```

### Web UI Setup
```powershell
pip install streamlit -q
python -m streamlit run app.py
```

### Jupyter Setup
```powershell
pip install notebook -q
python -m notebook
# Then open: notebooks/01_complete_pipeline.ipynb
```

### CLI Setup
```powershell
python src/main.py
# That's it!
```

---

## Quick Decision Guide

**Choose Web UI if:**
- You're new to DN-AI
- You want the simplest experience
- You prefer visual interfaces
- You're doing exploratory analysis
- You want to show results to others

**Choose Jupyter if:**
- You want to learn the code
- You like step-by-step execution
- You want to modify and experiment
- You need detailed explanations
- You're in an educational setting

**Choose CLI if:**
- You want the fastest results
- You're automating workflows
- You need scriptable processing
- You're in a server environment
- You prefer command-line tools

---

## Running All Three Simultaneously

You can run all three interfaces at the same time:

```powershell
# Terminal 1: Web UI
cd "c:\Users\nafia\main project\dn_ai" ; python -m streamlit run app.py

# Terminal 2: Jupyter Notebook
cd "c:\Users\nafia\main project\dn_ai" ; python -m notebook

# Terminal 3: CLI (run once and finish)
cd "c:\Users\nafia\main project\dn_ai" ; python src/main.py
```

Each runs independently on different ports:
- Web UI: `http://localhost:8501`
- Jupyter: `http://localhost:8888`
- CLI: Terminal output only

---

## Troubleshooting by Interface

### Web UI Issues
```powershell
# Port in use?
streamlit run app.py --server.port 8502

# Module not found?
pip install streamlit -q

# Slow performance?
# Close other applications and restart
```

### Jupyter Issues
```powershell
# Kernel not found?
pip install ipykernel -q

# Port in use?
jupyter notebook --port 9999

# Server won't start?
pip install notebook --upgrade -q
```

### CLI Issues
```powershell
# Import error?
pip install -r requirements.txt -q

# Dataset not found?
# Ensure synthetic_dna_dataset.csv is in parent directory

# Permission denied?
# Run PowerShell as Administrator
```

---

## Performance Comparison

| Operation | Web UI | Jupyter | CLI |
|-----------|--------|---------|-----|
| Load Data | 1-2 sec | <1 sec | <1 sec |
| Extract Features | 5-10 sec | 5-10 sec | 5-10 sec |
| Train Models | 30-60 sec | 30-60 sec | 30-60 sec |
| Evaluate | 2-5 sec | 2-5 sec | 2-5 sec |
| Total Time | 40-80 sec | 40-80 sec | 40-80 sec |

---

## Next Steps

1. **Choose your interface** based on the comparison above
2. **Follow the Quick Start** for your chosen interface
3. **Complete the workflow** from data loading to results
4. **Try another interface** later if curious

---

## File Locations

```
c:\Users\nafia\main project\dn_ai\
├─ app.py                          ← Web UI (Streamlit)
├─ notebooks\
│  └─ 01_complete_pipeline.ipynb   ← Jupyter Notebook
├─ src\
│  ├─ main.py                      ← CLI Pipeline
│  ├─ data_processor.py
│  ├─ feature_encoder.py
│  ├─ ml_models.py
│  ├─ evaluator.py
│  └─ explainer.py
├─ run_web_ui.bat                  ← Web UI Launcher (Windows)
├─ run_web_ui.ps1                  ← Web UI Launcher (PowerShell)
├─ STREAMLIT_UI_GUIDE.md           ← Web UI Documentation
├─ WEB_UI_QUICKSTART.md            ← Web UI Quick Start
└─ INTERFACE_GUIDE.md              ← This file
```

---

**Choose an interface and start exploring your DNA data! 🧬**

Need help? Check the specific guide:
- 🌐 Web UI: See `WEB_UI_QUICKSTART.md`
- 📓 Jupyter: See `QUICKSTART.md`
- 💻 CLI: See `README.md`
