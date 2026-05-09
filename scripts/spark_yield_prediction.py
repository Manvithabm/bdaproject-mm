#!/usr/bin/env python3
"""
Spark MLlib Yield Prediction - Distributed Machine Learning
Runs on Hadoop cluster to train yield prediction models at scale
"""

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.regression import LinearRegression, RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
import sys
import os

# Initialize Spark Session
spark = SparkSession \
    .builder \
    .appName("YieldPredictionMLlib") \
    .master("yarn") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "1g") \
    .config("spark.executor.cores", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

def load_and_prepare_data(hdfs_path="/crop_yield/cleaned"):
    """Load cleaned data from HDFS and prepare for ML"""
    print(f"[INFO] Loading data from HDFS: {hdfs_path}")
    
    # Read all CSV files from HDFS
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(f"{hdfs_path}/*.csv")
    
    print(f"[INFO] Loaded {df.count()} rows")
    print(f"[INFO] Schema: {df.schema}")
    
    # Select relevant columns (handle missing columns gracefully)
    available_cols = df.columns
    feature_cols = []
    
    # Try to identify feature columns
    for col in ['temperature', 'rainfall', 'pesticides', 'year']:
        if col in available_cols:
            feature_cols.append(col)
    
    # Target column
    target_col = 'yield'
    if target_col not in available_cols:
        print(f"[ERROR] Target column '{target_col}' not found in data")
        print(f"[INFO] Available columns: {available_cols}")
        return None
    
    # Remove rows with null values
    df_clean = df.select(feature_cols + [target_col]).dropna()
    print(f"[INFO] After removing nulls: {df_clean.count()} rows")
    
    return df_clean, feature_cols, target_col

def train_models(df, feature_cols, target_col):
    """Train multiple ML models using Spark MLlib"""
    
    # Split data into training and test sets (80/20)
    train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
    print(f"[INFO] Training set: {train_df.count()}, Test set: {test_df.count()}")
    
    # Feature assembly pipeline
    assembler = VectorAssembler(
        inputCols=feature_cols,
        outputCol="features"
    )
    
    # Standardize features
    scaler = StandardScaler(
        inputCol="features",
        outputCol="scaledFeatures",
        withMean=True,
        withStd=True
    )
    
    # Define models
    models = {
        "LinearRegression": LinearRegression(
            featuresCol="scaledFeatures",
            labelCol=target_col,
            maxIter=100,
            regParam=0.01
        ),
        "RandomForest": RandomForestRegressor(
            featuresCol="scaledFeatures",
            labelCol=target_col,
            numTrees=20,
            maxDepth=10,
            seed=42
        ),
        "GradientBoosting": GBTRegressor(
            featuresCol="scaledFeatures",
            labelCol=target_col,
            maxIter=50,
            maxDepth=5,
            seed=42
        )
    }
    
    results = {}
    
    # Train each model
    for model_name, model in models.items():
        print(f"\n[INFO] Training {model_name}...")
        
        # Create pipeline
        pipeline = Pipeline(stages=[assembler, scaler, model])
        
        # Train model
        trained_model = pipeline.fit(train_df)
        
        # Make predictions
        predictions = trained_model.transform(test_df)
        
        # Evaluate
        evaluator_rmse = RegressionEvaluator(
            labelCol=target_col,
            predictionCol="prediction",
            metricName="rmse"
        )
        evaluator_r2 = RegressionEvaluator(
            labelCol=target_col,
            predictionCol="prediction",
            metricName="r2"
        )
        
        rmse = evaluator_rmse.evaluate(predictions)
        r2 = evaluator_r2.evaluate(predictions)
        
        results[model_name] = {
            "model": trained_model,
            "rmse": rmse,
            "r2": r2
        }
        
        print(f"  RMSE: {rmse:.2f}")
        print(f"  R²: {r2:.4f}")
    
    return results

def save_best_model(results, output_path="/crop_yield/models"):
    """Save best model based on R² score"""
    
    # Find best model
    best_model_name = max(results.keys(), key=lambda x: results[x]["r2"])
    best_model = results[best_model_name]
    
    print(f"\n[INFO] Best Model: {best_model_name}")
    print(f"  R²: {best_model['r2']:.4f}")
    print(f"  RMSE: {best_model['rmse']:.2f}")
    
    # Save model to HDFS
    model_output_path = f"{output_path}/{best_model_name}_model"
    print(f"[INFO] Saving model to: {model_output_path}")
    
    best_model["model"].write().overwrite().save(model_output_path)
    
    return best_model_name, model_output_path

def make_predictions(model_path, test_data_path="/crop_yield/input"):
    """Make predictions on new data using trained model"""
    from pyspark.ml import PipelineModel
    
    print(f"\n[INFO] Loading model from: {model_path}")
    model = PipelineModel.load(model_path)
    
    print(f"[INFO] Loading test data from: {test_data_path}")
    df_test = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(f"{test_data_path}/*.csv") \
        .limit(100)
    
    print(f"[INFO] Making predictions on {df_test.count()} records")
    predictions = model.transform(df_test)
    
    # Show results
    predictions.select("temperature", "rainfall", "pesticides", "yield", "prediction") \
        .show(20)
    
    # Save predictions to HDFS
    output_predictions = "/crop_yield/predictions"
    predictions.coalesce(1).write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(output_predictions)
    
    print(f"[INFO] Predictions saved to: {output_predictions}")

def main():
    try:
        # Load and prepare data
        result = load_and_prepare_data()
        if result is None:
            sys.exit(1)
        df, feature_cols, target_col = result
        
        # Train models
        print("\n" + "="*60)
        print("TRAINING MODELS")
        print("="*60)
        results = train_models(df, feature_cols, target_col)
        
        # Save best model
        print("\n" + "="*60)
        print("SAVING BEST MODEL")
        print("="*60)
        best_model_name, model_path = save_best_model(results)
        
        # Make predictions
        print("\n" + "="*60)
        print("MAKING PREDICTIONS")
        print("="*60)
        make_predictions(model_path)
        
        print("\n" + "="*60)
        print("✅ SPARK MLlib PIPELINE COMPLETED SUCCESSFULLY")
        print("="*60)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
