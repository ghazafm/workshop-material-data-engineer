# 🚀 Workshop Prerequisites: Apache Airflow Setup

Welcome to the **Data Engineering Workshop**! This guide will help you install Apache Airflow 3.0.3 using `uv` - a modern, fast Python package manager.

> **🎯 Goal:** Get Airflow running on your machine before the workshop starts

## 📋 What You Need

- ✅ **Python 3.9, 3.10, 3.11, or 3.12** (required for Airflow 3.0.3)
- ✅ **Terminal/Command Prompt** access
- ✅ **Internet connection**
- ⏱️ **15-20 minutes**

## � Installation Steps

### Step 1: Install uv

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

For more installation options, visit the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### Step 2: Create Project & Install Airflow

```bash
# Create and enter project directory
mkdir airflow-workshop
cd airflow-workshop

# Set up Python environment
uv init --bare
uv sync
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Airflow
AIRFLOW_VERSION=3.0.3
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

uv add "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### Step 3: Start Airflow

```bash
# Set Airflow home directory
export AIRFLOW_HOME=$(pwd)/airflow

# Disacble example dags
AIRFLOW__CORE__LOAD_EXAMPLES=False

# Start Airflow
airflow standalone
```

### Step 4: Access the Web Interface

1. Open your browser and go to: [http://localhost:8080](http://localhost:8080)
2. Login with the credentials shown in your terminal (look for `username: admin password: xxxxxxxx`)

## ✅ Test Your Installation

Run this command to verify everything works:

```bash
airflow tasks test example_bash_operator runme_0 2024-01-01
```

**Success looks like:** You'll see lots of output ending with `Task instance in success state`

## 🔧 Common Issues & Fixes

**Port 8080 already in use?**
- Stop Airflow (`Ctrl+C`)
- Edit `airflow/airflow.cfg` 
- Change `port = 8080` to `port = 8081`
- Restart with `airflow standalone`

**Want a clean dashboard?**
- Stop Airflow (`Ctrl+C`)
- Edit `airflow/airflow.cfg`
- Find `load_examples = True` and change to `False`
- Run `airflow db reset`

## 🆘 Need Help?

Contact the workshop instructor or organizer if you encounter any issues!

---

> **� Want more details?** Check out our [comprehensive installation guide](DETAILED_SETUP.md) for troubleshooting and advanced options.

