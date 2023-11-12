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

![Screenshot 2023-10-23 at 00 23 41](https://github.com/zearkiatos/cloud-conversion-tool-api/assets/10298615/34ee3120-3c58-4bc8-bedb-4ec8bdf83e12)


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

![Screenshot 2023-10-23 at 00 39 06](https://github.com/zearkiatos/cloud-conversion-tool-api/assets/10298615/6394dc98-6df5-45c0-a019-a122183a0b66)


5. Finally, shutdown the environment in docker 🐳
```bash
# With Linux 🐧 or Mac 🍎
make docker-dev-down

# With Windows 🪟
source run.sh; docker_dev_down

# With docker compose for all Operative Systems

docker compose -f=docker-compose.develop.yml down
```

# If you want to try the application with postman 👩🏻‍🚀

1. Firstly, you need to check de folder **postman** inside the root of the project

**ADD A IMAGE**

2. You need to open your postman and import all of them, the collection and the three environment you have the next environment
* **CLOUD_CONVERSION_DOCKER_DEVELOP**: this is to run the project without any intermediate layer you can use this environment with **docker-compose.develop.yml** and the base api is on **http://localhost:5001**

* CLOUD_CONVERSION_DOCKER_PROXY_DEVELOP: This is to run the project with a proxy reverse with **nginx** simulating the cloud environment this base api run on **http://localhost/** on default http port 80

* CLOUD_CONVERSION_CLOUD_LOAD_BALANCE: This is the base url for test environment that run on public DNS the load balance the url is **http://cloud-conversion-tool.lb.lab-cloud-development.xyz/**

3. When you will have all environments and the collection on your postman you most add the prescript **postmanPrescript.js** on the folder **postman**

**ADD IMAGE**

* You should add this prescript on all http request that need a token,

* This prescript is to authenticate the user and create the token

* This is the prescript

```js
const CLOUD_CONVERSION_TOOL_BASE_API_URL = pm.environment.get('CLOUD_CONVERSION_TOOL_API_BASE_URL');
const username = pm.environment.get('DEFAULT_USERNAME');
const password = pm.environment.get('DEFAULT_PASSWORD');

const options = {
    url: `${CLOUD_CONVERSION_TOOL_BASE_API_URL}/api/auth/login`,
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            "username": username,
            "password": password
        })
    }
}

pm.sendRequest(options, function (error, response) {
    var jsonData = response.json();
    if (error) {
        console.log(error);
    }
    else {
        pm.environment.set('CLOUD_CONVERSION_TOOL_API_TOKEN', jsonData.accessToken)
    }
})
```

