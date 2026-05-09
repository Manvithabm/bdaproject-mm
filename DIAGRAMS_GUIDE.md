# 📊 Pipeline Diagrams - Visual Guide

## Overview
This directory contains high-quality PNG diagrams of the complete Crop Yield Prediction pipeline. These visual representations make it easy to understand the architecture and execution flow.

---

## 📸 Generated Diagrams

### 1. **pipeline_architecture.png** 🏗️
**Complete Pipeline Architecture Diagram**

Shows the entire data flow from Windows Python scripts through Ubuntu Hadoop cluster processing to final results.

**What it shows:**
- 🪟 Windows environment: Data generation scripts
- 📤 Data transfer to Ubuntu
- 🗂️ HDFS storage locations
- 🔄 MapReduce data cleaning
- 📊 Hive SQL analytics
- ⚙️ Spark MLlib ML models
- 📥 Results download back to Windows

**Key Sections:**
```
Windows (download_data.py) 
    ↓
CSV Files (cleaned_*.csv)
    ↓ (transfer)
Ubuntu (HDFS)
    ↓
MapReduce (DataCleaning.java)
    ↓
Hive (crop_trends.hql) + Spark MLlib (3 models)
    ↓
Results & Models
    ↓ (download)
Windows (Analysis)
```

---

### 2. **execution_phases.png** ⏱️
**Pipeline Execution Phases Flowchart**

Shows the 5 sequential phases of pipeline execution with timing information.

**Phases:**
1. **Phase 1: Environment Setup** (~2 min)
   - Configure Spark, Hadoop, Hive
   - Verify all services

2. **Phase 2: Hadoop Setup** (~2 min)
   - Start Hadoop/YARN services
   - Create HDFS directories

3. **Phase 3: MapReduce Execution** (~3 min)
   - Compile DataCleaning.java
   - Run distributed data cleaning

4. **Phase 4: Hive Analytics** (~1 min)
   - Create external table
   - Execute 8 SQL queries

5. **Phase 5: Spark MLlib Execution** (~5 min)
   - Train 3 regression models
   - Generate predictions

**Total Time: 10-20 minutes**

---

### 3. **data_transfer_methods.png** 🔄
**Data Transfer Options: Windows → Ubuntu**

Shows the 4 different methods to transfer data from Windows to Ubuntu.

**Methods:**
1. **Option 1: WSL** (Windows Subsystem for Linux)
   - Best for: Same machine, fastest
   - Command: `Copy-Item -Path ... -Destination "\\wsl$\Ubuntu\..."`

2. **Option 2: SCP** (Secure Copy)
   - Best for: Separate machines, remote servers
   - Command: `scp -r data ubuntu_user@ubuntu_ip:~/crop_data/`

3. **Option 3: Samba Share** (Network File Sharing)
   - Best for: Network share, multiple transfers
   - Configure SMB and mount network drive

4. **Option 4: Docker** (Containerized)
   - Best for: Complete isolation, reproducibility
   - Use volume mounts for data

**All methods → Ubuntu ~/crop_data/ → HDFS /crop_yield/input**

---

### 4. **hdfs_structure.png** 📁
**HDFS Directory Structure**

Shows the directory layout and content after pipeline execution completes.

**Directory Structure:**
```
/crop_yield/
├── input/          - Original cleaned CSV files
├── cleaned/        - MapReduce deduplicated data
├── results/        - Hive query results (8 queries)
├── models/         - Trained Spark MLlib models
│   ├── LinearRegression_model/     (Best selected)
│   ├── RandomForest_model/
│   └── GradientBoosting_model/
└── predictions/    - Yield predictions CSV
```

---

## 🎨 Color Coding in Diagrams

| Color | Meaning | Examples |
|-------|---------|----------|
| 🔵 Blue | Windows/Input | Windows, Original Data |
| 🟢 Green | Ubuntu/Processing | Ubuntu Cluster, Final Results |
| 🟡 Yellow | HDFS Storage | HDFS directories |
| 🔴 Red | Results/Download | Download, Final Output |
| 🟦 Light Blue | Setup/Config | Environment Setup |
| 🟩 Light Green | Analytics | Hive, Spark MLlib |

---

## 📖 How to Use These Diagrams

1. **Planning Phase**: Use `pipeline_architecture.png` to understand overall flow
2. **Setup Phase**: Reference `data_transfer_methods.png` to transfer data
3. **Execution Phase**: Follow `execution_phases.png` for step-by-step execution
4. **Monitoring Phase**: Check `hdfs_structure.png` to verify directory contents

---

## 🔧 Regenerating Diagrams

If you need to regenerate these diagrams or modify them:

```bash
# Run the diagram generator script
python scripts/generate_pipeline_diagrams.py

# This will create 4 PNG files:
# - pipeline_architecture.png
# - execution_phases.png
# - data_transfer_methods.png
# - hdfs_structure.png
```

**Requirements:**
- Python 3.7+
- matplotlib
- numpy

**Installation:**
```bash
pip install matplotlib numpy
```

---

## 📊 Integration with Documentation

These diagrams are referenced in:
- [START_HERE.md](START_HERE.md) - Overview with pipeline diagram
- [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md) - Phases diagram
- [DATA_TRANSFER_GUIDE.md](DATA_TRANSFER_GUIDE.md) - Transfer methods diagram
- [HADOOP_HIVE_SPARK_COMPLETION.md](HADOOP_HIVE_SPARK_COMPLETION.md) - Architecture diagram

---

## 🖼️ Viewing Diagrams

**On Windows:**
- Double-click PNG file to open in default image viewer
- Or right-click → "Open with" → Choose application

**In VS Code:**
- Open Explorer and find .png file
- Click to preview in editor

**On Web:**
- Upload to your project wiki
- Include in GitHub README
- Embed in documentation

---

## 📏 Diagram Specifications

| Diagram | Size | DPI | Format |
|---------|------|-----|--------|
| pipeline_architecture.png | 425 KB | 300 | PNG |
| execution_phases.png | 171 KB | 300 | PNG |
| data_transfer_methods.png | 260 KB | 300 | PNG |
| hdfs_structure.png | 278 KB | 300 | PNG |
| **Total** | **1.1 MB** | **300 DPI** | **PNG** |

High DPI (300) ensures diagrams are print-quality and readable at any size.

---

## 🚀 Next Steps

1. **Review Diagrams**: Open each PNG to understand the pipeline
2. **Follow EXECUTION_GUIDE.md**: Use execution phases for step-by-step execution
3. **Monitor Progress**: Check HDFS structure to verify completion
4. **Analyze Results**: Review predictions and model performance

---

## 💡 Tips

- **Print-Friendly**: All diagrams are print-quality (300 DPI)
- **Share-Ready**: Send PNG files to team members
- **Presentation**: Use in Powerpoint/Keynote presentations
- **Documentation**: Embed in project documentation
- **Reference**: Keep open while following execution guide

---

## 📞 Support

If diagrams are unclear or you need modifications:
1. Check the source script: `scripts/generate_pipeline_diagrams.py`
2. Modify colors/labels in the Python script
3. Run again to regenerate with your changes
4. Commit updated diagrams to version control

---

**Diagrams Generated**: May 5, 2026  
**Quality**: High-resolution (300 DPI) PNG format  
**Status**: ✅ Ready for use in presentations and documentation

