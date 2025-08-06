# 🚀 Workshop Prerequisites: Apache Airflow Setup

Welcome to the **Data Engineering Workshop**! This guide will help you install Apache Airflow 3.0.3 using `uv` - a modern, fast Python package manager.

> **🎯 Goal:** Get Airflow running on your machine before the workshop starts

## 📋 What You Need

- ✅ **Python 3.9, 3.10, 3.11, or 3.12** (required for Airflow 3.0.3)
- ✅ **Terminal/Command Prompt** access
- ✅ **Internet connection**
- ✅ **Docker Desktop** (Windows users - recommended approach)
- ✅ **Database management tools** (see Additional Tools section)
- ⏱️ **15-20 minutes** (or 10 minutes with Docker)

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

## 🪟 Windows Users: Docker Setup (Recommended)

Due to common compatibility issues on Windows, we **strongly recommend** using Docker for Windows users:

### 📺 Video Tutorial
**Watch this step-by-step setup guide:** [Airflow Windows Setup with Docker](https://youtu.be/ma8OuIz-ai0?si=ItCRf2XwfPZP5bdQ)

### Quick Docker Setup:
1. **Install Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop/)
2. **Download docker-compose.yml** for Airflow
3. **Run:** `docker-compose up -d`
4. **Access:** [http://localhost:8080](http://localhost:8080)

> **💡 Why Docker?** Eliminates `flask-session`, `os.register_at_fork`, and other Windows-specific errors that commonly occur during workshops.

---

### Step 2: Create Project & Install Airflow (non-Windows)

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

uv add pandas

uv add "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### Step 3: Start Airflow (non-Windows)

```bash
# Set Airflow home directory
export AIRFLOW_HOME=$(pwd)/airflow

# Start Airflow
airflow standalone
```

### Step 4: Access the Web Interface

1. Open your browser and go to: [http://localhost:8080](http://localhost:8080)
2. Login with the credentials shown in your terminal (look for `username: admin password: xxxxxxxx`)

## ✅ Test Your Installation (non-Windows)

Run this command to verify everything works:

```bash
airflow tasks test example_bash_operator runme_0 2024-01-01
```

**Success looks like:** You'll see lots of output ending with `Task instance in success state`

## 🛠️ Additional Tools for Workshop

Since this workshop involves working with various databases, please install these essential tools:

### Database Management Tools

**DBeaver (Universal Database Tool):**
- **Download:** [https://dbeaver.io/download/](https://dbeaver.io/download/)
- **Purpose:** Connect to PostgreSQL, MySQL, SQLite, and other SQL databases
- **Why needed:** For viewing and managing relational databases in the workshop

**MongoDB Compass (MongoDB GUI):**
- **Download:** [https://www.mongodb.com/try/download/compass](https://www.mongodb.com/try/download/compass)
- **Purpose:** Visual interface for MongoDB databases
- **Why needed:** For working with NoSQL databases and document collections

> **💡 Installation Tip:** Download and install both tools before the workshop to save time during the session.

## 🔧 Common Issues & Fixes

**Windows users experiencing errors?**
- **Recommended:** Follow the [Docker setup video](https://youtu.be/ma8OuIz-ai0?si=ItCRf2XwfPZP5bdQ) instead
- **Common errors:** `flask-session`, `os.register_at_fork`, compatibility issues

**Port 8080 already in use?**
- Stop Airflow (`Ctrl+C`)
- Edit `airflow/airflow.cfg` 
- Change `port = 8080` to `port = 8081`
- Restart with `airflow standalone`

**Want a clean dashboard?**
- Stop Airflow (`Ctrl+C`)
- Edit `airflow/airflow.cfg`
- Find `load_examples = True` and change to `False`
- Run `airflow db reset` (y option)
- Restart Airflow with `airflow standalone`

## 🆘 Need Help?

Contact the workshop instructor or organizer if you encounter any issues!

## 🎯 Final Step: Ready for Workshop

**You can now turn off Airflow:**
- Press `Ctrl+C` in your terminal to stop Airflow

**When the workshop starts, restart with:**
```bash
cd airflow-workshop
source .venv/bin/activate  # Windows: .venv\Scripts\activate
export AIRFLOW_HOME=$(pwd)/airflow
airflow standalone
```

🎉 **You're all set for the workshop!**

---

> **📖 Want more details?** Check out our [comprehensive installation guide](DETAILED_SETUP.md) for troubleshooting and advanced options.

