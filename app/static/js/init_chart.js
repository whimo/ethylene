google.charts.load('current', {'packages':['corechart', 'bar']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var data_table = google.visualization.arrayToDataTable(data_array);
    var material_options = {
        chart: {
            title: 'Comparison of old and new values of manipulable variables',
            subtitle: 'old value on the left, new value on the right'
        }
    };
    var chart = new google.charts.Bar(document.getElementById('chart_div'));
    chart.draw(data_table, google.charts.Bar.convertOptions(material_options));
}

window.addEventListener('resize', drawChart);
