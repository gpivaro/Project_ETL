// Plot closing prices using AJAX
$(document).ready(function () {

    // Get the path to find the API to provide JSON data
    var currentPath = window.location.pathname;

    // Set the request to the backend using Ajax and GET request
    req = $.ajax({
        url: currentPath + '/json',
        type: 'GET',

        success: function (stockData) {
            // console.log(stockData);

            // call function to generate plot
            generatePlotlyPlot(stockData)
        },
        error: function (error) {
            console.log(error);
        }
    });

});



function generatePlotlyPlot(stockData) {
    var trace1 = {
        // Convert date from unix to ISO format to match table
        x: stockData.map(element => {
            var myDate = new Date(element.date);
            var newDate = myDate.toISOString().split('T')[0];
            return newDate
        }),

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
            autorange: true,
            range: [`${stockData[0]}`, `${stockData[stockData.length - 1]}`],
            rangeselector: {
                buttons: [
                    {
                        count: 1,
                        label: '1m',
                        step: 'month',
                        stepmode: 'backward'
                    },
                    {
                        count: 6,
                        label: '6m',
                        step: 'month',
                        stepmode: 'backward'
                    },
                    {
                        count: 12,
                        label: '12m',
                        step: 'month',
                        stepmode: 'backward'
                    },
                    { step: 'all' }
                ]
            },
            rangeslider: { range: [`${stockData[0]}`, `${stockData[stockData.length - 1]}`] },
            type: 'date'
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
};