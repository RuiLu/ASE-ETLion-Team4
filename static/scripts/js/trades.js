"use strict";

$(document).ready(function () {
    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    // Event handler for server sent data.
    // The callback function is invoked whenever the server emits data
    // to the client. The data is then displayed in the "Received"
    // section of the page.
    var count = 1;
    var pnl = 0;
    var soldShares = 0;
    var tradeInfo;

    var dataArray = [];
    var dataYears = [];

    // dataArray = [90, 80, 70, 60, 50, 40, 30, 20, 10];
    // dataYears = ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008'];

    // used to receive transaction data
    socket.on("trade_log", function (param) {
        console.log(param);
        tradeInfo = "<tr><td>" + count + "</td><td>Sell</td><td>" + param.share_price + "</td><td>" + param.order_size + "</td><td>" + param.notional + "</td><td>Success</td></tr>";
        $("#trades-table").find("tbody").prepend(tradeInfo);
        count = count + 1;
        pnl += param.notional;
        soldShares += param.order_size;
        $("span#pnl").html(pnl);
        $("span#percentage").html(Math.round(soldShares * 100 / param.total_qty));

        dataArray.push(param.share_price);
        var x = JSON.parse(param.timestamp);
        var y = x.substring(0, x.lastIndexOf("."));
        var z = y.split("T");
        var zz = z[0].concat(" ", z[1]);
        dataYears.push(zz);

        setInterval(function () {
            update(dataArray, dataYears);
        }, 500);
    });

    // used to receive confirmation that transaction is over
    socket.on("trade_over", function (param) {
        console.log(param);
        $("#placeOrder").prop("disabled",false);
        $("#cancelOrder").prop("disabled",true);
    });

    $("#placeOrder").on('click',function() {

        var endTime = $('#timepicker').wickedpicker().wickedpicker('time');
        var startTime = new Date().toLocaleTimeString();

        var endTokens = endTime.split(":");
        var startTokens = startTime.split(":");
        var endHour = endTokens[0].trim();
        var startHour = startTokens[0].trim();
        var endMin = endTokens[1].trim().split(" ")[0];
        var startMin = startTokens[1];
        var endAP = endTokens[1].trim().split(" ")[1];
        var startAP = startTokens[2].trim().split(" ")[1];

        if (endAP == "PM") {
            endHour = (parseInt(endHour) + 12).toString();
        }
        if (startAP == "PM") {
            startHour = (parseInt(startHour) + 12).toString();
        }

        if ((parseInt(endHour) < parseInt(startHour)) ||
            (parseInt(endHour) == parseInt(startHour) && parseInt(endMin) <= parseInt(startMin))) {
            alert("Please choose a time after NOW.");
            return false;
        }

        $(this).prop("disabled",true);
        $("#cancelOrder").prop("disabled",false);

        var duration = (parseInt(endHour) - parseInt(startHour)) * 60 * 60 + 
                       (parseInt(endMin) - parseInt(startMin)) * 60;

        socket.emit("calculate", {
            order_discount: $("#order_discount").val(),
            order_size: $("#order_size").val(),
            inventory: $("#inventory").val(),
            total_duration: duration
        });

        soldShares = 0;
        pnl = 0;
        count = 1;

        $("#trades-table").find("tbody").children().remove();
        $("span#percentage").html(0);
        $("span#pnl").html(0);

        return false;
    });

    $("a#id").click(function (event) {
        socket.emit("logout");
        return false;
    });

    $('div#cancel').click(function(event) {
        $("#placeOrder").prop("disabled",false);
        $("#cancelOrder").prop("disabled",true);
        socket.emit('cancel_order');
        return false;
    });

    var count = 1;

    $("#testAdd").click(function (event) {
        
        console.log("add");
        
        var div = document.createElement('div');
        div.className = 'panel panel-default';
        div.innerHTML += '<div class="panel-heading">' +
                            '<h4 class="panel-title">' +
                                '<a data-toggle="collapse" href="#collapse' + count +'">Order-' + count + '</a>' +
                            '</h4>' +
                        '</div>' +
                        '<div id="collapse' + count + '" class="panel-collapse collapse">' +
                            '<table class = "table" id="history-table-' + count + '">' +
                                '<thead><tr><th>ID</th><th>Type</th><th>Price ($)</th><th>Shares</th><th>Notional</th><th>Timestamp</th><th>Status</th></tr></thead>' +
                                '<tbody id="history-log-'+ count +'">' + 
                                '</tbody>'
                            '</table>'+
                        '</div>';
        document.getElementById("history-group").appendChild(div);    

        var historyTableId = "#history-table-" + count;
        var historyInfo = '<tr><td>1</td><td>Sell</td><td>120.00</td><td>10</td><td>1200</td><td>2016-12-09</td><td>Success</td></tr>"';
        $(historyTableId).find("tbody").prepend(historyInfo);

        count++;
    });
});

var timepickers = $('#timepicker').wickedpicker(); 

// "2016-11-30T16:48:20.412771"
// "2016-11-30T16:48:20"

var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");

var height = 200;
var width = 500;

var margin = {left: 50, right: 50, top: 40, bottom: 0};

var svg = d3.select("#chart").append("svg").attr("width", "100%").attr("height", "100%");

function update(dataArray, dataYears) {

    svg.selectAll("*").remove();

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

    var chartGroup = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    chartGroup.append("path").attr("class", "line").attr("d", line(dataArray));

    chartGroup.append("g")
        .attr("class", "axis x")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    chartGroup.append("g")
        .attr("class", "axis y")
        .call(yAxis);

}