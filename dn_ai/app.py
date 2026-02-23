"""
Streamlit Web UI for DN-AI Project
DNA Sequence Classification & Gene Mutation Detection System
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# --------------------------------------------------
# Path setup
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR / "src"))

from data_processor import DataProcessor
from feature_encoder import FeatureEncoder
from ml_models import MLModels
from evaluator import Evaluator
from explainer import DNAExplainer
from model_loader import ModelLoader

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="DN-AI: DNA Sequence Classifier",
    page_icon="🧬",
    layout="wide"
)

# --------------------------------------------------
# Session State Initialization (FIXED)
# --------------------------------------------------
for key in [
    "df", "features", "models", "X", "y",
    "results", "predictions", "explanations",
    "user_dna", "user_result"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------
def load_data():
    processor = DataProcessor()
    csv_path = BASE_DIR / "synthetic_dna_dataset.csv"
    df = processor.load_data(str(csv_path))
    st.session_state.df = df
    return df


def extract_features(df):
    encoder = FeatureEncoder()

    kmer_features = np.array([
        encoder.kmer_frequency_vector(seq, k=3)
        for seq in df["Sequence"]
    ])

    hand_cols = ["GC_Content", "AT_Content", "Num_A", "Num_T", "Num_C", "Num_G"]
    hand_features = df[hand_cols].values.astype(np.float32)

    return {
        "kmer": kmer_features,
        "hand": hand_features
    }


def prepare_labels(df):
    labels = df["Class_Label"].unique()
    mapping = {l: i for i, l in enumerate(labels)}
    y = np.array([mapping[l] for l in df["Class_Label"]])
    return y


def evaluate_models(models, X, y):
    evaluator = Evaluator()
    results = {}

    svm = models["svm"]
    X_svm = svm["scaler"].transform(X)
    svm_pred = svm["model"].predict(X_svm)

    rf_pred = models["rf"]["model"].predict(X)

    results["SVM"] = evaluator.evaluate_model(y, svm_pred)
    results["Random Forest"] = evaluator.evaluate_model(y, rf_pred)

    return results, {"svm": svm_pred, "rf": rf_pred}


def explain_predictions():
    explainer = DNAExplainer()

    rf_model = st.session_state.models["rf"]["model"]
    feature_importance = explainer.get_feature_importance_ml(rf_model)

    df = st.session_state.df
    mutation_mask = df["Mutation_Flag"] == 1

    if mutation_mask.any():
        sequences = df.loc[mutation_mask, "Sequence"].tolist()
        y_pred = st.session_state.predictions["rf"][:len(sequences)]

        motifs = explainer.identify_mutation_motifs(
            sequences=sequences,
            y_pred=y_pred
        )
    else:
        motifs = {}

    return {
        "feature_importance": feature_importance,
        "motifs": motifs
    }

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("🧬 DN-AI: DNA Sequence Classification & Mutation Detection")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Data Explorer", "Model Training", "Results", "DNA Prediction", "XAI Analysis"]
)

# ---------------- HOME ----------------
if page == "Home":
    st.write("""
    *DN-AI* is a Machine Learning based system for  
    *DNA sequence classification and gene mutation detection*.

    ✔ Feature extraction (k-mer, GC content)  
    ✔ SVM & Random Forest models  
    ✔ Performance evaluation  
    ✔ Explainable AI (mutation motifs)
    """)

# ---------------- DATA EXPLORER ----------------
elif page == "Data Explorer":
    if st.button("📂 Load Dataset"):
        df = load_data()
        st.success(f"Loaded {len(df)} DNA sequences")

    if st.session_state.df is not None:
        st.dataframe(st.session_state.df.head())

# ---------------- MODEL TRAINING ----------------
elif page == "Model Training":
    if st.session_state.df is None:
        st.warning("Please load the dataset first")
    else:
        loader = ModelLoader()

        if loader.models_exist():
            if st.button("📥 Load Pre-trained Models"):
                models, _ = loader.load_all_models()
                st.session_state.models = models

                features = extract_features(st.session_state.df)
                X = np.hstack([features["kmer"], features["hand"]])
                y = prepare_labels(st.session_state.df)

                st.session_state.X = X
                st.session_state.y = y
                st.success("🎉 Pre-trained models loaded successfully!")

        if st.button("🔄 Train Models Again"):
            features = extract_features(st.session_state.df)
            X = np.hstack([features["kmer"], features["hand"]])
            y = prepare_labels(st.session_state.df)

            ml = MLModels()
            svm = ml.train_svm(X, y)
            rf = ml.train_random_forest(X, y)

            st.session_state.models = {"svm": svm, "rf": rf}
            st.session_state.X = X
            st.session_state.y = y
            st.success("🎉 Models trained successfully!")

        if st.session_state.models is not None:
            if st.button("📊 Evaluate Models"):
                results, preds = evaluate_models(
                    st.session_state.models,
                    st.session_state.X,
                    st.session_state.y
                )
                st.session_state.results = results
                st.session_state.predictions = preds
                st.success("✅ Model evaluation complete")

# ---------------- RESULTS ----------------
elif page == "Results":
    st.subheader("📊 Model Performance Metrics")

    if st.session_state.results is None:
        st.info("Run model evaluation first")
    else:
        results = st.session_state.results
        st.json(results)

        st.subheader("📈 Performance Metrics Comparison Graph")

        metrics = ["accuracy", "precision", "recall", "f1"]
        svm_scores = [results["SVM"][m] for m in metrics]
        rf_scores = [results["Random Forest"][m] for m in metrics]

        x = np.arange(len(metrics))
        width = 0.35

        fig, ax = plt.subplots()
        ax.bar(x - width/2, svm_scores, width, label="SVM")
        ax.bar(x + width/2, rf_scores, width, label="Random Forest")

        ax.set_xticks(x)
        ax.set_xticklabels(["Accuracy", "Precision", "Recall", "F1-score"])
        ax.set_ylim(0, 1.1)
        ax.set_title("Model Performance Comparison")
        ax.legend()

        st.pyplot(fig)

    st.divider()

    st.subheader("🧬 User DNA Mutation Result")

    if st.session_state.user_result is None:
        st.info("Please analyze a DNA sequence in DNA Prediction page first")
    else:
        st.code(st.session_state.user_dna)

        result = str(st.session_state.user_result).lower()

        if result in ["mutated", "abnormal", "1"]:
            st.error("🧬 This DNA sequence is MUTATED (Abnormal DNA Detected)")
        else:
            st.success("🧬 This DNA sequence is NORMAL (No Mutation Detected)")

# ---------------- DNA PREDICTION ----------------
elif page == "DNA Prediction":
    st.title("🧬 DNA Sequence Prediction")

    if st.session_state.models is None:
        st.warning("Please train or load models first")
    else:
        dna_input = st.text_area("Enter DNA Sequence (Only A, T, C, G allowed)", height=150)

        if st.button("🔍 Predict DNA"):
            if dna_input.strip() == "":
                st.warning("Please enter a DNA sequence.")
            elif not all(base in "ATCG" for base in dna_input.upper()):
                st.error("Invalid DNA sequence! Use only A, T, C, G.")
            else:
                dna_input = dna_input.upper()

                encoder = FeatureEncoder()
                kmer_feat = encoder.kmer_frequency_vector(dna_input, k=3).reshape(1, -1)

                gc = (dna_input.count("G") + dna_input.count("C")) / len(dna_input)
                at = (dna_input.count("A") + dna_input.count("T")) / len(dna_input)

                hand_feat = np.array([[gc, at,
                                       dna_input.count("A"),
                                       dna_input.count("T"),
                                       dna_input.count("C"),
                                       dna_input.count("G")]])

                X_new = np.hstack([kmer_feat, hand_feat])

                rf_model = st.session_state.models["rf"]["model"]
                prediction = rf_model.predict(X_new)[0]

                st.session_state.user_dna = dna_input
                st.session_state.user_result = prediction

                st.success(f"Predicted Class: {prediction}")

# ---------------- XAI ANALYSIS ----------------
elif page == "XAI Analysis":
    if st.session_state.predictions is None:
        st.warning("Train and evaluate models first")
    else:
        if st.button("🔍 Generate XAI Explanations"):
            st.session_state.explanations = explain_predictions()
            st.success("✅ XAI analysis completed")

        if st.session_state.explanations:
            st.subheader("Feature Importance (Random Forest)")
            st.write(st.session_state.explanations["feature_importance"])

            st.subheader("Top Mutation-Associated Motifs")
            motifs = list(st.session_state.explanations["motifs"].keys())[:10]
            st.write(motifs)
