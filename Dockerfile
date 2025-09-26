FROM python:3.11-slim

# set workdir
WORKDIR /app

# install system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# copy requirements first for caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# collect static (if used)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# run migrations & start gunicorn (entrypoint handles migrations in railway)
CMD ["gunicorn", "school.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
