var dataArray = [90, 80, 70, 60, 50, 40, 30, 20, 10];
var dataYears = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008'];

var parseDate = d3.timeParse("%Y");

var height = 200;
var width = 500;

var margin = {left: 50, right: 50, top: 40, bottom: 0};

var x = d3.scaleTime()
    .domain(d3.extent(dataYears, function (d) {
        return parseDate(d);
    }))
    .range([0, width]);

var y = d3.scaleLinear()
    .domain(d3.extent(dataArray, function (d) {
        return d;
    }))
    .range([height, 0]);

var xAxis = d3.axisBottom(x);
var yAxis = d3.axisLeft(y).ticks(3).tickPadding(10).tickSize(10);

var line = d3.line()
    .x(function (d, i) {
        return x(parseDate(dataYears[i]));
    })
    .y(function (d, i) {
        return y(dataArray[i]);
    });

var svg = d3.select("#chart").append("svg").attr("width", "100%").attr("height", "100%");

var chartGroup = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

chartGroup.append("path").attr("class", "line").attr("d", line(dataArray));

chartGroup.append("g")
    .attr("class", "axis x")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

chartGroup.append("g")
    .attr("class", "axis y")
    .call(yAxis);
