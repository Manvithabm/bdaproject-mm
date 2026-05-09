#!/bin/bash
# Hadoop Configuration

# Set Hadoop paths
export HADOOP_HOME=${HADOOP_HOME:-/usr/local/hadoop}
export HADOOP_HDFS_HOME=${HADOOP_HDFS_HOME:-$HADOOP_HOME}
export HADOOP_MAPRED_HOME=${HADOOP_MAPRED_HOME:-$HADOOP_HOME}
export HADOOP_YARN_HOME=${HADOOP_YARN_HOME:-$HADOOP_HOME}
export HADOOP_COMMON_HOME=${HADOOP_COMMON_HOME:-$HADOOP_HOME}

# Add to PATH
export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

# Java Home (adjust based on your system)
export JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-11-openjdk-amd64}

# Hadoop log directory
export HADOOP_LOG_DIR=${HADOOP_LOG_DIR:-$HADOOP_HOME/logs}

echo "Hadoop configuration loaded"
echo "HADOOP_HOME: $HADOOP_HOME"
echo "JAVA_HOME: $JAVA_HOME"
