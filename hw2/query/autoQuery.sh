#!/bin/bash

mkdir temporal
python temporal.py
mv *.txt temporal/

mkdir handgun
python spatialTemporl.py "handgun"
mv *.txt handgun/

mkdir shotgun
python spatialTemporl.py "shotgun"
mv *.txt shotgun/

