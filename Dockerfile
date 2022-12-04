FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache build-base gcc musl-dev libffi-dev
RUN pip3 install pip --upgrade

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk del build-base gcc musl-dev libffi-dev

COPY vedro_cloud_api/ vedro_cloud_api/

CMD ["python3", "-m", "vedro_cloud_api"]
