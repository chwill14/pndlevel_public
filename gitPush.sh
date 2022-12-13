#!/bin/bash

cd ~/pndlevel
sleep 1

git add .
sleep 1

git commit -m "daily levels update"
sleep 5

git push heroku main
exit 0
