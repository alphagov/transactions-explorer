describe("Table To Treemap", function () {

  beforeEach(function () {
    table = d3.select("body").append("table").append("tbody");
    table.append("tr").attr("data-title", "service1").attr("data-volume", "1000");
    table.append("tr").attr("data-title", "service2").attr("data-volume", "2000");
    table.append("tr").attr("data-title", "service3").attr("data-volume", "3000");
    table.append("tr").attr("data-title", "service4").attr("data-volume", "1");
    table.append("tr").attr("data-title", "service5").attr("data-volume", "10");
    table.append("tr").attr("data-title", "service6").attr("data-volume", "19");
    
    // Also add in a testmap div
    d3.select('body').append('div').attr('id','testmap');
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
      expect(treeMap.children[0].size).toBe(1000);
      expect(treeMap.children[1].name).toBe("service2");
      expect(treeMap.children[1].size).toBe(2000);
      expect(treeMap.children[2].name).toBe("service3");
      expect(treeMap.children[2].size).toBe(3000);
    });

    it("should group values lower than a threshold", function () {
      var treeMap = Tree.fromHtmlTable(d3.selectAll("tbody tr"), 20);

      expect(treeMap.children[3].name).toBe("Others");
      expect(treeMap.children[3].size).toBe(30);
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

    it("should apply the correct CSS classes to the nodes", function () {
      var data = {
        name: "TreeMap sample",
        children: [
          { name: "Service 1", size: 20 },
          { name: "Service 2", size: 40 },
          { name: "Service 3", size: 10 },
          { name: "Service 4", size: 8 },
          { name: "Service 5", size: 3 },
          { name: "Service 6", size: 1 },
          { name: "Service 7", size: 1 },
          { name: "Service 8", size: 0.1 }
        ]
      };

      TreeMapLayout.display("testmap", data);

      var classes = d3.selectAll('div.node')[0].map(function(d) { return d.className; });
      expect(classes[0]).toEqual('node x-large');
      expect(classes[1]).toEqual('node x-large');
      expect(classes[2]).toEqual('node x-large');
      expect(classes[3]).toEqual('node large');
      expect(classes[4]).toEqual('node medium');
      expect(classes[5]).toEqual('node small');
      expect(classes[6]).toEqual('node ellipsis');
      expect(classes[7]).toEqual('node ellipsis');
      expect(classes[8]).toEqual('node none');
    });
  });
});

