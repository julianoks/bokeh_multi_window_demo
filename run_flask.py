from flask import Flask, jsonify, request
from bokeh.models import AjaxDataSource
from bokeh.util.string import encode_utf8
from app.main import get_data, get_html

app = Flask(__name__)

from flask_cors import CORS, cross_origin
CORS(app)

time_slice = 0

@app.route('/edit_source_data', methods=['POST'])
def update_time_slice():
	json = request.get_json()
	if (json is None) or ('time_slice' not in json): return "false"
	global time_slice
	time_slice = int(json['time_slice'])
	return "true"

@app.route('/source_data', methods=['POST'])
def get_source_1():
	return jsonify(get_data(time_slice))

@app.route('/', methods=['GET'])
def index():
	streaming=True
	source = AjaxDataSource(data_url="http://localhost:5000/source_data", polling_interval=100)
	source.data = get_data(time_slice)
	payload = encode_utf8(get_html(source))
	return payload

if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5000)
