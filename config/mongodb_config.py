"""
MongoDB Configuration for Crop Yield Prediction Project.
"""

MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'crop_yield_db',
    'collections': {
        'yield_data': 'yield_data',
        'cleaned_data': 'cleaned_data',
        'predictions': 'predictions',
        'farming_trends': 'farming_trends'
    }
}

# Connection string
MONGODB_URI = f"mongodb://{MONGODB_CONFIG['host']}:{MONGODB_CONFIG['port']}/"
