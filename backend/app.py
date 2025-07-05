import os

from Scripts.bottle import redirect
from flask import Flask, render_template, jsonify, flash, request, url_for
from werkzeug.utils import secure_filename

# from .data_handler import load_data, build_graph
from .data_handler import validate_data, clear_data, load_data
import plotly .graph_objs as go
import plotly
import json


UPLOAD_FOLDER = 'backend/datasets'

app = Flask(__name__, template_folder='../frontend')
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

        df = load_data(filepath)

        print(validate_data(df))
        if validate_data(df):
            return f'Uploaded: {file.filename}'

        return f'Error: {file.filename}'
        # filename  = os.path.join(UPLOAD_FOLDER, file.filename)
        # file.save(filepath)
        # df = load_data(filepath)
        # valid = validate_data(df)

    return render_template('index.html')


@app.route('/graph_1', methods=['POST'])
def graph_1():
    # df = load_data()

    # df = load_data()
    # graph_html = build_graph(df)
    # trace = go.Scatter(x='Appliances', y='T1')
    # fig = go.Figure(data=[trace])
    # graphJSON = fig.to_plotly_json()
    # # return render_template('index.html', graph=graph_html)
    # return jsonify(graphJSON)
    x = [1, 2, 3, 4, 5]
    y = [10, 15, 13, 17, 14]
    # print(list(df['Appliances']))
    trace = go.Scatter(x=x, y=y, mode='lines+markers', name='Потребление')
    layout = go.Layout(title='График потребления электроэнергии')

    fig = go.Figure(data=[trace], layout=layout)

    graphJSON = fig.to_plotly_json()

    return jsonify(graphJSON)


@app.route('/graph_2', methods=['POST'])
def graph_2():
    pass


@app.route('/graph_3', methods=['POST'])
def graph_3():
    pass


@app.route('/graph_4', methods=['POST'])
def graph_4():
    pass


@app.route('/graph_5', methods=['POST'])
def graph_5():
    pass


@app.route('/graph_6', methods=['POST'])
def graph_6():
    pass


@app.route('/graph_7', methods=['POST'])
def graph_7():
    pass


@app.route('/graph_8', methods=['POST'])
def graph_8():
    pass


@app.route('/graph_9', methods=['POST'])
def graph_9():
    pass