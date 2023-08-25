# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . /

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "home.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]

# docker buildx build -t fovi-lab .
# docker run -p 8080:8080 --env OPENAI_API_KEY="$OPENAI_API_KEY" fovi-lab
# gcloud builds submit --tag gcr.io/fovi-site/fovi-lab
