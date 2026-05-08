import json
import os

import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.')


def db_connect():
    url = os.environ.get('DATABASE_URL', '')
    if url.startswith('postgres://'):
        url = 'postgresql://' + url[len('postgres://'):]
    return psycopg2.connect(url, connect_timeout=10)


def init_db():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS timers (
            name TEXT PRIMARY KEY,
            data JSONB NOT NULL
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


@app.route('/api/timers', methods=['GET'])
def list_timers():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('SELECT name FROM timers ORDER BY name')
    names = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(names)


@app.route('/api/timers/<name>', methods=['GET'])
def get_timer(name):
    conn = db_connect()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT data FROM timers WHERE name = %s', (name,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(row['data'])


@app.route('/api/timers/<name>', methods=['PUT'])
def save_timer(name):
    data = request.get_json()
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO timers (name, data) VALUES (%s, %s) '
        'ON CONFLICT (name) DO UPDATE SET data = EXCLUDED.data',
        (name, json.dumps(data))
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})


@app.route('/api/timers/<name>', methods=['DELETE'])
def delete_timer(name):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM timers WHERE name = %s', (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})


try:
    init_db()
except Exception as e:
    print(f'Warning: could not initialise database — {e}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
