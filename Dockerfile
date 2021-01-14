FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN yum install cryptography -y

COPY . .

RUN useradd appuser
RUN chown -R appuser:appuser /usr/src/app

USER appuser

EXPOSE 8080

CMD [ "python", "./app.py" ]
