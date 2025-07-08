import os

from Scripts.bottle import redirect
from flask import Flask, render_template, jsonify, flash, request, url_for
from werkzeug.utils import secure_filename

# from .data_handler import load_data, build_graph
from .data_handler import validate_data, clear_data, load_data
import plotly .graph_objs as go
import plotly
import json

df = None

UPLOAD_FOLDER = 'backend/datasets'

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
app.secret_key = 'debi'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/load-file', methods=['POST'])
def load_file():
    if 'file' not in request.files:
        flash('File not found')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
       flash('No selected file')
       return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        global df
        df = load_data(filepath)

        print(validate_data(df))
        if validate_data(df):
            return render_template('graphs.html')

        return f'Error: {file.filename}'
        # filename  = os.path.join(UPLOAD_FOLDER, file.filename)
        # file.save(filepath)
        # df = load_data(filepath)
        # valid = validate_data(df)

    return render_template('index.html')


'''
GRAPH PART
'''

from . import graphs

@app.route('/graph_1', methods=['POST'])
def graph_1():
    json_graph = graphs.plot_total_energy_consumption(df)
    return jsonify(json_graph)


@app.route('/graph_2', methods=['POST'])
def graph_2():
    json_graph = graphs.plot_appliances_and_lights_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


@app.route('/graph_3', methods=['POST'])
def graph_3():
    json_graph = graphs.plot_hourly_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


@app.route('/graph_4', methods=['POST'])
def graph_4():
    json_graph = graphs.plot_daily_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


@app.route('/graph_5', methods=['POST'])
def graph_5():
    json_graph = graphs.plot_temperature_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


@app.route('/graph_6', methods=['POST'])
def graph_6():
    json_graph = graphs.plot_humidity_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


@app.route('/graph_7', methods=['POST'])
def graph_7():
    json_graph = graphs.plot_temperature_diff_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


@app.route('/graph_8', methods=['POST'])
def graph_8():
    json_graph = graphs.plot_humidity_diff_energy_consumption(df)
    print(json_graph)
    return jsonify(json_graph)


# @app.route('/graph_9', methods=['POST'])
# def graph_9():
#     json_graph = graphs.plot_humidity_diff_energy_consumption(df)
#     print(json_graph)
#     return jsonify(json_graph)