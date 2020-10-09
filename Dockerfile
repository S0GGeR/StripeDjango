FROM python:3.8.2

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/stripe_django

RUN apt-get update && apt-get install netcat -y
RUN apt-get upgrade -y


RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]






#COPY ./req.txt /usr/src/req.txt
#RUN pip install -r /usr/src/req.txt
#
#COPY . /usr/src/stripe
#
#EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]