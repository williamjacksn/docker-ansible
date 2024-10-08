FROM python:3.12-slim

# ansible-test (sanity) needs git
# ansible needs to ssh to managed machines
# libpq5 is required for psycopg2, to use modules in the community.postgresql collection
# see https://docs.ansible.com/ansible/latest/collections/community/postgresql/index.html

ARG DEBIAN_FRONTEND=noninteractive
RUN /usr/bin/apt-get update \
 && /usr/bin/apt-get install --assume-yes git libpq5 openssh-client \
 && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd --create-home --shell /bin/bash --user-group python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

COPY --chown=python:python requirements.txt /home/python/docker-ansible/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/docker-ansible/requirements.txt

COPY --chown=python:python digicert-tls-rsa-sha256-2020-ca1.cer /home/python/docker-ansible/digicert-tls-rsa-sha256-2020-ca1.cer
RUN /bin/cat /home/python/docker-ansible/digicert-tls-rsa-sha256-2020-ca1.cer >> /home/python/venv/lib/python3.12/site-packages/certifi/cacert.pem

ENV PATH="/home/python/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/docker-ansible"
