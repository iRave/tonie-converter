FROM python:3.12-slim

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app
COPY app/ /app/

RUN pip install --no-cache-dir reflex werkzeug

EXPOSE 3000
CMD ["reflex", "run", "--env", "prod"]