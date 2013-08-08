var Tree = (function () {

  var valuesFrom = function(selection) {
    return selection[0].map(function (row) {
      return { 
        name: row.getAttribute("data-title"),
        size: parseInt(row.getAttribute("data-volume")),
        url: row.getAttribute("data-url")
      };
    });
  };

  var max = function (memo, v) {
    return (memo.size > v.size) ? memo : v;
  };

  var sum = function (memo, v) {
    memo.size += v.size;
    return memo;
  };

  var partition = function(col, partitionFunction) {
    return col.reduce(function (memo, v) {
      if (partitionFunction(v)) {
        memo.left.push(v)
      } else {
        memo.right.push(v);
      }
      return memo;
    }, { left: [], right: [] });
  };

  var condenseValuesUnderThreshold = function(values, thresholdRatio) {
    var threshold = values.reduce(max).size / thresholdRatio;
    var splitValues = partition(values, function (v) { return v.size > threshold; });
    var children = splitValues.left;
    var otherValue = splitValues.right.reduce(sum);
    children.push({
      name: "Others",
      size: otherValue.size
    });
    return children; 
  };
  
  return {
    fromHtmlTable: function(selection, thresholdRatio) {
      var values = valuesFrom(selection);

      return { 
        name: "Service Explorer", 
        children: condenseValuesUnderThreshold(values, thresholdRatio)
      };
    }
  }

}());

var TreeMapLayout = (function () {
    var position = function() {
        this.style("left", function(d) { return d.x + 1 + "px"; })
        .style("top", function(d) { return d.y + 1 + "px"; })
        .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
        .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; })
        .style('position','absolute')
        .style("cursor", function(d) { return d.url ? "pointer" : ""; });
    }
  
  var makeTree = function (divId, treeData) {
    var margin = {top: 0, right: 0, bottom: 40, left: 0},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
    
    var color = d3.scale.category20c();
    
    var treemap = d3.layout.treemap()
        .size([width, height])
        .value(function(d) { return d.size; })
        .sort(function(a, b) {
          return a.value - b.value;
        });
    
    var div = d3.select('#'+divId)
        .style("width", (width + margin.left + margin.right) + "px")
        .style("height", (height + margin.top + margin.bottom) + "px")
        .style("left", margin.left + "px")
        .style("top", margin.top + "px");
    
    var node = div.datum(treeData).selectAll(".node")
      .data(treemap.nodes)
      .enter().append("div")
      .attr("class", "node")
      .call(position)
      .on("click", function(d) {
        if (d.url){
          console.log('TODO make me go to ' + d.url);
        }
      })
      .style("background", function(d) { return d.children ? null : color(d.name); })
      .attr('href',function(d){ return d.url ? d.url : null })
      .text(function(d) { return d.children ?  null : d.name; });
  };
  
  return {
    display: makeTree
  }
}());

