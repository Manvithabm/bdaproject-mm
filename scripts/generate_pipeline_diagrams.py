#!/usr/bin/env python3
"""
Generate visual pipeline diagrams as PNG files for the Crop Yield Prediction project
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

def create_pipeline_diagram():
    """Create main pipeline architecture diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(8, 9.5, 'Crop Yield Prediction - Complete Pipeline Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Colors
    windows_color = '#4A90E2'
    ubuntu_color = '#50C878'
    hdfs_color = '#FFB700'
    result_color = '#FF6B6B'
    
    # Windows Environment
    windows_box = FancyBboxPatch((0.5, 7), 2, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 edgecolor='black', facecolor=windows_color, alpha=0.7, linewidth=2)
    ax.add_patch(windows_box)
    ax.text(1.5, 7.75, '🪟 Windows\nPython Scripts', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Step 1: Download Data
    step1 = FancyBboxPatch((0.5, 5), 2, 1, 
                           boxstyle="round,pad=0.05", 
                           edgecolor='black', facecolor='#E8F4F8', linewidth=1.5)
    ax.add_patch(step1)
    ax.text(1.5, 5.5, 'download_data.py\nGenerate Raw Data', fontsize=9, ha='center', va='center')
    
    # Step 2: CSV Files
    step2 = FancyBboxPatch((0.5, 3.5), 2, 1, 
                           boxstyle="round,pad=0.05", 
                           edgecolor='black', facecolor='#E8F4F8', linewidth=1.5)
    ax.add_patch(step2)
    ax.text(1.5, 4, 'cleaned_*.csv\n5 Files', fontsize=9, ha='center', va='center')
    
    # Ubuntu Environment
    ubuntu_box = FancyBboxPatch((5, 7), 2, 1.5, 
                                boxstyle="round,pad=0.1", 
                                edgecolor='black', facecolor=ubuntu_color, alpha=0.7, linewidth=2)
    ax.add_patch(ubuntu_box)
    ax.text(6, 7.75, '🐧 Ubuntu\nHadoop Cluster', fontsize=10, ha='center', va='center', fontweight='bold', color='white')
    
    # Data Transfer Arrow
    arrow1 = FancyArrowPatch((2.5, 4), (5, 4), 
                            arrowstyle='->', mutation_scale=30, linewidth=2.5, color='#FF6B6B')
    ax.add_patch(arrow1)
    ax.text(3.75, 4.3, 'Transfer\nData', fontsize=9, ha='center', fontweight='bold', color='#FF6B6B')
    
    # Arrow down from Windows to CSV
    arrow_down1 = FancyArrowPatch((1.5, 5), (1.5, 4.5), 
                                 arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_down1)
    
    # Arrow down from download to CSV
    arrow_down2 = FancyArrowPatch((1.5, 6), (1.5, 5.5), 
                                 arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_down2)
    
    # HDFS Input
    hdfs1 = FancyBboxPatch((5, 5), 2, 1, 
                          boxstyle="round,pad=0.05", 
                          edgecolor='black', facecolor=hdfs_color, alpha=0.8, linewidth=1.5)
    ax.add_patch(hdfs1)
    ax.text(6, 5.5, 'HDFS Input\n/crop_yield/input', fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Arrow down in Ubuntu
    arrow_down3 = FancyArrowPatch((6, 5), (6, 4.5), 
                                 arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_down3)
    
    # MapReduce
    mapreduce = FancyBboxPatch((4.5, 3), 3, 1.2, 
                              boxstyle="round,pad=0.05", 
                              edgecolor='black', facecolor='#FFE6E6', linewidth=2)
    ax.add_patch(mapreduce)
    ax.text(6, 3.6, 'MapReduce\nDataCleaning.java\nDuplicate Removal', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Arrow down from MapReduce
    arrow_down4 = FancyArrowPatch((6, 3), (6, 2.5), 
                                 arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_down4)
    
    # HDFS Cleaned
    hdfs2 = FancyBboxPatch((5, 1.5), 2, 0.9, 
                          boxstyle="round,pad=0.05", 
                          edgecolor='black', facecolor=hdfs_color, alpha=0.8, linewidth=1.5)
    ax.add_patch(hdfs2)
    ax.text(6, 1.95, 'HDFS Cleaned\n/crop_yield/cleaned', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Hive Branch
    hive = FancyBboxPatch((9, 3), 2.5, 1.2, 
                         boxstyle="round,pad=0.05", 
                         edgecolor='black', facecolor='#E6F3FF', linewidth=2)
    ax.add_patch(hive)
    ax.text(10.25, 3.6, 'Hive SQL\ncrop_trends.hql\n8 Queries', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Arrow from Cleaned to Hive
    arrow_hive = FancyArrowPatch((7, 2), (9, 3.3), 
                               arrowstyle='->', mutation_scale=25, linewidth=2.5, color='#4169E1')
    ax.add_patch(arrow_hive)
    ax.text(8, 2.5, 'Read', fontsize=9, ha='center', fontweight='bold')
    
    # Hive Results
    hive_result = FancyBboxPatch((9, 1.5), 2.5, 0.9, 
                                boxstyle="round,pad=0.05", 
                                edgecolor='black', facecolor=hdfs_color, alpha=0.8, linewidth=1.5)
    ax.add_patch(hive_result)
    ax.text(10.25, 1.95, 'HDFS Results\n/crop_yield/results', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrow down from Hive
    arrow_down5 = FancyArrowPatch((10.25, 3), (10.25, 2.4), 
                                 arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_down5)
    
    # Spark MLlib Branch
    spark = FancyBboxPatch((13, 3), 2.5, 1.2, 
                          boxstyle="round,pad=0.05", 
                          edgecolor='black', facecolor='#FFE6F3', linewidth=2)
    ax.add_patch(spark)
    ax.text(14.25, 3.6, 'Spark MLlib\nspark_yield_prediction.py\n3 Models', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Arrow from Cleaned to Spark
    arrow_spark = FancyArrowPatch((7, 1.95), (13, 3.3), 
                                arrowstyle='->', mutation_scale=25, linewidth=2.5, color='#DC143C')
    ax.add_patch(arrow_spark)
    ax.text(10, 2.5, 'Read', fontsize=9, ha='center', fontweight='bold')
    
    # Models
    models = FancyBboxPatch((13, 1.5), 2.5, 0.9, 
                           boxstyle="round,pad=0.05", 
                           edgecolor='black', facecolor=hdfs_color, alpha=0.8, linewidth=1.5)
    ax.add_patch(models)
    ax.text(14.25, 1.95, 'Trained Models\n/crop_yield/models', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Predictions
    pred_box = FancyBboxPatch((13, 0.2), 2.5, 0.9, 
                             boxstyle="round,pad=0.05", 
                             edgecolor='black', facecolor=hdfs_color, alpha=0.8, linewidth=1.5)
    ax.add_patch(pred_box)
    ax.text(14.25, 0.65, 'Predictions\n/crop_yield/predictions', fontsize=8, ha='center', va='center', fontweight='bold')
    
    # Arrow down from Spark
    arrow_down6 = FancyArrowPatch((14.25, 3), (14.25, 2.4), 
                                 arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_down6)
    
    # Arrow from Models to Predictions
    arrow_pred = FancyArrowPatch((14.25, 1.5), (14.25, 1.1), 
                               arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_pred)
    
    # Download Results
    download = FancyBboxPatch((10.5, 0.2), 2, 0.9, 
                             boxstyle="round,pad=0.05", 
                             edgecolor='black', facecolor=result_color, alpha=0.8, linewidth=2)
    ax.add_patch(download)
    ax.text(11.5, 0.65, '📊 Results', fontsize=10, ha='center', va='center', fontweight='bold', color='white')
    
    # Arrows to download
    arrow_d1 = FancyArrowPatch((10.25, 1.5), (11, 1), 
                              arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_d1)
    arrow_d2 = FancyArrowPatch((13, 1.95), (12.5, 0.95), 
                              arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_d2)
    arrow_d3 = FancyArrowPatch((13, 0.65), (12.5, 0.65), 
                              arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow_d3)
    
    # Download back to Windows
    arrow_back = FancyArrowPatch((11.5, 0.2), (1.5, 3), 
                               arrowstyle='->', mutation_scale=25, linewidth=2.5, 
                               color='#FF6B6B', linestyle='--')
    ax.add_patch(arrow_back)
    ax.text(6.5, 1.5, '📥 Download Results', fontsize=10, ha='center', 
           fontweight='bold', color='#FF6B6B', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Legend
    ax.text(8, 0.2, '✅ Complete Pipeline: Download → Transfer → HDFS → MapReduce → Hive Analytics → Spark MLlib → Predictions', 
           fontsize=10, ha='center', fontweight='bold', 
           bbox=dict(boxstyle='round', facecolor='#E6F3FF', alpha=0.9, pad=0.5))
    
    plt.tight_layout()
    plt.savefig('pipeline_architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: pipeline_architecture.png")
    plt.close()

def create_execution_phases_diagram():
    """Create execution phases diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Title
    ax.text(7, 5.5, 'Pipeline Execution Phases', fontsize=18, fontweight='bold', ha='center')
    
    # Phase colors
    colors = ['#87CEEB', '#90EE90', '#FFD700', '#FF8C00', '#FF6B9D', '#32CD32']
    phases = [
        ('PHASE 1\nEnvironment\nSetup', 1),
        ('PHASE 2\nHadoop\nSetup', 3),
        ('PHASE 3\nMapReduce\nExecution', 5),
        ('PHASE 4\nHive\nAnalytics', 7),
        ('PHASE 5\nSpark MLlib\nExecution', 9),
        ('✅ COMPLETE\nResults\nReady', 11)
    ]
    
    for i, (label, x) in enumerate(phases):
        box = FancyBboxPatch((x-0.8, 2), 1.6, 2, 
                            boxstyle="round,pad=0.1", 
                            edgecolor='black', facecolor=colors[i], alpha=0.8, linewidth=2)
        ax.add_patch(box)
        ax.text(x, 3, label, fontsize=10, ha='center', va='center', fontweight='bold')
        
        # Add arrow between phases
        if i < len(phases) - 1:
            arrow = FancyArrowPatch((x+0.8, 3), (phases[i+1][1]-0.8, 3), 
                                   arrowstyle='->', mutation_scale=25, linewidth=2.5, color='#333')
            ax.add_patch(arrow)
    
    # Timeline
    ax.plot([1, 11], [1.5, 1.5], 'k--', linewidth=1)
    ax.text(1, 1, '~2 min', fontsize=8, ha='center')
    ax.text(3, 1, '~2 min', fontsize=8, ha='center')
    ax.text(5, 1, '~3 min', fontsize=8, ha='center')
    ax.text(7, 1, '~1 min', fontsize=8, ha='center')
    ax.text(9, 1, '~5 min', fontsize=8, ha='center')
    ax.text(11, 1, 'Done!', fontsize=8, ha='center', fontweight='bold', color='#32CD32')
    
    ax.text(7, 0.3, 'Total Execution Time: ~10-20 minutes', fontsize=11, ha='center', 
           fontweight='bold', bbox=dict(boxstyle='round', facecolor='#FFE6E6', alpha=0.9, pad=0.5))
    
    plt.tight_layout()
    plt.savefig('execution_phases.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: execution_phases.png")
    plt.close()

def create_data_transfer_diagram():
    """Create data transfer methods diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, 'Data Transfer Methods: Windows → Ubuntu', fontsize=16, fontweight='bold', ha='center')
    
    # Windows
    windows = FancyBboxPatch((0.5, 6), 3, 1, 
                            boxstyle="round,pad=0.1", 
                            edgecolor='black', facecolor='#4A90E2', alpha=0.8, linewidth=2)
    ax.add_patch(windows)
    ax.text(2, 6.5, '🪟 Windows\ncleaned_*.csv', fontsize=10, ha='center', va='center', 
           fontweight='bold', color='white')
    
    # Decision
    decision = FancyBboxPatch((1.5, 4.5), 2, 0.8, 
                             boxstyle="round,pad=0.05", 
                             edgecolor='black', facecolor='#FFEB3B', linewidth=2)
    ax.add_patch(decision)
    ax.text(2.5, 4.9, 'Choose Method', fontsize=10, ha='center', va='center', fontweight='bold')
    
    # Arrow down
    arrow = FancyArrowPatch((2, 6), (2.5, 5.3), 
                           arrowstyle='->', mutation_scale=20, linewidth=2, color='#333')
    ax.add_patch(arrow)
    
    # Transfer methods
    methods = [
        ('Option 1\nWSL\n(Same Machine)', 0.5, 3),
        ('Option 2\nSCP\n(Separate Machine)', 3, 3),
        ('Option 3\nSamba Share\n(Network)', 5.5, 3),
        ('Option 4\nDocker\n(Containerized)', 8, 3)
    ]
    
    colors_method = ['#87CEEB', '#90EE90', '#FFD700', '#FF6B9D']
    
    for i, (label, x, y) in enumerate(methods):
        method = FancyBboxPatch((x, y), 2, 1, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='black', facecolor=colors_method[i], alpha=0.8, linewidth=1.5)
        ax.add_patch(method)
        ax.text(x+1, y+0.5, label, fontsize=9, ha='center', va='center', fontweight='bold')
        
        # Arrow from decision to method
        arrow_method = FancyArrowPatch((2.5, 4.5), (x+1, y+1), 
                                      arrowstyle='->', mutation_scale=15, linewidth=1.5, 
                                      color='#333', linestyle='--')
        ax.add_patch(arrow_method)
    
    # Ubuntu
    ubuntu = FancyBboxPatch((3.5, 0.5), 5, 1, 
                           boxstyle="round,pad=0.1", 
                           edgecolor='black', facecolor='#50C878', alpha=0.8, linewidth=2)
    ax.add_patch(ubuntu)
    ax.text(6, 1, '🐧 Ubuntu\n~/crop_data/', fontsize=10, ha='center', va='center', 
           fontweight='bold', color='white')
    
    # Arrows to Ubuntu
    for label, x, y in methods:
        arrow_ubuntu = FancyArrowPatch((x+1, y), (6, 1.5), 
                                     arrowstyle='->', mutation_scale=15, linewidth=1.5, 
                                     color='#333', linestyle='--', alpha=0.5)
        ax.add_patch(arrow_ubuntu)
    
    plt.tight_layout()
    plt.savefig('data_transfer_methods.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: data_transfer_methods.png")
    plt.close()

def create_hdfs_structure_diagram():
    """Create HDFS directory structure diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, 'HDFS Directory Structure After Pipeline Execution', fontsize=16, fontweight='bold', ha='center')
    
    # Root
    root = FancyBboxPatch((4.5, 6.5), 3, 0.7, 
                         boxstyle="round,pad=0.05", 
                         edgecolor='black', facecolor='#FFB700', alpha=0.9, linewidth=2)
    ax.add_patch(root)
    ax.text(6, 6.85, '/crop_yield/', fontsize=11, ha='center', va='center', fontweight='bold')
    
    # Subdirectories
    dirs = [
        ('/crop_yield/input', 'Original Cleaned\nCSV Files', 1, 5),
        ('/crop_yield/cleaned', 'MapReduce\nDeduplicated Data', 3, 5),
        ('/crop_yield/results', 'Hive Query\nResults', 5, 5),
        ('/crop_yield/models', 'Trained Spark\nMLlib Models', 7, 5),
        ('/crop_yield/predictions', 'Model\nPredictions', 9, 5)
    ]
    
    colors_dir = ['#87CEEB', '#90EE90', '#FFD700', '#FF6B9D', '#32CD32']
    
    for i, (path, desc, x, y) in enumerate(dirs):
        # Arrow from root
        arrow_down = FancyArrowPatch((6, 6.5), (x+0.75, y+0.7), 
                                   arrowstyle='->', mutation_scale=15, linewidth=1.5, color='#333')
        ax.add_patch(arrow_down)
        
        # Directory box
        dir_box = FancyBboxPatch((x, y), 1.5, 0.7, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='black', facecolor=colors_dir[i], alpha=0.8, linewidth=1.5)
        ax.add_patch(dir_box)
        ax.text(x+0.75, y+0.35, path.split('/')[-1], fontsize=9, ha='center', va='center', fontweight='bold')
    
    # Details below directories
    for path, desc, x, y in dirs:
        detail_box = FancyBboxPatch((x-0.1, y-1.2), 1.7, 0.8, 
                                  boxstyle="round,pad=0.03", 
                                  edgecolor='gray', facecolor='#F5F5F5', 
                                  linewidth=1, linestyle='--')
        ax.add_patch(detail_box)
        ax.text(x+0.75, y-0.8, desc, fontsize=8, ha='center', va='center')
        
        # Arrow from dir to detail
        arrow_detail = FancyArrowPatch((x+0.75, y), (x+0.75, y-0.4), 
                                     arrowstyle='->', mutation_scale=10, linewidth=1, 
                                     color='gray', linestyle=':')
        ax.add_patch(arrow_detail)
    
    # Summary at bottom
    summary_text = (
        'HDFS Workflow:\n'
        '1. Input: Original cleaned CSV files\n'
        '2. Cleaned: Deduplicated by MapReduce\n'
        '3. Results: Analytics from Hive queries\n'
        '4. Models: Trained Spark MLlib models (best model selected)\n'
        '5. Predictions: Yield predictions on entire dataset'
    )
    ax.text(6, 0.5, summary_text, fontsize=9, ha='center', va='center',
           bbox=dict(boxstyle='round', facecolor='#E8F4F8', alpha=0.9, pad=0.7))
    
    plt.tight_layout()
    plt.savefig('hdfs_structure.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: hdfs_structure.png")
    plt.close()

if __name__ == '__main__':
    print("🎨 Generating Pipeline Diagrams...")
    print()
    
    create_pipeline_diagram()
    create_execution_phases_diagram()
    create_data_transfer_diagram()
    create_hdfs_structure_diagram()
    
    print()
    print("=" * 60)
    print("✅ ALL DIAGRAMS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Generated PNG files:")
    print("  1. pipeline_architecture.png")
    print("  2. execution_phases.png")
    print("  3. data_transfer_methods.png")
    print("  4. hdfs_structure.png")
    print()
    print("📂 All files saved in current directory")
    print()
