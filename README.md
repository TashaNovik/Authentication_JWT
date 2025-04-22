## 1. Видеодемонстрация работы регистрации, аутентификации и отправки сообщения. - по ссылке внизу: ##

## Ход выполнения задания ##
1. Настройка Окружения и Базы Данных
     docker --version
     Docker version 28.0.1, build 068a01e
     docker-compose --version
     Docker Compose version v2.33.1-desktop.1
     Создать файл docker-compose.yml в каталоге проекта
     Скачать docker-образ : docker pull postgres:latest
     docker-compose up -d db
     Проверить что контейнер запущен: docker ps
     Подключиться к БД через DBeaver:
     Host: localhost
     Port: 5438
     Database: mydatabase
     User: tree
     Password: papa

2. Разработка Сервиса Аутентификации (Auth Service)
mkdir auth-service
cd auth-service
Внутри папки auth-service:
 - main.py (основной файл приложения)
 - models.py (модели базы данных)
 - Dockerfile
 - requirements.txt (зависимости)

В зависимости прописать:
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
passlib[bcrypt]
python-dotenv
pyjwt

Установить зависимости:
pip install -r requirements.txt

Создание моделей базы данных(models.py);

Реализация основного приложения (main.py);

Создание Docker-образа (Dockerfile);

Запуск сервиса: docker-compose up --build auth-service

3. Разработка сервиса для публикации постов (Post Service):
mkdir post-service
cd post-service

Внутри post-service создать файлы:
main.py (основной файл приложения)
models.py (модели базы данных)
Dockerfile
requirements.txt