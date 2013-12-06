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
        nameShortened: row.getAttribute("data-label"),
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
    var type   = d.children ? "group" : "leaf",
        nClass = ['node', classForSize(d.dx, d.dy), type].join(' ');

    //var nClass = ['node', classes[Math.min(dxIndex(d.dx), dyIndex(d.dy))], type].join(' ');
    if(d.deptClass){
      // currently using dashes to replace dept name spaces e.g. 'Home Office' becomes 'home-office'
      nClass += ' ' + d.deptClass.replace(/\s+/g, '-').toLowerCase();
    }
    return nClass;
  };

  var classForSize = function(width, height) {
    var size = (width + height) / 2,
        classes = ["none", "ellipsis", "small", "medium", "large", "x-large", "xx-large"],
        keys    = [0     , 1         , 2      , 3       , 4      , 5        , 6],
        sizeIndex = d3.scale.threshold().domain([10,40,150,300,350,400]).range(keys),
        widthIndex = d3.scale.threshold().domain([20,50,130,200,250,400]).range(keys);

    return classes[Math.min(sizeIndex(size), widthIndex(width))];
  };

  var contentForClass = function(classes) {
    if (classes.indexOf("none") > -1) {
        return '&nbsp;';
    }
    if (classes.indexOf("ellipsis") > -1) {
        return '…';
    }
    return null;
  }

  var setNodeContent = function (d) {
    // switch to position='static' to enable measurement of true height
    this.style.position = 'static';
    var availableHeight = this.parentNode.clientHeight,
        classes = this.parentNode.className,
        actualHeight = Infinity,
        name = d.name,
        text,
        node = d3.select(this);

    text = contentForClass(classes);

    if (text != null) {
        this.style.position = 'absolute';
        this.innerHTML = text;
        return;
    }

    var volumeSpan = '';
    if (d.volumeShortened) {
      volumeSpan = '<span class="amount">' + d.volumeShortened + '</span>';
    }

    // Check if it fits as-is
    this.innerHTML = name + volumeSpan;
    if (this.offsetHeight <= availableHeight) {
      this.style.position = 'absolute';
      // Content fits, all good.
      return;
    }

    if (d.nameShortened) {
      // Use shortened name when available
      name = d.nameShortened;

      // Check if it fits when shortened name is used
      this.innerHTML = name + volumeSpan;
      if (this.offsetHeight <= availableHeight) {
        this.style.position = 'absolute';
        // Content fits when shortened name is used, all good.
        return;
      }
    }

    // Check if trimming of name could yield a good result
    this.style['white-space'] = 'nowrap';
    text = name + volumeSpan;
    this.innerHTML = text;
    actualHeight = this.offsetHeight;
    this.style['white-space'] = 'normal';
    if (actualHeight > availableHeight) {
      this.style.position = 'absolute';
      // Content does not fit, even when name is on single line.
      // Simply display volume.
      this.innerHTML = volumeSpan;
      return;
    }

    // Shorten name until everything fits
    actualHeight = Infinity;
    while (actualHeight > availableHeight) {
      text = name;
      if (name.length > 0 && name.length !== d.name.length) {
        text += '…';
      }
      text += volumeSpan;
      this.innerHTML = text;

      if (name.length <= 0) {
        break;
      }
      actualHeight = this.offsetHeight;
      name = name.substring(0, name.length - 4);
    }

    // reset to position='absolute' to make link display across whole node area
    this.style.position = 'absolute';
  };

  var createTip = function(d){
    var tip = null;
    if(d && d.volumeLabel){
      tip = d.name + ': ' + d.volumeLabel + ' transactions per year';
    }
    return tip;
  };


  var makeTree = function (divId, treeData, options) {
    var options = options || {},
        el = document.getElementById(divId);

    if (!el) {
      // Wrapper element not found
      return;
    }

    var width = options.width || el.offsetWidth,
        height = options.height || el.offsetHeight;

    // Clean up wrapper element before populating
    el.innerHTML = '';

    var color = d3.scale.category20c();

    var treemap = d3.layout.treemap()
        .size([width, height])
        .value(function(d) { return d.size; })
        .sort(function(a, b) {
          return a.value - b.value;
        });

    var node = d3.select('#'+divId).datum(treeData).selectAll(".node")
      .data(treemap.nodes)
      .enter().append("div")
      .attr("class", getNodeClass)
      .attr('data-tooltip', createTip)
      .attr('title', createTip)
      .call(position)
      .append("a")
        .attr('href',function(d){ return d.url ? d.url : null })
        .style("color", function(d) { return d.textColor ? d.textColor : null; })
        .call(function (selection) {
          selection
            .filter(function (d) {
              return !d.children;
            })
            .each(setNodeContent);
        });

    var rsplit = function (str, matchThis) {
        var length = str.length, whereToSplit = undefined;
        for (var i = length; i > 0; i--) {
            if (str[i] === matchThis) {
                whereToSplit = i;
                break;
            }
        }
        return [
            str.slice(0,whereToSplit + 1),
            str.slice(whereToSplit + 1, length)
        ];
    };

    if (window.$) {
      var $figure = $('#' + divId);
      var $cap = $('<figcaption/>').prependTo($figure);

      // hide the first wrapping node
      $figure.find('.node').first().hide();

      $figure.find('.node').on('mouseenter',function(){
        var $this = $(this),
            bg = $this.css('background-color'),
            tooltipText = $this.data('tooltip'),
            serviceDetails = rsplit(tooltipText, ':');
        $cap.html('<span class="service-name">' + serviceDetails[0] + '</span><span class="service-details">' + serviceDetails[1] + '</span>');
        $('<span class="keyBlock"/>').css('background-color',bg).prependTo($cap);
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
