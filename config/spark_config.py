"""
Spark Configuration for Crop Yield Prediction Project.
"""

SPARK_CONFIG = {
    'app_name': 'Crop Yield Prediction',
    'master': 'local[*]',  # Change to 'spark://master:7077' for cluster mode
    'executor_memory': '2g',
    'driver_memory': '1g',
    'executor_cores': 4,
    'partitions': 4,
    'log_level': 'WARN',
    'mongodb_connection': 'mongodb://localhost:27017/crop_yield_db'
}

# Spark session configuration
SPARK_SESSION_CONFIG = {
    'spark.sql.shuffle.partitions': SPARK_CONFIG['partitions'],
    'spark.executor.memory': SPARK_CONFIG['executor_memory'],
    'spark.driver.memory': SPARK_CONFIG['driver_memory'],
    'spark.executor.cores': str(SPARK_CONFIG['executor_cores']),
    'spark.sql.adaptive.enabled': 'true',
    'spark.sql.adaptive.coalescePartitions.enabled': 'true'
}
