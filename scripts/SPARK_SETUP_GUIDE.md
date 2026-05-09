# Spark MLlib Setup & Execution Guide for Ubuntu

## Prerequisites Verification
```bash
# Check Spark installation
spark-submit --version
# Should show: Spark 3.x.x

# Verify Hadoop is running
jps
# Should show: NameNode, DataNode, ResourceManager, NodeManager

# Verify Hive is working
hive --version
# Should show: Hive 3.x.x
```

## STEP 1: Configure Spark Environment Variables
```bash
# Add to ~/.bashrc or ~/.bash_profile
export SPARK_HOME=/usr/local/spark
export PATH=$SPARK_HOME/bin:$PATH
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop

# Reload
source ~/.bashrc
```

## STEP 2: Verify Spark Can Access HDFS
```bash
# Test Spark shell with HDFS
spark-shell --master yarn --deploy-mode client

# In Spark shell, test:
scala> val df = spark.read.csv("hdfs:///crop_yield/input/cleaned_yield.csv")
scala> df.count()
scala> exit()

# If this works, Spark is properly configured
```

## STEP 3: Prepare Data in HDFS
```bash
# Copy cleaned data from Windows/local
hdfs dfs -mkdir -p /crop_yield/input /crop_yield/cleaned /crop_yield/models

# Upload cleaned CSV files
hdfs dfs -put ~/crop_data/cleaned_*.csv /crop_yield/input/

# Verify
hdfs dfs -ls /crop_yield/input/
```

## STEP 4: Run Spark MLlib Pipeline

### Option A: Submit from Windows (if using WSL/SSH)
```powershell
# In PowerShell on Windows
$ubuntu_user = "username"
$ubuntu_host = "ubuntu_ip_or_localhost"

ssh ${ubuntu_user}@${ubuntu_host} "cd ~/crop_yeild_prediction && bash scripts/run_full_pipeline.sh"
```

### Option B: Run on Ubuntu directly
```bash
# On Ubuntu
cd ~/crop_yeild_prediction

# Make script executable
chmod +x scripts/run_full_pipeline.sh

# Run complete pipeline
./scripts/run_full_pipeline.sh

# Or run just Spark MLlib
spark-submit \
    --master yarn \
    --deploy-mode client \
    --num-executors 2 \
    --executor-cores 2 \
    --executor-memory 2g \
    --driver-memory 1g \
    scripts/spark_yield_prediction.py
```

## STEP 5: Monitor Spark Jobs
```bash
# While job is running, check YARN UI
# http://ubuntu_ip:8088

# Or check logs
yarn logs -applicationId application_XXXXXXXX_XXXX

# Watch HDFS usage
hdfs dfsadmin -report | grep -E "DFS Used|DFS Remaining"
```

## STEP 6: Retrieve Results
```bash
# Check predictions output
hdfs dfs -ls /crop_yield/predictions/

# View predictions
hdfs dfs -cat /crop_yield/predictions/part-00000 | head -20

# Download to local
hdfs dfs -get /crop_yield/predictions ~/predictions_output/
hdfs dfs -get /crop_yield/models ~/models_output/
```

## STEP 7: Copy Results Back to Windows
```bash
# From Ubuntu
scp -r ~/predictions_output/* username@windows_ip:/path/to/crop_yeild_prediction/data/spark_predictions/

# Or if using WSL
cp ~/predictions_output/* /mnt/c/Users/manvi/crop_yeild_prediction/data/spark_predictions/
```

## Troubleshooting Spark MLlib

### Job Status
```bash
# Check if job is running
yarn application -list

# Check application logs
yarn logs -applicationId <APP_ID> -log_files stdout

# Check Spark driver logs
spark-submit ... --verbose > spark.log 2>&1
```

### Memory Issues
```bash
# Increase memory allocation
spark-submit \
    --driver-memory 2g \
    --executor-memory 4g \
    --executor-cores 4 \
    scripts/spark_yield_prediction.py
```

### HDFS Connection Issues
```bash
# Verify HDFS accessibility
hdfs dfs -test -d / && echo "HDFS OK" || echo "HDFS Failed"

# Check Hadoop logs
tail -f $HADOOP_HOME/logs/hadoop-*.log

# Restart HDFS if needed
$HADOOP_HOME/sbin/stop-dfs.sh
sleep 2
$HADOOP_HOME/sbin/start-dfs.sh
```

### Spark Data Type Issues
```bash
# If errors about STRING vs DOUBLE types:
# Edit spark_yield_prediction.py line where data is loaded:

# Change:
.option("inferSchema", "true")

# To explicit schema:
schema = "country STRING, year INT, temperature DOUBLE, rainfall DOUBLE, pesticides DOUBLE, yield DOUBLE"
.schema(schema)
```

## Performance Tuning
```bash
# For faster execution on smaller datasets
spark-submit \
    --master local[*] \
    --driver-memory 2g \
    scripts/spark_yield_prediction.py

# For distributed execution on YARN
spark-submit \
    --master yarn \
    --deploy-mode client \
    --num-executors 4 \
    --executor-cores 2 \
    --executor-memory 2g \
    scripts/spark_yield_prediction.py
```

## Expected Output
```
[INFO] Loading data from HDFS: /crop_yield/cleaned
[INFO] Loaded XXXX rows
[INFO] Training LinearRegression...
  RMSE: XXXX.XX
  R²: X.XXXX
[INFO] Training RandomForest...
  RMSE: XXXX.XX
  R²: X.XXXX
[INFO] Training GradientBoosting...
  RMSE: XXXX.XX
  R²: X.XXXX
[INFO] Best Model: LinearRegression
[INFO] Saving model to: /crop_yield/models/LinearRegression_model
[INFO] Predictions saved to: /crop_yield/predictions
✅ SPARK MLlib PIPELINE COMPLETED SUCCESSFULLY
```

## Next Steps
1. Download predictions from HDFS
2. Validate model performance
3. Schedule pipeline for regular execution
4. Integrate with web dashboard (if needed)
