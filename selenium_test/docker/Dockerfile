FROM python:3.10-slim
WORKDIR /selenium_test
COPY . /selenium_test
RUN apt update && apt install -y \
    bash \
    procps \
    curl \
    net-tools \
    vim \
    x11vnc \
    xvfb \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r /selenium_test/requirements.txt
