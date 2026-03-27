FROM python:3.11-slim AS builder

# Установка системных зависимостей, необходимых для сборки зависимостей Python
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка python-зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание скрипта ожидания базы данных и запуска Django
RUN echo '#!/bin/bash\n\
echo "Waiting for PostgreSQL..."\n\
while ! pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-postgres}"; do\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is ready!"\n\
python manage.py migrate\n\
python manage.py create_default_admin\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh && chmod +x /app/start.sh


# --- Runtime stage ---
FROM python:3.11-slim AS runtime

# Лёгкий набор системных зависимостей для работы уже собранного приложения
RUN apt-get update && apt-get install -y \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем установленный Python и зависимости из builder-слоя
COPY --from=builder /usr/local /usr/local

# Копируем сам проект и стартовый скрипт
COPY --from=builder /app /app

EXPOSE 8000

CMD ["/app/start.sh"]