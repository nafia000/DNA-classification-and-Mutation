"""
Machine Learning models for DNA sequence classification.
Implements SVM and Random Forest models.
"""

from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, GridSearchCV
import numpy as np
import pickle
from typing import Dict, Tuple, Any
import os


class MLModels:  # Changed from MLModelTrainer to MLModels
    """Trains and evaluates machine learning models for DNA classification."""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize the ML model trainer.
        
        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.models = {}
        self.best_models = {}
    
    def train_svm(self, X_train: np.ndarray, y_train: np.ndarray,
                  cv: int = 5, verbose: bool = True) -> Dict[str, Any]:
        """
        Train SVM model with hyperparameter tuning.
        """
        if verbose:
            print("Training SVM model...")
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        param_grid = {
            'C': [0.1, 1, 10, 100],
            'kernel': ['rbf', 'poly'],
            'gamma': ['scale', 'auto']
        }
        
        svm = SVC(random_state=self.random_state, probability=True)
        grid_search = GridSearchCV(svm, param_grid, cv=cv, n_jobs=-1, verbose=1 if verbose else 0)
        grid_search.fit(X_train_scaled, y_train)
        
        best_model = grid_search.best_estimator_
        self.models['svm'] = best_model
        
        cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=cv)
        
        if verbose:
            print(f"SVM - Best params: {grid_search.best_params_}")
            print(f"SVM - CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return {
            'model': best_model,
            'scaler': self.scaler,
            'best_params': grid_search.best_params_,
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    def train_random_forest(self, X_train: np.ndarray, y_train: np.ndarray,
                            cv: int = 5, verbose: bool = True) -> Dict[str, Any]:
        """
        Train Random Forest model with hyperparameter tuning.
        """
        if verbose:
            print("Training Random Forest model...")
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        rf = RandomForestClassifier(random_state=self.random_state, n_jobs=-1)
        grid_search = GridSearchCV(rf, param_grid, cv=cv, n_jobs=-1, verbose=1 if verbose else 0)
        grid_search.fit(X_train, y_train)
        
        best_model = grid_search.best_estimator_
        self.models['random_forest'] = best_model
        
        cv_scores = cross_val_score(best_model, X_train, y_train, cv=cv)
        
        if verbose:
            print(f"RF - Best params: {grid_search.best_params_}")
            print(f"RF - CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return {
            'model': best_model,
            'best_params': grid_search.best_params_,
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
    
    def get_feature_importance(self, model_name: str = 'random_forest') -> np.ndarray:
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            return model.feature_importances_
        else:
            raise ValueError(f"Model {model_name} does not support feature importance")
    
    def save_model(self, model_name: str, filepath: str):
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(self.models[model_name], f)
    
    def load_model(self, model_name: str, filepath: str):
        with open(filepath, 'rb') as f:
            self.models[model_name] = pickle.load(f)
    
    def predict_svm(self, X_test: np.ndarray, return_proba: bool = False):
        if 'svm' not in self.models:
            raise ValueError("SVM model not trained yet")
        
        X_test_scaled = self.scaler.transform(X_test)
        
        if return_proba:
            return self.models['svm'].predict_proba(X_test_scaled)
        else:
            return self.models['svm'].predict(X_test_scaled)
    
    def predict_random_forest(self, X_test: np.ndarray, return_proba: bool = False):
        if 'random_forest' not in self.models:
            raise ValueError("Random Forest model not trained yet")
        
        if return_proba:
            return self.models['random_forest'].predict_proba(X_test)
        else:
            return self.models['random_forest'].predict(X_test)