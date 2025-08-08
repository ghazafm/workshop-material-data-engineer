# 🚀 Welcome to the Data Engineering Workshop!
## Apache Airflow Installation Guide

Welcome to our **Data Engineering Workshop**! This comprehensive guide provides detailed instructions for installing **Apache Airflow 3.0.3** using two different approaches.

> **🎯 Workshop Goal:** By the end of this installation, you'll have a fully functional Airflow environment ready for our hands-on data engineering exercises.

## 🔍 Installation Methods Overview

We offer **two installation methods** with different trade-offs:

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Docker** 🐳 | ✅ Cross-platform consistency<br>✅ No dependency conflicts<br>✅ Easy cleanup<br>✅ Pre-configured environment | ⚠️ Uses more resources (RAM/CPU)<br>⚠️ Requires Docker knowledge | **Recommended for all users** |
| **Local (uv)** 🐍 | ✅ Lower resource usage<br>✅ Direct Python access<br>✅ Faster startup | ⚠️ OS-specific issues<br>⚠️ Dependency conflicts<br>⚠️ Complex troubleshooting | Power users with specific needs |

## 🐳 Method 1: Docker Installation (Recommended)

### Why Docker for Everyone?

Originally, we recommended Docker only for Windows users, but after extensive testing across different platforms, we now **strongly recommend Docker for ALL users** because:

- **🔄 Consistent Experience:** Everyone gets the same environment regardless of OS
- **⚡ Faster Setup:** No need to worry about Python versions, dependencies, or OS-specific issues  
- **🧹 Easy Cleanup:** Simply run `docker-compose down` to remove everything
- **🔧 Pre-configured:** Our optimized docker-compose.yml eliminates unnecessary services

### Resource Usage Note

> **⚠️ Resource Impact:** Docker will use approximately:
> - **2-4 GB RAM** (vs 1-2 GB for local installation)
> - **Additional CPU** for containerization overhead
> - **2-3 GB disk space** for Docker images
>
> **💡 Trade-off:** Slightly higher resource usage for significantly better reliability and consistency across all workshop participants.

### Prerequisites for Docker Method

- ✅ **Docker Desktop** installed and running
- ✅ **8 GB RAM minimum** (16 GB recommended)
- ✅ **Terminal/Command Prompt** access
- ✅ **Internet connection** for downloading images
- ⏱️ **10-15 minutes** setup time

### Docker Installation Steps

```bash
export AIRFLOW_HOME=~/airflow
```

#### Step 1: Install Docker Desktop

