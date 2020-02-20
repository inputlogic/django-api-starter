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
  heroku apps:create $1-staging --remote staging --team=$team
  heroku apps:create $1-production --remote production --team=$team
  heroku pipelines:create $1 -a $1-staging -s staging -t $team
  heroku pipelines:add $1 -a $1-admin -s production -t $team
  heroku reviewapps:enable -p $1 --a $1-production --autodeploy --autodestroy
  #heroku addons:create SERVICE:PLAN # papertrail for staging and production
fi


