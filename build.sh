#!/bin/bash

# Load .env file
if [ -f .env ]; then
  source .env
else
  echo "The .env file doesnt exist"
  exit 1
fi

#Login to github
docker login --username $GHCR_USER --password $GHCR_PASSWORD ghcr.io

#Build the image
docker build . -t $GHCR_PATH

#Push the image to github
docker push $GHCR_PATH