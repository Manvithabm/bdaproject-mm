"""
Main Application Configuration for Crop Yield Prediction Project.
"""

import os

# Project paths
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')
CONFIG_DIR = os.path.join(PROJECT_ROOT, 'config')

# Data paths
RAW_DATA = os.path.join(DATA_DIR, 'yield.csv')
CLEANED_DATA = os.path.join(DATA_DIR, 'cleaned_yield_data.csv')
PROCESSED_DATA = os.path.join(DATA_DIR, 'yield_df.csv')

# HDFS paths
HDFS_INPUT_PATH = '/crop_yield/input'
HDFS_CLEANED_PATH = '/crop_yield/cleaned'
HDFS_OUTPUT_PATH = '/crop_yield/output'

# Data processing config
DATA_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'missing_value_threshold': 0.5,  # Drop columns with >50% missing values
    'categorical_columns': ['crop', 'soil_type'],
    'numerical_columns': ['temperature', 'rainfall', 'year'],
    'target_column': 'yield'
}

# Model config
MODEL_CONFIG = {
    'models': {
        'linear_regression': {
            'max_iter': 100,
            'reg_param': 0.01,
            'elasticNetParam': 0.8
        },
        'random_forest': {
            'num_trees': 100,
            'max_depth': 10,
            'feature_subset_strategy': 'auto'
        },
        'gradient_boosting': {
            'num_iterations': 100,
            'step_size': 0.1,
            'max_depth': 5
        }
    },
    'cross_validation_folds': 5
}

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
