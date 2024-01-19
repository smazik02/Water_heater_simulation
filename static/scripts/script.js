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
	const power = document.getElementById('heaterPower').value;
	const temp = document.getElementById('tempSet').value;
	const checkDiv = document.getElementById('check');

	axios
		.post(
			'http://localhost:5000/start',
			{
				power: power,
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

	const power = data['heaterPower'];
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
};
