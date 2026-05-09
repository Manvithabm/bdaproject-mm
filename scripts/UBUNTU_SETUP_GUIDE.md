# Hadoop/Hive Setup Guide for Ubuntu

## Prerequisites Check
```bash
# Verify Hadoop installation
hadoop version
# Should show: Hadoop 3.x.x

# Verify Hive installation  
hive --version
# Should show: Hive 3.x.x
```

## STEP 1: Copy Data to Ubuntu
From Windows, copy cleaned CSV files to Ubuntu:
```bash
# Option A: If using WSL
cp /mnt/c/Users/manvi/crop_yeild_prediction/data/cleaned_*.csv ~/crop_data/

# Option B: Using SCP (if separate machine)
scp -r /path/to/cleaned_*.csv username@ubuntu_ip:~/crop_data/

# Verify
ls -la ~/crop_data/
```

## STEP 2: Set Up HDFS Directories
```bash
# Start Hadoop services
start-dfs.sh
start-yarn.sh

# Check HDFS status
jps
# Should show: NameNode, DataNode, ResourceManager, NodeManager

# Create HDFS directories
hdfs dfs -mkdir -p /crop_yield/input
hdfs dfs -mkdir -p /crop_yield/cleaned
hdfs dfs -mkdir -p /crop_yield/hive

# Verify
hdfs dfs -ls /crop_yield/
```

## STEP 3: Upload Cleaned Data to HDFS
```bash
# Upload all cleaned CSV files
hdfs dfs -put ~/crop_data/cleaned_*.csv /crop_yield/input/

# Verify upload
hdfs dfs -ls /crop_yield/input/
```

## STEP 4: Compile MapReduce Job (DataCleaning.java)
```bash
# Navigate to project directory
cd ~/crop_yield_prediction/src

# Compile with Hadoop libraries
javac -cp /usr/lib/hadoop/lib/*:/usr/lib/hadoop-hdfs/lib/*:/usr/lib/hadoop-yarn/lib/* DataCleaning.java

# Create JAR file
jar cf ../DataCleaning.jar DataCleaning.class

# Verify JAR created
ls -la ../DataCleaning.jar
```

## STEP 5: Run MapReduce Job
```bash
# Run from project root
cd ~/crop_yield_prediction

# Execute MapReduce
hadoop jar DataCleaning.jar DataCleaning /crop_yield/input /crop_yield/cleaned 2

# Monitor in browser (if X11 available)
# http://localhost:8088 (ResourceManager)
# http://localhost:50070 (NameNode)

# Wait for job completion, then verify
hdfs dfs -ls /crop_yield/cleaned/
```

## STEP 6: Create Hive Table for Cleaned Data
```bash
# Start Hive CLI
hive

# Create external table (in Hive CLI)
CREATE EXTERNAL TABLE IF NOT EXISTS cleaned_yield (
  country STRING,
  year INT,
  temperature DOUBLE,
  rainfall DOUBLE,
  pesticides DOUBLE,
  yield DOUBLE
)
COMMENT 'Cleaned crop yield data from MapReduce'
STORED AS TEXTFILE
LOCATION '/crop_yield/cleaned';

# Verify table created
SHOW TABLES;

# Check data loaded
SELECT COUNT(*) FROM cleaned_yield;
SELECT * FROM cleaned_yield LIMIT 5;
```

## STEP 7: Run Hive Analytics Queries
```bash
# Execute Hive queries from file
hive -f ~/crop_yield_prediction/scripts/crop_trends.hql

# Or run interactively in Hive CLI
# (see STEP 6 above - open Hive CLI and execute queries manually)
```

## STEP 8: Export Results
```bash
# Export Hive query results back to HDFS
INSERT OVERWRITE DIRECTORY '/crop_yield/results' 
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
SELECT * FROM cleaned_yield;

# Download results to local
hdfs dfs -get /crop_yield/results ~/crop_results/
ls -la ~/crop_results/
```

## STEP 9: Copy Results Back to Windows
```bash
# From Windows PowerShell
scp -r username@ubuntu_ip:~/crop_results/* C:\Users\manvi\crop_yeild_prediction\data\hive_results\

# Or if using WSL:
cp /mnt/home/username/crop_results/* /mnt/c/Users/manvi/crop_yeild_prediction/data/hive_results/
```

## Troubleshooting

### HDFS Not Starting
```bash
# Check logs
tail -f $HADOOP_HOME/logs/hadoop-*.log

# Format namenode (CAUTION: deletes data)
hdfs namenode -format
```

### MapReduce Job Fails
```bash
# Check job logs
yarn logs -applicationId application_XXXX_XXXX

# Re-run with verbose output
hadoop jar DataCleaning.jar DataCleaning /crop_yield/input /crop_yield/cleaned 2 -D mapred.reduce.tasks=4
```

### Hive Table Empty
```bash
# Check HDFS data location
hdfs dfs -ls /crop_yield/cleaned/
hdfs dfs -cat /crop_yield/cleaned/part-r-00000 | head -5

# Refresh table
MSCK REPAIR TABLE cleaned_yield;
```

## Next: Spark MLlib for Distributed ML
See: spark_ml_setup_guide.md
