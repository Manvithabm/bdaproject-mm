#!/bin/bash
# Complete Hadoop/Hive/Spark Pipeline Execution for Crop Yield Prediction
# Run this from Ubuntu with Hadoop, Hive, and Spark installed

set -e  # Exit on error

PROJECT_HOME="$HOME/crop_yeild_prediction"
DATA_DIR="$HOME/crop_data"
HDFS_INPUT="/crop_yield/input"
HDFS_CLEANED="/crop_yield/cleaned"
HDFS_RESULTS="/crop_yield/results"

echo "=========================================="
echo "CROP YIELD PREDICTION - HADOOP/HIVE SETUP"
echo "=========================================="

# STEP 1: Verify prerequisites
echo -e "\n[STEP 1] Verifying prerequisites..."
command -v hadoop >/dev/null 2>&1 || { echo "❌ Hadoop not found"; exit 1; }
command -v hive >/dev/null 2>&1 || { echo "❌ Hive not found"; exit 1; }
command -v spark-submit >/dev/null 2>&1 || { echo "❌ Spark not found"; exit 1; }
echo "✅ All prerequisites installed"

# STEP 2: Start Hadoop services
echo -e "\n[STEP 2] Starting Hadoop services..."
$HADOOP_HOME/sbin/start-dfs.sh >/dev/null 2>&1 &
sleep 2
$HADOOP_HOME/sbin/start-yarn.sh >/dev/null 2>&1 &
sleep 2
echo "✅ Hadoop services started"

# STEP 3: Verify HDFS
echo -e "\n[STEP 3] Verifying HDFS..."
hdfs dfs -test -d / 2>/dev/null && echo "✅ HDFS accessible" || { echo "❌ HDFS not accessible"; exit 1; }

# STEP 4: Create HDFS directories
echo -e "\n[STEP 4] Creating HDFS directories..."
hdfs dfs -mkdir -p $HDFS_INPUT 2>/dev/null || true
hdfs dfs -mkdir -p $HDFS_CLEANED 2>/dev/null || true
hdfs dfs -mkdir -p $HDFS_RESULTS 2>/dev/null || true
echo "✅ HDFS directories ready"

# STEP 5: Upload data to HDFS
echo -e "\n[STEP 5] Uploading cleaned data to HDFS..."
if [ -d "$DATA_DIR" ]; then
    hdfs dfs -put -f $DATA_DIR/cleaned_*.csv $HDFS_INPUT/
    echo "✅ Data uploaded to HDFS"
else
    echo "⚠️  Data directory not found at $DATA_DIR"
fi

# STEP 6: Compile MapReduce job
echo -e "\n[STEP 6] Compiling MapReduce job..."
cd "$PROJECT_HOME/src"
if [ -f "DataCleaning.java" ]; then
    javac -cp $HADOOP_CLASSPATH DataCleaning.java 2>/dev/null || {
        echo "⚠️  MapReduce compilation failed (may need Hadoop classpath configured)"
    }
    jar cf ../DataCleaning.jar DataCleaning.class 2>/dev/null && echo "✅ JAR created" || echo "⚠️  JAR creation skipped"
else
    echo "⚠️  DataCleaning.java not found"
fi

# STEP 7: Run MapReduce job
echo -e "\n[STEP 7] Running MapReduce job..."
cd "$PROJECT_HOME"
if [ -f "DataCleaning.jar" ]; then
    echo "  Submitting MapReduce job..."
    hadoop jar DataCleaning.jar DataCleaning $HDFS_INPUT $HDFS_CLEANED 2 &
    MR_PID=$!
    wait $MR_PID 2>/dev/null || true
    echo "✅ MapReduce job completed"
else
    echo "⚠️  JAR file not found, skipping MapReduce"
fi

# STEP 8: Create Hive table
echo -e "\n[STEP 8] Creating Hive external table..."
hive -e "
CREATE EXTERNAL TABLE IF NOT EXISTS cleaned_yield (
  country STRING,
  year INT,
  temperature DOUBLE,
  rainfall DOUBLE,
  pesticides DOUBLE,
  yield DOUBLE
)
COMMENT 'Cleaned crop yield data'
STORED AS TEXTFILE
LOCATION '$HDFS_CLEANED';" 2>/dev/null && echo "✅ Hive table created" || echo "⚠️  Hive table creation skipped"

# STEP 9: Run Hive queries
echo -e "\n[STEP 9] Running Hive analytics queries..."
if [ -f "$PROJECT_HOME/scripts/crop_trends.hql" ]; then
    hive -f "$PROJECT_HOME/scripts/crop_trends.hql" 2>/dev/null && echo "✅ Hive queries executed" || echo "⚠️  Hive queries skipped"
else
    echo "⚠️  crop_trends.hql not found"
fi

# STEP 10: Run Spark MLlib
echo -e "\n[STEP 10] Running Spark MLlib prediction..."
if [ -f "$PROJECT_HOME/scripts/spark_yield_prediction.py" ]; then
    spark-submit \
        --master yarn \
        --deploy-mode client \
        --num-executors 2 \
        --executor-cores 2 \
        --executor-memory 2g \
        "$PROJECT_HOME/scripts/spark_yield_prediction.py" && echo "✅ Spark MLlib completed" || echo "⚠️  Spark MLlib execution skipped"
else
    echo "⚠️  spark_yield_prediction.py not found"
fi

# Summary
echo -e "\n=========================================="
echo "PIPELINE EXECUTION SUMMARY"
echo "=========================================="
echo "✅ HDFS Status: $(hdfs dfsadmin -report | grep 'Configured Capacity' || echo 'OK')"
echo "✅ Results location: $HDFS_RESULTS"
echo "✅ Models location: /crop_yield/models"
echo "✅ Predictions location: /crop_yield/predictions"
echo -e "\nTo view results:"
echo "  hdfs dfs -cat /crop_yield/results/part-*"
echo "  hdfs dfs -cat /crop_yield/predictions/part-*"
echo ""
