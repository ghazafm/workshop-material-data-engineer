# Data Engineering Workshop - Weather Data Collection

Welcome to the Data Engineering Workshop! Your mission is to collect weather data from various cities around the world that are distributed across different storage systems and formats.

## 📊 Data Distribution Overview

The weather data has been distributed across multiple storage systems to simulate real-world data engineering challenges:

### Storage Systems & Datasets

| Storage Type | Location | Datasets | Format | Access Method |
|-------------|----------|----------|---------|---------------|
| **API Server** | Alibaba Cloud VM | Asia, Unknown | Parquet | HTTP REST API |
| **MinIO (S3)** | Object Storage | Europe, Antarctica | Parquet, HTML | S3 Compatible API |
| **PostgreSQL** | Cloud Database | Africa, North America | Tables | SQL Connection |
| **MongoDB** | Document Database | South America, Oceania | Collections | MongoDB Connection |

## 🔑 Access Credentials

All access credentials will be provided during the workshop session. **These are read-only credentials** for data access only.

```bash
# Environment file will be provided in class
# Make sure to load it properly in your scripts
```

## 🚀 Data Access Guide

### 1. API Server (Cloud VM)
**Datasets:** Asia, Unknown

**Access Method:**
```python
import requests
import pandas as pd

# Discover available endpoints
response = requests.get("http://<SERVER_IP>/datasets")
# Download data using REST API calls
```

**Tips:**
- Start with: `curl <SERVER_IP>` to explore available endpoints
- Check API documentation or use `/help` endpoints
- Data might be in binary format

### 2. MinIO (S3 Compatible Storage)
**Datasets:** Europe, Antarctica

**Access Method:**
```python
from minio import Minio
# Use environment variables for connection
# Explore bucket contents and download files
```

**Tips:**
- Review [MinIO Python SDK Documentation](https://github.com/minio/minio-py/blob/master/docs/API.md)
- Check bucket policies and object permissions
- Files may be in different formats

### 3. PostgreSQL Database
**Datasets:** Africa, North America

**Access Method:**
```python
import pandas as pd
from sqlalchemy import create_engine
# Build connection string from environment variables
# Query database tables
```

**Tips:**
- Use `INFORMATION_SCHEMA` to discover table structures
- Explore with `\dt` command in psql
- Consider connection pooling for large datasets
- **GUI Option:** Use DBeaver, pgAdmin, or any PostgreSQL client for visual exploration

### 4. MongoDB
**Datasets:** South America, Oceania

**Access Method:**
```python
import pymongo
import pandas as pd
# Connect using connection URI
# Explore collections and documents
```

**Tips:**
- Use `client.list_database_names()` and `db.list_collection_names()` in Python
- Or use `show collections` in MongoDB shell (mongosh)
- Handle nested JSON structures appropriately
- **GUI Option:** Use MongoDB Compass or any MongoDB client for visual exploration

## 🛠️ Quick Start Scripts

### Environment Setup
```bash
# Install required packages
uv add pandas pymongo sqlalchemy psycopg2-binary minio requests pyarrow

# Or using pip
pip install pandas pymongo sqlalchemy psycopg2-binary minio requests pyarrow
```

### Sample Data Pipeline (Airflow)
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def collect_all_data():
    """Collect data from all sources"""
    dataframes = {}
    
    # Task 1: API Data Collection
    # Task 2: Object Storage Data Collection  
    # Task 3: Database Data Collection
    # Task 4: Document Store Data Collection
    
    return dataframes

# Define your DAG structure
# Consider task dependencies and parallel execution
```

## 🧩 Data Challenges

Be prepared for these data quality issues:
- **Encoded text fields** (requires decoding)
- **Character-shifted values** (investigation needed)
- **Mixed data formats** (CSV, Parquet, HTML, JSON)
- **Randomized column order**
- **Inconsistent schemas across sources**

## Workshop Objective

Your ultimate goal is to build a complete **Extract, Transform, Load (ETL)** pipeline that:

1. **Extracts** weather data from all 4 distributed storage systems
2. **Transforms** the data by cleaning, normalizing, and combining it
3. **Loads** the final unified dataset into a **PostgreSQL database**

### Final Destination: PostgreSQL Database

After successfully collecting and transforming data from all sources, you must load the cleaned dataset into a PostgreSQL database. The target database connection details and required table schema will be provided during the workshop session.

**Loading Requirements:**
- All continent data must be combined into a single table
- Data must be properly cleaned and validated before loading
- Ensure data types are consistent with the target schema

*Note: The specific database connection details and target table columns will be revealed during the workshop to maintain the challenge level.*

## 🏆 Success Criteria

Your pipeline should:
1. ✅ Collect data from all storage systems
2. ✅ Handle different data formats correctly
3. ✅ Clean the data
4. ✅ Combine into a unified dataset
5. ✅ Load into the PostgreSQL target database efficiently

## 🚨 Important Notes

- **Read-only access**: You cannot modify source data
- **Time constraint**: Work efficiently and quickly
- **Documentation**: Document your approach and solutions
- **Performance**: Consider chunking for large datasets

## 📝 Deliverables

1. **Data collection script** that retrieves data from all sources
2. **Data cleaning pipeline** that handles corrupted data
3. **Unified dataset** combining all continents
4. **Documentation** explaining your approach
5. **Performance metrics** (execution time, data volume)

## 🔧 Troubleshooting

### Common Issues:
- **Connection timeouts**: Implement retry logic
- **Large datasets**: Use chunking and streaming
- **Memory issues**: Process data in batches
- **Authentication errors**: Verify credentials in `.env`
- **Network issues**: Check connectivity to each service

### Useful Commands:
```bash
# Test connections
python -c "import pymongo; print('MongoDB OK')"
python -c "import psycopg2; print('PostgreSQL OK')"
python -c "from minio import Minio; print('MinIO OK')"

# Check environment variables
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print([k for k in os.environ.keys() if any(x in k for x in ['MONGO', 'POSTGRES', 'S3'])])"
```

Good luck with your data engineering mission! 🚀

---
*Workshop Material - Data Engineer*