FROM python:3.8.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install netcat -y
RUN apt-get upgrade -y


RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

