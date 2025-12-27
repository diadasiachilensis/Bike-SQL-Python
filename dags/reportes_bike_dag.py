from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
import sys
import os

# Aseguramos que Python encuentre nuestros scripts
sys.path.append('/opt/airflow/scripts')
from etl_utils import extract_top_technicians

default_args = {
    'owner': 'data_engineer',
    'start_date': days_ago(1),
}

def generar_reporte_csv():
    df = extract_top_technicians()
    # Guardamos en la carpeta mapeada 'reports'
    output_file = "/opt/airflow/reports/tecnicos_destacados_2024.csv"
    df.to_csv(output_file, index=False)
    print(f"Reporte generado: {output_file}")

with DAG(
    dag_id='custombikes_reporte_automatizado',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Tarea 1: Verificar conectividad (Simple 'ping' SQL)
    check_db = PostgresOperator(
        task_id='verificar_db',
        postgres_conn_id='postgres_default', # Requiere configurar conexión en Airflow UI después
        sql="SELECT 1;"
    )

    # Tarea 2: Generar el reporte CSV usando Python
    generar_reporte = PythonOperator(
        task_id='exportar_csv_tecnicos',
        python_callable=generar_reporte_csv
    )

    check_db >> generar_reporte