FROM python:3.8.3
ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE = 1
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
COPY . /backend/
