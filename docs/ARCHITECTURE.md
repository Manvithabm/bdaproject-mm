# Architecture and Design Documentation

## System Architecture

### High-Level Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Data Pipeline Architecture                        │
└──────────────────────────────────────────────────────────────────────┘

1. DATA INGESTION LAYER
   ├─ Kaggle Dataset (External)
   └─ CSV Files (Local/HDFS)

2. STORAGE LAYER
   ├─ HDFS (Distributed Storage)
   │  ├─ /crop_yield/input (Raw data)
   │  └─ /crop_yield/cleaned (Processed data)
   └─ MongoDB (NoSQL Database)
      └─ crop_yield_db

3. PROCESSING LAYER
   ├─ MapReduce (ETL - Data Cleaning)
   │  ├─ Mapper: Data validation
   │  └─ Reducer: Data aggregation
   ├─ Hive (SQL Analytics)
   │  └─ Trend queries and analysis
   └─ Spark MLlib (ML Pipeline)
      ├─ Feature Engineering
      ├─ Model Training
      └─ Prediction & Evaluation

4. ANALYTICS LAYER
   ├─ Web Scraping (Farming Trends)
   ├─ Data Visualization
   └─ Reporting

5. OUTPUT LAYER
   ├─ Trained Models (models/)
   ├─ Analytics Results (data/farming_trends.*)
   ├─ Predictions
   └─ Logs (pipeline_execution.log)
```

## Component Details

### 1. Data Ingestion (download_data.py)

**Purpose**: Download and validate crop yield data from Kaggle

**Key Features**:
- Automated Kaggle API authentication
- Data quality checks (duplicates, missing values)
- Mean-based imputation for numerical fields
- Logging and error handling
- CSV export with validation metrics

**Input**: Kaggle API credentials
**Output**: 
- `data/yield.csv` (raw data)
- `data/cleaned_yield.csv` (processed data)

### 2. HDFS Storage (upload_to_hdfs.sh)

**Purpose**: Distribute data across Hadoop clusters

**Key Operations**:
- Creates HDFS directories for input/output
- Uploads CSV files to HDFS
- Handles file overwrites
- Verifies upload completion

**HDFS Structure**:
```
/crop_yield/
├── input/          # Raw data files
├── cleaned/        # MapReduce output
└── output/         # Final results
```

### 3. MapReduce Data Cleaning (DataCleaning.java)

**Purpose**: Large-scale data validation and cleansing

**Mapper Function**:
- Skips header rows and empty lines
- Validates field count (minimum 5 fields)
- Checks for null/NA values
- Validates numeric fields (temperature, rainfall, yield)
- Emits valid records grouped by crop

**Reducer Function**:
- Aggregates records by crop
- Deduplicates entries
- Maintains data integrity
- Statistics tracking

**Configuration**:
```bash
# Default: 1 reducer
bash scripts/run_mapreduce.sh 4    # Use 4 reducers
```

**Output**: Cleaned data in `/crop_yield/cleaned` with compression

### 4. Hive Analytics (crop_trends.hql)

**Purpose**: SQL-based trend analysis and reporting

**Key Queries**:

1. **Crop Performance**:
   - Average, min, max yield by crop
   - Standard deviation calculation
   
2. **Time Series Analysis**:
   - Yield trends over years
   - Year-over-year comparison
   - Growth rates

3. **Climate Impact**:
   - Temperature vs. yield correlation
   - Rainfall impact on production
   
4. **Soil Analysis**:
   - Performance by soil type
   - Climate factors by soil

5. **Ranking Queries**:
   - Top performing crops
   - Window functions for ranking

**Output**: SQL result sets for reporting

### 5. MongoDB Storage (load_to_mongodb.py)

**Purpose**: Store cleaned data for real-time querying

**Collections**:
- `yield_data`: Raw yield information
- `cleaned_data`: Processed records
- `predictions`: Model predictions
- `farming_trends`: Web analytics data

**Indexes Created**:
- `crop` (ascending)
- `year` (ascending)

**Connection**: MongoDB URI configurable in `config/mongodb_config.py`

**Features**:
- Connection pooling
- Error handling and retry logic
- Batch insert operations
- Index creation for query optimization

### 6. Spark MLlib Prediction (yield_prediction.py)

**Purpose**: Machine learning model training and prediction

**Pipeline Steps**:
1. **Data Loading**: Read from CSV with schema inference
2. **Preprocessing**:
   - Handle missing values (mean imputation)
   - Encode categorical variables
   - Create feature vectors
3. **Feature Scaling**: Standardization using StandardScaler
4. **Model Training**: Three models evaluated:
   - Linear Regression
   - Random Forest (100 trees)
   - Gradient Boosting Trees
5. **Evaluation**: RMSE and R² metrics
6. **Model Selection**: Best model based on RMSE
7. **Model Persistence**: Save best model to disk

**Configuration**:
```python
# In config/spark_config.py
SPARK_SESSION_CONFIG = {
    'spark.sql.shuffle.partitions': 4,
    'spark.executor.memory': '2g',
    'spark.driver.memory': '1g',
    # ...
}
```

**Output**:
- Trained model: `models/best_yield_prediction_model_*`
- Performance metrics (logged)
- Predictions on test data

### 7. Web Analytics (web_analytics.py)

**Purpose**: Collect and analyze farming trends

**Data Sources**:
- Agriculture news websites
- Online articles
- Sample trend data (fallback)

**Analysis**:
- Trend collection and categorization
- Impact classification
- Time-series tracking

**Output**:
- `data/farming_trends.csv`
- `data/farming_trends.json`

## Data Flow

```
Kaggle Dataset
     ↓
