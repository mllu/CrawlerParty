# CrawlerParty
HW1

1-1 copy nutch/conf/* into your nutch/conf/
1-2 copy nutch/lib/* into your nutch/lib/
1-3 copy nutch/src/* into your nutch/src/

2. cd hw1

3. ./autoCrawl.sh URL_Seed_FileName NUM_OF_RUN


#######################
Enable ListImageHandler
#######################

1. make sure settings in nutch-site.xml have ListImageHandler enabled
<property>
  <name>interactiveselenium.handlers</name>
  <value>ListImageHandler,DefaultHandler</value>
  <description></description>
</property>

2. make sure ListImageHandler.java under src/plugin/protocol-interactiveselenium/src/java/org/apache/nutch/protocol/interactiveselenium/handlers/

ps: recommend to return fasle in shouldProcessURL() in DefaultHandler.java to save time

3. ant runtime

4. cd hw1; ./autoCrawl.sh testURL 2

5. check if /tmp/outlinks exists?
