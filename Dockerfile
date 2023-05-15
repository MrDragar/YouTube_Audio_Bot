# Базовый образ
FROM python:3.11

# Создание директории приложения
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копирование кода в образ
COPY . .

# Запуск приложения
CMD ["python3", "main.py"]
