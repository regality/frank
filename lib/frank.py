import os, os.path
import imp
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

_frank = False

def frank():
  global _frank
  if not _frank:
    _frank = Frank()
  return _frank

class Frank():
  routes = {
    'get': [],
    'put': [],
    'post': [],
    'head': [],
    'options': []
  }

  servers = []

  def listen(self, port):
    server = HTTPServer(("localhost", port), FrankHandler)
    self.server = server
    print('Frank listening on port ' + str(port))
    server.serve_forever()

  def get(self, route, *stack):
    self.route('get', route, stack)

  def put(self, route, *stack):
    self.route('put', route, stack)

  def head(self, route, *stack):
    self.route('head', route, stack)

  def post(self, route, *stack):
    self.route('post', route, stack)

  def options(self, route, *stack):
    self.route('options', route, stack)

  def route(self, method, route, stack):
    self.routes[method].append({
      'route': route,
      'stack': stack
    })

  def handle(self, method, res):
    for handler in self.routes[method]:
      if handler['route'] == res.path:
        for i in range(0, len(handler['stack'])):
          handler['stack'][i](res)
          if res.ended:
            return
    # error handlers
    defaultError(res)

  def loadRoutes(self, path):
    for root, _, files in os.walk(path):
      for f in files:
        if f[-3:] == '.py' and not f == '__init__.py':
          print 'loading routes from %s' % f
          name = f[:-3]
          m = __import__('.'.join([ path, name ]))
          init = getattr(getattr(m, name), 'init')
          init(self)

def defaultError(res):
  res.writeHead(404)
  res.end('Could not ' + res.command + ' ' + res.path + '\n')

class FrankHandler(BaseHTTPRequestHandler):
  headersSent = False
  ended = False
  locals = {}

  def do_GET(self):
    self.app = frank()
    self.app.handle('get', self)

  def do_HEAD(self):
    self.app = frank()
    self.app.handle('head', self)

  def do_PUT(self):
    self.app = frank()
    self.app.handle('put', self)

  def do_POST(self):
    self.app = frank()
    self.app.handle('post', self)

  def do_OPTIONS(self):
    self.app = frank()
    self.app.handle('options', self)

  def writeHead(self, code=200, headers={}):
    if self.headersSent:
      print("Headers already sent")
      return
    self.send_response(code)
    self.headers['Server'] = 'Frank'
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

