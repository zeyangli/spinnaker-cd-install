#!/bin/bash
# Wait for the Hal daemon to be ready
export DAEMON_ENDPOINT=http://127.0.0.1:8064
export HAL_COMMAND="hal --daemon-endpoint $DAEMON_ENDPOINT"
until $HAL_COMMAND --ready; do sleep 10 ; done

SPINNAKER_VERSION=$1

hal version list
hal version bom ${SPINNAKER_VERSION} -q -o yaml >/opt/${SPINNAKER_VERSION}.yml
