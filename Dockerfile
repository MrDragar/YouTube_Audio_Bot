FROM python:3.11

# Создание директории приложения
WORKDIR /app
# Установка зависимостей Python

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

    # Установка зависимостей Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование кода в образ
COPY bot .
COPY main.py .
COPY .env .

# Запуск приложения
CMD ["python3", "main.py"]