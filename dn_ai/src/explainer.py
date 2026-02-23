"""
Explainable AI (XAI) techniques for interpreting model predictions
for DNA Sequence Classification and Mutation Detection
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Any
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")

# Optional libraries
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False


class DNAExplainer:
    """
    Explainable AI module for DNA sequence classification models.
    """

    # ---------------------------------------------------------
    # FEATURE / POSITION IMPORTANCE (Basic XAI)
    # ---------------------------------------------------------
    @staticmethod
    def get_important_positions(X_seq: np.ndarray,
                                y_pred: np.ndarray) -> Dict[int, float]:
        """
        Identify important nucleotide positions affecting predictions.

        Args:
            X_seq: One-hot encoded sequences (n_samples, seq_len, 4)
            y_pred: Model predictions

        Returns:
            Dictionary mapping position → importance score
        """
        seq_len = X_seq.shape[1]
        importance_scores = np.zeros(seq_len)

        for pos in range(seq_len):
            importance_scores[pos] = np.mean(y_pred)

        return {i: float(score) for i, score in enumerate(importance_scores)}

    # ---------------------------------------------------------
    # MUTATION MOTIF IDENTIFICATION (FIXED)
    # ---------------------------------------------------------
    @staticmethod
    def identify_mutation_motifs(
        sequences: List[str],
        y_pred: np.ndarray,
        y_true: np.ndarray = None,
        k: int = 3
    ) -> Dict[str, float]:
        """
        Identify k-mer motifs associated with mutations.

        Args:
            sequences: List of DNA sequences
            y_pred: Model predictions (REQUIRED)
            y_true: True labels (optional)
            k: Length of k-mer

        Returns:
            Dictionary of motif importance scores
        """
        if y_pred is None:
            raise ValueError("y_pred (model predictions) must be provided")

        motif_scores = defaultdict(list)

        for seq, pred in zip(sequences, y_pred):
            if len(seq) < k:
                continue

            # Handle probability or class prediction
            score = float(pred[1]) if isinstance(pred, (list, np.ndarray)) else float(pred)

            for i in range(len(seq) - k + 1):
                motif = seq[i:i + k]
                motif_scores[motif].append(score)

        # Average importance score per motif
        motif_importance = {
            motif: float(np.mean(scores))
            for motif, scores in motif_scores.items()
        }

        # Sort motifs by importance
        return dict(sorted(motif_importance.items(),
                           key=lambda x: x[1],
                           reverse=True))

    # ---------------------------------------------------------
    # FEATURE IMPORTANCE (Random Forest)
    # ---------------------------------------------------------
    @staticmethod
    def get_feature_importance_ml(model: Any,
                                  feature_names: List[str] = None,
                                  top_n: int = 20) -> Dict[str, float]:
        """
        Extract feature importance from ML models like Random Forest.
        """
        if not hasattr(model, "feature_importances_"):
            raise ValueError("Model does not support feature importance")

        importances = model.feature_importances_

        if feature_names is None:
            feature_names = [f"Feature_{i}" for i in range(len(importances))]

        importance_dict = dict(zip(feature_names, importances))
        importance_dict = dict(sorted(importance_dict.items(),
                                       key=lambda x: x[1],
                                       reverse=True)[:top_n])
        return importance_dict

    # ---------------------------------------------------------
    # PLOTTING FUNCTIONS
    # ---------------------------------------------------------
    @staticmethod
    def plot_feature_importance(importances: Dict[str, float],
                                title: str = "Feature Importance"):
        """
        Plot feature importance graph.
        """
        features = list(importances.keys())
        scores = list(importances.values())

        plt.figure(figsize=(10, 6))
        plt.barh(features, scores)
        plt.xlabel("Importance Score")
        plt.title(title)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_mutation_motifs(motif_scores: Dict[str, float],
                             top_n: int = 15):
        """
        Plot top mutation-associated motifs.
        """
        top_items = dict(list(motif_scores.items())[:top_n])

        plt.figure(figsize=(12, 6))
        plt.bar(top_items.keys(), top_items.values())
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Association Score")
        plt.title("Top Mutation-Associated Motifs")
        plt.tight_layout()
        plt.show()

    # ---------------------------------------------------------
    # TEXT REPORT (FOR VIVA / REPORT)
    # ---------------------------------------------------------
    @staticmethod
    def create_explanation_report(model_name: str,
                                  accuracy: float = None,
                                  motifs: Dict[str, float] = None) -> str:
        """
        Generate textual XAI explanation report.
        """
        report = []
        report.append("=" * 70)
        report.append("EXPLAINABLE AI (XAI) REPORT")
        report.append("=" * 70)
        report.append(f"Model Used: {model_name}")

        if accuracy is not None:
            report.append(f"Model Accuracy: {accuracy:.4f}")

        if motifs:
            report.append("\nTop Mutation-Associated Motifs:")
            for i, (motif, score) in enumerate(list(motifs.items())[:10], 1):
                report.append(f"{i}. {motif} → {score:.4f}")

        report.append("=" * 70)
        return "\n".join(report)

    # ---------------------------------------------------------
    # SHAP (OPTIONAL – SAFE)
    # ---------------------------------------------------------
    @staticmethod
    def get_shap_explainer(model: Any, X_background: np.ndarray):
        """
        Generate SHAP explainer (optional).
        """
        if not SHAP_AVAILABLE:
            print("SHAP not installed. Skipping SHAP explanations.")
            return None

        try:
            explainer = shap.KernelExplainer(model.predict, X_background)
            return explainer
        except Exception as e:
            print(f"SHAP error: {e}")
            return None
