#!/bin/bash


if [[$EUID -ne 0]] ; then
    echo "Error: Deployment script requires root priviledges"
    exit 1
fi

# login to docker and azure
docker login
az login

# Run .py script to create container(if not exists), and upload
# default dataset files to azure
./azure_container_create.py
