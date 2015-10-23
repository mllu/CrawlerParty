# NER Annotate
Given a input of html file, this script is going to generate a xml file that is ready to feed the solr index system.
The xml would contain field like title, gun type, gun category, location, etc.

# Usage
Run the following to open the stanford ner server
```
bash openServer.sh
```
Run the python script to generate the xml file ready to index.
```
python2 testTikaPython.py
```

# Dependency
Apache Tika: 
Note that this is a python2.7 project, run the correct pip to install to the python2.7 library
```
pip install tika
```