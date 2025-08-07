# 🚀 Workshop Prerequisites: Apache Airflow Setup

Welcome to the **Data Engineering Workshop**! This guide provides two methods to install Apache Airflow 3.0.3 for the workshop.

> **🎯 Goal:** Get Airflow running on your machine before the workshop starts

## 📋 What You Need

- ✅ **Docker Desktop** (recommended for all platforms)
- ✅ **Terminal/Command Prompt** access
- ✅ **Internet connection**
- ✅ **Database management tools** (see Additional Tools section)
- ⏱️ **10-15 minutes** (Docker) or **20-25 minutes** (Local installation)

## 🐳 Method 1: Docker Setup (Recommended for All Platforms)

**We strongly recommend using Docker for ALL users** (Windows, macOS, and Linux) because it:
- ✅ Eliminates compatibility issues across different operating systems
- ✅ Provides consistent environment for all workshop participants
- ✅ Includes all necessary dependencies pre-configured
- ✅ Easy to clean up after the workshop

> **⚠️ Note:** Docker will use slightly more system resources (RAM and CPU) but provides the most reliable experience.

### 📺 Video Tutorial
**Watch this step-by-step setup guide:** [Airflow Docker Setup](https://youtu.be/ma8OuIz-ai0?si=ItCRf2XwfPZP5bdQ)

### Quick Docker Setup:
1. **Install Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop/)
2. **Download our optimized docker-compose.yml** from the `Prerequisite/` folder (lightweight version without Celery workers)
3. **Run:** `docker-compose up -d`
4. **Access:** [http://localhost:8080](http://localhost:8080) (airflow/airflow)

### Step-by-Step Docker Instructions:

```bash
# 1. Create workshop directory
mkdir airflow-workshop
cd airflow-workshop

# 2. Copy the optimized docker-compose.yml
# Download from: Prerequisite/docker-compose.yml in this repository
# Or copy from the Prerequisite/ folder

# 3. Set required environment variable
export AIRFLOW_UID=$(id -u)  # Linux/macOS
# For Windows PowerShell: $env:AIRFLOW_UID=50000

# 4. Start Airflow services
docker-compose up -d

# 5. Wait for services to be ready (2-3 minutes)
docker-compose ps

# 6. Access Airflow UI at http://localhost:8080
# Default credentials: airflow/airflow
```

> **💡 Our Optimized Configuration:** The `docker-compose.yml` in the `Prerequisite/` folder is specifically optimized for workshops - it removes resource-heavy components like Celery workers, saving ~40% RAM and CPU usage while maintaining all essential functionality.

---

## 🐍 Method 2: Local Installation with uv (Alternative)

If you prefer local installation or have limited system resources:

### Step 1: Install uv and Python Requirements

> **Prerequisites:** Python 3.9, 3.10, 3.11, or 3.12

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Create Project & Install Airflow

```bash
# Create and enter project directory
mkdir airflow-workshop
cd airflow-workshop

# Set up Python environment
uv init --bare
uv sync
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Airflow with dependencies
AIRFLOW_VERSION=3.0.3
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

uv add pandas flask-appbuilder apache-airflow-task-sdk pyarrow requests

uv add "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

### Step 3: Start Airflow

```bash
# Set Airflow home directory
export AIRFLOW_HOME=$(pwd)/airflow

# Start Airflow
airflow standalone
```

### Step 4: Access the Web Interface

1. Open your browser and go to: [http://localhost:8080](http://localhost:8080)
2. Login with the credentials shown in your terminal (look for `username: admin password: xxxxxxxx`)

## ✅ Test Your Installation

### For Docker Installation:
```bash
# Check if all services are running
docker-compose ps

# Test DAG parsing
docker exec $(docker-compose ps -q airflow-scheduler) airflow dags list
```

### For Local Installation:
```bash
# Test example task
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

### Docker Issues:
**Services not starting properly:**
```bash
# Check service status
docker-compose ps

# View logs for specific service
docker-compose logs airflow-scheduler
docker-compose logs airflow-apiserver

# Restart all services
docker-compose down && docker-compose up -d
```

**Port 8080 already in use:**
- Edit the docker-compose.yml file
- Change `"8080:8080"` to `"8081:8080"` under airflow-apiserver ports
- Restart: `docker-compose down && docker-compose up -d`

### Local Installation Issues:
**Installation errors with uv:**
- **Recommended:** Switch to Docker installation method
- **Common errors:** Package conflicts, OS compatibility issues

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
- Restart Airflow

## 🆘 Need Help?

Contact the workshop instructor or organizer if you encounter any issues!

## 🎯 Final Step: Ready for Workshop

### For Docker Installation:
**Stop Airflow:**
```bash
docker-compose down
```

**When the workshop starts:**
```bash
cd airflow-workshop
docker-compose up -d
# Wait 2-3 minutes, then access http://localhost:8080
```

### For Local Installation:
**Stop Airflow:**
- Press `Ctrl+C` in your terminal

**When the workshop starts:**
```bash
cd airflow-workshop
source .venv/bin/activate  # Windows: .venv\Scripts\activate
export AIRFLOW_HOME=$(pwd)/airflow
airflow standalone
```

🎉 **You're all set for the workshop!**

---

> **📖 Want more details?** Check out our [comprehensive installation guide](DETAILED_SETUP.md) for advanced Docker configuration, troubleshooting, and complete local installation instructions.

