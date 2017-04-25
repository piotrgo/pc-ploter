#!bin/python
from flask import Flask, jsonify, request, abort, make_response
import pygsheets
import datetime

app = Flask(__name__)

# http://8values.github.io/results.html?e=54.5&d=69.9&g=74.3&s=75.0'


@app.route('/pc-ploter/api/v1.0/upload', methods=['POST'])
def upload():
    if len(request.full_path) != 54:
        abort(400)
    if not 'name' in request.headers:
        abort(400)
    gc = pygsheets.authorize(service_file='service_creds.json')
    sh = gc.open("ss-python")
    wks = sh.sheet1
    last_id = wks.get_value('A1')
    timestamp = datetime.datetime.now()
    wks.update_row(int(last_id), [str(timestamp), request.headers['name'], request.args['e'],
                                  request.args['d'], request.args['g'], request.args['s']])
    wks.update_cell('A1', int(last_id)+1)
    return jsonify({'record_id': last_id}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)