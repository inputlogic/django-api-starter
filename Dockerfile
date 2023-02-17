# Build minimal base image with required packages
FROM python:3.11-alpine as base
RUN apk add --update --virtual .build-deps \
    build-base \
    bash \
    make \
    postgresql-dev \
    python3-dev \
    libpq

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Multistage build using binaries from base 
FROM python:3.11-alpine
WORKDIR /app
RUN apk add libpq
COPY --from=base /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY --from=base /usr/bin/make /usr/bin/make
COPY --from=base /bin/bash /bin/bash
COPY . /app
ENV PYTHONUNBUFFERED 1
