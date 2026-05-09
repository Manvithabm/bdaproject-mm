#!/usr/bin/env python3
"""
Crop Yield Prediction using scikit-learn (compatible with Windows).
Implements multiple regression models and compares their performance.
"""

import sys
import logging
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class YieldPredictionModel:
    """Crop Yield Prediction using multiple scikit-learn models."""
    
    def __init__(self):
        self.models = {}
        self.evaluations = {}
        self.label_encoders = {}
    
    def load_data(self, data_path):
        """Load data from CSV file."""
        try:
            logger.info(f"Loading data from {data_path}")
            df = pd.read_csv(data_path)
            logger.info(f"Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
            logger.info(f"Columns: {df.columns.tolist()}")
            return df
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def preprocess_data(self, df):
        """Preprocess data: handle missing values, encode categorical variables."""
        try:
            logger.info("Preprocessing data...")
            
            df = df.copy()
            
            # Fill missing numerical values with mean
            numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            for col in numerical_cols:
                if df[col].isnull().any():
                    mean_val = df[col].mean()
                    df[col].fillna(mean_val, inplace=True)
            
            # Identify categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            # Remove 'yield' or similar target columns from categorical list
            categorical_cols = [c for c in categorical_cols if c.lower() != 'yield']
            
            # Encode categorical variables
            for col in categorical_cols:
                if col in df.columns:
                    le = LabelEncoder()
                    df[f"{col}_encoded"] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                    df = df.drop(columns=[col])
            
            logger.info("Data preprocessing completed")
            return df, numerical_cols, categorical_cols
        except Exception as e:
            logger.error(f"Error preprocessing data: {str(e)}")
            raise
    
    def prepare_features(self, df):
        """Prepare feature matrix and target variable."""
        try:
            logger.info("Preparing features...")
            
            # Find target column (yield)
            target_col = None
            for col in df.columns:
                if 'yield' in col.lower() or 'hg/ha' in col.lower() or 'value' in col.lower():
                    target_col = col
                    break
            
            if target_col is None:
                logger.warning("Target column not found, using last numerical column")
                target_col = df.select_dtypes(include=[np.number]).columns[-1]
            
            logger.info(f"Target column: {target_col}")
            
            # Remove non-numeric columns
            numeric_df = df.select_dtypes(include=[np.number])
            
            # Separate features and target
            X = numeric_df.drop(columns=[target_col], errors='ignore')
            y = numeric_df[target_col]
            
            logger.info(f"Feature matrix shape: {X.shape}")
            logger.info(f"Target shape: {y.shape}")
            
            return X, y
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise
    
    def train_models(self, X_train, y_train):
        """Train multiple regression models."""
        try:
            # Standardize features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            
            # Linear Regression
            logger.info("Training Linear Regression model...")
            self.models['LinearRegression'] = LinearRegression()
            self.models['LinearRegression'].fit(X_train_scaled, y_train)
            
            # Random Forest
            logger.info("Training Random Forest model...")
            self.models['RandomForest'] = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.models['RandomForest'].fit(X_train, y_train)
            
            # Gradient Boosting
            logger.info("Training Gradient Boosting model...")
            self.models['GradientBoosting'] = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            self.models['GradientBoosting'].fit(X_train, y_train)
            
            logger.info(f"Successfully trained {len(self.models)} models")
            return self.models, scaler
        except Exception as e:
            logger.error(f"Error training models: {str(e)}")
            raise
    
    def evaluate_models(self, X_test, y_test, scaler):
        """Evaluate all trained models."""
        try:
            X_test_scaled = scaler.transform(X_test)
            
            logger.info("Evaluating models on test data...")
            for model_name, model in self.models.items():
                
                # Use scaled features for LinearRegression, original for others
                if model_name == 'LinearRegression':
                    predictions = model.predict(X_test_scaled)
                else:
                    predictions = model.predict(X_test)
                
                rmse = np.sqrt(mean_squared_error(y_test, predictions))
                r2 = r2_score(y_test, predictions)
                
                self.evaluations[model_name] = {
                    'rmse': rmse,
                    'r2': r2,
                    'predictions': predictions
                }
                
                logger.info(f"{model_name}: RMSE={rmse:.4f}, R²={r2:.4f}")
            
            return self.evaluations
        except Exception as e:
            logger.error(f"Error evaluating models: {str(e)}")
            raise
    
    def save_best_model(self, models_dir, scaler):
        """Save the best performing model."""
        try:
            best_model_name = min(self.evaluations.items(), key=lambda x: x[1]['rmse'])[0]
            model_path = Path(models_dir) / f"best_yield_prediction_model_{best_model_name}.pkl"
            
            logger.info(f"Saving best model: {best_model_name} to {model_path}")
            joblib.dump(self.models[best_model_name], model_path)
            
            # Also save scaler
            scaler_path = Path(models_dir) / "scaler.pkl"
            joblib.dump(scaler, scaler_path)
            
            return str(model_path)
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

def main():
    """Main execution function."""
    logger.info("Starting Crop Yield Prediction with scikit-learn...")
    
    try:
        # Setup paths
        project_root = Path(__file__).parent.parent
        data_dir = project_root / 'data'
        models_dir = project_root / 'models'
        models_dir.mkdir(exist_ok=True)
        
        # Find data file
        data_files = list(data_dir.glob('cleaned_*.csv'))
        if not data_files:
            logger.error("No cleaned data files found")
            return 1
        
        # Try to use yield-related file
        data_path = None
        for f in data_files:
            if 'yield' in f.name.lower():
                data_path = f
                break
        
        if data_path is None:
            data_path = data_files[0]
        
        logger.info(f"Using data file: {data_path}")
        
        # Initialize model
        predictor = YieldPredictionModel()
        
        # Load and preprocess data
        df = predictor.load_data(data_path)
        df, numerical_cols, categorical_cols = predictor.preprocess_data(df)
        X, y = predictor.prepare_features(df)
        
        # Handle any remaining missing values
        X = X.fillna(X.mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logger.info(f"Training set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
        
        # Train and evaluate models
        models, scaler = predictor.train_models(X_train, y_train)
        predictor.evaluate_models(X_test, y_test, scaler)
        
        # Save best model
        model_path = predictor.save_best_model(models_dir, scaler)
        logger.info(f"Best model saved to: {model_path}")
        
        # Print summary
        logger.info("\n=== Model Evaluation Summary ===")
        for model_name, metrics in predictor.evaluations.items():
            logger.info(f"{model_name}: RMSE={metrics['rmse']:.4f}, R²={metrics['r2']:.4f}")
        
        logger.info("Crop Yield Prediction completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())