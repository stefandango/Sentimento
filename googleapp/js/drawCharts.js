function drawAllChart(json_data) {
	var data = google.visualization.arrayToDataTable(json_data);

	var options = {
	  title: 'Samlet sentiment',
	  width: 600,
	  height: 400,
	  vAxis: { minValue: 0 }
	};

	var chart = new google.visualization.ColumnChart(document.getElementById('allChartDiv'));
	chart.draw(data, options);
}

function drawYearChart(json_data) {
	var data = google.visualization.arrayToDataTable(json_data);

	var options = {
	  title: 'Visualiseret over år',
	  width: 600,
	  height: 400
	};

	var chart = new google.visualization.ColumnChart(document.getElementById('yearChartDiv'));
	chart.draw(data, options);
}

function drawMonthChart(json_data) {
	var data = google.visualization.arrayToDataTable(json_data);

	var options = {
	  title: 'Visualiseret over måneder',
	  width: 600,
	  height: 400
	};

	var chart = new google.visualization.ColumnChart(document.getElementById('monthChartDiv'));
	chart.draw(data, options);
}

function drawWeekChart(json_data) {
	var data = google.visualization.arrayToDataTable(json_data);

	var options = {
	  title: 'Visualiseret over uger',
	  width: 600,
	  height: 400
	};

	var chart = new google.visualization.ColumnChart(document.getElementById('weekChartDiv'));
	chart.draw(data, options);
}

function drawDayChart(json_data) {
	var data = google.visualization.arrayToDataTable(json_data);

	var options = {
	  title: 'Visualiseret over dage',
	  width: 600,
	  height: 400
	};

	var chart = new google.visualization.LineChart(document.getElementById('dayChartDiv'));
	chart.draw(data, options);
}