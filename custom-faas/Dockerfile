ARG PYTHON_VERSION=3.10
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/of-watchdog:0.9.10 as watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:${PYTHON_VERSION}-slim-buster as build

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)

RUN apt-get -qy update \
    && apt-get -qy install ${ADDITIONAL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/*

# Add non root user
RUN addgroup --system app && adduser app --system --ingroup app
RUN chown app /home/app

USER app

ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY --chown=app:app app.py       .
COPY --chown=app:app classes.json   .
COPY --chown=app:app model.pt .
USER root

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install Flask timm gunicorn

USER app

FROM build as ship
WORKDIR /home/app/

USER app

ENV FLASK_ENV=development
ENV FLASK_APP=/home/app/app.py

# Set up of-watchdog for HTTP mode
ENV fprocess="gunicorn --preload app:app -b 127.0.0.1:5000 --timeout=10"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

# EXPOSE 8080

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
