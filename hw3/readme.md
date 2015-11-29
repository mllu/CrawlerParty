
# Setup of D3 visualization for weapon search 
cp -r banana solr/server/solr-webapp/webapp/ 
cp -r facetview-d3 solr/server/solr-webapp/webapp/
cp config/schema.xml solr/example/techproducts/solr/techproducts/conf/
../hw2/index/cleanSolrAll.sh
../hw2/index/updateSolr.sh finaloutput.json

# =====================================================
# Installation for react wrapper of D3 visualization
# =====================================================
cd react_wrapper

# Install node.js
$ brew install node

$ npm install -g npm
$ npm install -g gulp

$ npm install
$ npm install history react-router@latest
$ npm install react-script-loader
# =====================================================

# banana
template json file:

# facetview
  facetview-d3/facetview.html
  facetview-d3/jquery_facetview.js

# d3
main page: 
  facetview-d3/index.html
  facetview-d3/jquery.facetview.js

gallery pages:
  facetview-d3/d3_bar.html
  facetview-d3/d3_bubble.html
  facetview-d3/d3_cloud.html
  facetview-d3/d3_line.html
  facetview-d3/d3_map.html
  facetview-d3/d3_pie.html

