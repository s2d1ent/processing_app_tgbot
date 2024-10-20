FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    sqlite3 \
    build-essential \
    libsqlite3-dev \
    python-is-python3 \
    pip \
    git \
    nano \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/ .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python /app/db_configur.py ./db_dump.sql
RUN python /app/db_configur.py ./db_dump_triggers.sql
RUN python /app/db_configur.py ./db_dump_data.sql

CMD ["bash","-c","python3 /app/main.py"]