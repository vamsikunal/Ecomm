FROM python:latest

ENV DB_NAME \
    DB_USER \
    DB_PASSWORD \
    DB_HOST\
    DB_PORT

RUN mkdir /app
COPY ./app /app
COPY entrypoint.sh /app

WORKDIR /app

RUN python3 -m pip install Pillow
RUN pip3 install -r /requirements.txt
RUN chmod +x /entrypoint.sh

EXPOSE 8000 

CMD ["/entrypoint.sh"]
