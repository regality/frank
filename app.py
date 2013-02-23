from lib.frank import frank
#from routes.index import init

app = frank()
app.loadRoutes('routes')
app.listen(3000)
#init(app)
