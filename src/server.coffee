# DEAD SIMPLE WEB SERVER
http  = require 'http'
spawn = require('child_process').spawn
qs    = require 'querystring'

# if you're using pat-the-campfire-bot, make sure you add the same API_TOKEN to both heroku envs
guard_token = process.env.API_TOKEN || 'dev'
guard       = new RegExp("^" + guard_token + "$");

generate = (req, res) -> 
  query = req.url.match(generate.matcher)
  query = query[2]
  query = qs.parse(query)

  unless query.token && guard.test(query.token)
    console.log "expected: #{ guard }, got: #{ query.token }"
    res.writeHead 403, "Content-Type": "application/json"
    out = 
      status: "error"
      message: "api access token does not match"
    res.end JSON.stringify(out)
    return

  phrase = query.phrase.replace /[^a-z]/, ''

  # start the generator
  pygen = spawn 'python', ['langs/python/anagrammit.py', phrase]

  data = []

  pygen.stdout.on 'data', (text) ->
    data.push(phrase.trim()) for phrase in text.toString().split('\n')

  pygen.stderr.on 'data', (err) ->
    console.log('stderr: ' + err)

  pygen.on 'exit', (code) ->
    res.writeHead 200, "Content-Type": "application/json"

    data = (word for word in data when word.length)
    out = 
      status: 'success'
      results: data

    res.end JSON.stringify(out)

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

server = http.createServer (req, res) ->
  if generate.matcher.test(req.url)
    generate(req, res)
  else if favicon.matcher.test(req.url)
    favicon(req, res)
  else
    generic req, res

port = process.env.PORT || 3000
server.listen port, -> console.log("listening on port " + port)

