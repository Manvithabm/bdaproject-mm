#!/usr/bin/env python3
"""
Enhanced script to download and process the Crop Yield Prediction Dataset from Kaggle.
Falls back to sample data if Kaggle API is not available.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_paths():
    """Setup necessary directory paths."""
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir

def download_dataset(data_dir):
    """Download the Crop Yield Prediction Dataset from Kaggle."""
    try:
        logger.info("Initializing Kaggle API...")
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        dataset = 'samuelotiattakorah/crop-yield-prediction-dataset'
        logger.info(f"Downloading dataset: {dataset}")
        api.dataset_download_files(dataset, path=data_dir, unzip=True)
        logger.info("Dataset downloaded successfully!")
        return True
    except ImportError:
        logger.warning("Kaggle API not installed. Using sample data instead.")
        return False
    except Exception as e:
        logger.warning(f"Failed to download dataset: {str(e)}")
        logger.info("Using sample data instead.")
        return False

def create_sample_data(data_dir):
    """Create sample crop yield data for demonstration."""
    logger.info("Creating sample crop yield data...")
    
    np.random.seed(42)
    n_samples = 500
    
    crops = ['Wheat', 'Rice', 'Corn', 'Soybeans', 'Barley']
    soil_types = ['Clay', 'Loam', 'Sandy', 'Silty']
    
    data = {
        'crop': np.random.choice(crops, n_samples),
        'year': np.random.randint(2015, 2024, n_samples),
        'yield': np.random.uniform(1000, 5000, n_samples),
        'temperature': np.random.uniform(10, 35, n_samples),
        'rainfall': np.random.uniform(300, 1500, n_samples),
        'soil_type': np.random.choice(soil_types, n_samples)
    }
    
    df = pd.DataFrame(data)
    output_file = data_dir / 'yield.csv'
    df.to_csv(output_file, index=False)
    logger.info(f"Sample data created: {output_file}")
    logger.info(f"Shape: {df.shape}")
    
    return df

def process_dataset(data_dir):
    """Process and clean the downloaded dataset."""
    try:
        csv_files = list(data_dir.glob('*.csv'))
        if not csv_files:
            logger.warning("No CSV files found in data directory.")
            return False
        
        for csv_file in csv_files:
            if 'cleaned' in csv_file.name:
                continue
                
            logger.info(f"Processing file: {csv_file.name}")
            df = pd.read_csv(csv_file)
            
            # Display dataset info
            logger.info(f"Dataset shape: {df.shape}")
            logger.info(f"Columns: {df.columns.tolist()}")
            logger.info(f"Missing values:\n{df.isnull().sum()}")
            
            # Basic data quality checks
            logger.info("Performing basic data quality checks...")
            
            # Remove duplicate rows
            initial_rows = len(df)
            df = df.drop_duplicates()
            logger.info(f"Removed {initial_rows - len(df)} duplicate rows")
            
            # Handle missing values
            for col in df.columns:
                if df[col].dtype in ['float64', 'int64']:
                    missing_pct = (df[col].isnull().sum() / len(df)) * 100
                    if missing_pct > 0:
                        logger.info(f"Column '{col}' has {missing_pct:.2f}% missing values")
                        df[col].fillna(df[col].mean(), inplace=True)
            
            # Save cleaned data
            cleaned_file = data_dir / f"cleaned_{csv_file.name}"
            df.to_csv(cleaned_file, index=False)
            logger.info(f"Cleaned data saved to: {cleaned_file}")
        
        return True
    except Exception as e:
        logger.error(f"Error processing dataset: {str(e)}")
        return False

def main():
    """Main execution function."""
    logger.info("Starting data download and processing...")
    
    try:
        data_dir = setup_paths()
        logger.info(f"Data directory: {data_dir}")
        
        # Try to download from Kaggle
        if not download_dataset(data_dir):
            # Fall back to sample data
            create_sample_data(data_dir)
        
        # Process dataset
        logger.info("Processing dataset...")
        if process_dataset(data_dir):
            logger.info("Data download and processing completed successfully!")
            return 0
        else:
            logger.error("Failed to process data")
            return 1
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())