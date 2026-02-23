"""
Model loader for pre-trained DN-AI models
"""

import pickle
from pathlib import Path
import numpy as np

class ModelLoader:
    """Load pre-trained models"""
    
    def __init__(self, model_dir='models'):
        self.model_dir = Path(model_dir)
    
    def load_svm_model(self):
        """Load pre-trained SVM model and scaler"""
        try:
            model_path = self.model_dir / 'svm_model.pkl'
            scaler_path = self.model_dir / 'svm_scaler.pkl'
            
            if not model_path.exists() or not scaler_path.exists():
                return None, None
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)
            
            return model, scaler
        except Exception as e:
            print(f"Error loading SVM model: {str(e)}")
            return None, None
    
    def load_rf_model(self):
        """Load pre-trained Random Forest model"""
        try:
            model_path = self.model_dir / 'rf_model.pkl'
            
            if not model_path.exists():
                return None
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            return model
        except Exception as e:
            print(f"Error loading RF model: {str(e)}")
            return None
    
    def load_all_models(self):
        """Load all pre-trained models"""
        svm_model, svm_scaler = self.load_svm_model()
        rf_model = self.load_rf_model()
        
        models_loaded = []
        if svm_model is not None and svm_scaler is not None:
            models_loaded.append('SVM')
        if rf_model is not None:
            models_loaded.append('Random Forest')
        
        return {
            'svm': {'model': svm_model, 'scaler': svm_scaler},
            'rf': {'model': rf_model}
        }, models_loaded
    
    def models_exist(self):
        """Check if pre-trained models exist"""
        svm_path = self.model_dir / 'svm_model.pkl'
        rf_path = self.model_dir / 'rf_model.pkl'
        
        return svm_path.exists() and rf_path.exists()
