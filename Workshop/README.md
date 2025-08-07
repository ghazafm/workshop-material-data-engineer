# Airflow ETL Pipeline for Bank Customer Churn Data

## Struktur Project

```
airflow-docker/
├── dags/
│   └── etl_churn_pipeline.py    # DAG utama untuk ETL pipeline
├── config/
│   └── airflow.cfg              # Konfigurasi Airflow
├── docker-compose.yaml          # Konfigurasi Docker Compose
├── key.json                     # Google Cloud credentials
├── requirements.txt             # Dependencies Python
├── prep.py                      # Script original (tidak digunakan lagi)
└── README.md                    # Dokumentasi ini
```

## Fitur DAG

DAG `etl_churn_pipeline` terdiri dari 4 task:

1. **load_data_from_sheets**: Memuat data dari Google Sheets
2. **preprocess_data**: Melakukan preprocessing data (encoding, cleaning, dll)
3. **upload_to_bigquery**: Upload data ke BigQuery
4. **cleanup_temp_files**: Membersihkan file temporary

## Setup dan Instalasi Lengkap

### 1. Prerequisites
- Docker Desktop terinstall dan running
- Docker Compose terinstall
- Google Cloud Project dengan BigQuery enabled
- Service account key untuk BigQuery (file `key.json`)

### 2. Persiapan File
1. Pastikan file `key.json` ada di root folder project
2. Pastikan file `docker-compose.yaml` sudah terupdate dengan dependencies
3. Pastikan folder `dags/` berisi file `etl_churn_pipeline.py`

### 3. Menjalankan Airflow - Step by Step

#### Step 1: Cek Docker Status
```bash
# Pastikan Docker Desktop running
docker --version
docker-compose --version
```

#### Step 2: Stop Container yang Ada (jika ada)
```bash
# Masuk ke direktori project
cd C:\ARCHIVE\airflow-docker

# Stop container yang sedang berjalan
docker-compose down
```

#### Step 3: Start Airflow dengan Dependencies Baru
```bash
# Start semua container
docker-compose up -d

# Tunggu beberapa menit sampai semua container healthy
```

#### Step 4: Cek Status Container
```bash
# Cek apakah semua container running
docker-compose ps

# Output yang diharapkan: semua container status "Up" dan "healthy"
```

#### Step 5: Copy File Credentials ke Container
```bash
# Copy key.json ke semua container yang diperlukan
docker cp key.json airflow-docker-airflow-worker-1:/opt/airflow/key.json
docker cp key.json airflow-docker-airflow-scheduler-1:/opt/airflow/key.json
docker cp key.json airflow-docker-airflow-dag-processor-1:/opt/airflow/key.json
```

#### Step 6: Verifikasi DAG Terdeteksi
```bash
# Cek apakah DAG sudah terdeteksi
docker exec airflow-docker-airflow-scheduler-1 airflow dags list

# Cari baris yang mengandung "etl_churn_pipeline"
```

#### Step 7: Test DAG
```bash
# Test DAG secara manual
docker exec airflow-docker-airflow-scheduler-1 airflow dags test etl_churn_pipeline 2024-01-01

# Output yang diharapkan: semua task berhasil dengan status "success"
```

### 4. Akses Airflow UI
- Buka browser dan akses: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

### 5. Menjalankan DAG dari UI
1. Buka Airflow UI di browser
2. Cari DAG `etl_churn_pipeline`
3. Klik tombol "Play" (▶️) untuk trigger manual
4. Monitor progress di tab "Graph" atau "Tree"

## Konfigurasi DAG

### Schedule
DAG dijadwalkan untuk berjalan setiap hari (`schedule=timedelta(days=1)`)

### Retry Policy
- Retry: 1 kali
- Retry delay: 5 menit

### Dependencies
DAG menggunakan package berikut (sudah ditambahkan di docker-compose.yaml):
- `pandas>=1.5.0`
- `google-cloud-bigquery>=3.0.0`
- `scikit-learn>=1.0.0`
- `openpyxl>=3.0.0`
- `xlrd>=2.0.0`

### Common Issues dan Solusi

