#!/usr/bin/env python3
"""
Enhanced script to load cleaned data into MongoDB.
"""

import pandas as pd
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from config.mongodb_config import MONGODB_CONFIG, MONGODB_URI
except ImportError:
    logger.warning("Using default MongoDB config")
    MONGODB_CONFIG = {
        'host': 'localhost',
        'port': 27017,
        'database': 'crop_yield_db',
        'collections': {
            'yield_data': 'yield_data',
            'cleaned_data': 'cleaned_data',
            'predictions': 'predictions'
        }
    }
    MONGODB_URI = "mongodb://localhost:27017/"

def connect_to_mongodb():
    """Establish connection to MongoDB."""
    try:
        logger.info(f"Connecting to MongoDB at {MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}")
        client = MongoClient(
            MONGODB_CONFIG['host'],
            MONGODB_CONFIG['port'],
            serverSelectionTimeoutMS=5000
        )
        # Verify connection
        client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        return client
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        logger.error("Ensure MongoDB is running on localhost:27017")
        return None

def load_to_mongodb():
    """Load cleaned data into MongoDB with proper error handling."""
    try:
        client = connect_to_mongodb()
        if not client:
            return False
        
        db = client[MONGODB_CONFIG['database']]
        collection = db[MONGODB_CONFIG['collections']['cleaned_data']]
        
        # Find data files
        project_root = Path(__file__).parent.parent
        data_dir = project_root / 'data'
        
        # Look for cleaned data files
        cleaned_files = list(data_dir.glob('cleaned_*.csv')) or list(data_dir.glob('*.csv'))
        
        if not cleaned_files:
            logger.error("No data files found in data directory")
            return False
        
        total_inserted = 0
        for data_file in cleaned_files:
            logger.info(f"Loading data from {data_file.name}...")
            try:
                df = pd.read_csv(data_file)
                
                # Drop rows with missing critical values
                df = df.dropna(subset=['yield'] if 'yield' in df.columns else [])
                
                if df.empty:
                    logger.warning(f"No valid data in {data_file.name}")
                    continue
                
                # Convert to dictionary records
                data_dict = df.to_dict('records')
                
                # Insert data
                result = collection.insert_many(data_dict, ordered=False)
                inserted = len(result.inserted_ids)
                total_inserted += inserted
                logger.info(f"Inserted {inserted} records from {data_file.name}")
                
            except Exception as e:
                logger.error(f"Error loading {data_file.name}: {str(e)}")
                continue
        
        # Create indexes for better query performance
        try:
            collection.create_index([('crop', ASCENDING)])
            collection.create_index([('year', ASCENDING)])
            logger.info("Created database indexes")
        except Exception as e:
            logger.warning(f"Could not create indexes: {str(e)}")
        
        logger.info(f"Total records loaded to MongoDB: {total_inserted}")
        client.close()
        return total_inserted > 0
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False

def main():
    """Main execution function."""
    logger.info("Starting MongoDB data loading...")
    if load_to_mongodb():
        logger.info("Data successfully loaded to MongoDB!")
        return 0
    else:
        logger.error("Failed to load data to MongoDB")
        return 1

if __name__ == "__main__":
    sys.exit(main())