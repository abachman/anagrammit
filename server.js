// DEAD SIMPLE WEB SERVER
var http = require('http');
var port = process.env.PORT || 3000;

generate_anagrams = (req, res) ->
  

// heroku wants the app to bind to a port, so lets do that
var server = http.createServer(function ( req, res ) {
  res.writeHead(200, { 'Content-Type': 'text/plain' })
  res.end('hello from anagrammit!')
});

server.listen(port, function () { console.log("listening on port " + port ) });

