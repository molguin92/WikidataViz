function drawGraph(json) {
    var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function (d) {
        return "<span style='color:red'>" + d.label + "</span>";
    });

    var width  = window.innerWidth * 0.8,
        height = window.innerHeight * 0.8;

    var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

    var force = d3.layout.force()
    .gravity(.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);


    svg.call(tip);
    force
    .nodes(json.nodes)
    .links(json.links)
    .start();

    var link = svg.selectAll(".link")
    .data(json.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", 2);

    var node = svg.selectAll(".node")
    .data(json.nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(force.drag);

    node.append("circle")
    .attr("r", "5")
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide)
    .on('click', function (d) {
        window.open(d.id);
    });

    force.on("tick", function () {
        link.attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });

        node.attr("transform", function (d) { return "translate(" + d.x + "," + d.y + ")"; });
    });
}
