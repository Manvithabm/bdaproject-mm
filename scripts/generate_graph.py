#!/usr/bin/env python3
"""
Generate Top 5 States by Total Exports graph with visible labels
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
csv_path = os.path.join(os.path.dirname(__file__), '..', 'yield.csv')
df = pd.read_csv(csv_path)

# Get top 5 states by total exports
top_5_states = df.groupby('state')['total exports'].sum().nlargest(5)

# Create figure with larger size for better visibility
fig, ax = plt.subplots(figsize=(14, 8))

# Create bar chart
bars = ax.bar(range(len(top_5_states)), top_5_states.values, 
              color='#1f77b4', alpha=0.8, edgecolor='black', linewidth=1.5)

# Customize title with larger font
ax.set_title('Top 5 States by Total Exports', fontsize=18, fontweight='bold', pad=20)

# Customize axes with better visibility
ax.set_xlabel('State', fontsize=14, fontweight='bold')
ax.set_ylabel('Exports', fontsize=14, fontweight='bold')

# Set x-axis labels with state names - larger and angled for better visibility
ax.set_xticks(range(len(top_5_states)))
ax.set_xticklabels(top_5_states.index, fontsize=13, fontweight='bold', rotation=0)

# Set y-axis labels
y_ticks = ax.get_yticks()
ax.set_yticklabels([f'{int(y)}' for y in y_ticks], fontsize=12)

# Add value labels on top of bars
for i, (bar, value) in enumerate(zip(bars, top_5_states.values)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(value)}', ha='center', va='bottom', 
            fontsize=12, fontweight='bold')

# Add grid for better readability
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
ax.set_axisbelow(True)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Save figure
output_path = os.path.join(os.path.dirname(__file__), '..', 'graph.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ Graph generated successfully: {output_path}")

# Show stats
print(f"\nTop 5 States by Total Exports:")
for state, exports in top_5_states.items():
    print(f"  {state}: {exports}")

plt.close()
