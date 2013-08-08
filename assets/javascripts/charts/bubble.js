
var gds = gds || {};
    gds.transactions = gds.transactions || {};
    gds.transactions.charts = gds.transactions.charts || {};

gds.transactions.charts.bubble = gds.transactions.charts.bubble || (function() {

    var bubble_d3js = function BubbleChart(_node, options) {
        this.opts = $.extend({}, gds.transactions.charts.bubble.BubbleChart.default_options, options);
        this.node = _node;
        this.layout = null;
        this.svg = null;
        this.data = this.opts.data;

        $(this.node).data('spend-chart', this);
        this._init();
    }

    bubble_d3js.default_options = {
        data: null,
        fixedScale: null,
        relativeScale: null,
    };

    bubble_d3js.prototype = {
        _init: function() {},

        _draw: function(width, height) {
            var that = this,
                data = this.data,
                margin = this.opts.margin;

            var r = Math.min(width, height),
                format = d3.format(",d"),
                fill = d3.scale.ordinal().range(['#2e358b', '#2b8cc4', '#f47738', '#df3034', '#28a197', '#d53880' ]);

            var bubble = d3.layout.pack()
                .sort(null)
                .size([r, r])
                .fixedScale(this.opts.fixedScale)
                .relativeScale(this.opts.relativeScale);

            this.width = width;
            this.height = height;

            // svg
            this.svg = d3.select('#' + this.node.id).append('svg')
                .attr('class', 'chart bubble')
                .attr('width', width)
                .attr('height', height);

            var node = this.svg
                .append('g')
                    .attr('class', 'chart')
                    .attr('transform', 'translate(0,0)')
                .selectAll("g.node")
                  .data(bubble.nodes({ children : data }).filter(function(d) { return !d.children; }))
                  .enter().append("g")
                  .attr("class", "node")
                  .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
                  .classed("breakdown", function(d) { return $.trim(d.bubbleLink) !== ''; })
                  .classed("larger",  function(d) { return d.r >  160; })
                  .classed("large",   function(d) { return d.r >= 130 && d.r < 160; })
                  .classed("medium",  function(d) { return d.r >= 90  && d.r < 130; })
                  .classed("small",   function(d) { return d.r >= 60  && d.r < 90; })
                  .classed("smaller", function(d) { return d.r <  60; })
                  .on("mouseover", function(d) { tooltip.show("<h3>" + d.title + '</h3>' + '<div class="volume gov"><span>' + d.volumeTooltip + '</span>transactions per year</div>'); })
                  .on('mouseout', function(d) { tooltip.hide(); })
                  .on("click", function(d) {
                    if (d.bubbleLink) {
                        if (event.metaKey==1 || event.ctrlKey==1)
                        {
                            window.open(d.bubbleLink, d.name);
                        }
                        else
                        {
                            window.location = d.bubbleLink;
                        }
                    }
                    //if (d.url) window.location = d.url;
                    });

            node.append("circle")
                .attr("r", function(d) { return d.r; })
                .style("fill", function(d) { return d.color; });

            this._drawText(node);

            var chart = this.svg.select('g.chart'),
                chart_bbox = chart.node().getBBox();

            this.svg.attr('height', chart_bbox.height + 2);
            chart.attr('transform', 'translate(0,' + (-chart_bbox.y) + ")");
        },

        _drawText: function(node) {
            var that = this;

            node.each(function(d) {
                var g = d3.select(this),
                    lines = that._fitTextIntoCircle(d),
                    textOffset = (lines.length > 1)? 2 : 1.5,
                    volTextOffset = (d.r > 80)? 1.3 : 1.0;

                if (d.r <= 24) return;
                if (lines === null) return;

                lines.push(d.volumeLabel);

                for (i = 0; i < lines.length; i++) {
                    g.append("text")
                        .attr("text-anchor", "middle")
                        .attr("fill", d.textColor)
                        .text(lines[i])
                        .classed("label",    function(d) { return i < (lines.length-1); })
                        .classed("vol bold", function(d) { return i === lines.length-1; })
                        .attr("x", "0")
                        .attr("dy", function(d) {
                            return (i != lines.length-1)? (i-lines.length) + textOffset + "em" : volTextOffset + "em";
                        });
                }
            });
        },

        _fitTextIntoCircle: function(d) {
            var lineLength = 14,
                name = (d.r > 90) ? d.title : d.name,
                lines = this._splitIntoLines(name, lineLength),
                maxLines = (d.r > 100)? 4 : (d.r > 60)? 3 : 2;

            if (lines.length > maxLines) {
                lines = lines.slice(0,maxLines)
                lines[lines.length-1] = lines[lines.length-1].length > lineLength-3 ? lines[lines.length-1].substring(0, lineLength-4) + "..." : lines[lines.length-1];
            }

            return lines;
        },

        _splitIntoLines: function(input, len) {
            var i;
            var output = [];
            var lineSoFar = "";
            var temp;
            var words = input.split(' ');
            for (i = 0; i < words.length;) {
                // check if adding this word would exceed the len
                temp = this._addWordOntoLine(lineSoFar, words[i]);
                if (temp.length > len) {
                    if (lineSoFar.length == 0) {
                        lineSoFar = temp;     // force to put at least one word in each line
                        i++;                  // skip past this word now
                    }
                    output.push(lineSoFar);   // put line into output
                    lineSoFar = "";           // init back to empty
                } else {
                    lineSoFar = temp;         // take the new word
                    i++;                      // skip past this word now
                }
            }
            if (lineSoFar.length > 0) {
                output.push(lineSoFar);
            }
            return(output);
        },

        _addWordOntoLine: function(line, word) {
            if (line.length != 0) {
                line += " ";
            }
            return(line += word);
        },

        draw: function(width, height) {
            $(this.node).children().remove();
            this.width = width;
            this._draw(width, width);
        }
    };

    return {
        BubbleChart: bubble_d3js
    };
})();