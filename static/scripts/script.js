const submitButton = document.getElementById('submitButton');

const toggleDiv = (id) => {
	const x = document.getElementById(id);
	if (x.style.display === 'none') {
		x.style.display = 'block';
	} else {
		x.style.display = 'none';
	}
};

const startSim = () => {
	const time = document.getElementById('simulationTime').value;
	const power = document.getElementById('heaterPower').value;
	const capacity = document.getElementById('waterCapacity').value;
	const checkDiv = document.getElementById('check');

	axios
		.post(
			'http://localhost:5000/start',
			{
				simTime: time,
				power: power,
				waterCap: capacity,
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

	const temp = data['temp'];
	let graphData = [
		{
			x: time,
			y: temp,
			mode: 'lines',
		},
	];
	let layout = [
		{
			xaxis: { title: 'Time' },
			yaxis: { title: 'Temperature' },
			title: 'Water temperature',
		},
	];
	Plotly.newPlot('tempGraph', graphData, layout);

	const volt = data['volt'];
	graphData = [
		{
			x: time,
			y: volt,
			mode: 'lines',
		},
	];
	layout = [
		{
			xaxis: { title: 'Time' },
			yaxis: { title: 'Voltage' },
			title: 'Regulator voltage',
		},
	];
	Plotly.newPlot('voltGraph', graphData, layout);

	const power = data['power'];
	graphData = [
		{
			x: time,
			y: power,
			mode: 'lines',
		},
	];
	layout = [
		{
			xaxis: { title: 'Time' },
			yaxis: { title: 'Power' },
			title: 'Heater power',
		},
	];
	Plotly.newPlot('powerGraph', graphData, layout);

	const flow = data['outFlow'];
	graphData = [
		{
			x: time,
			y: flow,
			mode: 'lines',
		},
	];
	layout = [
		{
			xaxis: { title: 'Time' },
			yaxis: { title: 'Flow' },
			title: 'Water flow',
		},
	];
	Plotly.newPlot('flowGraph', graphData, layout);

	const e = data['e'];
	graphData = [
		{
			x: time,
			y: e,
			mode: 'lines',
		},
	];
	layout = [
		{
			xaxis: { title: 'Time' },
			yaxis: { title: 'E' },
			title: 'E',
		},
	];
	Plotly.newPlot('eGraph', graphData, layout);
};
