# Description
Cloud conversion tool ☁️ 🛠️ is an api gateway 🌉 project in python 🐍 with flask 🌶️ to receive files 🗂️ and convert to another file format. This is a project for cloud ☁ software engineering ⚙️🧑🏻‍💻

# Made with
[![Python](https://img.shields.io/badge/python-2b5b84?style=for-the-badge&logo=python&logoColor=white&labelColor=000000)]()
[![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white&labelColor=000000)]()


# Prerequirements


* Python 🐍
* Redis.
* Docker & docker-compose 🐳 (Optional).
* For Linux 🐧 and mac 🍎 you can use makefile.
* For Windows 🪟 you can use bash function.

## ⚠️ Important

It is important to have all the projects and repositories in the next folder

**Insertar imagen aqui**

# How to execute

If you want execute without docker then execute the next commands in your terminal.
Note: firstable is important that you have your python virtual environmente created.


1. Firstly, you should have the **.env** please follow the file **.env.example** you should have something like this

```txt
FLASK_APP=flaskr/app
FLASK_ENV=development
APP_NAME=cloud-conversion-tool-api
REDIS_BROKER_BASE_URL=[Your redis broker]
SECRET_KEY=[Your secret key]
JWT_SECRET_KEY=[Your secret key]
DATA_BASE_URI=[Your postgres uri]
TOPIC_TASK_POSTED=task-convert
PATH_STORAGE=/app/videos/
APP_URL=[APP_URL]
```

2. First step you should activate the python environment

```sh
# With Linux 🐧 or Mac 🍎
make activate

# With Windows 🪟
source run.sh; activate

# With python flask 🐍 🌶️
python3 -m venv venv
source venv/bin/activate
```

3. Second step you should install all the dependencies and python 🐍 packages 📦

```sh
# With Linux 🐧 or Mac 🍎
make install

# With Windows 🪟
source run.sh; install

# With python flask 🐍 🌶️
pip install -r requirements.txt
```

4. Finally, into directory flaskr execute

```bash
# With Linux 🐧 or Mac 🍎 you can send a specific port with port=8000 param
make run
#or
make run port=8000

# With Windows 🪟 you can send a specific port with 8000 param
source run.sh; run
# or
source run.sh; run 8000

# With python flask 🐍 🌶️
flask run
```

# How to execute with docker 🐳

1. Step one locate in the root of the project

```bash
cd cloud-conversion-tool-api
```

2. Run in docker 🐳

```bash
# With Linux 🐧 or Mac 🍎
make docker-dev-up

# Command to run with nginx  and proxy reverse 
make docker-up

# With Windows 🪟
source run.sh; docker_dev_up

# Command to run with nginx  and proxy reverse 
source run.sh; docker_up

# With docker compose for all Operative Systems

docker compose -f=docker-compose.develop.yml up --build

# Command to run with nginx  and proxy reverse

docker compose up --build
```

3. Make sure that all microservices are running

* Executing this command

```bash
    docker ps
```

**Insertar imagen**

5. Finally, shutdown the environment in docker 🐳
```bash
# With Linux 🐧 or Mac 🍎
make docker-dev-down

# With Windows 🪟
source run.sh; docker_dev_down

# With docker compose for all Operative Systems

docker compose -f=docker-compose.develop.yml down
```

