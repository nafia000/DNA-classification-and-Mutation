"""
DN-AI Main Execution Script
Runs the complete DNA sequence classification and mutation detection pipeline.
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Setup paths
PROJECT_ROOT = Path(__file__).parent.parent
SRC_PATH = PROJECT_ROOT / 'src'
DATA_PATH = PROJECT_ROOT.parent / 'synthetic_dna_dataset.csv'
CONFIG_PATH = PROJECT_ROOT / 'config.json'

sys.path.insert(0, str(SRC_PATH))

# Import modules
from feature_encoder import FeatureEncoder, prepare_sequences_for_ml, prepare_sequences_for_dl
from data_processor import DataProcessor
from ml_models import MLModelTrainer
from dl_models import CNNModel, LSTMModel
from evaluator import ModelEvaluator
from explainer import DNAExplainer

# Try importing TensorFlow
try:
    from tensorflow.keras.utils import to_categorical
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("Warning: TensorFlow not available. Deep learning models will be skipped.")


def load_config(config_path):
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def print_header(text):
    """Print formatted section header."""
    print(f"\n{'='*70}")
    print(f"{text.center(70)}")
    print(f"{'='*70}\n")


def main():
    """Execute complete DN-AI pipeline."""
    
    print_header("DN-AI: DNA SEQUENCE CLASSIFICATION PIPELINE")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config(CONFIG_PATH)
    print(f"[OK] Configuration loaded from {CONFIG_PATH}\n")
    
    # 1. DATA LOADING AND EXPLORATION
    print_header("STEP 1: DATA LOADING & EXPLORATION")
    
    processor = DataProcessor(random_state=config['data']['random_state'])
    df = processor.load_data(str(DATA_PATH))
    print(f"[OK] Loaded {df.shape[0]} samples with {df.shape[1]} features")
    
    # 2. DATA PREPARATION
    print_header("STEP 2: DATA PREPARATION")
    
    data_dict = processor.prepare_classification_data(
        df,
        sequence_col=config['data']['sequence_column'],
        label_col=config['data']['label_column'],
        test_size=config['data']['test_size']
    )
    print(f"[OK] Prepared {len(data_dict['sequences'])} valid sequences")
    
    # 3. FEATURE ENCODING
    print_header("STEP 3: FEATURE ENCODING")
    
    print("Encoding sequences for ML models...")
    X_ml = prepare_sequences_for_ml(data_dict['sequences'], data_dict['features'])
    print(f"[OK] ML features shape: {X_ml.shape}")
    
    print("Encoding sequences for DL models...")
    X_dl = prepare_sequences_for_dl(
        data_dict['sequences'],
        max_length=config['feature_encoding']['max_sequence_length']
    )
    print(f"[OK] DL features shape: {X_dl.shape}")
    
    y = data_dict['labels']
    
    # 4. DATA SPLITTING
    print_header("STEP 4: DATA SPLITTING")
    
    (X_train_ml, X_val_ml, X_test_ml), (y_train, y_val, y_test) = processor.split_data(
        X_ml, y,
        test_size=config['data']['test_size'],
        val_size=config['data']['val_size']
    )
    
    (X_train_dl, X_val_dl, X_test_dl), _ = processor.split_data(
        X_dl, y,
        test_size=config['data']['test_size'],
        val_size=config['data']['val_size']
    )
    
    # Convert labels for DL
    if TF_AVAILABLE:
        y_train_cat = to_categorical(y_train)
        y_val_cat = to_categorical(y_val)
        y_test_cat = to_categorical(y_test)
    
    # 5. MACHINE LEARNING MODELS
    print_header("STEP 5: TRAINING MACHINE LEARNING MODELS")
    
    ml_trainer = MLModelTrainer(random_state=config['data']['random_state'])
    
    print("Training SVM...")
    svm_results = ml_trainer.train_svm(
        X_train_ml, y_train,
        cv=config['evaluation']['cross_validation'],
        verbose=True
    )
    print("[OK] SVM training complete")
    
    print("\nTraining Random Forest...")
    rf_results = ml_trainer.train_random_forest(
        X_train_ml, y_train,
        cv=config['evaluation']['cross_validation'],
        verbose=True
    )
    print("[OK] Random Forest training complete")
    
    # 6. ML PREDICTIONS AND EVALUATION
    print_header("STEP 6: ML MODEL EVALUATION")
    
    y_pred_svm = ml_trainer.predict_svm(X_test_ml)
    y_pred_svm_proba = ml_trainer.predict_svm(X_test_ml, return_proba=True)
    
    y_pred_rf = ml_trainer.predict_random_forest(X_test_ml)
    y_pred_rf_proba = ml_trainer.predict_random_forest(X_test_ml, return_proba=True)
    
    evaluator = ModelEvaluator()
    svm_metrics = evaluator.evaluate_model(y_test, y_pred_svm, y_pred_svm_proba[:, 1])
    rf_metrics = evaluator.evaluate_model(y_test, y_pred_rf, y_pred_rf_proba[:, 1])
    
    ml_results = {'SVM': svm_metrics, 'Random Forest': rf_metrics}
    evaluator.compare_models(ml_results)
    
    # 7. DEEP LEARNING MODELS (if TensorFlow available)
    if TF_AVAILABLE:
        print_header("STEP 7: TRAINING DEEP LEARNING MODELS")
        
        print("Building and training CNN...")
        cnn_model = CNNModel(
            sequence_length=config['feature_encoding']['max_sequence_length'],
            num_classes=2,
            random_state=config['data']['random_state']
        )
        cnn_model.compile(learning_rate=config['models']['deep_learning']['cnn']['learning_rate'])
        cnn_history = cnn_model.train(
            X_train_dl, y_train_cat,
            X_val_dl, y_val_cat,
            epochs=config['models']['deep_learning']['cnn']['epochs'],
            batch_size=config['models']['deep_learning']['cnn']['batch_size'],
            verbose=False
        )
        print("[OK] CNN training complete")
        
        print("\nBuilding and training LSTM...")
        lstm_model = LSTMModel(
            sequence_length=config['feature_encoding']['max_sequence_length'],
            num_classes=2,
            random_state=config['data']['random_state']
        )
        lstm_model.compile(learning_rate=config['models']['deep_learning']['lstm']['learning_rate'])
        lstm_history = lstm_model.train(
            X_train_dl, y_train_cat,
            X_val_dl, y_val_cat,
            epochs=config['models']['deep_learning']['lstm']['epochs'],
            batch_size=config['models']['deep_learning']['lstm']['batch_size'],
            verbose=False
        )
        print("[OK] LSTM training complete")
        
        # 8. DL PREDICTIONS AND EVALUATION
        print_header("STEP 8: DL MODEL EVALUATION")
        
        y_pred_cnn = cnn_model.predict(X_test_dl, return_proba=False)
        y_pred_cnn_proba = cnn_model.predict(X_test_dl, return_proba=True)
        
        y_pred_lstm = lstm_model.predict(X_test_dl, return_proba=False)
        y_pred_lstm_proba = lstm_model.predict(X_test_dl, return_proba=True)
        
        cnn_metrics = evaluator.evaluate_model(y_test, y_pred_cnn, y_pred_cnn_proba[:, 1])
        lstm_metrics = evaluator.evaluate_model(y_test, y_pred_lstm, y_pred_lstm_proba[:, 1])
        
        dl_results = {'CNN': cnn_metrics, 'LSTM': lstm_metrics}
        evaluator.compare_models(dl_results)
        
        all_results = {**ml_results, **dl_results}
    else:
        all_results = ml_results
    
    # 9. EXPLAINABLE AI
    print_header("STEP 9: EXPLAINABLE AI ANALYSIS")
    
    explainer = DNAExplainer()
    
    feature_names = [
        'Freq_A', 'Freq_T', 'Freq_C', 'Freq_G',
        'GC_Content', 'AT_Content',
        'AA', 'AT', 'AC', 'AG',
        'TA', 'TT', 'TC', 'TG',
        'CA', 'CT', 'CC', 'CG',
        'GA', 'GT', 'GC', 'GG'
    ]
    
    rf_feature_importance = explainer.get_feature_importance_ml(
        ml_trainer.models['random_forest'],
        feature_names=feature_names,
        top_n=config['xai']['top_features']
    )
    
    print(f"[OK] Extracted top {len(rf_feature_importance)} important features")
    
    motif_importance = explainer.identify_mutation_motifs(
        data_dict['sequences'],
        y_pred_rf_proba[:len(y_pred_rf_proba)],
        k=config['xai']['kmer_size_for_motifs']
    )
    
    print(f"[OK] Identified {len(motif_importance)} mutation-associated motifs")
    
    # 10. SUMMARY AND SAVE RESULTS
    print_header("STEP 10: RESULTS SUMMARY")
    
    summary = f"""
