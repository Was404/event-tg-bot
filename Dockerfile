FROM python:alpine

WORKDIR /event-tg-bot

COPY . /event-tg-bot

RUN pip3 install -r requirements.txt

EXPOSE 8443

CMD [ "python3", "app.py" ]