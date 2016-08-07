#!/bin/bash
docker run -ti --name batch_colorize -v $(pwd)/images:/images sergekatzmann/batch_colorize:latest
docker rm batch_colorize