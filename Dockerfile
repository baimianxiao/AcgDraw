FROM python:3.11-alpine

WORKDIR /app
ADD . /app

RUN pip install -r requirements.txt
RUN apk update && apk add python3-tkinter

CMD ["python3", "-u", "main.py", "start"]