#!/usr/bin/env python3
"""
Master orchestration script for the crop yield prediction pipeline.
Coordinates all steps from data collection through prediction and analytics.
"""

import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline_execution.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CropYieldPipeline:
    """Orchestrate the complete crop yield prediction pipeline."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.scripts_dir = self.project_root / 'scripts'
        self.src_dir = self.project_root / 'src'
        self.results = {}
    
    def run_command(self, cmd, description):
        """Run a command and track results."""
        try:
            logger.info(f"Starting: {description}")
            result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
            if result.returncode == 0:
                logger.info(f"Completed: {description}")
                self.results[description] = 'SUCCESS'
                return True
            else:
                logger.warning(f"Failed: {description}")
                self.results[description] = 'FAILED'
                return False
        except Exception as e:
            logger.error(f"Error running {description}: {str(e)}")
            self.results[description] = 'ERROR'
            return False
    
    def step1_download_data(self):
        """Step 1: Download dataset from Kaggle."""
        cmd = f"python3 {self.scripts_dir}/download_data.py"
        return self.run_command(cmd, "Download Data from Kaggle")
    
    def step2_upload_to_hdfs(self):
        """Step 2: Upload data to HDFS."""
        cmd = f"bash {self.scripts_dir}/upload_to_hdfs.sh"
        return self.run_command(cmd, "Upload Data to HDFS")
    
    def step3_run_mapreduce(self):
        """Step 3: Run MapReduce data cleaning."""
        cmd = f"bash {self.scripts_dir}/run_mapreduce.sh"
        return self.run_command(cmd, "Run MapReduce Cleaning Job")
    
    def step4_run_hive_queries(self):
        """Step 4: Run Hive trend analysis queries."""
        cmd = f"bash {self.scripts_dir}/run_hive_queries.sh"
        return self.run_command(cmd, "Run Hive Trend Queries")
    
    def step5_load_mongodb(self):
        """Step 5: Load cleaned data to MongoDB."""
        cmd = f"python3 {self.scripts_dir}/load_to_mongodb.py"
        return self.run_command(cmd, "Load Data to MongoDB")
    
    def step6_spark_prediction(self):
        """Step 6: Run Spark MLlib yield prediction."""
        cmd = f"python3 {self.src_dir}/yield_prediction.py"
        return self.run_command(cmd, "Run Spark MLlib Prediction")
    
    def step7_web_analytics(self):
        """Step 7: Perform web analytics on farming trends."""
        cmd = f"python3 {self.scripts_dir}/web_analytics.py"
        return self.run_command(cmd, "Perform Web Analytics")
    
    def print_summary(self):
        """Print pipeline execution summary."""
        logger.info("\n" + "="*60)
        logger.info("PIPELINE EXECUTION SUMMARY")
        logger.info("="*60)
        for step, result in self.results.items():
            status_symbol = "✓" if result == "SUCCESS" else "✗"
            logger.info(f"{status_symbol} {step}: {result}")
        logger.info("="*60 + "\n")
    
    def execute_all(self):
        """Execute the complete pipeline."""
        logger.info("Starting Crop Yield Prediction Pipeline")
        logger.info(f"Project Root: {self.project_root}")
        
        steps = [
            self.step1_download_data,
            self.step2_upload_to_hdfs,
            self.step3_run_mapreduce,
            self.step4_run_hive_queries,
            self.step5_load_mongodb,
            self.step6_spark_prediction,
            self.step7_web_analytics
        ]
        
        success_count = 0
        for step_func in steps:
            try:
                if step_func():
                    success_count += 1
                else:
                    # Continue with next steps even if one fails
                    logger.warning(f"Step {step_func.__name__} failed, continuing...")
            except Exception as e:
                logger.error(f"Unexpected error in {step_func.__name__}: {str(e)}")
        
        self.print_summary()
        return success_count == len(steps)
    
    def execute_step(self, step_name):
        """Execute a specific pipeline step."""
        steps = {
            'download': self.step1_download_data,
            'hdfs': self.step2_upload_to_hdfs,
            'mapreduce': self.step3_run_mapreduce,
            'hive': self.step4_run_hive_queries,
            'mongodb': self.step5_load_mongodb,
            'spark': self.step6_spark_prediction,
            'analytics': self.step7_web_analytics
        }
        
        if step_name not in steps:
            logger.error(f"Unknown step: {step_name}")
            logger.info(f"Available steps: {', '.join(steps.keys())}")
            return False
        
        logger.info(f"Executing step: {step_name}")
        return steps[step_name]()

def main():
    """Main execution function."""
    pipeline = CropYieldPipeline()
    
    if len(sys.argv) < 2:
        # Run complete pipeline
        success = pipeline.execute_all()
    else:
        step = sys.argv[1]
        if step == 'all':
            success = pipeline.execute_all()
        else:
            success = pipeline.execute_step(step)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
