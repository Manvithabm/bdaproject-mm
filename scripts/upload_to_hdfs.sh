#!/bin/bash
# Script to upload data to HDFS

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$PROJECT_ROOT/data"

echo "=== Uploading Data to HDFS ==="
echo "Data Directory: $DATA_DIR"

# Check if data directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "ERROR: Data directory not found at $DATA_DIR"
    exit 1
fi

# Check if Hadoop is available
if ! command -v hdfs &> /dev/null; then
    echo "ERROR: Hadoop is not installed or not in PATH"
    exit 1
fi

# Create HDFS directories
echo "Creating HDFS directories..."
hdfs dfs -mkdir -p /crop_yield/input

# Upload CSV files
echo "Uploading CSV files to HDFS..."
for csv_file in "$DATA_DIR"/*.csv; do
    if [ -f "$csv_file" ]; then
        filename=$(basename "$csv_file")
        echo "Uploading $filename..."
        hdfs dfs -put -f "$csv_file" /crop_yield/input/
    fi
done

# Verify upload
echo ""
echo "Files uploaded to HDFS:"
hdfs dfs -ls /crop_yield/input/

echo ""
echo "Data upload to HDFS completed successfully!"