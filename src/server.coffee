# DEAD SIMPLE WEB SERVER
http = require('http');
port = process.env.PORT || 3000;

# heroku wants the app to bind to a port, so lets do that
server = http.createServer (req, res) ->
  res.writeHead 200, 
    'Content-Type': 'text/plain'
  res.end 'hello from anagrammit!'

server.listen port, -> console.log("listening on port " + port)

