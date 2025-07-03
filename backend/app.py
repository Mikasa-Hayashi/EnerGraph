import os
from flask import Flask, render_template, jsonify
# from .data_handler import load_data, build_graph
import plotly .graph_objs as go
import plotly
import json

app = Flask(__name__, template_folder='../frontend')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_graph', methods=['POST'])
def get_graph():
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