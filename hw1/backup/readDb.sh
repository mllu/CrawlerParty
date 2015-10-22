
#!/bin/bash

rm -rf dbDump
./runtime/local/bin/nutch readdb crawl/crawldb/ -dump dbDump

