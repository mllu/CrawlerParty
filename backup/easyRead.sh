#!/bin/bash

./runtime/local/bin/nutch mergesegs mergeSegments -dir crawl/segments 

./runtime/local/bin/nutch readseg -dump mergeSegments/2* resultDump


