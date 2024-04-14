from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
from airflow.operators.python_operator import BranchPythonOperator
import config

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 13),
    'retries': 1,
}

# Database connection parameters
db_host = config.db_host
db_port = config.db_port
db_name = config.db_name
db_user = config.db_user
db_password = config.db_password

# Function to save DataFrame to PostgreSQL in batches
def save_df_to_postgresql():
    # Define the source and destination file paths
    source_file_path = '/opt/airflow/bucket-source/yellow_tripdata_2024-01.parquet'
    destination_table_name = 'cleaned_data_testing'

    # Read the Parquet file
    table = pq.read_table(source_file_path)
    df = table.to_pandas()
    
    # Filter out rows where passenger_count is not greater than 0
    cleaned_df = df[df['passenger_count'] > 0]

    # Create the database connection string
    db_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Create SQLAlchemy engine
    engine = create_engine(db_string)

    # Define batch size
    batch_size = 10000

    # Calculate number of batches
    num_batches = int(np.ceil(len(cleaned_df) / batch_size))

    print(f"Total batches: {num_batches}")

    # Split DataFrame into batches and insert into PostgreSQL in parallel
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = (i + 1) * batch_size
        batch_df = cleaned_df.iloc[start_idx:end_idx]

        batch_df.to_sql(destination_table_name, engine, if_exists='append', index=False)

        print(f"Batch {i+1} inserted successfully!")

    # Close the database connection
    engine.dispose()

    print("All batches inserted successfully!")

# Function to create and save the plot
def create_and_save_plot():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    # Fetch data
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date_trunc('day', tpep_pickup_datetime) AS day,
               SUM(total_amount) AS total_amount
        FROM cleaned_data_testing
        WHERE EXTRACT(year FROM tpep_pickup_datetime) = 2024
          AND EXTRACT(month FROM tpep_pickup_datetime) = 1
        GROUP BY day
        ORDER BY day;
    """)
    results = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Process data for plotting
    dates = [result[0] for result in results]
    total_amounts = [result[1] for result in results]

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, total_amounts, marker='o')
    plt.title('Total Amount per Day')
    plt.xlabel('Date')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    # Save plot as an image
    plt.savefig('/opt/airflow/plots/total_amount_per_day.png')

# Define the DAG
dag = DAG(
    'testing',
    default_args=default_args,
    description='A DAG to save DataFrame to PostgreSQL and visualize total amount per day',
    schedule_interval=None,
)

# Define the task to save DataFrame to PostgreSQL
save_to_postgresql_task = PythonOperator(
    task_id='save_to_postgresql',
    python_callable=save_df_to_postgresql,
    dag=dag,
)

# Define the task to create and save the plot
create_and_save_plot_task = PythonOperator(
    task_id='create_and_save_plot',
    python_callable=create_and_save_plot,
    dag=dag,
)

# Set task dependencies
save_to_postgresql_task >> create_and_save_plot_task
