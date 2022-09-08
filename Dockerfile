FROM python:3.11.0rc1-alpine3.16

RUN /usr/sbin/adduser -g python -D python

USER python
RUN /usr/local/bin/python -m venv /home/python/venv

COPY --chown=python:python requirements.txt /home/python/docker-ansible/requirements.txt
RUN /home/python/venv/bin/pip install --no-cache-dir --requirement /home/python/docker-ansible/requirements.txt

COPY --chown=python:python digicert-tls-rsa-sha256-2020-ca1.cer /home/python/thycotic-secret-server-api/digicert-tls-rsa-sha256-2020-ca1.cer
RUN /bin/cat /home/python/thycotic-secret-server-api/digicert-tls-rsa-sha256-2020-ca1.cer >> /home/python/venv/lib/python3.10/site-packages/certifi/cacert.pem

ENV PATH="/home/python/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/docker-ansible"
