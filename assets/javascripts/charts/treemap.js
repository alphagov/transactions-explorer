
var gds = gds || {};
    gds.transactions = gds.transactions || {};
    gds.transactions.charts = gds.transactions.charts || {};

gds.transactions.charts.treemap = gds.transactions.charts.treemap || (function() {

    var treemap_d3js = function TreeMapChart(_node, options) {
        this.opts = $.extend({}, gds.transactions.charts.treemap.TreeMapChart.default_options, options);
        this.node = _node;
        this.layout = null;
        this.svg = null;
        this.data = this.opts.data;

        $(this.node).data('spend-chart', this);
        this._init();
    }

    treemap_d3js.default_options = {
        data: null,
        fixedScale: null,
        relativeScale: null,
        valueFunc: function(d) { return d.volume; },
        sortFunc:  function(a,b) { return a.volume - b.volume; }
    };

    treemap_d3js.prototype = {
        _init: function() {},

        _draw: function(width, height) {
            var that = this,
                data = this.data,
                margin = this.opts.margin;

            this.width = width;
            this.height = height;

            var root = d3.select('#' + this.node.id).append('div')
               .style('position',   'relative')
               .style('width', width + 'px')
               .style('height', height + 'px')
               .attr('class', 'chart treemap');

            var layout = d3.layout.treemap()
                 .size([width, height])
                 .sticky(true)
                 .value(this.opts.valueFunc)
                 .sort(this.opts.sortFunc);

            this.cells = root
                .data([{ name: 'all', children: this.opts.data}])
                .selectAll('div')
                    .data(layout.nodes)
                    .enter()
                    .append('div')
                        .attr("class", "node")
                        .style("left", function(d) { return d.x + "px"; })
                        .style("top", function(d) { return d.y + "px"; })
                        .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
                        .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; })
                        .style("background", function(d) { return d.children ? null : d.color; })
                        .append('div')
                            .attr("class", "label")
                            .append('a')
                                .attr("href", function(d) { return d.bubbleLink ? d.bubbleLink : '#' })
                                .html(function(d) { return d.children ? null : d.title + "<br/>" + d.volume; });;
        },

        draw: function(width, height) {
            $(this.node).children().remove();
            this.width = width;
            this.height = height;
            this._draw(width, height);
        }
    };

    return {
        TreeMapChart: treemap_d3js
    };
})();