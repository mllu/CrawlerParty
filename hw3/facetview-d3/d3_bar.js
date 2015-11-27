var x, y, xAxis, yAxis, formatPercent;
$.getScript("d3.v3.min.js", function(){

   formatPercent = d3.format(".0%");
   x = d3.scale.ordinal()
    .rangeRoundBands([0, width], 0.9, 1);

   y = d3.scale.linear()
        .range([height, 0]);

   xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

   yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickFormat(d3.format("d"));

});
var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;
var valueArr = new Array();
var keyArr = new Array();
var data = new Array();
var maxPost = 0;
var svg;

function drawBar(solrJsonArr){
  // var solrJsonArr;
var dataArr = {};
jQuery.each(solrJsonArr, function() {
    var currJson = this;
    var state = currJson["state"];
    if(typeof dataArr[state] == 'undefined'){
      dataArr[state] = 1;
    } else {
      var posts = dataArr[state] + 1;
      dataArr[state] = posts;
    }
});
for (var key in dataArr){
    if (typeof dataArr[key] !== 'function') {
        valueArr.push(dataArr[key]);
        keyArr.push(key);
        maxPost = (dataArr[key] > maxPost) ? dataArr[key] : maxPost;
        data.push({count: dataArr[key], state: key});
    }
}
x.domain(d3.extent(keyArr));
y.domain(d3.extent([0, maxPost]));
yAxis.ticks(maxPost - 1);
d3.selectAll("svg > *").remove();
d3.select("#sort").remove();
d3.select("body")
    .append("label")
    .attr("id", "sort")
      .append("center")
        .append("input")
        .attr("checked", false)
        .attr("type", "checkbox")
        .attr("onClick", "change()");;
svg = d3.select("#statesvg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text", "Sort Value")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Posts");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.state); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) {  return y(d.count); })
      .attr("height", function(d) { return height - y(d.count); });
  d3.select("input").on("change", change);
  // console.log(svg);
}
var sortTimeout = setTimeout(function() { 
   d3.select("input").property("checked", true).each(change);
}, 2000);

  function change() {
    clearTimeout(sortTimeout);

    // Copy-on-write since tweens are evaluated after a delay.
    var x0 = x.domain(data.sort(this.checked
        ? function(a, b) { return b.count  - a.count; }
        : function(a, b) { return d3.ascending(a.state, b.state); })
        .map(function(d) { return d.state; }))
        .copy();

    svg.selectAll(".bar")
        .sort(function(a, b) { return x0(a.state) - x0(b.state); });

    var transition = svg.transition().duration(750),
        delay = function(d, i) { return i * 50; };

    transition.selectAll(".bar")
        .delay(delay)
        .attr("x", function(d) { return x0(d.state); });

    transition.select(".x.axis")
        .call(xAxis)
      .selectAll("g")
        .delay(delay);
  }