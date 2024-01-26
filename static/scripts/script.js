const submitButton = document.getElementById('submitButton');
const tempSlider = document.getElementById('tempRange');
const tempLabel = document.getElementById('tempLabel');
tempLabel.innerHTML = tempSlider.value + ' °C';

const toggleDiv = (id) => {
	const x = document.getElementById(id);
	if (x.style.display === 'none') {
		x.style.display = 'block';
	} else {
		x.style.display = 'none';
	}
};

tempSlider.oninput = () => {
	tempLabel.innerHTML = tempSlider.value + ' °C';
};

const startSim = () => {
	const temp = tempSlider.value;
	const probe = document.getElementById('probe').value;
	const gain = document.getElementById('gain').value;
	const integral = document.getElementById('integral').value;
	const checkDiv = document.getElementById('check');

	axios
		.post(
			'http://localhost:5000/start',
			{
				temp: temp,
				probe: probe,
				gain: gain,
				integral: integral,
			},
			{
				headers: {
					'Content-Type': 'application/json',
				},
			}
		)
		.then((response) => {
			genGraphs(response['data']);
			checkDiv.style.display = 'block';
		})
		.catch((error) => {
			console.error(error);
		});
};

const genGraphs = (data) => {
	const time = data['time'];
	const config = {
		responsive: true,
	};

	const temp = data['temp'];
	let graphData = [
		{
			x: time,
			y: temp,
			mode: 'lines',
			line: {
				color: 'rgb(0, 170, 0)',
				width: 4,
			},
		},
	];
	let layout = {
		title: {
			text: 'Water temperature',
			font: {
				size: 32,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		yaxis: {
			title: 'Temperature [°C]',
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		height: 700,
	};
	Plotly.newPlot('tempGraph', graphData, layout, config);

	const power = data['heaterPower'];
	graphData = [
		{
			x: time,
			y: power,
			mode: 'lines',
			line: {
				color: 'rgb(255, 0, 0)',
				width: 4,
			},
		},
	];
	layout = {
		title: {
			text: 'Heater power',
			font: {
				size: 32,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		yaxis: {
			title: 'Power [W]',
			dtick: 6000,
			tickformat: ',.0f',
			title: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		height: 700,
	};
	Plotly.newPlot('powerGraph', graphData, layout, config);

	graphData = [
		{
			x: time,
			y: temp,
			name: 'water temperature',
			mode: 'lines',
			line: {
				color: 'rgb(0, 170, 0)',
				width: 4,
			},
		},
		{
			x: time,
			y: power,
			name: 'heater power',
			yaxis: 'y2',
			mode: 'lines',
			line: {
				color: 'rgb(255, 0, 0)',
				width: 4,
			},
		},
	];
	layout = {
		title: {
			text: 'Combined water temp and heater power',
			font: {
				size: 32,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		yaxis: {
			title: 'Temperature [°C]',
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		yaxis2: {
			title: 'Power [W]',
			dtick: 6000,
			tickformat: ',.0f',
			title: {
				size: 24,
			},
			titlefont: {
				size: 24,
				color: 'rgb(0, 0, 0)',
			},
			tickfont: {
				size: 16,
			},
			overlaying: 'y',
			side: 'right',
		},
		height: 700,
	};
	Plotly.newPlot('combinedGraph', graphData, layout, config);

	const flow = data['outFlow'];
	graphData = [
		{
			x: time,
			y: flow,
			mode: 'lines',
			line: {
				width: 4,
			},
		},
	];
	layout = {
		title: {
			text: 'Water flow',
			font: {
				size: 32,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		yaxis: {
			title: 'Flow [l/min]',
			titlefont: {
				size: 24,
			},
			tickfont: {
				size: 16,
			},
		},
		height: 700,
	};
	Plotly.newPlot('flowGraph', graphData, layout, config);
};
