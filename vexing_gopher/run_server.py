#!/usr/bin/env python3

'''
'''

import sqlite3
import argparse
from flask import Flask, request
from flask_gopher import GopherExtension, GopherRequestHandler


app = Flask(__name__)
gopher = GopherExtension(app)


@app.route('/')
def index():
    with sqlite3.connect('vexing.db') as conn:
        cur = conn.cursor()

        cur.execute('''
        INSERT INTO hits (remote_ip) VALUES (?);
        ''', (request.environ['REMOTE_ADDR'],))

        cur.execute('''
        SELECT COUNT(remote_ip) FROM hits;
        ''')
        (count,) = cur.fetchone()

    return gopher.render_menu_template('index.gopher', count=count)


@app.route('/about')
def about():
    return gopher.render_menu_template('about.gopher')


@app.route('/guestbook')
def guestbook():
    message = request.environ.get('SEARCH_TEXT', None)
    remote_ip = request.environ.get('REMOTE_ADDR', None)

    with sqlite3.connect('vexing.db') as conn:
        cur = conn.cursor()

        if message != '':
            cur.execute('''
            INSERT INTO guestbook (message, remote_ip)
            VALUES (?, ?);
            ''', (message[:250], remote_ip))

        cur.execute('''
        SELECT message, remote_ip, submitted
        FROM guestbook
        ORDER BY submitted DESC;
        ''')

        messages = cur.fetchall()

    form_url = gopher.url_for('guestbook')
    return gopher.render_menu_template('guestbook.gopher',
                                       url=form_url,
                                       messages=messages)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host',
                        default='0.0.0.0')
    parser.add_argument('-p', '--port',
                        default=70)
    parser.add_argument('-P', '--processes',
                        type=int, default=1)
    parser.add_argument('-t', '--threaded',
                        type=bool, default=True)
    args = parser.parse_args()

    with sqlite3.connect('vexing.db') as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS hits
        (id INTEGER PRIMARY KEY ASC,
         remote_ip TEXT,
         accessed TEXT DEFAULT CURRENT_TIMESTAMP);

        CREATE TABLE IF NOT EXISTS guestbook
        (id INTEGER PRIMARY KEY ASC,
         remote_ip TEXT,
         message TEXT,
         submitted TEXT DEFAULT CURRENT_TIMESTAMP);
        ''')

    app.run(host=args.host,
            port=args.port,
            threaded=args.threaded,
            processes=args.processes,
            request_handler=GopherRequestHandler)


if __name__ == '__main__':
    main()
