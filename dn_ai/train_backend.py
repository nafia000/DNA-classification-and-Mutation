# filepath: c:\Users\nafia\main project\dn_ai\train_backend.py
"""
Backend model training script for DN-AI
Trains models, evaluates performance, and saves results
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pickle
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_processor import DataProcessor
from feature_encoder import FeatureEncoder
from ml_models import MLModels
from evaluator import Evaluator

def load_data(csv_path):
    """Load DNA dataset"""
    print(f"📂 Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded {len(df)} sequences")
    return df

def extract_features(df):
    """Extract features from DNA sequences"""
    print("\n🔬 Extracting features...")
    encoder = FeatureEncoder()
    
    # K-mer features
    print("  📊 Extracting k-mer features...")
    kmer_features = np.array([
        encoder.kmer_frequency_vector(seq, k=3) for seq in df['Sequence'].values
    ])
    print(f"    ✓ K-mer shape: {kmer_features.shape}")
    
    # Hand-crafted features from existing dataset columns
    print("  📊 Extracting hand-crafted features...")
    hand_crafted_cols = ['GC_Content', 'AT_Content', 'Num_A', 'Num_T', 'Num_C', 'Num_G']
    hand_crafted = df[hand_crafted_cols].values.astype(np.float32)
    print(f"    ✓ Hand-crafted shape: {hand_crafted.shape}")
    
    # Combine features
    X_combined = np.hstack([
        kmer_features.astype(np.float32),
        hand_crafted.astype(np.float32)
    ])
    print(f"✅ Combined features shape: {X_combined.shape}")
    
    return X_combined, encoder

def prepare_labels(df):
    """Prepare labels for training"""
    print("\n📋 Preparing labels...")
    unique_labels = df['Class_Label'].unique()
    label_mapping = {label: idx for idx, label in enumerate(unique_labels)}
    y = np.array([label_mapping[label] for label in df['Class_Label'].values])
    
    print(f"  Classes: {dict(label_mapping)}")
    print(f"  Label distribution:\n{df['Class_Label'].value_counts()}")
    
    return y, label_mapping

def train_models(X, y):
    """Train ML models"""
    print("\n🤖 Training models...")
    ml_models = MLModels()
    
    # Train SVM
    print("  🎯 Training SVM...")
    svm_result = ml_models.train_svm(X, y)
    print("    ✓ SVM trained")
    
    # Train Random Forest
    print("  🎯 Training Random Forest...")
    rf_result = ml_models.train_random_forest(X, y)
    print("    ✓ Random Forest trained")
    
    print("✅ Models trained successfully")
    
    return {'svm': svm_result, 'rf': rf_result}

def evaluate_models(models, X, y):
    """Evaluate model performance"""
    print("\n📊 Evaluating models...")
    evaluator = Evaluator()
    
    results = {}
    predictions = {}
    
    # Evaluate SVM
    print("  📈 Evaluating SVM...")
    svm_model = models['svm']['model']
    svm_scaler = models['svm']['scaler']
    X_scaled_svm = svm_scaler.transform(X)
    svm_pred = svm_model.predict(X_scaled_svm)
    svm_metrics = evaluator.evaluate_model(y, svm_pred)
    results['SVM'] = svm_metrics
    predictions['svm'] = svm_pred
    print(f"    ✓ Accuracy: {svm_metrics['accuracy']:.4f}")
    
    # Evaluate Random Forest
    print("  📈 Evaluating Random Forest...")
    rf_model = models['rf']['model']
    rf_pred = rf_model.predict(X)
    rf_metrics = evaluator.evaluate_model(y, rf_pred)
    results['Random Forest'] = rf_metrics
    predictions['rf'] = rf_pred
    print(f"    ✓ Accuracy: {rf_metrics['accuracy']:.4f}")
    
    print("✅ Evaluation complete")
    
    return results, predictions

def save_models(models, output_dir='models'):
    """Save trained models"""
    print(f"\n💾 Saving models to {output_dir}/...")
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save SVM
    svm_path = output_path / 'svm_model.pkl'
    with open(svm_path, 'wb') as f:
        pickle.dump(models['svm']['model'], f)
    print(f"  ✓ Saved: {svm_path}")
    
    # Save SVM Scaler
    svm_scaler_path = output_path / 'svm_scaler.pkl'
    with open(svm_scaler_path, 'wb') as f:
        pickle.dump(models['svm']['scaler'], f)
    print(f"  ✓ Saved: {svm_scaler_path}")
    
    # Save Random Forest
    rf_path = output_path / 'rf_model.pkl'
    with open(rf_path, 'wb') as f:
        pickle.dump(models['rf']['model'], f)
    print(f"  ✓ Saved: {rf_path}")
    
    print("✅ Models saved")

def save_results(results, predictions, output_dir='results'):
    """Save evaluation results and predictions"""
    print(f"\n📄 Saving results to {output_dir}/...")
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save as JSON
    results_json = {}
    for model_name, metrics in results.items():
        results_json[model_name] = {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                                     for k, v in metrics.items()}
    
    results_file = output_path / 'model_results.json'
    with open(results_file, 'w') as f:
        json.dump(results_json, f, indent=2)
    print(f"  ✓ Saved: {results_file}")
    
    # Save predictions as pickle
    predictions_file = output_path / 'predictions.pkl'
    with open(predictions_file, 'wb') as f:
        pickle.dump(predictions, f)
    print(f"  ✓ Saved: {predictions_file}")
    
    # Save text summary
    summary_file = output_path / 'summary.txt'
    with open(summary_file, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("DN-AI Model Training Summary\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        for model_name, metrics in results.items():
            f.write(f"\n{model_name}:\n")
            f.write("-" * 40 + "\n")
            for metric_name, value in metrics.items():
                if isinstance(value, float):
                    f.write(f"  {metric_name}: {value:.4f}\n")
                else:
                    f.write(f"  {metric_name}: {value}\n")
    
    print(f"  ✓ Saved: {summary_file}")
    print("✅ Results saved")

def main():
    """Main training pipeline"""
    print("=" * 60)
    print("🧬 DN-AI Backend Model Training")
    print("=" * 60)
    
    # Load data
    csv_path = Path(__file__).parent / "synthetic_dna_dataset.csv"
    df = load_data(csv_path)
    
    # Extract features
    X, encoder = extract_features(df)
    
    # Prepare labels
    y, label_mapping = prepare_labels(df)
    
    # Train models
    models = train_models(X, y)
    
    # Evaluate models
    results, predictions = evaluate_models(models, X, y)
    
    # Save models
    save_models(models)
    
    # Save results and predictions
    save_results(results, predictions)
    
    print("\n" + "=" * 60)
    print("✅ Training pipeline completed successfully!")
    print("=" * 60)
    print("\nResults Summary:")
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1-Score: {metrics['f1']:.4f}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)