# TaskDataEngineer
Initial Data Task (Data Engineer)


# Project Overview

This project involves setting up Apache Airflow and a PostgreSQL database using Docker containers. Apache Airflow is used to orchestrate the data pipeline, which includes processing taxi trip data, cleaning it, storing it in a PostgreSQL database, and visualizing the total amount of fares per day for January 2024.

# Setup Instructions

## Building Docker Image in Visual Studio:

1. Clone this repository to your local machine.
2. Open Visual Studio.
3. Navigate to the directory containing the `Dockerfile`.
4. Right-click on the `Dockerfile` and select "Build Image".
5. Follow the prompts to build the Docker image.

Once the build process is complete, you'll have a Docker image ready to use for running containers.

## Running Docker Compose in Visual Studio:

1. changed the following credentials in  `docker-compose.yml`: `POSTGRES_USER`,`POSTGRES_PASSWORD`,`POSTGRES_DB`
2. Navigate to the directory containing the `docker-compose.yml` file.
3. Right-click on the `docker-compose.yml` file and select "Compose Up".
4. This will start two services: `sleek-airflow` and `postgresql`.
5. Access Apache Airflow UI by visiting `http://localhost:8080` in your web browser.
6. Use the default username (`airflow`) and the password generated in `standalone_admin_password.txt` to log in to Apache Airflow.
7. Once logged in, you can find and trigger the `testing` DAG to execute the data processing and visualization tasks.

# Execution Instructions

To run the code and generate the visualization using the Docker containers:
1.  Modify the database connection parameters (`db_host`, `db_port`, `db_name`, `db_user`, `db_password`) in the Python scripts `workflow.py` to match your PostgreSQL setup.
2. Ensure that the Parquet data file (`yellow_tripdata_2024-01.parquet`) is located in the specified source directory (`/opt/airflow/bucket-source/`).
3. Trigger the `testing` DAG in Apache Airflow to execute the data processing and visualization tasks.
4. Once the DAG is executed successfully, you can find the generated plot image (`total_amount_per_day.png`) in the specified output directory (`/opt/airflow/plots/`).
![total_amount_per_day](https://github.com/raymond2016a/DATATASK/assets/23325685/4778b2a0-5689-4f79-8ff0-3be86e05d8b3)

# Discussion

This project demonstrates a data pipeline for processing taxi trip data, cleaning it, storing it in a PostgreSQL database, and visualizing the total amount of fares per day. Challenges faced during development include handling large datasets efficiently and ensuring data consistency during insertion into the database. Due to the limited capacity of the laptop environment, processing the entire dataset in one go was not feasible. Therefore, the approach of breaking the processing into batches was adopted to manage memory usage effectively and prevent performance issues. Assumptions were made regarding the structure and format of the input data and the availability of necessary libraries and resources.

You can customize this template according to your project specifics and add more details as needed.

