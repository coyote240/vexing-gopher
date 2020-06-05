#!/usr/bin/env python3


'''
'''

from flask import Flask
from flask_gopher import GopherExtension, GopherRequestHandler


app = Flask(__name__)
app.config.from_pyfile('vexing.cfg')

gopher = GopherExtension(app)


@app.route('/')
def index():
    return gopher.render_menu_template('index.gopher')


@app.route('/about')
def about():
    return gopher.render_menu_template('about.gopher')


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            threaded=app.config['THREADED'],
            processes=app.config['PROCESSES'],
            request_handler=GopherRequestHandler)
