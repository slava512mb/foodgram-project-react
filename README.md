# Яндекс.Практикум. Дипломный проект.
![foodgram-project-react Workflow Status](https://github.com/slava512mb/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)
# Продуктовый помощник - приложение Foodgram

После запуска проекта, он будет доступен по адресу: 

Локальная машина http://127.0.0.1/

Виртуальная машина: http://158.160.6.239/

Как запустить и посмотреть в действии описано ниже.

## Описание приложения Foodgram
Foodgram - приложение, с помощью которого пользователи просматривают предоставленные другими пользователями рецепты блюд, подписываются на авторов понравившихся рецептов и добавляю свои собственные рецепты.
Внутри приложения есть сервис «Список покупок», позволяющий создавать список продуктов, которые нужно купить для приготовления блюд согласно рецепта.

## Запуск с использованием CI/CD и Docker

```bash
# В Settings - Secrets and variables создаем переменный с вашими данными
# Это необходимо для работы с CI/CD, DockerHub, GitHub
DB_ENGINE
DB_NAME
DB_USER
DB_PASSWORD
DB_HOST
DB_PORT
POSTGRES_USER
POSTGRES_PASSWORD
DOCKER_USERNAME
DOCKER_PASSWORD
SECRET_KEY
SSH_KEY
USER
PASSPHRASE
```

Все действия будут выполняться в Docker, docker-compose как на локальной машине так и на сервере ВМ Yandex.Cloud.
Предварительно установим на ВМ в облаке необходимые компоненты для работы:

```bash
# username - ваш логин, ip - ip ВМ под управлением Linux Дистрибутива с пакетной базой deb.
ssh username@ip
```

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
```

```bash
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
```

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

```bash
sudo systemctl start docker.service && sudo systemctl enable docker.service
```

Всё, что нам нужно, установлено, далее, создаем папку /infra в домашней директории /home/username/:

```bash
cd ~
```

```bash
mkdir infra
```

Предварительно из папки /backend и /frontend загрузим актуальные данные на DockerHub (на вашем ПК):

```bash
docker login -u themasterid
```

```bash
cd backend
```

```bash
docker build -t slava512mb/foodgram_backend:latest .
```

```bash
docker push slava512mb/foodgram_backend:latest
```

```bash
cd ..
```

```bash
cd frontend
```

```bash
docker build -t slava512mb/foodgram_frontend:latest .
```

```bash
docker push slava512mb/foodgram_frontend:latest
```

Перенести файлы docker-compose.yml и default.conf на сервер, из папки infra в текущем репозитории (на вашем ПК).

```bash
cd infra
```

```bash
scp docker-compose.yml username@server_ip:/home/username/
```

```bash
scp default.conf username@server_ip:/home/username/
```

Так же, создаем файл .env в директории infra на ВМ:

```bash
touch .env
```

Заполнить в настройках репозитория секреты .env

```python
DB_ENGINE='django.db.backends.postgresql'
DB_NAME='postgres'
DB_USER='postgres'
DB_PASSWORD='secret'
DB_HOST='db'
DB_PORT='5432' 
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='secret'
DOCKER_USERNAME='secret'
DOCKER_PASSWORD='secret'
SECRET_KEY='secret'
```

На этом настройка закончена, далее в папке infra выполняем команду:

```bash
sudo docker-compose up -d --build
```

Проект запустится на ВМ и будет доступен по указанному вами адресу либо IP. Завершение настройки на ВМ:

В папке infra выполняем команду, что бы собрать контейнеры:

Остановить: 

```bash
sudo docker-compose stop
```

Удалить вместе с volumes:

```bash
# Все данные удалятся!
sudo docker-compose down -v
``` 

Для доступа к контейнеру backend и сборки финальной части выполняем следующие команды:

```bash
sudo docker-compose exec backend python manage.py makemigrations
```

```bash
sudo docker-compose exec backend python manage.py migrate --noinput
```

```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Дополнительно можно наполнить DB ингредиентами и тэгами:

```bash
sudo docker-compose exec backend python manage.py load_tags
```

```bash
sudo docker-compose exec backend python manage.py load_ingrs
```

Вот и всё. Продуктовый помощник запущен. Можно наполнять его рецептами, подписываться на других пользователей, отправляться за покупками продуктов и готовить свои любимые блюда!