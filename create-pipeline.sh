#!/bin/bash

name=$1
team="inputlogic" # default value
shift

while [[ "$#" -gt 0 ]]; do case $1 in
  -t|--team) team="$2"; shift;;
  *) echo "Unknown parameter passed: $1"; exit 1;;
esac; shift; done

if [ -z "$name" ]
then
  echo "Usage: create-pipeline <app-name> [--team <team-name>]"
else
  echo "Creating Heroku Pipeline: '$name', for team: '$team'"
  heroku apps:create $name-staging --remote staging --team=$team
  heroku apps:create $name-production --remote production --team=$team
  heroku pipelines:create $name -a $name-staging -s staging -t $team
  heroku pipelines:add $name -a $name-api -s production -t $team
  #heroku reviewapps:enable -p $name --a $name-production --autodeploy --autodestroy
  #heroku addons:create SERVICE:PLAN # papertrail for staging and production
fi

