const submitButton = document.getElementById('submitButton');

const startSim = () => {
	const time = document.getElementById('simulationTime').value;
	const power = document.getElementById('heaterPower').value;
	const capacity = document.getElementById('waterCapacity').value;

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
			console.log(response);
		})
		.catch((error) => {
			console.error(error);
		});
};
