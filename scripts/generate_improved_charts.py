#!/usr/bin/env python3
"""
Generate improved pipeline diagrams with better visibility and proper axes
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

def create_execution_timeline_chart():
    """Create execution timeline as a proper bar chart with visible axes"""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Data
    phases = ['Phase 1:\nEnvironment\nSetup', 
              'Phase 2:\nHadoop\nSetup', 
              'Phase 3:\nMapReduce\nExecution', 
              'Phase 4:\nHive\nAnalytics', 
              'Phase 5:\nSpark MLlib\nExecution']
    times = [2, 2, 3, 1, 5]  # minutes
    colors = ['#87CEEB', '#90EE90', '#FFD700', '#FF8C00', '#FF6B9D']
    
    # Create bar chart
    x_pos = np.arange(len(phases))
    bars = ax.bar(x_pos, times, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Customize axes
    ax.set_ylabel('Time (minutes)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Pipeline Phases', fontsize=14, fontweight='bold')
    ax.set_title('Crop Yield Prediction Pipeline - Execution Timeline', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # X-axis
    ax.set_xticks(x_pos)
    ax.set_xticklabels(phases, fontsize=11, fontweight='bold')
    
    # Y-axis
    ax.set_ylim(0, max(times) + 2)
    ax.set_yticks(range(0, max(times) + 2))
    ax.set_yticklabels([f'{i} min' for i in range(0, max(times) + 2)], fontsize=10)
    
    # Add value labels on bars
    for i, (bar, time) in enumerate(zip(bars, times)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{time} min', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add total time annotation
    total_time = sum(times)
    ax.text(0.5, 0.95, f'Total Execution Time: {total_time} minutes (~{total_time//10}-{total_time*2//10} minutes with overhead)',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#FFE6E6', alpha=0.9, pad=0.7),
            ha='center', va='top')
    
    plt.tight_layout()
    plt.savefig('execution_timeline.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: execution_timeline.png")
    plt.close()

def create_hdfs_capacity_chart():
    """Create HDFS storage capacity visualization"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data - typical sizes after pipeline
    directories = ['Input\n(original)', 'Cleaned\n(deduplicated)', 'Results\n(Hive queries)', 
                  'Models\n(3 trained)', 'Predictions\n(output)']
    sizes = [60, 45, 15, 25, 8]  # MB
    colors = ['#4A90E2', '#50C878', '#FFB700', '#FF6B9D', '#32CD32']
    
    # Create bar chart
    x_pos = np.arange(len(directories))
    bars = ax.bar(x_pos, sizes, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    # Customize axes
    ax.set_ylabel('Size (MB)', fontsize=14, fontweight='bold')
    ax.set_xlabel('HDFS Directories', fontsize=14, fontweight='bold')
    ax.set_title('HDFS Storage Usage by Directory', fontsize=16, fontweight='bold', pad=20)
    
    # X-axis labels with better visibility
    ax.set_xticks(x_pos)
    ax.set_xticklabels(directories, fontsize=11, fontweight='bold')
    
    # Y-axis
    max_size = max(sizes) + 10
    ax.set_ylim(0, max_size)
    ax.set_yticks(range(0, max_size + 5, 10))
    ax.set_yticklabels([f'{i} MB' for i in range(0, max_size + 5, 10)], fontsize=10)
    
    # Add value labels on bars
    for bar, size in zip(bars, sizes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{size} MB', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add total annotation
    total_size = sum(sizes)
    ax.text(0.5, 0.95, f'Total Storage Used: {total_size} MB (~{total_size/1024:.2f} GB)',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#E8F4F8', alpha=0.9, pad=0.7),
            ha='center', va='top')
    
    plt.tight_layout()
    plt.savefig('hdfs_storage_chart.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: hdfs_storage_chart.png")
    plt.close()

def create_model_performance_chart():
    """Create ML model performance comparison chart"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data - model metrics
    models = ['Linear\nRegression', 'Random\nForest', 'Gradient\nBoosting']
    rmse = [1142.28, 1149.12, 1227.14]
    r2 = [0.0050, -0.0070, -0.1483]
    
    # Create grouped bar chart
    x_pos = np.arange(len(models))
    width = 0.35
    
    # Normalize RMSE for visualization (scale down for readability)
    rmse_scaled = [r/100 for r in rmse]
    
    bars1 = ax.bar(x_pos - width/2, rmse_scaled, width, label='RMSE (÷100)',
                   color='#4A90E2', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Create second y-axis for R²
    ax2 = ax.twinx()
    bars2 = ax2.bar(x_pos + width/2, r2, width, label='R² Score',
                    color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Customize primary axes
    ax.set_ylabel('RMSE (scaled ÷100)', fontsize=12, fontweight='bold', color='#4A90E2')
    ax.set_xlabel('ML Models', fontsize=14, fontweight='bold')
    ax.set_title('Spark MLlib Model Performance Comparison', fontsize=16, fontweight='bold', pad=20)
    
    # Customize secondary y-axis
    ax2.set_ylabel('R² Score', fontsize=12, fontweight='bold', color='#FF6B6B')
    
    # X-axis
    ax.set_xticks(x_pos)
    ax.set_xticklabels(models, fontsize=12, fontweight='bold')
    
    # Add value labels
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        
        ax.text(bar1.get_x() + bar1.get_width()/2., height1 + 0.1,
                f'RMSE:\n{rmse[i]:.0f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold', color='#4A90E2')
        
        ax2.text(bar2.get_x() + bar2.get_width()/2., height2 - 0.03,
                f'R²: {r2[i]:.4f}', ha='center', va='top', 
                fontsize=10, fontweight='bold', color='white')
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Legend
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11, framealpha=0.9)
    
    # Add best model annotation
    best_idx = np.argmin(rmse)
    ax.text(0.5, 0.95, f'Best Model: {models[best_idx].replace(chr(10), " ")} (Lowest RMSE)',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#90EE90', alpha=0.9, pad=0.7),
            ha='center', va='top')
    
    plt.tight_layout()
    plt.savefig('model_performance.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: model_performance.png")
    plt.close()

def create_data_volume_progression():
    """Create data volume changes through pipeline stages"""
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Data - rows count at each stage
    stages = ['Original\nData', 'After Download\n(Python)', 'After MapReduce\nCleaning', 
              'Hive Query\nResults', 'Spark\nPredictions']
    rows = [500, 500, 450, 450, 450]  # rows
    labels = ['500', '500', '450\n(50 duplicates\nremoved)', '450', '450']
    colors = ['#E8F4F8', '#4A90E2', '#50C878', '#FFB700', '#FF6B9D']
    
    # Create line + bar combo
    x_pos = np.arange(len(stages))
    line = ax.plot(x_pos, rows, 'o-', linewidth=3, markersize=12, 
                   color='#333', markerfacecolor='#FF6B6B', markeredgecolor='black', 
                   markeredgewidth=2, label='Row Count')
    bars = ax.bar(x_pos, rows, alpha=0.5, color=colors, edgecolor='black', linewidth=2)
    
    # Customize axes
    ax.set_ylabel('Number of Rows', fontsize=14, fontweight='bold')
    ax.set_xlabel('Pipeline Stages', fontsize=14, fontweight='bold')
    ax.set_title('Data Volume Changes Through Pipeline Stages', fontsize=16, fontweight='bold', pad=20)
    
    # X-axis
    ax.set_xticks(x_pos)
    ax.set_xticklabels(stages, fontsize=11, fontweight='bold')
    
    # Y-axis
    ax.set_ylim(400, 550)
    ax.set_yticks(range(400, 551, 25))
    ax.set_yticklabels([f'{i} rows' for i in range(400, 551, 25)], fontsize=10)
    
    # Add value labels
    for i, (x, y, label) in enumerate(zip(x_pos, rows, labels)):
        ax.text(x, y + 5, label, ha='center', va='bottom', 
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=0.3))
    
    # Add data quality annotation
    removed = 50
    ax.annotate('', xy=(2, 450), xytext=(2, 500),
                arrowprops=dict(arrowstyle='<->', color='red', lw=2))
    ax.text(2.3, 475, f'{removed} rows\nremoved', fontsize=10, fontweight='bold',
            color='red', bbox=dict(boxstyle='round', facecolor='#FFE6E6', alpha=0.8))
    
    # Grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Legend
    ax.legend(fontsize=11, loc='lower left', framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('data_volume_progression.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("✅ Created: data_volume_progression.png")
    plt.close()

if __name__ == '__main__':
    print("🎨 Generating Improved Pipeline Charts with Visible Axes...")
    print()
    
    create_execution_timeline_chart()
    create_hdfs_capacity_chart()
    create_model_performance_chart()
    create_data_volume_progression()
    
    print()
    print("=" * 60)
    print("✅ ALL IMPROVED CHARTS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("Generated PNG files (with visible X and Y axes):")
    print("  1. execution_timeline.png - Execution time per phase")
    print("  2. hdfs_storage_chart.png - Storage usage by directory")
    print("  3. model_performance.png - ML model metrics comparison")
    print("  4. data_volume_progression.png - Data rows through stages")
    print()
    print("All charts have:")
    print("  ✓ Visible X-axis with labels")
    print("  ✓ Visible Y-axis with measurements")
    print("  ✓ Grid lines for easy reading")
    print("  ✓ Value labels on bars/lines")
    print("  ✓ Clear titles and legends")
    print()
