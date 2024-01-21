# base image
FROM python:3.9

WORKDIR /app

# install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# expose port 8000
EXPOSE 8000