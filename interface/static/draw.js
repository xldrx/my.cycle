function draw_rose(start_date, width, height, radius) {
    //start_date = date(start_date);
    width = typeof width !== 'undefined' ? width : 300;
    height = typeof height !== 'undefined' ? height : 300;
    radius = typeof radius !== 'undefined' ? radius : 100;

    innerRadius = 0.0 * radius;

    var pie = d3.layout.pie()
        .sort(null)
        .value(function (d) {
            return d.intra;
        });

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .direction('s')
        //.offset([0, 0])
        .html(function (d) {
            var tip_src = "";
            if (d.data.img != ''){
                tip_src+="<img src='" + d.data.img_addr + "' height=400px weight=400px/>"
            }
            tip_src+="<br/>"+ d.data.acctual_date;
            tip_src+="<br/><b>Awesome: </b>"+ d.data.awesomeness;
            tip_src+="<br/><b>Activity: </b>"+ d.data.activity;
            return tip_src;
        });

    var arc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(function (d) {
            return (radius - innerRadius) * (d.data.inter / 100.0) + innerRadius;
        });

    var outlineArc = d3.svg.arc()
        .innerRadius(innerRadius)
        .outerRadius(radius);


    var svg = d3.select("#timeline").append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr('class','child')
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


    svg.call(tip);

    d3.csv('/data/' + start_date, function (error, data) {

        data.forEach(function (d) {
            d.id = d.date;
            d.acctual_date = d.date;
            //d.img = d.img;
            d.img_addr = "/static/imgs/" + d.img;
            d.inter = d.awesomeness;
            d.intra = d.activity;
        });

        data.forEach(function (d) {
            svg.append("pattern")
                .attr("id", d.img)
                .attr("patternContentUnits", "objectBoundingBox")
                .attr("viewBox", "0 0 1 1")
                .attr("preserveAspectRatio", "xMidYMid slice")
                .attr("width", "100%")
                .attr("height", "100%")
                .append("image")
                .attr("xlink:href", d.img_addr)
                .attr("width", "1")
                .attr("height", "1")
                .attr("preserveAspectRatio", "xMidYMid slice")
        });


        var path = svg.selectAll(".solidArc")
            .data(pie(data))
            .enter().append("path")
            .attr("fill", function (d) {
                return "url(#" + d.data.img + ")";
            })
            .attr("class", "solidArc")
            .attr("stroke", "white")
            .attr("stroke-width", "1")
            .attr("d", arc)
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        var outerPath = svg.selectAll(".outlineArc")
            .data(pie(data))
            .enter().append("path")
            .attr("fill", "none")
            .attr("stroke", "gray")
            .attr("stroke-width", "1")
            .attr("class", "outlineArc")
            .attr("d", outlineArc);

    });
}