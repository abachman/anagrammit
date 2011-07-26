# DEAD SIMPLE WEB SERVER
http = require('http')
port = process.env.PORT || 3000

spawn = require('child_process').spawn

qs   = require 'querystring'

generate = (req, res) -> 
  query = qs.parse req.url.match(generate.matcher)[2]

  phrase = query.phrase
  phrase = phrase.replace /[^a-z]/, ''

  res.writeHead 200
  res.write "you asked me to generate anagrams of #{ query.phrase }"

  pygen = spawn 'python', ['langs/python/anagrammit.py', phrase]

  data = []

  pygen.stdout.on 'data', (data) ->
    console.log('stdout: ' + data)
    data.push data.trim()

  pygen.stderr.on 'data', (data) ->
    console.log('stderr: ' + data)

  pygen.on 'exit', (code) ->
    console.log('child process exited with code ' + code);
    res.end JSON.stringify(data)
    


generate.matcher = /^\/generate(\?(.*))?$/i

favicon = (req, res) ->
  # don't ask again
  res.writeHead 200, 
    "Last-Modified": "Tue, 15 Nov 1994 12:45:26 GMT"
    "Expires": "1 Jan 2100 12:45:26 GMT"

  res.end ''
favicon.matcher = /favicon/i

generic = (req, res) ->
  res.writeHead 200, 'Content-Type': 'text/plain'
  res.end "hello from anagrammit!"

# Important bits of the request: 
# headers: 
#    { host: 'localhost:3000',
#      connection: 'keep-alive',
#      accept: '*/*',
#      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30',
#      'accept-encoding': 'gzip,deflate,sdch',
#      'accept-language': 'en-US,en;q=0.8',
#      'accept-charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3' }
# url: '/favicon.ico',
# method: 'GET',

# heroku wants the app to bind to a port, so lets do that
server = http.createServer (req, res) ->
  console.log '----------------   REQUEST  --------------------------'
  console.log req.url

  if generate.matcher.test(req.url)
    generate(req, res)
  else if favicon.matcher.test(req.url)
    favicon(req, res)
  else
    generic req, res

  console.log '------------------------------------------------------'

server.listen port, -> console.log("listening on port " + port)

