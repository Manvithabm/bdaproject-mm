#!/bin/bash
# Script to run Hive queries for crop yield trend analysis

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HIVE_SCRIPT="$PROJECT_ROOT/scripts/crop_trends.hql"

echo "=== Running Hive Trend Analysis Queries ==="
echo "Hive Script: $HIVE_SCRIPT"

# Check if Hive is available
if ! command -v hive &> /dev/null; then
    echo "ERROR: Hive is not installed or not in PATH"
    exit 1
fi

# Check if HQL script exists
if [ ! -f "$HIVE_SCRIPT" ]; then
    echo "ERROR: Hive script not found at $HIVE_SCRIPT"
    exit 1
fi

# Run Hive queries
echo "Executing Hive queries..."
hive -f "$HIVE_SCRIPT"

echo ""
echo "Hive queries executed successfully!"