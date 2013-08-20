var Tree = (function () {

  /**
   * Format a number to be displayed with abbreviated suffixes.
   * This function is more complicated than one would think it need be,
   * this is due to lack of predictability in Number.toPrecision, Number.toFixed
   * and some rounding issues.
   */
  var formatNumericLabel = function(value) {
    if (value === 0) return "0";
    
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

  // http://stackoverflow.com/questions/2901102/how-to-print-a-number-with-commas-as-thousands-separators-in-javascript
  var numberWithCommas = function(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  var hasValue;

  var valuesFrom = function(selection) {
    return selection[0].map(function (row) {
      var volume = parseInt(row.getAttribute("data-volume"), 10);
        volume = isNaN(volume) ? 0 : volume;
      return {
        name: row.getAttribute("data-title"),
        size: volume, 
        volumeShortened: formatNumericLabel(volume),
        volumeLabel: row.getAttribute("data-volumelabel"),
        url: row.getAttribute("data-href"),
        color: row.getAttribute("data-color"),
        textColor: row.getAttribute('data-text-color'),
        cost: row.getAttribute('data-cost'),
        deptClass: row.getAttribute('data-dept-class')
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
    var sumVals = d3.sum(values,function(val){
      return val.size;
    });
    
    var threshold = sumVals / thresholdRatio;
    var splitValues = partition(values, function (v) {
      return (v.size > threshold || v.url); });
    var children = splitValues.left;
    if (splitValues.right.length) {
      var otherValue = splitValues.right.reduce(sum);
      children.push({
        name: "Others",
        size: otherValue.size,
        volumeLabel : numberWithCommas(otherValue.size),
        cost : otherValue.cost

      });
    }
    return children; 
  };
  
  return {
    formatNumericLabel: formatNumericLabel,
    numberWithCommas: numberWithCommas,
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
  };

  var getNodeClass = function (d) {
    var classes = ["none", "ellipsis", "small", "medium", "large", "x-large", "xx-large"],
        keys    = [0     , 1         , 2      , 3       , 4      , 5        , 6],
        dxIndex = d3.scale.threshold().domain([20,50,130,200,250,400]).range(keys),
        dyIndex = d3.scale.threshold().domain([10,40,100,150,200,400]).range(keys),
        type    = d.children ? "group" : "leaf";

    var nClass = ['node', classes[Math.min(dxIndex(d.dx), dyIndex(d.dy))], type].join(' ');
    if(d.deptClass){
      // currently using dashes to replace dept name spaces e.g. 'Home Office' becomes 'home-office'
      nClass += ' ' + d.deptClass.replace(/\s+/g, '-').toLowerCase();
    }
    return nClass;
  };

  var createTip = function(d){
    var tip = null;
    if(d && d.volumeLabel){
      tip = d.name + ': ' + d.volumeLabel + ' transactions per year';
    }
    if(d.cost){
      tip += ' (total cost: ' + d.cost + ')';
    }
    return tip;
  };


  var makeTree = function (divId, treeData, options) {
    var options = options || {},
        el = document.getElementById(divId);
    
    if(el){
        var width = options.width || el.offsetWidth,
            height = options.height || el.offsetHeight;
    }

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
      .attr('data-tooltip', createTip)    
      .call(position)
      .append("a")
        .attr('href',function(d){ return d.url ? d.url : null })
        .style("color", function(d) { return d.textColor ? d.textColor : null; })
        .text(function(d) {
          return d.children ?  null : d.name;
        })
        .call(function (selection) {
          selection.filter(function (d) {
            return !!d.volumeShortened;
          }).append('span')
            .attr('class', 'amount')
            .text(function (d) {
              return d.volumeShortened;
            });
        });

    if (window.$) {
      var $figure = $('#' + divId);
      var $cap = $('<figcaption/>').appendTo($figure);

      // hide the first wrapping node
      $figure.find('.node').first().hide();

      $figure.find('.node').on('mouseenter',function(){
        var $this = $(this),
            bg = $this.css('background-color');

        $cap.html($('<div class="caption"/>').text($this.data('tooltip')));
        $('<div class="keyBlock"/>').css('background-color',bg).prependTo($cap);
      });
      $figure.on('mouseleave', function () {
        $cap.empty();
      });
    }

  };

  return {
    display: makeTree
  }
}());
