
var gds    = gds    || {};
    gds.transactions = gds.transactions || {};

gds.transactions.views = gds.transactions.views || (function() {

    var charts   = gds.transactions.charts,
        bubble  = charts.bubble,
        treemap = charts.treemap,
        magnitudes = {
            million:  {value: 1e6, suffix:"m"},
            thousand: {value: 1e3, suffix:"k"},
            unit:     {value: 1, suffix:""}
        };

        departmentScale = function(abbr) {
            var default_scale = 1,
                scales = {
                    'dcms': 0.5
                };
            if (abbr in scales) { return scales[abbr]; } else { return default_scale; }
        },

        volume2Value = function(volume) {
            var s = d3.scale.pow().exponent(0.45)
            return s(volume);
        },
        formatNumber = function(number, precision) {
            var precision = precision === undefined ? 0 : precision,
                num_str = number.toFixed(precision)
                x = (num_str + '').split('.'),
                x1 = x[0],
                x2 = x.length > 1 ? '.' + x[1] : '',
                rgx = /(\d+)(\d{3})/;

            while (rgx.test(x1)) {
                x1 = x1.replace(rgx, '$1' + ',' + '$2');
            }
            return x1 + x2;
        },
        formatNumberForMagnitude = function(number) {
            return magnitudeFormat(number, magnitudeFor(number));
        },
        chart_resizer = function(chart, container, max_width) {
            var timeout_id = null,
                max_width = max_width || 1000000,
                jcontainer = $(container);

            $(window).resize(function() {
                window.clearTimeout(timeout_id);
                timeout_id = setTimeout(function() {
                    var width = jcontainer.width();
                    if (chart.width != width) {
                        chart.draw(Math.min(width, max_width), chart.height);
                    }
                }, 20)
            });
        },
        groupColorsByBody = function(data) {
            var colors = $(data).map(function(i) { return this.color; });
            var color_idx = 0;
            var bodies = {};

            $.each(data, function(i, v){
                if (!(v.body in bodies)) {
                    bodies[v.body] = colors[color_idx];
                    color_idx += 1;
                }
                v.color = bodies[v.body];
            });

            return data;
        },

        magnitudeFor = function (value) {
            if (value >= 1e9) return magnitudes.billion;
            if (value >= 1e6) return magnitudes.million;
            if (value >= 1e3) return magnitudes.thousand;
            return magnitudes.unit;
        }
        magnitudeFormat = function (value, magnitude) {
            return (parseFloat(value.toPrecision(3)) / magnitude.value).toString() + magnitude.suffix;
        };


    return {
        index: function(department_slug, chartDivId, chartTableId) {

            var transactions_charts = $('#' + chartDivId),
                charts_width = transactions_charts.width(),
                transactions_table  = document.getElementById(chartTableId),
                data = gds.transactions.views.getChartData(transactions_table, department_slug);

            var transaction_chart = gds.transactions.views.setupChart(data, department_slug);

            transactions_charts.empty();

            transaction_chart.draw(charts_width, 400);
            chart_resizer(transaction_chart, transactions_charts);
        },

        setupChart: function(data, department_slug) {
            var fixedScale = null,
                relativeScale = department_slug === "" ? 1 : departmentScale(department_slug),
                transactions_table  = document.getElementById('transactions-table'),
                new_chart = null;

            if (gds.transactions.views.getQueryStringParam('chart') !== 'tree') {
              new_chart = new bubble.BubbleChart(
                  document.getElementById('bubble'), {
                      data: data,
                      fixedScale: fixedScale,
                      relativeScale: relativeScale
                  }
              );
            } else {
              new_chart = new treemap.TreeMapChart(
                document.getElementById('bubble'), {
                    data: data,
                    fixedScale: fixedScale,
                    relativeScale: relativeScale
                }
              );
            }

            return new_chart;
        },

        getQueryStringParam: function(key) {
            key = key.replace(/[*+?^$.\[\]{}()|\\\/]/g, "\\$&"); // escape RegEx meta chars
            var match = location.search.match(new RegExp("[?&]"+key+"=([^&]+)(&|$)"));
            return match && decodeURIComponent(match[1].replace(/\+/g, " "));
        },

        getChartData: function(table, dept_slug) {
            var data = $('tbody tr:not([data-volume="-1"])', table).map(function() {
                var tr = $(this),
                cells = tr.children('td');
                var properVolume = parseInt(tr.attr('data-volume'));

                return {
                    name: tr.attr('data-label'),
                    title: tr.attr('data-title'),
                    color: tr.attr('data-color'),
                    textColor: tr.attr('data-text-color'),
                    body: tr.attr('data-body'),
                    bodyAbbr: tr.attr('data-body-abbr'),
                    volume: properVolume,
                    volumeLabel: formatNumberForMagnitude(properVolume),
                    volumeTooltip: tr.attr('data-volumeLabel'),
                    category: tr.attr('data-category'),
                    url: tr.attr('data-url'),
                    bubbleLink: tr.attr('data-bubbleLink'),
                    value: volume2Value(properVolume)
                };
            }).get();

            if (dept_slug) {
                data = groupColorsByBody(data);
            }

            if (data.length <= 10 || dept_slug === "") {
                return data;
            } else {
                var orig_data = data.concat([])
                var top10 = data.sort(function(a,b) { return b.volume - a.volume;  }).slice(0, 10),
                restSum = d3.sum(data.slice(10), function(d) { return d.volume >= 0 ? d.volume : 0; }),
                rest = {
                    name: 'Other transactions',
                    title: 'Other transactions',
                    color: '#666',
                    textColor: '#fff',
                    volume: restSum,
                    volumeLabel: formatNumberForMagnitude(restSum),
                    volumeTooltip: formatNumber(restSum),
                    category: 'other',
                    url: '',
                    value: volume2Value(restSum)
                };
                return orig_data.filter(function(d) { return top10.indexOf(d) !== -1 ? true : false; }).concat([rest]);
            }
        }
    }
})();