#!/bin/bash

docker run --rm -it --name squid-container \
    -v "$(pwd)/squid.conf:/etc/squid/squid.conf" \
    -e TZ=UTC \
    -p 3128:3128 \
    ubuntu/squid:5.2-22.04_beta
