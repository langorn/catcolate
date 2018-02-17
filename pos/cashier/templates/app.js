var express = require('express');
var app = express();


app.use(express.static(__dirname+'/www'));

var server = app.listen(8082, function(){
	var port = server.address().port;
	console.log('port at '+ port);
})

