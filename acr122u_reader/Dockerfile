FROM ghcr.io/home-assistant/base:latest

RUN apk add --no-cache \
    pcsc-lite \
    pcsc-lite-libs \
    ccid \
    python3 \
    py3-pip \
    build-base \
    swig \
    pcsc-lite-dev \
    python3-dev

RUN pip3 install --no-cache-dir --break-system-packages pyscard requests

COPY run.sh /run.sh
COPY reader.py /reader.py
COPY custom_components/acr122u /opt/acr122u_integration

RUN chmod +x /run.sh

CMD ["/run.sh"]
