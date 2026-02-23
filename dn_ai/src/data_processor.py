"""
Data preprocessing and utilities for DNA sequence classification.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from typing import Tuple, Dict, List, Any
import os


class DataProcessor:
    """Process and prepare DNA sequence data for machine learning."""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize data processor.
        
        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.label_encoders = {}
        self.class_labels = {}
    
    def load_data(self, csv_path: str) -> pd.DataFrame:
        """
        Load DNA dataset from CSV.
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            Pandas DataFrame
        """
        df = pd.read_csv(csv_path)
        print(f"Loaded data: {df.shape[0]} samples, {df.shape[1]} features")
        return df
    
    def validate_sequences(self, sequences: List[str]) -> Tuple[List[str], List[int]]:
        """
        Validate DNA sequences and return valid ones with indices.
        
        Args:
            sequences: List of DNA sequences
            
        Returns:
            Tuple of (valid_sequences, valid_indices)
        """
        valid_sequences = []
        valid_indices = []
        valid_nucleotides = set('ATCG')
        
        for idx, seq in enumerate(sequences):
            if all(nuc in valid_nucleotides for nuc in seq.upper()):
                valid_sequences.append(seq.upper())
                valid_indices.append(idx)
        
        print(f"Valid sequences: {len(valid_sequences)}/{len(sequences)}")
        return valid_sequences, valid_indices
    
    def encode_labels(self, labels: List[str], label_name: str = None) -> np.ndarray:
        """
        Encode categorical labels to integers.
        
        Args:
            labels: List of label strings
            label_name: Name of the label column (for caching encoder)
            
        Returns:
            Encoded labels as numpy array
        """
        if label_name and label_name in self.label_encoders:
            encoder = self.label_encoders[label_name]
        else:
            encoder = LabelEncoder()
            encoder.fit(labels)
            if label_name:
                self.label_encoders[label_name] = encoder
        
        encoded = encoder.transform(labels)
        
        if label_name:
            self.class_labels[label_name] = encoder.classes_
        
        return encoded
    
    def decode_labels(self, encoded_labels: np.ndarray, label_name: str) -> List[str]:
        """
        Decode integer labels back to original strings.
        
        Args:
            encoded_labels: Encoded labels
            label_name: Name of the label column
            
        Returns:
            List of decoded label strings
        """
        if label_name not in self.label_encoders:
            raise ValueError(f"No encoder for {label_name}")
        
        encoder = self.label_encoders[label_name]
        return encoder.inverse_transform(encoded_labels).tolist()
    
    def split_data(self, X: np.ndarray, y: np.ndarray,
                   test_size: float = 0.2, val_size: float = 0.1) -> Tuple[
                   Tuple[np.ndarray, np.ndarray, np.ndarray],
                   Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Split data into train, validation, and test sets.
        
        Args:
            X: Features
            y: Labels
            test_size: Proportion for test set
            val_size: Proportion of training data for validation
            
        Returns:
            Tuple of ((X_train, X_val, X_test), (y_train, y_val, y_test))
        """
        # First split: train+val vs test
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.random_state, stratify=y
        )
        
        # Second split: train vs val
        val_ratio = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_ratio, 
            random_state=self.random_state, stratify=y_train_val
        )
        
        print(f"Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")
        
        return (X_train, X_val, X_test), (y_train, y_val, y_test)
    
    def get_class_distribution(self, y: np.ndarray, labels: List[str] = None) -> Dict[str, int]:
        """
        Get class distribution.
        
        Args:
            y: Labels
            labels: Label names (optional)
            
        Returns:
            Dictionary of class counts
        """
        unique, counts = np.unique(y, return_counts=True)
        
        if labels is None:
            return dict(zip(unique.astype(str), counts.tolist()))
        else:
            return dict(zip([labels[int(u)] for u in unique], counts.tolist()))
    
    def prepare_classification_data(self, df: pd.DataFrame,
                                   sequence_col: str = 'Sequence',
                                   label_col: str = 'Mutation_Flag',
                                   test_size: float = 0.2) -> Dict[str, Any]:
        """
        Prepare data for mutation classification task.
        
        Args:
            df: Input DataFrame
            sequence_col: Column name for sequences
            label_col: Column name for labels
            test_size: Test set proportion
            
        Returns:
            Dictionary with train/val/test data and metadata
        """
        # Validate sequences
        sequences, valid_indices = self.validate_sequences(df[sequence_col].tolist())
        df_valid = df.iloc[valid_indices].reset_index(drop=True)
        
        # Encode labels
        y = self.encode_labels(df_valid[label_col].tolist(), label_name=label_col)
        
        # Collect feature dictionary for feature encoding
        feature_dict = {}
        for col in ['GC_Content', 'AT_Content', 'Num_A', 'Num_T', 'Num_C', 'Num_G']:
            if col in df_valid.columns:
                feature_dict[col] = df_valid[col].tolist()
        
        return {
            'sequences': sequences,
            'labels': y,
            'class_labels': self.class_labels.get(label_col, np.unique(y)),
            'features': feature_dict,
            'original_df': df_valid
        }
    
    @staticmethod
    def get_one_hot_encoding_shape(max_length: int = 100) -> Tuple[int, int, int]:
        """
        Get shape for one-hot encoded sequences.
        
        Args:
            max_length: Maximum sequence length
            
        Returns:
            Tuple of (batch_size=None, sequence_length, num_nucleotides=4)
        """
        return (None, max_length, 4)


def create_data_splits(data_dict: Dict[str, Any],
                      feature_encoder: Any,
                      random_state: int = 42) -> Dict[str, Dict[str, np.ndarray]]:
    """
    Create data splits with encoded features for both ML and DL.
    
    Args:
        data_dict: Dictionary from prepare_classification_data
        feature_encoder: Feature encoder instance
        random_state: Random seed
        
    Returns:
        Dictionary with 'ml' and 'dl' keys containing split data
    """
    from feature_encoder import prepare_sequences_for_ml, prepare_sequences_for_dl
    
    X_ml = prepare_sequences_for_ml(data_dict['sequences'], data_dict['features'])
    X_dl = prepare_sequences_for_dl(data_dict['sequences'])
    y = data_dict['labels']
    
    processor = DataProcessor(random_state=random_state)
    
    # Split data
    (X_train_ml, X_val_ml, X_test_ml), (y_train, y_val, y_test) = processor.split_data(
        X_ml, y, test_size=0.2, val_size=0.1
    )
    
    (X_train_dl, X_val_dl, X_test_dl), _ = processor.split_data(
        X_dl, y, test_size=0.2, val_size=0.1
    )
    
    return {
        'ml': {
            'X_train': X_train_ml, 'X_val': X_val_ml, 'X_test': X_test_ml,
            'y_train': y_train, 'y_val': y_val, 'y_test': y_test
        },
        'dl': {
            'X_train': X_train_dl, 'X_val': X_val_dl, 'X_test': X_test_dl,
            'y_train': y_train, 'y_val': y_val, 'y_test': y_test
        }
    }
