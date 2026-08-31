FROM python:3.10-slim
ENV PIP_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "self_storage.wsgi:application"]
