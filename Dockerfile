# Базовый образ
FROM debian:buster-slim

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y python3.11 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создание директории приложения
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование кода в образ
COPY . .

# Запуск приложения
CMD ["python3", "main.py"]