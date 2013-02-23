def init(app):

  app.get('/hai',
    writeHai,
    writeHai,
    writeHai,
    finishHai
  )

  app.get('/bai',
    writeBai,
    writeBai,
    writeBai,
    finishBai
  )

def writeHai(res):
  res.write('hai\n')

def finishHai(res):
  res.end('hai\n')

def writeBai(res):
  res.write('bai\n')

def finishBai(res):
  res.end('bai\n')
