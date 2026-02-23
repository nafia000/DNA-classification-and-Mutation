"""
Evaluation metrics and model comparison utilities.
"""

import numpy as np
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                           f1_score, roc_auc_score, roc_curve, confusion_matrix,
                           classification_report, auc)
from typing import Dict, Tuple, Any
import matplotlib.pyplot as plt

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False


class Evaluator:
    def __init__(self):
        pass
    
    @staticmethod
    def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, 
                      y_pred_proba: np.ndarray = None,
                      average: str = 'weighted') -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities
            average: Averaging method for multi-class
            
        Returns:
            Dictionary of evaluation metrics
        """
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
            'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
            'f1': f1_score(y_true, y_pred, average=average, zero_division=0)
        }
        
        # ROC AUC for binary classification or one-vs-rest for multi-class
        try:
            if y_pred_proba is not None:
                if y_pred_proba.ndim == 1 or y_pred_proba.shape[1] == 1:
                    # Binary classification
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba)
                else:
                    # Multi-class
                    metrics['roc_auc'] = roc_auc_score(y_true, y_pred_proba, 
                                                      average='weighted', multi_class='ovr')
        except:
            metrics['roc_auc'] = np.nan
        
        return metrics
    
    @staticmethod
    def get_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """Get confusion matrix."""
        return confusion_matrix(y_true, y_pred)
    
    @staticmethod
    def get_classification_report(y_true: np.ndarray, y_pred: np.ndarray) -> str:
        """Get detailed classification report."""
        return classification_report(y_true, y_pred)
    
    @staticmethod
    def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, 
                             class_labels: np.ndarray = None,
                             title: str = "Confusion Matrix") -> plt.Figure:
        """
        Plot confusion matrix heatmap.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_labels: Class label names
            title: Plot title
            
        Returns:
            Matplotlib figure
        """
        cm = confusion_matrix(y_true, y_pred)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        if SEABORN_AVAILABLE:
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                       xticklabels=class_labels, yticklabels=class_labels)
        else:
            im = ax.imshow(cm, cmap='Blues')
            ax.set_xticks(range(len(class_labels)))
            ax.set_yticks(range(len(class_labels)))
            ax.set_xticklabels(class_labels)
            ax.set_yticklabels(class_labels)
            for i in range(cm.shape[0]):
                for j in range(cm.shape[1]):
                    text = ax.text(j, i, cm[i, j], ha="center", va="center", color="w")
        ax.set_xlabel('Predicted')
        ax.set_ylabel('True')
        ax.set_title(title)
        
        return fig
    
    @staticmethod
    def plot_roc_curve(y_true: np.ndarray, y_pred_proba: np.ndarray,
                       title: str = "ROC Curve") -> plt.Figure:
        """
        Plot ROC curve.
        
        Args:
            y_true: True labels (binary)
            y_pred_proba: Predicted probabilities
            title: Plot title
            
        Returns:
            Matplotlib figure
        """
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(title)
        ax.legend(loc="lower right")
        
        return fig
    
    @staticmethod
    def compare_models(results: Dict[str, Dict[str, float]]) -> None:
        """
        Compare multiple models and print results.
        
        Args:
            results: Dictionary of model names to metrics
        """
        print("\n" + "="*70)
        print("MODEL COMPARISON RESULTS")
        print("="*70)
        
        # Create comparison table
        metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        
        for metric in metrics:
            print(f"\n{metric.upper()}:")
            print("-" * 50)
            
            scores = []
            for model_name, model_metrics in results.items():
                if metric in model_metrics:
                    score = model_metrics[metric]
                    print(f"  {model_name:20} : {score:.4f}")
                    scores.append((model_name, score))
            
            if scores:
                best_model = max(scores, key=lambda x: x[1])
                print(f"\n  Best: {best_model[0]} ({best_model[1]:.4f})")
        
        print("\n" + "="*70)
    
    @staticmethod
    def plot_metrics_comparison(results: Dict[str, Dict[str, float]],
                               metrics: list = None) -> plt.Figure:
        """
        Plot comparison of metrics across models.
        
        Args:
            results: Dictionary of model names to metrics
            metrics: List of metrics to compare (default: all)
            
        Returns:
            Matplotlib figure
        """
        if metrics is None:
            metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        
        # Filter available metrics
        metrics = [m for m in metrics if all(m in results[model] for model in results)]
        
        fig, axes = plt.subplots(1, len(metrics), figsize=(15, 4))
        if len(metrics) == 1:
            axes = [axes]
        
        model_names = list(results.keys())
        
        for idx, metric in enumerate(metrics):
            values = [results[model].get(metric, 0) for model in model_names]
            
            axes[idx].bar(model_names, values, color='skyblue', edgecolor='navy')
            axes[idx].set_ylabel('Score')
            axes[idx].set_title(metric.upper())
            axes[idx].set_ylim([0, 1])
            axes[idx].grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for i, v in enumerate(values):
                axes[idx].text(i, v + 0.02, f'{v:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_training_history(history: Dict[str, list], 
                             metrics: list = None) -> plt.Figure:
        """
        Plot training history.
        
        Args:
            history: Training history dictionary from Keras
            metrics: List of metrics to plot
            
        Returns:
            Matplotlib figure
        """
        if metrics is None:
            metrics = ['loss', 'accuracy']
        
        fig, axes = plt.subplots(1, len(metrics), figsize=(15, 4))
        if len(metrics) == 1:
            axes = [axes]
        
        for idx, metric in enumerate(metrics):
            if metric in history and f'val_{metric}' in history:
                axes[idx].plot(history[metric], label='Train')
                axes[idx].plot(history[f'val_{metric}'], label='Validation')
                axes[idx].set_xlabel('Epoch')
                axes[idx].set_ylabel(metric.capitalize())
                axes[idx].set_title(f'Training {metric.capitalize()}')
                axes[idx].legend()
                axes[idx].grid(alpha=0.3)
        
        plt.tight_layout()
        return fig
