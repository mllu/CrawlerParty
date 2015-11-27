	function tooltipHtml(n, d){	/* function to create html content string in tooltip div. */
		return "<h4>"+n+"</h4><table>"+
			"<tr><td>Seller</td><td>"+(d.seller)+"</td></tr>"+
			"</table>";
	}
	function drawMap(solrJsonArr){
	// var solrJsonArr;
	var dataArr = {};
	// $.ajaxSettings.async = false;
	// $.getJSON("solrOutput.json", function(json) {
	// 	solrJsonArr = json;
	// });
	var sampleData ={};	/* Sample random data. */	
	jQuery.each(solrJsonArr, function() {
		var currJson = this;
		var state = currJson["state"];
	  	// console.log(dataArr[state]);
	  	if(typeof dataArr[state] == 'undefined'){
	  		dataArr[state] = {seller: 1, color: d3.interpolate("#ffffcc", "#800026")(1 / 100)};
	  	} else {
	  		var seller = dataArr[state]["seller"] + 1;
	  		dataArr[state] = {"seller": seller, color: d3.interpolate("#ffffcc", "#800026")(seller / 100)};
	  	}
	});
	console.log("into drawMap");
	/* draw states on id #statesvg */
	d3.selectAll("svg > *").remove();
	uStates.draw("#statesvg", dataArr, tooltipHtml);
}