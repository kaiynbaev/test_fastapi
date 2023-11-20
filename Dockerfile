FROM python:3.10

RUN mkdir /fastapi_testovoe_zadanie

WORKDIR /fastapi_testovoe_zadanie

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD uvicorn main:app --port 8000