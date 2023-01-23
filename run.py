import webapp.config as c
from webapp import app

if __name__ == '__main__':
    app.run(port=c.flask_port,host=c.host, debug=c.debug)
