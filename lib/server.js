(function() {
  var favicon, generate, generic, http, port, qs, server;
  http = require('http');
  port = process.env.PORT || 3000;
  qs = require('querystring');
  generate = function(req, res) {
    var query;
    console.log(req.url);
    console.log(req.url.split('?')[1]);
    query = qs.parse(req.url.match(generate.matcher)[2]);
    console.dir(query);
    res.writeHead(200);
    return res.end("you asked me to generate " + query.phrase);
  };
  generate.matcher = /^\/generate(\?(.*))?$/i;
  favicon = function(req, res) {
    res.writeHead(200, {
      "Last-Modified": "Tue, 15 Nov 1994 12:45:26 GMT",
      "Expires": "1 Jan 2100 12:45:26 GMT"
    });
    return res.end('');
  };
  favicon.matcher = /favicon/i;
  generic = function(req, res) {
    res.writeHead(200, {
      'Content-Type': 'text/plain'
    });
    return res.end("hello from anagrammit!");
  };
  server = http.createServer(function(req, res) {
    console.log('----------------   REQUEST  --------------------------');
    console.log(req.url);
    if (generate.matcher.test(req.url)) {
      generate(req, res);
    } else if (favicon.matcher.test(req.url)) {
      favicon(req, res);
    } else {
      generic(req, res);
    }
    return console.log('------------------------------------------------------');
  });
  server.listen(port, function() {
    return console.log("listening on port " + port);
  });
}).call(this);
