describe("Table To Treemap", function () {

  var wrapper;
  beforeEach(function () {
    table = d3.select("body").append("table").append("tbody");
    table.append("tr")
      .attr("data-title", "service1")
      .attr("data-label", "srvc1")
      .attr("data-href", "service1")
      .attr("data-volume", "1000");
    table.append("tr")
      .attr("data-title", "service2")
      .attr("data-href", "service2")
      .attr("data-volume", "2000");
    table.append("tr")
      .attr("data-title", "service3")
      .attr("data-href", "service3")
      .attr("data-volume", "3000");
    table.append("tr")
      .attr("data-title", "service4")
      .attr("data-volume", "1");
    table.append("tr")
      .attr("data-title", "service5")
      .attr("data-volume", "10");
    table.append("tr")
      .attr("data-title", "service6")
      .attr("data-volume", "19");

    // Also add in a testmap div
    wrapper = d3.select('body').append('div')
      .attr('id','testmap')
      .style({
        width: '960px',
        height: '460px'
      });

    this.addMatchers(customMatchers);

  });

  afterEach(function () {;
    d3.selectAll("table").data([]).exit().remove();
    d3.selectAll("div#testmap").data([]).exit().remove();
  });

  describe("HTML Table to D3 TreeMap", function () {
    it("should convert html table to d3 treemap representation", function () {
      var treeMap = Tree.fromHtmlTable(d3.selectAll("tbody tr"), 20);

      expect(treeMap.name).toBe("Service Explorer");
      expect(treeMap.children[0].name).toBe("service1");
      expect(treeMap.children[0].nameShortened).toBe("srvc1");
      expect(treeMap.children[0].size).toBe(1000);
      expect(treeMap.children[1].name).toBe("service2");
      expect(treeMap.children[1].size).toBe(2000);
      expect(treeMap.children[2].name).toBe("service3");
      expect(treeMap.children[2].size).toBe(3000);
    });

    it("should group values lower than a threshold and without a link", function () {
      var treeMap = Tree.fromHtmlTable(d3.selectAll("tbody tr"), 20);

      expect(treeMap.children[3].name).toBe("Others");
      expect(treeMap.children[3].size).toBe(30);
    });
    it("should not group values lower than a threshold when they have a link", function () {
      table.append("tr")
        .attr("data-title", "service7")
        .attr("data-href", "service7")
        .attr("data-volume", "19");

      var treeMap = Tree.fromHtmlTable(d3.selectAll("tbody tr"), 20);

      expect(treeMap.children[3].name).toBe("service7");
      expect(treeMap.children[3].size).toBe(19);
      expect(treeMap.children[4].name).toBe("Others");
      expect(treeMap.children[4].size).toBe(30);
    });
  });

  describe("TreeMap display", function() {
    it("should display services in a treemap", function() {
      var data = {
        name: "TreeMap sample",
        children: [
          { name: "Service 1", size: 20 },
          { name: "Service 2", size: 40 },
          { name: "Service 3", size: 10 }
        ]
      };

      TreeMapLayout.display("testmap", data);

      var treeNodes = d3.selectAll('div.node a')[0].map(function(d) { return d.innerHTML; });

      expect(treeNodes).toEqual(["", "Service 1", "Service 2", "Service 3"]);
    });

    it("should display services in a treemap with shortened volume label when available", function() {
      var data = {
        name: "TreeMap sample",
        children: [
          { name: "Service 1", size: 20 },
          { name: "Service 2", size: 40, volumeShortened: '44' },
          { name: "Service 3", size: 10, volumeShortened: '' }
        ]
      };

      TreeMapLayout.display("testmap", data);

      var treeNodes = d3.selectAll('div.node a')[0].map(function(d) { return d.innerHTML; });

      expect(treeNodes).toEqual([
        "",
        "Service 1",
        'Service 2<span class="amount">44</span>',
        "Service 3"
      ]);
    });

    it("should apply the correct CSS classes to the nodes, including department abbreviation", function () {
      var data = {
        name: "TreeMap sample",
        children: [
          { name: "Service 1", deptClass: "hmrc", size: 20 },
          { name: "Service 2", deptClass: "hmrc", size: 40 },
          { name: "Service 3", deptClass: "hmrc", size: 10 },
          { name: "Service 4", deptClass: "dft", size: 8 },
          { name: "Service 5", deptClass: "silly-walks", size: 3 },
          { name: "Service 6", deptClass: "dfid", size: 1 },
          { name: "Service 7", deptClass: "defra", size: 1 },
          { name: "Service 8", deptClass: "hmrc", size: 0.1 }
        ]
      };

      TreeMapLayout.display("testmap", data);


      var classes = d3.selectAll('div.node')[0].map(function(d) { return d.className; });
      expect(classes[0]).shouldContain(['xx-large', 'group']);
      expect(classes[1]).shouldContain(['node', 'x-large', 'leaf', 'hmrc']);
      expect(classes[2]).shouldContain(['node', 'xx-large', 'leaf', 'hmrc']);
      expect(classes[3]).shouldContain(['node', 'large', 'leaf', 'hmrc']);
      expect(classes[4]).shouldContain(['node', 'medium', 'dft']);
      expect(classes[5]).shouldContain(['node', 'small', 'leaf', 'silly-walks']);
      expect(classes[6]).shouldContain(['node', 'ellipsis', 'leaf', 'dfid']);
      expect(classes[7]).shouldContain(['node', 'ellipsis', 'leaf', 'defra']);
      expect(classes[8]).shouldContain(['node', 'none', 'leaf', 'hmrc']);
    });

    it("should shorten displayed text to make it fit", function () {
      wrapper.style('height', '60px');
      wrapper.style('width', '300px');

      var data = {
        name: "TreeMap sample",
        children: [
          { name: "Service 1 has a very long name that needs to be shortened", size: 20 },
          { name: "Service 2 also has a name that is shortened in favour of the amount", size: 20, volumeShortened: '44' },
          { name: "Service 3", size: 50, volumeShortened: '' }
        ]
      };

      TreeMapLayout.display("testmap", data);

      var treeNodes = d3.selectAll('div.node a')[0].map(function(d) { return d.innerHTML; });

      expect(treeNodes[1].length < data.children[0].name.length).toBe(true);
      expect(treeNodes[1].indexOf('…')).not.toEqual(-1);

      expect(treeNodes[2].length < data.children[1].name.length).toBe(true);
      expect(treeNodes[2].indexOf('…')).not.toEqual(-1);
      expect(treeNodes[2].indexOf('<span class="amount">44</span>')).not.toEqual(-1);

      expect(treeNodes[3].length).toEqual(data.children[2].name.length);
      expect(treeNodes[3].indexOf('…')).toEqual(-1);
    });

    it("should use a shortened name when available to make it fit", function () {
      wrapper.style('height', '60px');
      wrapper.style('width', '300px');

      var data = {
        name: "TreeMap sample",
        children: [
          {
            name: "Service 1 has a very long name that needs to be shortened",
            nameShortened: "Service 1",
            size: 20
          },
          {
            name: "Service 2 also has a name that is shortened in favour of the amount",
            nameShortened: "Service 2 shortname is still too long",
            size: 20,
            volumeShortened: '44'
          },
          {
            name: "Service 3",
            size: 50,
            volumeShortened: ''
          }
        ]
      };

      TreeMapLayout.display("testmap", data);

      var treeNodes = d3.selectAll('div.node a')[0].map(function(d) { return d.innerHTML; });

      expect(treeNodes[1].length).toEqual(data.children[0].nameShortened.length);
      expect(treeNodes[1].indexOf('…')).toEqual(-1);

      expect(treeNodes[2].length < data.children[1].name.length).toBe(true);
      expect(treeNodes[2].indexOf('…')).not.toEqual(-1);
      expect(treeNodes[2].indexOf('<span class="amount">44</span>')).not.toEqual(-1);

      expect(treeNodes[3].length).toEqual(data.children[2].name.length);
      expect(treeNodes[3].indexOf('…')).toEqual(-1);
    });

    it("passes if all treemap nodes are positioned absolutely (not stactically)", function () {

      wrapper.style('height', '30px');

      var data = {
        name: "TreeMap sample",
        children: [
          { name: "Service 1 has a very long name that needs to be shortened", size: 20 },
          { name: "Service 2 also has a name that is shortened in favour of the amount", size: 20, volumeShortened: '44' },
          { name: "Service 3", size: 50, volumeShortened: '' }
        ]
      };

      TreeMapLayout.display("testmap", data);

      var positions = d3.selectAll('div.node a')[0].map(function(d) {
          return d.style.position;
      });

      // cut out the parent node
      positions.splice(0, 1);

      expect(positions).toEqual(['absolute','absolute','absolute']);

    });


  });

  describe("formatNumericLabel", function() {

    var formatNumericLabel = Tree.formatNumericLabel;

    it("should display entire numbers from 0 to 499", function() {
      expect(formatNumericLabel(0)).toBe('0');
      expect(formatNumericLabel(1)).toBe('1');
      expect(formatNumericLabel(9)).toBe('9');
      expect(formatNumericLabel(10)).toBe('10');
      expect(formatNumericLabel(77)).toBe('77');
      expect(formatNumericLabel(100)).toBe('100');
      expect(formatNumericLabel(398)).toBe('398');
      expect(formatNumericLabel(499)).toBe('499');
    });

    it("should display numbers from 500 to 499499 as fractions of 1k", function() {
      expect(formatNumericLabel(500)).toBe('0.50k');
      expect(formatNumericLabel(777)).toBe('0.78k');
      expect(formatNumericLabel(994)).toBe('0.99k');
      expect(formatNumericLabel(995)).toBe('1.00k');
      expect(formatNumericLabel(996)).toBe('1.00k');
      expect(formatNumericLabel(999)).toBe('1.00k');
      expect(formatNumericLabel(1000)).toBe('1.00k');
      expect(formatNumericLabel(1005)).toBe('1.01k');
      expect(formatNumericLabel(1006)).toBe('1.01k');
      expect(formatNumericLabel(100000)).toBe('100k');
      expect(formatNumericLabel(234568)).toBe('235k');
      expect(formatNumericLabel(499499)).toBe('499k');
    });

    it("should display numbers from 499500 and above as fractions of 1m", function() {
      expect(formatNumericLabel(499500)).toBe('0.50m');
      expect(formatNumericLabel(500000)).toBe('0.50m');
      expect(formatNumericLabel(777777)).toBe('0.78m');
      expect(formatNumericLabel(994499)).toBe('0.99m');
      expect(formatNumericLabel(994999)).toBe('0.99m');
      expect(formatNumericLabel(995000)).toBe('1.00m');
      expect(formatNumericLabel(995001)).toBe('1.00m');
      expect(formatNumericLabel(999900)).toBe('1.00m');
      expect(formatNumericLabel(1000000)).toBe('1.00m');
      expect(formatNumericLabel(1005000)).toBe('1.01m');
      expect(formatNumericLabel(1005001)).toBe('1.01m');
      expect(formatNumericLabel(100000000)).toBe('100m');
      expect(formatNumericLabel(234568234)).toBe('235m');
      expect(formatNumericLabel(499499499)).toBe('499m');
    });

    describe("generative tests", function() {
      var createTests = function(start, end, increment, format) {
        it("should correctly format numbers in the range " + start + "-" + end, function() {
          for (var i = start; i < end; i+=increment) {
            createExpectation(i, format(i));
          }
        })
      },
      createExpectation = function(i, expectation) {
        expect(formatNumericLabel(i)).toBe(expectation);
      };


      createTests(0,   20,   1, function(i) { return i.toString(); });
      createTests(500, 600,  1, function(i) { return "0." + Math.round(i / 10) + "k"; });
      createTests(980, 995,  1, function(i) { return "0." + Math.round(i / 10) + "k"; });
      createTests(995, 1000, 1, function(i) {
        var expected = "1." + (Math.round(i / 10) - 100);
        if (expected.length < 4) {
          expected += "0";
        }
        return expected + "k";
      });
      createTests(1000,   1100,    1,    function(i) { return (Math.round(i / 10) / 100).toPrecision(3) + "k"; });
      createTests(9400,   10000,   10,   function(i) { return (Math.round(i / 10) / 100).toPrecision(3) + "k"; });
      createTests(10000,  11500,   10,   function(i) { return (Math.round(i / 100) / 10).toPrecision(3) + "k"; });
      createTests(50450,  50500,   10,   function(i) { return (Math.round(i / 100) / 10).toPrecision(3) + "k"; });
      createTests(100000, 101000,  10,   function(i) { return Math.round(i / 1000).toPrecision(3) + "k"; });
      createTests(499000, 499500,  100,  function(i) { return Math.round(i / 1000).toPrecision(3) + "k"; });
      createTests(499500, 500000,  100,  function(i) { return (Math.round(i / 10000) / 100).toPrecision(2) + "m"; });
      createTests(504500, 506000,  150,  function(i) { return (Math.round(i / 10000) / 100).toPrecision(2) + "m"; });
      createTests(700000, 800000,  150,  function(i) { return (Math.round(i / 10000) / 100).toPrecision(2) + "m"; });
      createTests(994499, 995000,  150,  function(i) { return (Math.round(i / 10000) / 100).toPrecision(2) + "m"; });
      createTests(995000, 999999,  150,  function(i) { return (Math.round(i / 10000) / 100).toPrecision(3) + "m"; });
      createTests(999999, 1999999, 10000, function(i) { return (Math.round(i / 10000) / 100).toPrecision(3) + "m"; });
    });

    describe("Number Formatting", function () {
      it("should now show millions to two decimal places", function () {
        expect(formatNumericLabel(1220000)).toBe("1.22m");
      });

      it("should show all millions to two decimal places", function () {
        expect(formatNumericLabel(1000000)).toBe("1.00m");
        expect(formatNumericLabel(1010000)).toBe("1.01m");
        expect(formatNumericLabel(9099000)).toBe("9.10m");
        expect(formatNumericLabel(1009900)).toBe("1.01m");
      });

      var numberWithCommas = Tree.numberWithCommas;

      it("should add commas to separate a number by thousands (return as a string)", function () {
        expect(numberWithCommas(1000000)).toBe("1,000,000");
        expect(numberWithCommas(9999)).toBe("9,999");
        expect(numberWithCommas(19823749873249)).toBe("19,823,749,873,249");
        expect(numberWithCommas(100)).toBe("100");
        expect(numberWithCommas(10)).toBe("10");
        expect(numberWithCommas(0)).toBe("0");
      })
    });



  });
});

