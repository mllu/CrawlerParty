#!/bin/bash
if [ ! -f ./lib/stanford-corenlp-3.5.2-models.jar ]; then
  echo "Model not Found! Downloading ..."
  wget -O ./lib/stanford-corenlp-3.5.2-models.jar http://repo.maven.apache.org/maven2/edu/stanford/nlp/stanford-corenlp/3.5.2/stanford-corenlp-3.5.2-models.jar
fi
javac -cp ".:./lib/*" SUTimeParser.java

