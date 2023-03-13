FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY foodplan_service /foodplan_service
WORKDIR /foodplan_service
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password foodplan-user

USER foodplan-user