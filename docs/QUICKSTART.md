# Quick Start Guide

## 5-Minute Setup

### Prerequisites Check
```bash
# Check Java
java -version

# Check Python
python3 --version

# Check pip
pip3 --version
```

### Install Python Dependencies
```bash
cd crop_yield_prediction
pip install -r requirements.txt
```

### Setup Environment
```bash
# Linux/macOS
source myenv/bin/activate

# Windows CMD
myenv\Scripts\activate.bat
```

## Running the Project

### Option 1: Complete Pipeline (Recommended)
```bash
# Python orchestration (simplest)
python3 scripts/orchestrate_pipeline.py

# Or Bash script
bash scripts/pipeline.sh all
```

### Option 2: Step-by-Step Execution
```bash
# Step 1: Download data
python3 scripts/download_data.py

# Step 2: Upload to HDFS (if available)
bash scripts/upload_to_hdfs.sh

# Step 3: Run MapReduce (if available)
bash scripts/run_mapreduce.sh

# Step 4: Hive queries (if available)
bash scripts/run_hive_queries.sh

# Step 5: Load MongoDB (if installed)
python3 scripts/load_to_mongodb.py

# Step 6: Train prediction models
python3 src/yield_prediction.py

# Step 7: Analyze farming trends
python3 scripts/web_analytics.py
```

### Option 3: Single Components
```bash
# Just download data
python3 scripts/download_data.py

# Just train models
python3 src/yield_prediction.py

# Just analyze trends
python3 scripts/web_analytics.py
```

## Configuration

### Basic Settings
Edit `config/app_config.py`:
```python
DATA_CONFIG = {
    'test_size': 0.2,           # Train/test split
    'random_state': 42,          # For reproducibility
    'target_column': 'yield'     # Prediction target
}
```

### MongoDB Settings (if using)
Edit `config/mongodb_config.py`:
```python
MONGODB_CONFIG = {
    'host': 'localhost',
    'port': 27017,
    'database': 'crop_yield_db'
}
```

## Expected Outputs

After running the pipeline, you'll have:

1. **Data Files** (`data/`):
   - `cleaned_yield.csv` - Processed data
   - `farming_trends.csv` - Trend analysis results
   - `farming_trends.json` - JSON format trends

2. **Models** (`models/`):
   - `best_yield_prediction_model_*` - Trained model directory

3. **Logs**:
   - `pipeline_execution.log` - Complete execution trace

## Checking Results

### View Data
```bash
# Check cleaned data
head data/cleaned_yield.csv

# View farming trends
cat data/farming_trends.csv

# Check results
ls -lah models/
```

### View Logs
```bash
# See pipeline execution logs
tail pipeline_execution.log

# Monitor in real-time
tail -f pipeline_execution.log
```

### Using Python
```python
import pandas as pd

# Load cleaned data
df = pd.read_csv('data/cleaned_yield.csv')
print(df.head())
print(df.describe())

# Load trends
trends = pd.read_csv('data/farming_trends.csv')
print(trends)
```

## Troubleshooting

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check installed packages
pip list | grep pyspark
```

### Data File Errors
```bash
# Verify data exists
ls -la data/

# Check Kaggle credentials
cat ~/.kaggle/kaggle.json
```

### Memory Issues
```bash
# For Spark jobs, increase memory in config/spark_config.py
SPARK_CONFIG = {
    'executor_memory': '4g',  # Increase from 2g
    'driver_memory': '2g'
}
```

## Next Steps

1. **Explore Data**: Open `notebooks/exploratory_analysis.ipynb`
2. **Customize Models**: Edit `src/yield_prediction.py`
3. **Add Hive Queries**: Edit `scripts/crop_trends.hql`
4. **Deploy**: Follow deployment guide in main README

## Support Resources

- **Python Issues**: Check `requirements.txt` versions
- **Data Issues**: Verify Kaggle dataset availability
- **Big Data Issues**: Check component installation guides in README
- **Logs**: Check `pipeline_execution.log` for detailed errors

## Tips & Tricks

```bash
# Run only specific steps
python3 scripts/orchestrate_pipeline.py download
python3 scripts/orchestrate_pipeline.py spark

# Clear output and re-run
rm -f pipeline_execution.log
python3 scripts/orchestrate_pipeline.py

# Monitor long-running jobs
watch -n 5 'tail -10 pipeline_execution.log'

# Check Python environment
python3 -m pip show pyspark
```

## Common Questions

**Q: Can I run this without Hadoop/Spark?**
A: Yes, data download, MongoDB loading, and trend analysis work standalone.

**Q: How long does the full pipeline take?**
A: Depends on data size, typically 10-30 minutes for full execution.

**Q: Can I modify the models?**
A: Yes, edit `src/yield_prediction.py` to add or modify ML models.

**Q: How do I add more data?**
A: Place CSV files in `data/` directory with same schema as original data.

**Q: Can I use this with real databases?**
A: Yes, modify configuration files for your database credentials.
