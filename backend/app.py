import os
from flask import Flask, render_template, jsonify


app = Flask(__name__, template_folder='../frontend')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello', methods=['POST'])
def say_hello():
    print('Hello, World!')
    return jsonify({'message': 'DONE!'})