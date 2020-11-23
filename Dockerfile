FROM python:3.8

COPY requirements.txt .

RUN pip3 install -r requirements.txt


WORKDIR /bot


COPY ./src .


CMD ["python3", "start.py"]
