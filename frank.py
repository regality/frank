from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

_frank = False

routes = {
  'get': [],
  'head': [],
  'post': [],
  'put': [],
  'options': []
}

def handle(method, res):
  for handler in routes[method]:
    if handler['route'] == res.path:
      for i in range(0, len(handler['stack'])):
        handler['stack'][i](res)
        if res.ended:
          return
  fourOhFour(res)

def fourOhFour(res):
  res.writeHead(404)
  res.end('Could not ' + res.command + ' ' + res.path + '\n')

class Handler(BaseHTTPRequestHandler):
  headersSent = False
  ended = False
  locals = {}

  def do_GET(self):
    handle('get', self)

  def do_POST(self):
    handle('post', self)

  def writeHead(self, code=200, headers={}):
    if self.headersSent:
      print("Headers already sent")
      return
    self.send_response(code)
    for name, value in headers:
      self.send_header(name, value)
    self.end_headers()
    self.headersSent = True

  def write(self, response):
    if not self.headersSent:
      self.writeHead(200)
    self.wfile.write(response)

  def end(self, response):
    if response:
      self.write(response)
    self.ended = True

class Frank():
  def __init__(self):
    pass

  def listen(self, port):
    server = HTTPServer(("localhost", port), Handler)
    server.serve_forever()

  def get(self, route, *stack):
    self.route('get', route, stack)

  def head(self, route, *stack):
    self.route('head', route, stack)

  def post(self, route, *stack):
    self.route('post', route, stack)

  def put(self, route, *stack):
    self.route('put', route, stack)

  def options(self, route, *stack):
    self.route('options', route, stack)

  def route(self, method, route, stack):
    routes[method].append({
      'route': route,
      'stack': stack
    })

def frank():
  global _frank
  if not _frank:
    _frank = Frank()
  return _frank