[Download & Validate]
     ↓
Local CSV Files
     ↓
[Upload to HDFS]
     ↓
HDFS Raw Data (/crop_yield/input)
     ↓
[MapReduce Cleaning]
     ↓
HDFS Cleaned Data (/crop_yield/cleaned)
     ↓
┌─────────────────────────┐
│   Parallel Processing   │
├─────────────────────────┤
│ [Hive Queries]          │ → Trend Analysis
│ [Load MongoDB]          │ → Document Store
│ [Spark MLlib]           │ → Predictions
│ [Web Analytics]         │ → Trend Collection
└─────────────────────────┘
     ↓
[Results & Models]
     ↓
Reports, Predictions, Analytics
```

## Error Handling

### Pipeline Resilience

- **Graceful Degradation**: Failed steps don't block subsequent steps
- **Comprehensive Logging**: All operations logged to `pipeline_execution.log`
- **Connection Retries**: MongoDB and HDFS operations include retry logic
- **Data Validation**: Multiple checkpoints validate data quality

### Common Issues

| Issue | Solution |
|-------|----------|
| Kaggle auth fails | Check `~/.kaggle/kaggle.json` credentials |
| HDFS connection error | Verify Hadoop is running: `jps` |
| MongoDB connection timeout | Check MongoDB service: `systemctl status mongod` |
| MapReduce compilation error | Ensure Hadoop classpath is correct |
| Spark memory error | Increase `executor_memory` in config |

## Performance Considerations

### Optimization Tips

1. **MapReduce**:
   - Increase reducers for large datasets
   - Enable compression for I/O efficiency

2. **Hive**:
   - Partition tables by year/crop for faster queries
   - Create materialized views for frequent queries

3. **Spark**:
   - Tune executor and driver memory based on cluster
   - Increase partitions for better parallelism
   - Use broadcast variables for small datasets

4. **MongoDB**:
   - Create compound indexes for frequent queries
   - Use projection to minimize data transfer

## Scalability

### Horizontal Scaling

- **HDFS**: Add more DataNodes for storage
- **Hadoop**: Deploy on cluster instead of pseudo-distributed
- **Spark**: Configure for YARN or Standalone cluster mode
- **MongoDB**: Configure replication or sharding

### Vertical Scaling

- Increase memory allocation
- Add CPU cores
- Use faster storage (SSD)

## Security Considerations

- Store credentials in `~/.kaggle/kaggle.json` (not in code)
- Use MongoDB authentication in production
- Set proper file permissions (chmod 600 for configs)
- Log sensitive operations (without exposing credentials)

## Monitoring

Monitor these metrics:
- HDFS storage usage
- MapReduce job execution time
- Hive query performance
- MongoDB document count
- Spark job duration
- Model accuracy/RMSE

## Future Enhancements

- Real-time streaming with Apache Kafka
- Advanced ML models (Neural Networks, XGBoost)
- Auto-scaling based on data volume
- REST API for predictions
- Web dashboard for monitoring
- Integration with cloud platforms
