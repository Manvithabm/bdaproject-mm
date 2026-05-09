#!/bin/bash
# Script to compile, package, and run MapReduce data cleaning job

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== MapReduce Data Cleaning Job ==="
echo "Project Root: $PROJECT_ROOT"

# Source Hadoop configuration
if [ -f "$PROJECT_ROOT/config/hadoop_config.sh" ]; then
    source "$PROJECT_ROOT/config/hadoop_config.sh"
fi

# Check if Hadoop is available
if ! command -v hadoop &> /dev/null; then
    echo "ERROR: Hadoop is not installed or not in PATH"
    exit 1
fi

# Create HDFS directories
echo "Creating HDFS directories..."
hdfs dfs -mkdir -p /crop_yield/input
hdfs dfs -mkdir -p /crop_yield/cleaned

# Upload input data
echo "Uploading data to HDFS..."
if [ -d "$PROJECT_ROOT/data" ]; then
    hdfs dfs -put -f "$PROJECT_ROOT/data"/*.csv /crop_yield/input/
    echo "Data uploaded successfully"
else
    echo "WARNING: Data directory not found at $PROJECT_ROOT/data"
fi

# Compile Java code
echo "Compiling DataCleaning.java..."
cd "$PROJECT_ROOT"
HADOOP_CLASSPATH=$(hadoop classpath)
javac -cp "$HADOOP_CLASSPATH" DataCleaning.java 2>/dev/null || {
    echo "Attempting compilation from src directory..."
    javac -cp "$HADOOP_CLASSPATH" src/DataCleaning.java
    cp src/DataCleaning*.class .
}

# Create JAR file
echo "Creating JAR file..."
jar cf DataCleaning.jar DataCleaning*.class

# Run MapReduce job
echo "Running MapReduce job..."
NUM_REDUCERS=${1:-4}
hadoop jar DataCleaning.jar DataCleaning /crop_yield/input /crop_yield/cleaned $NUM_REDUCERS

echo "MapReduce job completed!"
echo "Cleaned data available at: /crop_yield/cleaned/"

# List output
echo "Output files:"
hdfs dfs -ls /crop_yield/cleaned/