FROM python:3.13-alpine

LABEL org.opencontainers.image.title="Poddie"
LABEL org.opencontainers.image.description="Generate podcast feeds from any sites supported by yt-dlp"
LABEL org.opencontainers.image.licenses="GPL-3.0"

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache \
        curl \
        ffmpeg && \
    pip install \
        --no-cache-dir \
        -r requirements.txt && \
    mkdir -p \
        /config \
        /data \
        /opt/bin

COPY src/poddie ./poddie
COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh

EXPOSE 8080

HEALTHCHECK \
    --interval=1m \
    --timeout=5s \
    --start-period=30s \
CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/', timeout=5)"

ENTRYPOINT ["/entrypoint.sh"]
