#!/usr/bin/env bash
java -mx1000m -cp stanford-ner-2015-04-20/stanford-ner.jar edu.stanford.nlp.ie.NERServer \
-loadClassifier stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz -port 9191