**Download and install Docker Desktop:**
- **Windows:** [Download Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe)
- **macOS:** [Download Docker Desktop for Mac](https://desktop.docker.com/mac/main/amd64/Docker.dmg) (Intel) or [Apple Silicon](https://desktop.docker.com/mac/main/arm64/Docker.dmg)
- **Linux:** Follow [Docker Engine installation guide](https://docs.docker.com/engine/install/) for your distribution

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

#### Step 2: Download Workshop Files

```bash
# Create workshop directory
mkdir airflow-workshop
cd airflow-workshop

# Download our optimized docker-compose.yml
# Copy the docker-compose.yml from the Prerequisite folder or download from:
# https://github.com/ghazafm/workshop-material-data-engineer/blob/master/Prerequisite/docker-compose.yml

# Alternative: Create minimal docker-compose.yml (see below)
```

#### Step 3: Our Optimized Docker Compose Configuration

Our `docker-compose.yml` is specifically optimized for workshops by removing resource-heavy components:

**✅ What's included:**
- PostgreSQL database (metadata storage)
- Airflow API Server (web interface)
- Airflow Scheduler (DAG processing)  
- Airflow DAG Processor (separate process for parsing DAGs)
- Initialization service

**❌ What's removed to save resources:**
- Celery Worker (not needed for local development)
- Redis (not needed without Celery)
- Flower (Celery monitoring - not needed)
- Additional worker nodes

> **💡 Resource Savings:** Our configuration uses ~40% less RAM and CPU compared to the full Airflow Docker setup.

#### Step 4: Set Environment Variables

```bash
# For Linux/macOS
export AIRFLOW_UID=$(id -u)

# For Windows PowerShell
$env:AIRFLOW_UID=50000

# For Windows Command Prompt
set AIRFLOW_UID=50000
```

#### Step 5: Start Airflow Services

```bash
# Start all services in background
docker-compose up -d

# Monitor startup progress (optional)
docker-compose logs -f airflow-init

# Check service status
docker-compose ps
```

**Expected Output:**
```
NAME                                    STATUS
airflow-workshop_airflow-apiserver_1    Up (healthy)
airflow-workshop_airflow-dag-processor_1 Up (healthy) 
airflow-workshop_airflow-scheduler_1    Up (healthy)
airflow-workshop_postgres_1             Up (healthy)
```

#### Step 6: Access Airflow Web Interface

1. **Wait for services to be ready** (2-3 minutes for first startup)
2. **Open browser:** [http://localhost:8080](http://localhost:8080)
3. **Login credentials:**
   - Username: `airflow`
   - Password: `airflow`

#### Step 7: Verify Installation

```bash
# List available DAGs
docker exec $(docker-compose ps -q airflow-scheduler) airflow dags list

# Test a simple command
docker exec $(docker-compose ps -q airflow-scheduler) airflow version
```

### Docker Management Commands

```bash
# Stop all services
docker-compose down

# Start services
docker-compose up -d

# View logs
docker-compose logs airflow-scheduler
docker-compose logs airflow-apiserver

# Restart specific service
docker-compose restart airflow-scheduler

# Remove everything (including volumes)
docker-compose down -v
```

---

## 🐍 Method 2: Local Installation with uv

> **⚠️ Note:** This method is more complex and can have OS-specific issues. We recommend the Docker method above for most users.

### Prerequisites for Local Method

- ✅ **Python 3.9, 3.10, 3.11, or 3.12** (required for Airflow 3.0.3)
- ✅ **Terminal/Command Prompt** access
- ✅ **Internet connection** for downloading packages
- ⏱️ **20-25 minutes** setup time

### Step 1: Install uv

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 2: Set Airflow Home (Optional)

```bash
# Set Airflow home to current project directory (recommended)
export AIRFLOW_HOME=$(pwd)/airflow
```

### Step 3: Create Virtual Environment with uv

```bash
# Create a new project directory
mkdir airflow-workshop
cd airflow-workshop

# Initialize a new uv project
uv init --bare
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 4: Install Apache Airflow with uv

```bash
# Set Airflow version
AIRFLOW_VERSION=3.0.3

# Get Python version
PYTHON_VERSION="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"

# Set constraint URL
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# Install Airflow using uv
uv add "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

> **What are constraints?** Constraint files ensure all dependencies are compatible with each other, preventing version conflicts.

## 🚀 Step 5: Initialize and Run Airflow

```bash
# Initialize database and start all components
airflow standalone
```

### 🔧 Troubleshooting Port Issues

If you encounter `"[Errno 48] Address already in use"`:

1. **Stop Airflow** with `Ctrl + C`
2. **Navigate** to the `airflow` folder
3. **Edit** the `airflow.cfg` file
4. **Find** the line `port = 8080`
5. **Change** it to `port = 8081` (or any available port)
6. **Restart** Airflow with `airflow standalone`

## 🧹 Step 6: Clean Configuration (Recommended)

For a cleaner workshop experience, disable example DAGs:

1. **Stop Airflow** with `Ctrl + C`
2. **Edit** `airflow/airflow.cfg`
3. **Search** for `load_examples`
4. **Change** the value to `False`:
   ```cfg
   # Find this line in the [core] section:
   load_examples = True
   
   # Change it to:
   load_examples = False
   ```
5. **Reset the database** to remove existing examples:
   ```bash
   airflow db reset
   ```

> **💡 Why disable examples?** This gives you a clean dashboard without clutter, making it easier to focus on your own DAGs during the workshop.

## 🌐 Step 7: Access Airflow UI

Visit [http://localhost:8080](http://localhost:8080) (or the port you defined in the config file) in your browser and log in with the admin credentials.

### 🔑 Finding Your Login Credentials

When you run `airflow standalone`, the admin credentials are displayed in the terminal output. Look for lines like:
```
standalone | Airflow is ready
standalone | Login with username: admin  password: xxxxxxxx
standalone | Airflow standalone is ready.
```

**Alternative:** You can also find the credentials in the `airflow/simple_auth_manager_passwords.json.generated` file.

### 🎉 What You'll See

Once logged in, you'll see the Airflow web interface with:
- **📊 Dashboard**: Overview of your DAGs and their status
- **🔄 DAGs**: List of all available workflows
- **📝 Task Instances**: Individual task execution details
- **⚙️ Admin**: Configuration and connection settings

> **💡 First Time Tip:** If you disabled example DAGs in Step 6, you'll see a clean, empty dashboard - perfect for starting fresh!

## 🔌 Installing Airflow Providers (Optional)

> **⚠️ Note:** You don't need this for now, but you'll probably need additional providers during the workshop.

Airflow providers extend functionality with integrations to third-party services. Install providers using `uv add`:

### Popular Providers

```bash
# Amazon Web Services
uv add "apache-airflow-providers-amazon"

# Google Cloud Platform
uv add "apache-airflow-providers-google"

# Microsoft Azure
uv add "apache-airflow-providers-microsoft-azure"

# PostgreSQL
uv add "apache-airflow-providers-postgres"

# HTTP requests
uv add "apache-airflow-providers-http"

# Docker
uv add "apache-airflow-providers-docker"

# Kubernetes
uv add "apache-airflow-providers-cncf-kubernetes"
```

> **Note:** You'll probably need additional providers during this workshop.

### Complete Provider List

For a comprehensive list of available providers, visit:
- [Official Airflow Providers Documentation](https://airflow.apache.org/docs/#providers-packages)
- [Provider Packages Documentation](https://airflow.apache.org/docs/apache-airflow-providers/)

### Popular Provider Categories

| Category | Provider Package | Description |
|----------|------------------|-------------|
| **Cloud Platforms** |
| Amazon | `apache-airflow-providers-amazon` | AWS services (S3, EC2, RDS, etc.) |
| Google | `apache-airflow-providers-google` | GCP services (BigQuery, GCS, etc.) |
| Microsoft Azure | `apache-airflow-providers-microsoft-azure` | Azure services |
| **Databases** |
| PostgreSQL | `apache-airflow-providers-postgres` | PostgreSQL database |
| MySQL | `apache-airflow-providers-mysql` | MySQL database |
| MongoDB | `apache-airflow-providers-mongo` | MongoDB database |
| **Data Processing** |
| Apache Spark | `apache-airflow-providers-apache-spark` | Spark jobs |
| Databricks | `apache-airflow-providers-databricks` | Databricks platform |
| dbt Cloud | `apache-airflow-providers-dbt-cloud` | dbt transformations |
| **Communication** |
| Slack | `apache-airflow-providers-slack` | Slack notifications |
| Email/SMTP | `apache-airflow-providers-smtp` | Email notifications |
| **Containerization** |
| Docker | `apache-airflow-providers-docker` | Docker containers |
| Kubernetes | `apache-airflow-providers-cncf-kubernetes` | Kubernetes jobs |

## ✅ Testing Your Installation

Run a simple test to verify everything works:

```bash
# Test a simple task
airflow tasks test example_bash_operator runme_0 2024-01-01
```

### 🎯 What You'll See

When you run the test command, you'll see **a lot of output**. **This is completely normal!** Airflow 3.0.3 provides detailed logging for transparency. Here's what to look for:

#### ✅ **Success Indicators (Look for these key lines):**
```
[INFO] Running command: ['/bin/bash', '-c', 'echo "example_bash_operator__runme_0__20240101" && sleep 1']
[INFO] Output:
[INFO] example_bash_operator__runme_0__20240101
[INFO] Command exited with return code 0
Task instance in success state
```

#### ⚠️ **Normal Warnings (You Can Safely Ignore These):**
```
WARNING - Could not import DAGs in example_local_kubernetes_executor.py
WARNING - Install Kubernetes dependencies with: pip install apache-airflow[cncf.kubernetes]
WARNING - The example_kubernetes_executor example DAG requires the kubernetes provider
INFO - The hook_class '...' is not fully initialized (UI widgets will be missing)
```

> **💡 Don't panic about the verbose output!** All that detailed logging is Airflow 3.0.3's new enhanced debugging system working as intended.

### 🔍 **Understanding the Verbose Output**

The detailed output includes:
- **🔄 DAG Discovery**: Airflow scanning for workflow definitions
- **📊 Task Lifecycle**: Step-by-step task state transitions  
- **🐛 Debug Information**: Internal task execution details (new in 3.0.3)
- **✅ Success Confirmation**: Final task completion status

#### **🎯 Key Success Markers:**
1. ✅ `Task instance in success state` (at the very end)
2. ✅ `Command exited with return code 0`
3. ✅ The actual output: `example_bash_operator__runme_0__20240101`

### 🚨 **When Something Actually Goes Wrong**

If the test fails, you'll see:
- ❌ `Task instance in failed state`
- 🔴 Messages with `ERROR` level (not just warnings)
- ⚠️ Non-zero return codes

**Troubleshooting steps:**
1. Ensure your virtual environment is activated: `source .venv/bin/activate`
2. Verify Airflow installation: `airflow version`
3. Check for actual ERROR messages (warnings are fine)

## 🎯 Next Steps

1. **Enable Example DAGs**: In the Airflow UI, enable the `example_bash_operator` DAG to see it in action
2. **Create Your First DAG**: Start building your own workflows
3. **Install Relevant Providers**: Add the providers you need for your use case
4. **Configure Connections**: Set up connections to external services in the Airflow UI

## 📚 Useful Resources

- [Airflow Documentation](https://airflow.apache.org/docs/apache-airflow/stable/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Airflow Tutorials](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html)
- [Provider Packages](https://airflow.apache.org/docs/apache-airflow-providers/)

## 🔧 Troubleshooting

### Common Issues

1. **Permission Errors**: Make sure your virtual environment is activated
2. **Port 8080 in Use**: Change the port in the `airflow.cfg` file
3. **Database Issues**: Try `airflow db reset` to reset the database

### Getting Help

If you encounter any issues during the installation or have questions about this workshop:

- **🎓 Workshop Support**: Contact the instructor or workshop organizer
- **💬 Direct Contact**: Reach out via workshop communication channels
- **🔧 Technical Issues**: Share your error messages and we'll help troubleshoot

For general Airflow questions beyond this workshop:
- [Airflow Slack Community](https://apache-airflow-slack.herokuapp.com/)
- [GitHub Issues](https://github.com/apache/airflow/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/airflow)
