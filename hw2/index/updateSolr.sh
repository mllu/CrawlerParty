#!/bin/bash
if [ -z "$1" ]
  then
    echo "./updateSolr.sh FILE"
    exit
fi
FILE=$1
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/techproducts/update' --data-binary @$FILE
curl http://localhost:8983/solr/techproducts/update --data '<commit/>' -H 'Content-type:text/xml; charset=utf-8'
# curl http://localhost:8983/solr/techproducts/update --data '<delete><query>*:*</query></delete>' -H 'Content-type:text/xml; charset=utf-8'