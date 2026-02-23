"""
Feature encoding module for DNA sequences.
Implements one-hot encoding and k-mer based representation.
"""

import numpy as np
import pandas as pd
from collections import Counter
from typing import Tuple, List, Dict


class FeatureEncoder:
    """Encodes DNA sequences into numerical representations."""
    
    def __init__(self, k: int = 3):
        """
        Initialize the feature encoder.
        
        Args:
            k: K-mer size (default: 3)
        """
        self.k = k
        self.nucleotides = ['A', 'T', 'C', 'G']
        self.nucleotide_to_index = {nuc: i for i, nuc in enumerate(self.nucleotides)}
    
    def one_hot_encode(self, sequence: str) -> np.ndarray:
        """
        Perform one-hot encoding on a DNA sequence.
        
        Args:
            sequence: DNA sequence string
            
        Returns:
            One-hot encoded array of shape (sequence_length, 4)
        """
        encoded = np.zeros((len(sequence), 4), dtype=np.float32)
        for i, nuc in enumerate(sequence):
            if nuc in self.nucleotide_to_index:
                encoded[i, self.nucleotide_to_index[nuc]] = 1
        return encoded
    
    def one_hot_encode_padded(self, sequence: str, max_length: int = 100) -> np.ndarray:
        """
        Perform one-hot encoding with padding to fixed length.
        
        Args:
            sequence: DNA sequence string
            max_length: Maximum sequence length (default: 100)
            
        Returns:
            Padded one-hot encoded array of shape (max_length, 4)
        """
        encoded = self.one_hot_encode(sequence)
        
        if len(sequence) < max_length:
            # Pad with zeros
            padded = np.zeros((max_length, 4), dtype=np.float32)
            padded[:len(sequence)] = encoded
            return padded
        else:
            # Truncate if necessary
            return encoded[:max_length]
    
    def get_kmers(self, sequence: str, k: int = None) -> List[str]:
        """
        Extract k-mers from a DNA sequence.
        
        Args:
            sequence: DNA sequence string
            k: K-mer size (uses self.k if None)
            
        Returns:
            List of k-mers
        """
        if k is None:
            k = self.k
        kmers = []
        for i in range(len(sequence) - k + 1):
            kmers.append(sequence[i:i+k])
        return kmers
    
    def kmer_frequency(self, sequence: str, k: int = None) -> Dict[str, float]:
        """
        Calculate k-mer frequencies in a DNA sequence.
        
        Args:
            sequence: DNA sequence string
            k: K-mer size (uses self.k if None)
            
        Returns:
            Dictionary of k-mer frequencies
        """
        if k is None:
            k = self.k
        
        kmers = self.get_kmers(sequence, k)
        total = len(kmers)
        
        if total == 0:
            return {}
        
        counter = Counter(kmers)
        frequencies = {kmer: count / total for kmer, count in counter.items()}
        return frequencies
    
    def kmer_frequency_vector(self, sequence: str, k: int = None) -> np.ndarray:
        """
        Create a k-mer frequency vector for a sequence.
        
        Args:
            sequence: DNA sequence string
            k: K-mer size (uses self.k if None)
            
        Returns:
            Array of k-mer frequencies
        """
        if k is None:
            k = self.k
        
        freq_dict = self.kmer_frequency(sequence, k)
        # Generate all possible k-mers
        all_kmers = self._generate_all_kmers(k)
        
        vector = np.array([freq_dict.get(kmer, 0.0) for kmer in all_kmers], dtype=np.float32)
        return vector
    
    def _generate_all_kmers(self, k: int) -> List[str]:
        """Generate all possible k-mers."""
        if k == 1:
            return self.nucleotides
        else:
            prev_kmers = self._generate_all_kmers(k - 1)
            return [kmer + nuc for kmer in prev_kmers for nuc in self.nucleotides]
    
    def extract_features(self, sequence: str, 
                        gc_content: float = None,
                        at_content: float = None,
                        num_a: int = None,
                        num_t: int = None,
                        num_c: int = None,
                        num_g: int = None) -> np.ndarray:
        """
        Extract hand-crafted features from a DNA sequence.
        
        Args:
            sequence: DNA sequence string
            gc_content: GC content percentage (computed if None)
            at_content: AT content percentage (computed if None)
            num_a, num_t, num_c, num_g: Nucleotide counts (computed if None)
            
        Returns:
            Feature vector
        """
        features = []
        
        # Basic nucleotide counts
        if num_a is None:
            num_a = sequence.count('A')
        if num_t is None:
            num_t = sequence.count('T')
        if num_c is None:
            num_c = sequence.count('C')
        if num_g is None:
            num_g = sequence.count('G')
        
        seq_len = len(sequence)
        
        # Normalize counts
        features.extend([
            num_a / seq_len,
            num_t / seq_len,
            num_c / seq_len,
            num_g / seq_len
        ])
        
        # GC and AT content
        if gc_content is None:
            gc_content = (num_c + num_g) / seq_len * 100
        if at_content is None:
            at_content = (num_a + num_t) / seq_len * 100
        
        features.extend([gc_content, at_content])
        
        # Dinucleotide frequencies
        dinucleotides = self.kmer_frequency(sequence, k=2)
        all_dinucs = self._generate_all_kmers(2)
        features.extend([dinucleotides.get(dinuc, 0.0) for dinuc in all_dinucs])
        
        return np.array(features, dtype=np.float32)


def prepare_sequences_for_ml(sequences: List[str], 
                             features_dict: Dict[str, List] = None) -> np.ndarray:
    """
    Prepare sequences for traditional ML models using hand-crafted features.
    
    Args:
        sequences: List of DNA sequences
        features_dict: Dictionary with precomputed features
        
    Returns:
        Feature matrix of shape (n_samples, n_features)
    """
    encoder = FeatureEncoder(k=3)
    feature_vectors = []
    
    for i, seq in enumerate(sequences):
        if features_dict:
            features = encoder.extract_features(
                seq,
                gc_content=features_dict.get('GC_Content', [None])[i] if 'GC_Content' in features_dict else None,
                at_content=features_dict.get('AT_Content', [None])[i] if 'AT_Content' in features_dict else None,
                num_a=features_dict.get('Num_A', [None])[i] if 'Num_A' in features_dict else None,
                num_t=features_dict.get('Num_T', [None])[i] if 'Num_T' in features_dict else None,
                num_c=features_dict.get('Num_C', [None])[i] if 'Num_C' in features_dict else None,
                num_g=features_dict.get('Num_G', [None])[i] if 'Num_G' in features_dict else None,
            )
        else:
            features = encoder.extract_features(seq)
        
        feature_vectors.append(features)
    
    return np.array(feature_vectors, dtype=np.float32)


def prepare_sequences_for_dl(sequences: List[str], max_length: int = 100) -> np.ndarray:
    """
    Prepare sequences for deep learning models using one-hot encoding.
    
    Args:
        sequences: List of DNA sequences
        max_length: Maximum sequence length
        
    Returns:
        One-hot encoded sequences of shape (n_samples, max_length, 4)
    """
    encoder = FeatureEncoder()
    encoded_sequences = []
    
    for seq in sequences:
        encoded = encoder.one_hot_encode_padded(seq, max_length)
        encoded_sequences.append(encoded)
    
    return np.array(encoded_sequences, dtype=np.float32)
