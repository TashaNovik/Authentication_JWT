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

2. Регистрация. 