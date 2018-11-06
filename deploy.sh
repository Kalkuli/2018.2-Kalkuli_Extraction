#!/bin/bash

set -e
set -u

if [ $TRAVIS_PULL_REQUEST != "false" -o $TRAVIS_BRANCH != "master" ]
then
    echo "Skipping deployment on branch=$TRAVIS_BRANCH, PR=$TRAVIS_PULL_REQUEST"
    exit 0;
fi

docker login -u _ -p "$HEROKU_TOKEN" registry.heroku.com

docker build -t registry.heroku.com/kalkuli-extraction/web -f Dockerfile-prod .

docker push registry.heroku.com/kalkuli-extraction/web

heroku container:release web -a kalkuli-extraction
heroku ps:scale worker=1 -a kalkuli-extraction