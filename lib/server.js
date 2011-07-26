(function() {
  var favicon, generate, generic, guard, guard_token, http, port, qs, server, spawn;
  http = require('http');
  port = process.env.PORT || 3000;
  spawn = require('child_process').spawn;
  qs = require('querystring');
  guard_token = process.env.API_TOKEN || 'dev';
  guard = new RegExp("^" + guard_token + "$");
  generate = function(req, res) {
    var data, out, phrase, pygen, query;
    query = qs.parse(req.url.match(generate.matcher)[2]);
    if (!(query.token && guard.test(query.token))) {
      console.log("expected: " + guard + ", got: " + query.token);
      res.writeHead(403, {
        "Content-Type": "application/json"
      });
      out = {
        status: "error",
        message: "api access token does not match"
      };
      res.end(JSON.stringify(out));
      return;
    }
    phrase = query.phrase;
    phrase = phrase.replace(/[^a-z]/, '');
    res.writeHead(200, {
      "Content-Type": "application/json"
    });
    pygen = spawn('python', ['langs/python/anagrammit.py', phrase]);
    data = [];
    pygen.stdout.on('data', function(text) {
      var phrase, _i, _len, _ref, _results;
      _ref = text.toString().split('\n');
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        phrase = _ref[_i];
        _results.push(data.push(phrase.trim()));
      }
      return _results;
    });
    pygen.stderr.on('data', function(err) {
      return console.log('stderr: ' + err);
    });
    return pygen.on('exit', function(code) {
      var word;
      console.log('child process exited with code ' + code);
      data = (function() {
        var _i, _len, _results;
        _results = [];
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          word = data[_i];
          if (word.length) {
            _results.push(word);
          }
        }
        return _results;
      })();
      out = {
        status: 'success',
        results: data
      };
      return res.end(JSON.stringify(out));
    });
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
