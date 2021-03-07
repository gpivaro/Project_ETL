// Update categories using Jquery/Ajax

// Return date formated to local string
function formatDate(myDate) {
    /* Date.prototype.toLocaleDateString()
     https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString */
    var timeOptions = { year: 'numeric', month: 'numeric', day: 'numeric' };
    // timeOptions.timeZone = 'UTC';
    // Retrieve the newest meas time and convert the format
    var newestData = new Date(myDate);
    var newestDataTime = newestData.toLocaleTimeString("en-US", timeOptions);
    return newestDataTime
}


$(document).ready(function () {

    // Get the path to find the API to provide JSON data
    var currentPath = window.location.pathname;

    // Set the request to the backend using Ajax and GET request
    req = $.ajax({
        url: currentPath + '/json',
        type: 'GET',

        success: function (stockData) {
            console.log(stockData);
            // Fade out and fade in the section to visualization

            // var myDate = new Date(stockData[stockData.length - 1].date);
            // console.log(`${myDate.getFullYear()}-${myDate.getMonth() + 1}-${myDate.getDate() + 1}`);

            var format = { year: '2-digit', month: '2-digit', day: '2-digit' };
            var trace1 = {
                x: stockData.map(element => Intl.DateTimeFormat('en-US', format).format(element.date)),
                y: stockData.map(element => element.CLOSING_PRICE),
                type: 'scatter'
            };

            var data = [trace1];

            var layout = {
                title: `Closing Prices for ${stockData[1].comp_tick} Over Time`,
                xaxis: {
                    title: 'Date',
                    showgrid: false,
                    zeroline: false,
                },
                yaxis: {
                    title: 'Closing Price ($)',
                    showline: false
                },
                margin: {
                    l: 60,
                    r: 60,
                    b: 160,
                    t: 60,
                    pad: 4
                }
            };

            // Responsive chart
            var config = { responsive: true, displayModeBar: false }

            Plotly.newPlot('closingPricePlot', data, layout, config);


        },
        error: function (error) {
            console.log(error);
        }
    });

});
