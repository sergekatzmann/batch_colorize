#!/bin/bash
docker run --rm  -ti --name batch_colorize -v $(pwd)/images:/images sergekatzmann/batch_colorize:latest