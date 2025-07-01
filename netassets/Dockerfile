FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей напрямую
RUN pip install --no-cache-dir django psycopg2-binary djangorestframework django-auth-ldap django-cors-headers django-simple-history pandas

# Копирование кода приложения
COPY . .

# Создание скрипта ожидания базы данных
RUN echo '#!/bin/bash\n\
echo "Waiting for PostgreSQL..."\n\
while ! pg_isready -h db -p 5432 -U postgres; do\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is ready!"\n\
python manage.py migrate\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh && chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"] 