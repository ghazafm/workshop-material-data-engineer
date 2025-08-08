from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pandas as pd
from google.cloud import bigquery
import os
import time
from sklearn.preprocessing import LabelEncoder

# Environment variable configuration
BIGQUERY_PROJECT_ID = os.getenv('BIGQUERY_PROJECT_ID', 'workshop-airflow-468305')
BIGQUERY_DATASET_ID = os.getenv('BIGQUERY_DATASET_ID', 'bank_data')
BIGQUERY_TABLE_ID = os.getenv('BIGQUERY_TABLE_ID', 'preprocessed_customer_churn')
GOOGLE_SHEETS_URL = os.getenv('GOOGLE_SHEETS_URL', 'https://docs.google.com/spreadsheets/d/17-5IHQzbn8rlPM29lYwuBjrz8RrQJyHQ/edit?usp=sharing&ouid=112054943148298379262&rtpof=true&sd=true')
GOOGLE_SHEETS_SHEET_NAME = os.getenv('GOOGLE_SHEETS_SHEET_NAME', 'bank_customer_data')

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG definition
dag = DAG(
    'etl_churn_pipeline',
    default_args=default_args,
    description='ETL pipeline for bank customer churn data',
    schedule=timedelta(days=1),
    catchup=False,
    tags=['etl', 'churn', 'bigquery'],
)

def load_data_from_sheets(**context):
    """Load data from Google Sheets"""
    url = GOOGLE_SHEETS_URL
    sheet_name = GOOGLE_SHEETS_SHEET_NAME
    
    file_id = url.split('/d/')[1].split('/edit')[0]
    export_url = f'https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx'
    
    try:
        df = pd.read_excel(export_url, sheet_name=sheet_name)
        print(f"✅ Data loaded successfully from Google Sheets. Shape: {df.shape}")
        
        # Save to temporary CSV for next task
        temp_path = '/tmp/bank_customer_data_raw.csv'
        df.to_csv(temp_path, index=False)
        context['task_instance'].xcom_push(key='temp_file_path', value=temp_path)
        
        return f"Loaded {len(df)} rows successfully"
    except Exception as e:
        print(f"❌ Error loading data from URL: {e}")
        raise

def clean_column_names(df):
    """Clean column names for BigQuery compatibility"""
    cleaned_columns = {}
    for col in df.columns:
        cleaned_col = col.replace('$', 'USD').replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '')
        cleaned_col = ''.join(c for c in cleaned_col if c.isalnum() or c == '_')
        if cleaned_col and cleaned_col[0].isdigit():
            cleaned_col = 'col_' + cleaned_col
        cleaned_columns[col] = cleaned_col
    
    df = df.rename(columns=cleaned_columns)
    return df

def preprocess_data(**context):
    """Preprocess the data for machine learning"""
    temp_path = context['task_instance'].xcom_pull(key='temp_file_path', task_ids='load_data_from_sheets')
    if not temp_path:
        raise ValueError("Could not retrieve file path from previous task")
    df = pd.read_csv(temp_path)
    
    # Drop unnecessary columns
    columns_to_drop = [
        'CLIENTNUM',
        'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1',
        'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2'
    ]
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
    
    # Convert target variable
    df['Attrition_Flag'] = df['Attrition_Flag'].map({'Existing Customer': 0, 'Attrited Customer': 1})
    
    # Encode categorical variables
    if 'Gender' in df.columns:
        le = LabelEncoder()
        df['Gender'] = le.fit_transform(df['Gender'])
    
    # One-hot encode categorical columns
    categorical_cols = ['Education_Level', 'Income_Category', 'Marital_Status', 'Card_Category']
    categorical_cols = [col for col in categorical_cols if col in df.columns]
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    # Clean column names
    df = clean_column_names(df)
    
    # Save preprocessed data
    preprocessed_path = '/tmp/bank_customer_data_preprocessed.csv'
    df.to_csv(preprocessed_path, index=False)
    context['task_instance'].xcom_push(key='preprocessed_file_path', value=preprocessed_path)
    
    print(f"✅ Data preprocessed successfully. Shape: {df.shape}")
    return f"Preprocessed {len(df)} rows successfully"

