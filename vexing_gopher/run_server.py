#!/usr/bin/env python3


'''
'''

import argparse
from flask import Flask
from flask_gopher import GopherExtension, GopherRequestHandler


app = Flask(__name__)
gopher = GopherExtension(app)


@app.route('/')
def index():
    return gopher.render_menu_template('index.gopher')


@app.route('/about')
def about():
    return gopher.render_menu_template('about.gopher')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='config file',
                        default='/etc/vexing-gopher.ini')
    parser.add_argument('-H', '--host',
                        default='0.0.0.0')
    parser.add_argument('-p', '--port',
                        default=70)
    parser.add_argument('-P', '--processes',
                        type=int, default=1)
    parser.add_argument('-t', '--threaded',
                        type=bool, default=True)
    args = parser.parse_args()

    app.run(host=args.host,
            port=args.port,
            threaded=args.threaded,
            processes=args.processes,
            request_handler=GopherRequestHandler)


if __name__ == '__main__':
    main()
