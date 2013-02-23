def init(app):

  app.get('/',
    setStr,
    hello
  )

def setStr(res):
  res.locals['str'] = 'Hello World\n'

def hello(res):
  res.end(res.locals['str'])
