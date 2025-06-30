#!/bin/bash

echo "⏳ Waiting for MySQL to be ready..."

# Wait for MySQL
until python -c "
import socket
s = socket.socket()
try:
    s.connect(('${DB_HOST}', int('${DB_PORT}')))
    s.close()
except:
    exit(1)
"; do
    echo "❌ MySQL not ready, retrying..."
    sleep 2
done

echo "✅ MySQL is ready!"

# Run Alembic migrations (skip creating revision if already exists)
if [ -z "$(ls alembic/versions/*.py 2>/dev/null)" ]; then
  echo "📜 No migrations found. Generating initial migration..."
  alembic revision --autogenerate -m "Initial Migration"
else
  echo "📜 Migrations already exist. Skipping revision creation."
fi

echo "⬆️ Running migrations..."
alembic upgrade head

# Run seed
echo "🌱 Running seed data..."
PYTHONPATH=. python app/seeder.py

# Start FastAPI
echo "🚀 Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
