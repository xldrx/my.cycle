var width = 960,
    height = 640,
    radius = 250,
    //radius = Math.min(width, height) / 2,
    innerRadius = 0.0 * radius;

var pie = d3.layout.pie()
    .sort(null)
    .value(function (d) {
        return d.intra;
    });

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([0, 0])
    .html(function (d) {
//    return d.data.label + ": <span style='color:orangered;'>" + d.data.score + "</span>";
        return "<img src='" + d.data.img_addr + "' height=100px weight=100px/>"
    });

var arc = d3.svg.arc()
    .innerRadius(innerRadius)
    .outerRadius(function (d) {
        return (radius - innerRadius) * (d.data.inter / 100.0) + innerRadius;
    });

var outlineArc = d3.svg.arc()
    .innerRadius(innerRadius)
    .outerRadius(radius);


var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

//var svg = d3.select("g");

svg.call(tip);

d3.csv('data.txt', function (error, data) {

    data.forEach(function (d) {
        d.id = d.date;
        d.img = d.img;
        d.img_addr = "imgs/" + d.img;
        d.like = +d.like;
        d.comment = +d.comment;
        d.steps = +d.steps;
        d.inter = d.like;
        d.intra = Math.log(d.steps);
    });
    // for (var i = 0; i < data.score; i++) { console.log(data[i].id) }

    data.forEach(function (d){
        svg.append("pattern")
            .attr("id", d.img)
            //.attr("patternUnits","objectBoundingBox")
            .attr("patternUnits","userSpaceOnUse")
            .attr("x",0)
            .attr("y",radius)
            .attr("width",radius*2)
            .attr("height",radius*2)
            .append("image")
            .attr("xlink:href", d.img_addr)
            .attr("x","0")
            .attr("y","0")
            .attr("width",radius*2)
            .attr("height",radius*2)
    });


    var path = svg.selectAll(".solidArc")
        .data(pie(data))
        .enter().append("path")
//      .attr("fill", function(d) { return d.data.color; })
        .attr("fill", function(d) {
            return "url(#"+ d.data.img+")"; })
        .attr("class", "solidArc")
        .attr("stroke", "black")
        .attr("stroke-width", "3")
        .attr("d", arc)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);


//  var outerPath = svg.selectAll(".outlineArc")
//      .data(pie(data))
//    .enter().append("path")
//      .attr("fill", "none")
//      .attr("stroke", "gray")
//      .attr("class", "outlineArc")
//      .attr("d", outlineArc);


    // calculate the weighted mean score
//  var score =
//    data.reduce(function(a, b) {
//      //console.log('a:' + a + ', b.score: ' + b.score + ', b.weight: ' + b.weight);
//      return a + (b.score * b.weight);
//    }, 0) /
//    data.reduce(function(a, b) {
//      return a + b.weight;
//    }, 0);

//  svg.append("svg:text")
//    .attr("class", "aster-score")
//    .attr("dy", ".35em")
//    .attr("text-anchor", "middle") // text-align: right
//    .text(Math.round(score));

});