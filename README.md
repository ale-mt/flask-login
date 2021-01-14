# flask-login

## Dockerfile:

```
FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd appuser
RUN chown -R appuser:appuser /usr/src/app

USER appuser

EXPOSE 8080

CMD [ "python", "./app.py" ]

```

## Build:
```
oc new-app https://github.com/ale-mt/flask-login -e MYSQL_USER=root -e MYSQL_PASSWORD=password -e MYSQL_SERVICE_HOST=host -e MYSQL_DATABASE=flask_mysql -l app=studenti-python --name=studenti --image-stream=openshift/python
```

it is possible to not specify a value for ```MYSQL_SERVICE_HOST``` and let oc manage it

## Run:
```
oc expose svc/studenti
```
