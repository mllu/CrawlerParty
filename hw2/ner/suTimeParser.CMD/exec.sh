#!/bin/bash
if [ "$#" -ne 2 ]; then
    echo 'Usage: ./exec.sh InputPath OutputPath'
    exit
fi
if [ ! -f ./lib/stanford-corenlp-3.5.2-models.jar ]; then
  echo "Model not Found! Downloading ..."
  wget -O ./lib/stanford-corenlp-3.5.2-models.jar http://repo.maven.apache.org/maven2/edu/stanford/nlp/stanford-corenlp/3.5.2/stanford-corenlp-3.5.2-models.jar
fi
# Usage: 
#   java -cp ".:./lib/*" SUTimeParser InputPath OutputPath
#java -cp ".:./lib/*" SUTimeParser input/ViewItem.aspx output/ViewItem.aspx
java -cp ".:./lib/*" SUTimeParser $1 $2

