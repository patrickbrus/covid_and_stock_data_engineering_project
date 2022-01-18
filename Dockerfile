FROM apache/airflow:2.2.3

COPY requirements.txt .

ENV RAPID_WEATHER_API_KEY=${RAPID_WEATHER_API_KEY} 

RUN pip3 install -r requirements.txt