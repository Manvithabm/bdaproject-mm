# Agricultural Crop Yield Prediction

A comprehensive big data analytics solution for predicting crop production based on climate and soil data using Hadoop, Hive, Spark, and MongoDB.

## Project Overview

This project implements a complete machine learning pipeline that:
1. Collects government datasets on crop yield from Kaggle
2. Stores raw data in HDFS (Hadoop Distributed File System)
3. Cleans and preprocesses data using MapReduce
4. Performs trend analysis using Hive SQL
5. Stores refined data in MongoDB
6. Applies Spark MLlib for yield prediction with multiple models
7. Performs web analytics on farming trends

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Pipeline                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Kaggle Dataset → HDFS → MapReduce → Hive → MongoDB → Spark ML  │
│                          (Clean)    (Analyze) (Store) (Predict)  │
│                                                                   │
│                      Web Analytics Integration                   │
│                         (Farming Trends)                         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Dataset

- **Source**: Kaggle - Crop Yield Prediction Dataset
- **Description**: Contains crop yield data along with climate and soil parameters
- **Key Attributes**: 
  - Crop type
  - Year
  - Yield (target variable)
  - Temperature
  - Rainfall
  - Soil type

## Prerequisites

### System Requirements
- Linux/Unix or WSL for Windows
- 8GB+ RAM
- 20GB+ free disk space

### Software Requirements
- **Java**: 8 or higher
- **Hadoop**: 3.x or higher
- **Hive**: Compatible with your Hadoop version
- **Spark**: 3.x with MLlib
- **MongoDB**: Latest version
- **Python**: 3.8 or higher
- **pip**: For Python package management

## Installation

### 1. Install Hadoop
```bash
# Download and install Hadoop
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz
tar -xzf hadoop-3.3.0.tar.gz
mv hadoop-3.3.0 /usr/local/hadoop
```

### 2. Install Hive
```bash
# Download and install Hive
wget https://archive.apache.org/dist/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz
tar -xzf apache-hive-3.1.2-bin.tar.gz
mv apache-hive-3.1.2-bin /usr/local/hive
```

### 3. Install Spark
```bash
# Download and install Spark
wget https://archive.apache.org/dist/spark/spark-3.3.0/spark-3.3.0-bin-hadoop3.tgz
tar -xzf spark-3.3.0-bin-hadoop3.tgz
mv spark-3.3.0-bin-hadoop3 /usr/local/spark
```

### 4. Install MongoDB
```bash
# For Ubuntu/Debian
curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### 5. Install Python Dependencies
```bash
# Create virtual environment (optional but recommended)
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6. Setup Kaggle API
```bash
# Create ~/.kaggle/kaggle.json with your Kaggle API credentials
# Download from: https://www.kaggle.com/settings/account
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

### 7. Set Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc
export HADOOP_HOME=/usr/local/hadoop
export HIVE_HOME=/usr/local/hive
export SPARK_HOME=/usr/local/spark
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin:$SPARK_HOME/bin:$PATH

# Load configuration
source config/hadoop_config.sh
```

## Usage

### Quick Start - Execute Complete Pipeline

#### Option 1: Bash Script
```bash
# Execute all pipeline steps
bash scripts/pipeline.sh all

# Execute specific step
bash scripts/pipeline.sh download
bash scripts/pipeline.sh hdfs
bash scripts/pipeline.sh mapreduce
bash scripts/pipeline.sh hive
bash scripts/pipeline.sh mongodb
bash scripts/pipeline.sh spark
bash scripts/pipeline.sh analytics
```

#### Option 2: Python Orchestration
```bash
# Execute complete pipeline
python3 scripts/orchestrate_pipeline.py

# Execute specific step
python3 scripts/orchestrate_pipeline.py download
python3 scripts/orchestrate_pipeline.py spark
```

### Individual Pipeline Steps

#### 1. Data Collection
```bash
python3 scripts/download_data.py
```
Downloads the Kaggle dataset and performs basic data quality checks.

#### 2. Data Ingestion to HDFS
```bash
bash scripts/upload_to_hdfs.sh
```
Uploads raw data files to HDFS `/crop_yield/input` directory.

#### 3. Data Cleaning with MapReduce
```bash
bash scripts/run_mapreduce.sh [number_of_reducers]
```
Runs MapReduce job to clean and validate data. Output stored in `/crop_yield/cleaned`.

**MapReduce Operations**:
- Validates data format and field count
- Removes empty or null values
- Filters invalid numeric entries
- Groups data by crop

#### 4. Trend Analysis with Hive
```bash
bash scripts/run_hive_queries.sh
```
Executes Hive queries for trend analysis including:
- Average yield by crop
- Yield trends over years
- Temperature impact on yield
- Rainfall impact on yield
- Soil type performance
- Year-over-year comparisons

#### 5. Data Storage in MongoDB
```bash
python3 scripts/load_to_mongodb.py
```
Loads cleaned data into MongoDB with:
- Automatic index creation for fast queries
- Error handling for data validation
- Connection pooling for efficiency

#### 6. Yield Prediction with Spark MLlib
```bash
python3 src/yield_prediction.py
```
Trains and evaluates multiple models:
- **Linear Regression**: Baseline model
- **Random Forest**: 100 trees with max depth 10
- **Gradient Boosting Trees**: Advanced ensemble method

Output includes:
- Model performance metrics (RMSE, R²)
- Best model selection based on RMSE
- Saved model for future predictions

#### 7. Web Analytics
```bash
python3 scripts/web_analytics.py
```
Scrapes and analyzes farming trends from web sources. Outputs:
- `data/farming_trends.csv`: Trend data
- `data/farming_trends.json`: JSON format

## Project Structure

```
crop_yield_prediction/
├── config/                          # Configuration files
│   ├── app_config.py               # Application configuration
│   ├── mongodb_config.py           # MongoDB connection config
│   ├── spark_config.py             # Spark session config
│   └── hadoop_config.sh            # Hadoop environment setup
│
├── data/                            # Data directory
│   ├── yield.csv                   # Raw data
│   ├── cleaned_yield_data.csv      # Cleaned data
│   ├── farming_trends.csv          # Web analytics results
│   └── models/                     # Trained models
│
├── src/                             # Source code
│   ├── DataCleaning.java           # MapReduce job
│   └── yield_prediction.py         # Spark MLlib models
│
├── scripts/                         # Execution scripts
│   ├── download_data.py            # Data download
│   ├── upload_to_hdfs.sh           # HDFS upload
│   ├── run_mapreduce.sh            # MapReduce execution
│   ├── run_hive_queries.sh         # Hive query execution
│   ├── crop_trends.hql             # Hive SQL queries
│   ├── load_to_mongodb.py          # MongoDB loading
│   ├── web_analytics.py            # Trend analysis
│   ├── pipeline.sh                 # Bash orchestration
│   └── orchestrate_pipeline.py     # Python orchestration
│
├── notebooks/                       # Jupyter notebooks
│   ├── exploratory_analysis.ipynb  # EDA
│   └── model_training.ipynb        # Model training
│
├── docs/                            # Documentation
│   └── CONTRIBUTING.md             # Contribution guidelines
│
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── LICENSE                          # License
```

## Configuration

### Hadoop Configuration
Edit `config/hadoop_config.sh` to set your Hadoop paths:
```bash
export HADOOP_HOME=/path/to/hadoop
export JAVA_HOME=/path/to/java
```

### Spark Configuration
Edit `config/spark_config.py` to adjust:
- Master URL (local, YARN, Standalone cluster)
- Memory allocation
- Number of partitions
- Log level

### MongoDB Configuration
Edit `config/mongodb_config.py`:
```python
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'crop_yield_db'
}
```

## Performance Tuning

### MapReduce
```bash
# Increase number of reducers for large datasets
bash scripts/run_mapreduce.sh 8
```

### Spark
```python
# In config/spark_config.py
SPARK_CONFIG = {
    'executor_memory': '4g',      # Increase for large datasets
    'driver_memory': '2g',
    'executor_cores': 4,
    'partitions': 8               # Increase for parallelization
}
```

## Troubleshooting

### Hadoop Issues
```bash
# Check Hadoop status
jps

# Check HDFS health
hdfs dfsadmin -report

# View Hadoop logs
tail -f $HADOOP_HOME/logs/hadoop-*.log
```

### MongoDB Connection Issues
```bash
# Check MongoDB status
systemctl status mongod

# Test connection
mongo --eval "db.adminCommand('ping')"
```

### Spark Issues
```bash
# Check Spark context
spark-shell --version

# View Spark logs
tail -f $SPARK_HOME/logs/*.log
```

### Python Dependency Issues
```bash
# Verify packages
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Model Evaluation

The Spark MLlib module evaluates models using:
- **RMSE** (Root Mean Squared Error): Measures prediction error magnitude
- **R² Score**: Proportion of variance explained (0-1, higher is better)

Example output:
```
LinearRegression: RMSE=125.34, R²=0.8234
RandomForest: RMSE=98.21, R²=0.8756
GradientBoosting: RMSE=89.45, R²=0.9012
```

## Notebooks

### exploratory_analysis.ipynb
- Data loading and exploration
- Statistical analysis
- Visualization of trends
- Missing data analysis

### model_training.ipynb
- Feature engineering
- Model training and comparison
- Hyperparameter tuning
- Performance visualization

## Logging

All pipeline executions are logged to:
- `pipeline_execution.log`: Complete execution trace
- Console output: Real-time progress

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## References

- [Hadoop Documentation](https://hadoop.apache.org/docs/stable/)
- [Hive Documentation](https://cwiki.apache.org/confluence/display/Hive/)
- [Spark MLlib Guide](https://spark.apache.org/docs/latest/ml-guide.html)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [Kaggle Datasets](https://www.kaggle.com/datasets)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in `pipeline_execution.log`
3. Consult the official documentation for each component
4. Open an issue on GitHub

## Future Enhancements

- [ ] Real-time data streaming with Kafka
- [ ] Additional ML models (Neural Networks, XGBoost)
- [ ] Advanced visualization dashboards
- [ ] Automated pipeline scheduling
- [ ] Multi-region distributed processing
- [ ] Model serving with REST API
- [ ] Integration with cloud platforms (AWS, GCP, Azure)

## License

This project is licensed under the MIT License - see the LICENSE file for details.