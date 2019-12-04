#!/bin/bash

heroku login
git add .

echo "Confirm you wish to update the Heroku deployment server? Y or N"
read $INPUT