#### Issue 1: DAG Tidak Terdeteksi
**Gejala**: DAG tidak muncul di list
**Solusi**:
```bash
# Cek error import
docker exec airflow-docker-airflow-scheduler-1 airflow dags list-import-errors

# Restart scheduler jika perlu
docker-compose restart airflow-scheduler
```

#### Issue 2: BigQuery Authentication Error
**Gejala**: Error "Could not automatically determine credentials"
**Solusi**:
```bash
# Pastikan key.json sudah di-copy ke container
docker exec airflow-docker-airflow-worker-1 ls -la /opt/airflow/key.json

# Copy ulang jika file tidak ada
docker cp key.json airflow-docker-airflow-worker-1:/opt/airflow/key.json
```

#### Issue 3: Package Import Error
**Gejala**: ModuleNotFoundError saat menjalankan task
**Solusi**:
```bash
# Restart semua container untuk menginstall dependencies baru
docker-compose down
docker-compose up -d

# Tunggu beberapa menit sampai dependencies terinstall
```

#### Issue 4: XCom Error
**Gejala**: "Could not retrieve file path from previous task"
**Solusi**:
- Pastikan task sebelumnya berhasil
- Cek logs task sebelumnya di Airflow UI
- Restart DAG jika perlu

#### Issue 5: Google Sheets Access Error
**Gejala**: Error saat membaca Google Sheets
**Solusi**:
- Pastikan URL Google Sheets dapat diakses secara publik
- Cek koneksi internet
- Pastikan sheet name benar ('bank_customer_data')

### Debugging Commands

#### Cek Logs Container
```bash
# Logs scheduler
docker-compose logs -f airflow-scheduler

# Logs worker
docker-compose logs -f airflow-worker

# Logs semua container
docker-compose logs -f
```

#### Cek Status Task
```bash
# Cek task instances
docker exec airflow-docker-airflow-scheduler-1 airflow tasks list etl_churn_pipeline

# Cek task states
docker exec airflow-docker-airflow-scheduler-1 airflow tasks states-for-dag-run etl_churn_pipeline manual__2024-01-01T00:00:00+00:00
```

#### Test Individual Task
```bash
# Test task tertentu
docker exec airflow-docker-airflow-scheduler-1 airflow tasks test etl_churn_pipeline load_data_from_sheets 2024-01-01
```

## Manual Execution

### Via Command Line
```bash
# Trigger DAG manual
docker exec airflow-docker-airflow-scheduler-1 airflow dags trigger etl_churn_pipeline

# Test DAG (dry run)
docker exec airflow-docker-airflow-scheduler-1 airflow dags test etl_churn_pipeline 2024-01-01
```

### Via Airflow UI
1. Buka Airflow UI: http://localhost:8080
2. Login dengan username: `airflow`, password: `airflow`
3. Pilih DAG `etl_churn_pipeline`
4. Klik tombol "Play" (▶️) untuk trigger manual
5. Monitor progress di tab "Graph" atau "Tree"

## Expected Output

### Successful Run
```
✅ Data loaded successfully from Google Sheets. Shape: (10127, 23)
✅ Data preprocessed successfully. Shape: (10127, 33)
✅ Successfully uploaded 10127 rows!
✅ Verification: 10127 rows in BigQuery
✅ Removed temporary file: /tmp/bank_customer_data_raw.csv
✅ Removed preprocessed file: /tmp/bank_customer_data_preprocessed.csv
```

### Task Status di UI
- `load_data_from_sheets`: ✅ Success
- `preprocess_data`: ✅ Success  
- `upload_to_bigquery`: ✅ Success
- `cleanup_temp_files`: ✅ Success

## Next Steps (for improvements) (optinal)

1. **Add Data Validation**: Tambahkan task untuk validasi data sebelum upload
2. **Add Notifications**: Integrasikan dengan Slack/Email untuk notifikasi
3. **Add Data Quality Checks**: Implementasi data quality monitoring
4. **Add ML Model Training**: Tambahkan task untuk training model churn prediction
5. **Add Monitoring Dashboard**: Buat dashboard untuk monitoring pipeline performance
