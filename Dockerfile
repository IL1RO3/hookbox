FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /app
CMD ["python3", "manage.py", "runserver" , "0.0.0.0:8000"]


