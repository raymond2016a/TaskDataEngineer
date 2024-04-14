FROM apache/airflow:latest
# Install additional dependencies
RUN pip install matplotlib
RUN pip install pandas
RUN pip install pyarrow
RUN pip install apache-airflow


USER root

RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean



USER airflow