DN-AI EXECUTION SUMMARY
{'-'*70}
Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Dataset Statistics:
  Total Samples: {len(data_dict['sequences'])}
  Train: {X_train_ml.shape[0]}, Val: {X_val_ml.shape[0]}, Test: {X_test_ml.shape[0]}
  
Model Performance (Test Set):
"""
    
    for model_name, metrics in all_results.items():
        summary += f"\n  {model_name}:\n"
        summary += f"    Accuracy:  {metrics['accuracy']:.4f}\n"
        summary += f"    Precision: {metrics['precision']:.4f}\n"
        summary += f"    Recall:    {metrics['recall']:.4f}\n"
        summary += f"    F1-Score:  {metrics['f1']:.4f}\n"
        summary += f"    ROC-AUC:   {metrics['roc_auc']:.4f}\n"
    
    best_model = max(all_results.items(), key=lambda x: x[1]['accuracy'])
    summary += f"\nBest Model: {best_model[0]} (Accuracy: {best_model[1]['accuracy']:.4f})\n"
    
    print(summary)
    
    # Save results
    results_dir = PROJECT_ROOT / config['output']['results_dir']
    results_dir.mkdir(exist_ok=True)
    
    with open(results_dir / 'summary.txt', 'w') as f:
        f.write(summary)
    
    print(f"\n[OK] Results saved to {results_dir}")
    print("\n" + "="*70)
    print("DN-AI PIPELINE EXECUTION COMPLETE".center(70))
    print("="*70)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
