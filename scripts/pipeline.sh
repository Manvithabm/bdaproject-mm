#!/bin/bash
# Master setup and execution script for the entire crop yield prediction pipeline

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=================================================="
echo "Crop Yield Prediction - Full Pipeline Execution"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing=0
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        missing=1
    fi
    
    if ! command -v hadoop &> /dev/null; then
        log_warn "Hadoop is not in PATH (required for MapReduce)"
    fi
    
    if ! command -v hive &> /dev/null; then
        log_warn "Hive is not in PATH (required for trend analysis)"
    fi
    
    if [ $missing -eq 1 ]; then
        log_error "Missing required tools. Please install them first."
        return 1
    fi
    
    return 0
}

# Step 1: Download data
download_data() {
    log_info "Step 1: Downloading dataset from Kaggle..."
    
    if [ -f "$PROJECT_ROOT/scripts/download_data.py" ]; then
        python3 "$PROJECT_ROOT/scripts/download_data.py"
        log_info "Dataset download completed"
    else
        log_error "download_data.py not found"
        return 1
    fi
}

# Step 2: Upload to HDFS
upload_to_hdfs() {
    log_info "Step 2: Uploading data to HDFS..."
    
    if [ -x "$PROJECT_ROOT/scripts/upload_to_hdfs.sh" ]; then
        bash "$PROJECT_ROOT/scripts/upload_to_hdfs.sh"
        log_info "Data upload to HDFS completed"
    else
        log_warn "upload_to_hdfs.sh not executable, skipping"
    fi
}

# Step 3: Run MapReduce
run_mapreduce() {
    log_info "Step 3: Running MapReduce data cleaning job..."
    
    if [ -x "$PROJECT_ROOT/scripts/run_mapreduce.sh" ]; then
        bash "$PROJECT_ROOT/scripts/run_mapreduce.sh"
        log_info "MapReduce job completed"
    else
        log_warn "run_mapreduce.sh not executable, skipping"
    fi
}

# Step 4: Run Hive queries
run_hive_queries() {
    log_info "Step 4: Running Hive trend analysis queries..."
    
    if [ -x "$PROJECT_ROOT/scripts/run_hive_queries.sh" ]; then
        bash "$PROJECT_ROOT/scripts/run_hive_queries.sh"
        log_info "Hive queries completed"
    else
        log_warn "run_hive_queries.sh not executable, skipping"
    fi
}

# Step 5: Load to MongoDB
load_to_mongodb() {
    log_info "Step 5: Loading data to MongoDB..."
    
    if [ -f "$PROJECT_ROOT/scripts/load_to_mongodb.py" ]; then
        python3 "$PROJECT_ROOT/scripts/load_to_mongodb.py"
        log_info "MongoDB data loading completed"
    else
        log_error "load_to_mongodb.py not found"
        return 1
    fi
}

# Step 6: Run Spark prediction
run_spark_prediction() {
    log_info "Step 6: Running Spark MLlib yield prediction..."
    
    if [ -f "$PROJECT_ROOT/src/yield_prediction.py" ]; then
        python3 "$PROJECT_ROOT/src/yield_prediction.py"
        log_info "Spark prediction completed"
    else
        log_error "yield_prediction.py not found"
        return 1
    fi
}

# Step 7: Web analytics
run_web_analytics() {
    log_info "Step 7: Performing web analytics on farming trends..."
    
    if [ -f "$PROJECT_ROOT/scripts/web_analytics.py" ]; then
        python3 "$PROJECT_ROOT/scripts/web_analytics.py"
        log_info "Web analytics completed"
    else
        log_error "web_analytics.py not found"
        return 1
    fi
}

# Main execution
main() {
    log_info "Starting pipeline execution..."
    
    if ! check_prerequisites; then
        log_error "Prerequisites check failed"
        return 1
    fi
    
    # Parse command line arguments
    STEPS=${1:-"all"}
    
    case $STEPS in
        all)
            download_data || log_warn "Failed to download data"
            upload_to_hdfs || log_warn "Failed to upload to HDFS"
            run_mapreduce || log_warn "Failed to run MapReduce"
            run_hive_queries || log_warn "Failed to run Hive queries"
            load_to_mongodb || log_warn "Failed to load to MongoDB"
            run_spark_prediction || log_warn "Failed to run Spark prediction"
            run_web_analytics || log_warn "Failed to run web analytics"
            ;;
        download)
            download_data
            ;;
        hdfs)
            upload_to_hdfs
            ;;
        mapreduce)
            run_mapreduce
            ;;
        hive)
            run_hive_queries
            ;;
        mongodb)
            load_to_mongodb
            ;;
        spark)
            run_spark_prediction
            ;;
        analytics)
            run_web_analytics
            ;;
        *)
            log_error "Unknown step: $STEPS"
            echo "Usage: $0 [all|download|hdfs|mapreduce|hive|mongodb|spark|analytics]"
            return 1
            ;;
    esac
    
    log_info "Pipeline execution completed!"
}

# Run main
main "$@"
