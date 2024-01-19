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
	const checkDiv = document.getElementById('check');

	axios
		.post(
			'http://localhost:5000/start',
			{
				temp: temp,
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
		},
	];
	let layout = {
		title: {
			text: 'Water temperature',
			font: {
				size: 22,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
		},
		yaxis: {
			title: 'Temperature [°C]',
		},
	};
	Plotly.newPlot('tempGraph', graphData, layout, config);

	const power = data['heaterPower'];
	graphData = [
		{
			x: time,
			y: power,
			mode: 'lines',
		},
	];
	layout = {
		title: {
			text: 'Heater power',
			font: {
				size: 22,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
		},
		yaxis: {
			title: 'Power [W]',
			dtick: 6000,
			tickformat: ',.0f',
		},
	};
	Plotly.newPlot('powerGraph', graphData, layout, config);

	const flow = data['outFlow'];
	graphData = [
		{
			x: time,
			y: flow,
			mode: 'lines',
		},
	];
	layout = {
		title: {
			text: 'Water flow',
			font: {
				size: 22,
			},
		},
		xaxis: {
			title: 'Time [s]',
			dtick: 60,
		},
		yaxis: {
			title: 'Flow [l/min]',
		},
	};
	Plotly.newPlot('flowGraph', graphData, layout, config);
};
