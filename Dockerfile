FROM python:3.10

RUN apt update && apt install gdal-bin netcat-traditional -y

WORKDIR /app

COPY . .

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE ${PORT}