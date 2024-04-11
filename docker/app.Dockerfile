FROM python:3.12.2-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python3 -m pip install -U -r requirements.txt

EXPOSE 5000

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]

