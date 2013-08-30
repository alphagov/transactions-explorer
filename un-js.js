var page = require('webpage').create(),
    fs = require('fs'),
    args = require('system').args;

if (args.length !== 4) {
    console.log("Usage: \n\tphantomjs un-js.js [domain] [pagePaths.json] [outputDir]");
    phantom.exit();
}

page.viewportSize = { width: 1024, height: 768 };

var domain = args[1],
    pagePaths = JSON.parse(fs.open(args[2], 'r').read()),
    outputDir = args[3];
    
var renderPage = function (pages) {
    var urlFragment = pages.pop(),
        url = domain + urlFragment;

    console.log('visiting: ' + url);
    page.open(url, function () {
        var html = page.evaluate(function () {
            return document.getElementsByClassName('treemap')[0].outerHTML;
        });

        fs.write(outputDir + '/treemaps/' + urlFragment + '.html', html);

        if (pages.length > 0) {
            renderPage(pages); 
        } else {
            phantom.exit();
        }
    });
};

renderPage(pagePaths);

