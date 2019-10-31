const exec = require('child_process').exec;

if (process.argv.length <= 2) {
	console.log('Usage: ' + __filename + ' service_name');
	process.exit(-1);
}
const cluster = process.argv[2];
const services = process.argv[3];

services.split(',').forEach((service) => {
	console.log(`killing all ${service} tasks`);
	killService(service);
});

function killService(service) {
	exec(`aws --region us-west-2 ecs list-tasks --cluster ${cluster} --service-name ${service}`, (error, stdout, stderr) => {
		console.log(stdout);
		console.log(stderr);
		const tasks = JSON.parse(stdout);
		const arns = tasks.taskArns;
		arns.forEach(arn => {
			const task = arn.split('/')[1];
			exec(`aws --region us-west-2 ecs stop-task --cluster ${cluster} --task ${task}`, (error, stdout, stderr) => {
				console.log(stdout);
				console.log(stderr);
				if (error !== null) {
					throw new Error(`exec error: ${error}`);
				}
			});
		});
		if (error !== null) {
			throw new Error(`exec error: ${error}`);
		}
	});

}
