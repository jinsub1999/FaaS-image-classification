#!/bin/sh

export OPENFAAS_URL=http://127.0.0.1:31112
export OPENFAAS_PREFIX=timido7021

faas-cli deploy -f custom-faas.yml
