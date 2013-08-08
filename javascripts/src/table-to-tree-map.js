var Tree = (function () {

  /**
   * Format a number to be displayed with abbreviated suffixes.
   * This function is more complicated than one would think it need be,
   * this is due to lack of predictability in Number.toPrecision, Number.toFixed
   * and some rounding issues.
   */
  var formatNumericLabel = function(value) {
    if (value == 0) return "0";
    
    var magnitudes = {
      million:  {value: 1e6, suffix:"m"},
      thousand: {value: 1e3, suffix:"k"},
      unit:     {value: 1, suffix:""}
    };
    var magnitude = function(num, n) {
          return Math.pow(10, n - Math.ceil(Math.log(Math.abs(num)) / Math.LN10));
        },
        roundToSignificantFigures = function(num, n) {
          return Math.round(num * magnitude(num, n)) / magnitude(num, n);
        },
        thresholds = [ magnitudes.million, magnitudes.thousand ],
        roundedValue = roundToSignificantFigures(value, 3),
        significantFigures = null;

    for (var i = 0; i < thresholds.length; i++) {
      if (roundedValue >= (thresholds[i].value / 2)) {
        if (roundedValue < thresholds[i].value) {
          significantFigures = 2;
        } else {
          significantFigures = 3;
          value = roundedValue;
        }
        value = roundToSignificantFigures(value, significantFigures) / thresholds[i].value;
        return value.toPrecision(value < 1 ? 2 : 3) + thresholds[i].suffix;
      }
    }
    return roundedValue.toString();
  };

  var valuesFrom = function(selection) {
    return selection[0].map(function (row) {
      var volume = parseInt(row.getAttribute("data-volume"), 10);
      return {
        name: row.getAttribute("data-title"),
        size: volume,
        volumeLabel: formatNumericLabel(volume),
        url: '/' + row.getAttribute("data-bubbleLink"),
        color: row.getAttribute("data-color"),
        textColor: row.getAttribute('data-text-color')
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
    if (thresholdRatio == null) {
      return values;
    }

    var threshold = values.reduce(max).size / thresholdRatio;
    var splitValues = partition(values, function (v) { return v.size > threshold; });
    var children = splitValues.left;
    if (splitValues.right.length) {
      var otherValue = splitValues.right.reduce(sum);
      children.push({
        name: "Others",
        size: otherValue.size
      });
    }
    return children; 
  };
  
  return {
    formatNumericLabel: formatNumericLabel,
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

  var getNodeClass = function (d) {
    var classes = ["none", "ellipsis", "small", "medium", "large", "x-large"],
        keys    = [0     , 1         , 2      , 3       , 4      , 5],
        dxIndex = d3.scale.threshold().domain([20,50,130,200,250]).range(keys),
        dyIndex = d3.scale.threshold().domain([10,40,100,150,200]).range(keys);
    return 'node ' + classes[Math.min(dxIndex(d.dx), dyIndex(d.dy))];
  };


  var makeTree = function (divId, treeData, options) {
    var options = options || {},
        el = document.getElementById(divId),
        width = options.width || el.offsetWidth,
        height = options.height || el.offsetHeight;

    var color = d3.scale.category20c();
    
    var treemap = d3.layout.treemap()
        .size([width, height])
        .value(function(d) { return d.size; })
        .sort(function(a, b) {
          return a.value - b.value;
        });
    
    var div = d3.select('#'+divId);
    
    var node = div.datum(treeData).selectAll(".node")
      .data(treemap.nodes)
      .enter().append("div")
      .attr("class", getNodeClass)
      .call(position)
      .style("background", function(d) { return d.color ? d.color : color(d.name); })
      .append("a")
        .attr('href',function(d){ return d.url ? d.url : null })
        .style("color", function(d) { return d.textColor ? d.textColor : null; })
        .text(function(d) {
          return d.children ?  null : d.name;
        })
        .call(function (selection) {
          selection.filter(function (d) {
            return !!d.volumeLabel;
          }).append('span')
            .attr('class', 'amount')
            .text(function (d) {
              return d.volumeLabel;
            });
        });
  };
  
  return {
    display: makeTree
  }
}());

