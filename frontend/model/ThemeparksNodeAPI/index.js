const express = require('express')
const Themeparks = require("themeparks");

const app = express()
const port = 3150

const disneyMagicKingdom = new Themeparks.Parks.WaltDisneyWorldMagicKingdom();


app.get('/waittime', function (req, res) {	
	var data = {};
	disneyMagicKingdom.GetWaitTimes().then((times) => {
		times.forEach((ride) => {
			data[ride.name] = ride.waitTime;
        })
	}, function(err) {
		console.log(err)
	}).then( function(result){
		res.setHeader('Content-Type', 'application/json')
		res.end(JSON.stringify(data));
	}).catch(function (err) {
		console.log(err);
	});
});

app.listen(port, () => console.log(`Wait time server listening on port ${port}`))