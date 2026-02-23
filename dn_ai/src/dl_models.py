"""
Deep Learning models for DNA sequence classification.
Implements CNN and LSTM models using Keras/TensorFlow.
"""

import numpy as np
from typing import Dict, Tuple, Any
import os

# Try to import TensorFlow (optional)
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models, callbacks
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    keras = None
    layers = None
    models = None
    callbacks = None


class CNNModel:
    """Convolutional Neural Network for DNA sequence classification."""
    
    def __init__(self, sequence_length: int = 100, num_classes: int = 2, random_state: int = 42):
        """
        Initialize CNN model.
        
        Args:
            sequence_length: Input sequence length
            num_classes: Number of output classes
            random_state: Random seed
        """
        if not TF_AVAILABLE:
            raise ImportError("TensorFlow is required for CNN models. Install with: pip install tensorflow")
        
        self.sequence_length = sequence_length
        self.num_classes = num_classes
        self.random_state = random_state
        self.model = None
        self.history = None
        
        tf.random.set_seed(random_state)
        np.random.seed(random_state)
    
    def build(self) -> models.Sequential:
        """
        Build CNN architecture.
        
        Returns:
            Keras Sequential model
        """
        self.model = models.Sequential([
            layers.Conv1D(32, 3, activation='relu', input_shape=(self.sequence_length, 4)),
            layers.BatchNormalization(),
            layers.Conv1D(64, 3, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(2),
            layers.Dropout(0.3),
            
            layers.Conv1D(128, 3, activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling1D(2),
            layers.Dropout(0.3),
            
            layers.Conv1D(64, 3, activation='relu'),
            layers.BatchNormalization(),
            layers.GlobalAveragePooling1D(),
            layers.Dropout(0.3),
            
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(self.num_classes, activation='softmax' if self.num_classes > 2 else 'sigmoid')
        ])
        
        return self.model
    
    def compile(self, optimizer: str = 'adam', learning_rate: float = 0.001):
        """
        Compile the model.
        
        Args:
            optimizer: Optimizer name
            learning_rate: Learning rate
        """
        if self.model is None:
            self.build()
        
        opt = keras.optimizers.Adam(learning_rate=learning_rate)
        loss = 'categorical_crossentropy' if self.num_classes > 2 else 'binary_crossentropy'
        
        self.model.compile(
            optimizer=opt,
            loss=loss,
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              epochs: int = 50, batch_size: int = 32, verbose: bool = True) -> Dict[str, Any]:
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Print training progress
            
        Returns:
            Training history and metrics
        """
        if self.model is None:
            self.compile()
        
        # Early stopping
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Reduce learning rate
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, reduce_lr],
            verbose=1 if verbose else 0
        )
        
        return {
            'history': self.history.history,
            'final_loss': self.history.history['loss'][-1],
            'final_val_loss': self.history.history['val_loss'][-1],
            'final_accuracy': self.history.history['accuracy'][-1],
            'final_val_accuracy': self.history.history['val_accuracy'][-1]
        }
    
    def predict(self, X_test: np.ndarray, return_proba: bool = True):
        """
        Make predictions.
        
        Args:
            X_test: Test features
            return_proba: Return probabilities
            
        Returns:
            Predictions or probabilities
        """
        predictions = self.model.predict(X_test, verbose=0)
        
        if not return_proba:
            if self.num_classes > 2:
                return np.argmax(predictions, axis=1)
            else:
                return (predictions > 0.5).astype(int).flatten()
        
        return predictions
    
    def save(self, filepath: str):
        """Save model."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
    
    def load(self, filepath: str):
        """Load model."""
        self.model = keras.models.load_model(filepath)


class LSTMModel:
    """Long Short-Term Memory network for DNA sequence classification."""
    
    def __init__(self, sequence_length: int = 100, num_classes: int = 2, random_state: int = 42):
        """
        Initialize LSTM model.
        
        Args:
            sequence_length: Input sequence length
            num_classes: Number of output classes
            random_state: Random seed
        """
        if not TF_AVAILABLE:
            raise ImportError("TensorFlow is required for LSTM models. Install with: pip install tensorflow")
        
        self.sequence_length = sequence_length
        self.num_classes = num_classes
        self.random_state = random_state
        self.model = None
        self.history = None
        
        tf.random.set_seed(random_state)
        np.random.seed(random_state)
    
    def build(self) -> models.Sequential:
        """
        Build LSTM architecture.
        
        Returns:
            Keras Sequential model
        """
        self.model = models.Sequential([
            layers.LSTM(128, return_sequences=True, input_shape=(self.sequence_length, 4)),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.LSTM(64, return_sequences=True),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.LSTM(32, return_sequences=False),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(self.num_classes, activation='softmax' if self.num_classes > 2 else 'sigmoid')
        ])
        
        return self.model
    
    def compile(self, optimizer: str = 'adam', learning_rate: float = 0.001):
        """
        Compile the model.
        
        Args:
            optimizer: Optimizer name
            learning_rate: Learning rate
        """
        if self.model is None:
            self.build()
        
        opt = keras.optimizers.Adam(learning_rate=learning_rate)
        loss = 'categorical_crossentropy' if self.num_classes > 2 else 'binary_crossentropy'
        
        self.model.compile(
            optimizer=opt,
            loss=loss,
            metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
        )
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              epochs: int = 50, batch_size: int = 32, verbose: bool = True) -> Dict[str, Any]:
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Batch size
            verbose: Print training progress
            
        Returns:
            Training history and metrics
        """
        if self.model is None:
            self.compile()
        
        # Early stopping
        early_stop = callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )
        
        # Reduce learning rate
        reduce_lr = callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6
        )
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stop, reduce_lr],
            verbose=1 if verbose else 0
        )
        
        return {
            'history': self.history.history,
            'final_loss': self.history.history['loss'][-1],
            'final_val_loss': self.history.history['val_loss'][-1],
            'final_accuracy': self.history.history['accuracy'][-1],
            'final_val_accuracy': self.history.history['val_accuracy'][-1]
        }
    
    def predict(self, X_test: np.ndarray, return_proba: bool = True):
        """
        Make predictions.
        
        Args:
            X_test: Test features
            return_proba: Return probabilities
            
        Returns:
            Predictions or probabilities
        """
        predictions = self.model.predict(X_test, verbose=0)
        
        if not return_proba:
            if self.num_classes > 2:
                return np.argmax(predictions, axis=1)
            else:
                return (predictions > 0.5).astype(int).flatten()
        
        return predictions
    
    def save(self, filepath: str):
        """Save model."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.model.save(filepath)
    
    def load(self, filepath: str):
        """Load model."""
        self.model = keras.models.load_model(filepath)