def upload_to_bigquery(**context):
    """Upload preprocessed data to BigQuery"""
    preprocessed_path = context['task_instance'].xcom_pull(key='preprocessed_file_path', task_ids='preprocess_data')
    if not preprocessed_path:
        raise ValueError("Could not retrieve preprocessed file path from previous task")
    df = pd.read_csv(preprocessed_path)
    
    # BigQuery configuration
    project_id = BIGQUERY_PROJECT_ID
    dataset_id = BIGQUERY_DATASET_ID
    table_id = BIGQUERY_TABLE_ID
    
    # Set up BigQuery client
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/key.json"
    client = bigquery.Client(project=project_id)
    
    table_ref = client.dataset(dataset_id).table(table_id)
    
    try:
        client.get_table(table_ref)
        print(f"ℹ️ Table {dataset_id}.{table_id} exists. Checking for updates...")
        
        query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
        existing_df = client.query(query).to_dataframe()
        
        combined_df = pd.concat([existing_df, df]).drop_duplicates(keep='last')
        print(f"ℹ️ Deduplicated data: {combined_df.shape[0]} rows after combining.")
        
        df_to_upload = combined_df
        write_disposition = "WRITE_TRUNCATE"
    except:
        print(f"ℹ️ Table {dataset_id}.{table_id} does not exist. Creating new table...")
        df_to_upload = df
        write_disposition = "WRITE_TRUNCATE"

    # Upload with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"\n🔄 Upload attempt {attempt + 1}/{max_retries}")
            job_config = bigquery.LoadJobConfig(
                write_disposition=write_disposition,
                autodetect=True,
                create_disposition="CREATE_IF_NEEDED"
            )
            
            job = client.load_table_from_dataframe(
                df_to_upload, table_ref, job_config=job_config
            )
            
            print("⏳ Waiting for job completion...")
            job.result(timeout=300)
            print(f"✅ Successfully uploaded {job.output_rows} rows!")
            
            # Verify upload
            query = f"SELECT COUNT(*) as total FROM `{project_id}.{dataset_id}.{table_id}`"
            result = client.query(query).to_dataframe()
            print(f"✅ Verification: {result['total'][0]} rows in BigQuery")
            
            return f"Successfully uploaded {job.output_rows} rows to BigQuery"
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 30
                print(f"⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("❌ All upload attempts failed!")
                raise

def cleanup_temp_files(**context):
    """Clean up temporary files"""
    import os
    
    temp_path = context['task_instance'].xcom_pull(key='temp_file_path', task_ids='load_data_from_sheets')
    preprocessed_path = context['task_instance'].xcom_pull(key='preprocessed_file_path', task_ids='preprocess_data')
    
    try:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"✅ Removed temporary file: {temp_path}")
        
        if preprocessed_path and os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)
            print(f"✅ Removed preprocessed file: {preprocessed_path}")
            
        return "Cleanup completed successfully"
    except Exception as e:
        print(f"⚠️ Warning during cleanup: {e}")
        return "Cleanup completed with warnings"

# Task definitions
load_data_task = PythonOperator(
    task_id='load_data_from_sheets',
    python_callable=load_data_from_sheets,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

upload_to_bigquery_task = PythonOperator(
    task_id='upload_to_bigquery',
    python_callable=upload_to_bigquery,
    dag=dag,
)

cleanup_task = PythonOperator(
    task_id='cleanup_temp_files',
    python_callable=cleanup_temp_files,
    dag=dag,
)

# Task dependencies
load_data_task >> preprocess_data_task >> upload_to_bigquery_task >> cleanup_task
