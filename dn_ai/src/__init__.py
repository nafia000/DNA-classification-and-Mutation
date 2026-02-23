"""DN-AI: DNA Sequence Classification and Gene Mutation Detection"""

__version__ = "1.0.0"
__author__ = "DN-AI Team"

from .feature_encoder import FeatureEncoder, prepare_sequences_for_ml, prepare_sequences_for_dl
from .ml_models import MLModels
from .dl_models import CNNModel, LSTMModel
from .evaluator import Evaluator as ModelEvaluator
from .explainer import DNAExplainer
from .data_processor import DataProcessor, create_data_splits

__all__ = [
    'FeatureEncoder',
    'prepare_sequences_for_ml',
    'prepare_sequences_for_dl',
    'MLModelTrainer',
    'CNNModel',
    'LSTMModel',
    'ModelEvaluator',
    'DNAExplainer',
    'DataProcessor',
    'create_data_splits'
]
