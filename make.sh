#!/bin/sh

export OPENFAAS_URL=http://127.0.0.1:31112
export OPENFAAS_PREFIX=timido7021

sudo faas-cli build -f custom-faas.yml && \
sudo docker push timido7021/custom-faas:latest && \
sudo docker rmi $(sudo docker images -q --filter "dangling=true")
