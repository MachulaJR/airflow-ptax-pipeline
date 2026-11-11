FROM apache/airflow:3.4.0
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt