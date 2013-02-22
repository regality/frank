from frank import frank

def init():
  app = frank()

  app.get('/',
    setStr,
    hello
  )

  app.get('/hai',
    writeHai,
    writeHai,
    writeHai,
    finishHai
  )

  app.listen(3000)

def setStr(res):
  res.locals['str'] = 'Hello World\n'

def hello(res):
  res.end(res.locals['str'])

def writeHai(res):
  res.write('hai\n')

def finishHai(res):
  res.end('hai\n')

init()
