FROM ghcr.io/astral-sh/uv:0.7.9-bookworm-slim

# ansible-test (sanity) needs git
# ansible needs openssh-client to ssh to managed machines

ARG DEBIAN_FRONTEND=noninteractive
RUN /usr/bin/apt-get update \
 && /usr/bin/apt-get install --assume-yes git openssh-client \
 && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd --create-home --shell /bin/bash --user-group python
USER python

WORKDIR /app
COPY --chown=python:python .python-version pyproject.toml uv.lock ./
RUN /usr/local/bin/uv sync --frozen

COPY --chown=python:python digicert-tls-rsa-sha256-2020-ca1.cer ./
RUN /bin/cat /app/digicert-tls-rsa-sha256-2020-ca1.cer >> /app/.venv/lib/python3.13/site-packages/certifi/cacert.pem

ENV PATH="/app/.venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

LABEL org.opencontainers.image.authors="William Jackson <william@subtlecoolness.com>" \
      org.opencontainers.image.source="https://github.com/williamjacksn/docker-ansible"
