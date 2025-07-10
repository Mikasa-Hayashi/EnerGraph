import os
import pandas as pd

from Scripts.bottle import redirect
from flask import Flask, render_template, jsonify, flash, request, url_for
from werkzeug.utils import secure_filename

# from .data_handler import load_data, build_graph
from .data_handler import validate_data, load_data
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
    plot_json = graphs.plot_total_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_2', methods=['POST'])
def graph_2():
    plot_json = graphs.plot_appliances_and_lights_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_3', methods=['POST'])
def graph_3():
    plot_json = graphs.plot_hourly_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_4', methods=['POST'])
def graph_4():
    plot_json = graphs.plot_daily_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_5', methods=['POST'])
def graph_5():
    plot_json = graphs.plot_temperature_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_6', methods=['POST'])
def graph_6():
    plot_json = graphs.plot_humidity_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_7', methods=['POST'])
def graph_7():
    plot_json = graphs.plot_temperature_diff_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_8', methods=['POST'])
def graph_8():
    plot_json = graphs.plot_humidity_diff_energy_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_9', methods=['POST'])
def graph_9():
    plot_json = graphs.histogram_average_hourly_consumption(df)
    return jsonify(plot_json)


@app.route('/graph_10', methods=['POST'])
def graph_10():
    plot_json = graphs.histogram_average_weekly_consumption(df)
    return jsonify(plot_json)


'''
ANAL PART
'''

@app.route('/anal_1', methods=['POST'])
def anal_1():
    data = {}

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    max_val = df_clean['total_energy'].max()
    min_val = df_clean['total_energy'].min()
    mean_val = df_clean['total_energy'].mean()

    max_time = df_clean.loc[df_clean['total_energy'].idxmax(), 'date']
    min_time = df_clean.loc[df_clean['total_energy'].idxmin(), 'date']

    out = (
        f"Максимальное значение энергопотребления достигается {max_time.strftime('%d.%m.%Y %H:%M')} "
        f"и равно: {max_val:.2f} кВт\n"
        f"Минимальное значение энергопотребления достигается {min_time.strftime('%d.%m.%Y %H:%M')} "
        f"и равно: {min_val:.2f} кВт\n"
        f"Среднее значение энергопотребления за весь период: {mean_val:.2f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_2', methods=['POST'])
def anal_2():
    data = {}

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if df_clean.empty:
        data['anal'] = "Нет данных для анализа после удаления NaN."
        return data

    df_tail = df_clean.tail(75)

    max_app = df_tail['Appliances'].max()
    min_app = df_tail['Appliances'].min()
    mean_app = df_tail['Appliances'].mean()
    time_max_app = df_tail.loc[df_tail['Appliances'].idxmax(), 'date']
    time_min_app = df_tail.loc[df_tail['Appliances'].idxmin(), 'date']

    max_light = df_tail['lights'].max()
    min_light = df_tail['lights'].min()
    mean_light = df_tail['lights'].mean()
    time_max_light = df_tail.loc[df_tail['lights'].idxmax(), 'date']
    time_min_light = df_tail.loc[df_tail['lights'].idxmin(), 'date']

    out = (
        f"🔌 Бытовые приборы:\n"
        f"• Максимум: {max_app:.2f} кВт ({time_max_app.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Минимум: {min_app:.2f} кВт ({time_min_app.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Среднее: {mean_app:.2f} кВт\n\n"
        f"💡 Освещение:\n"
        f"• Максимум: {max_light:.2f} кВт ({time_max_light.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Минимум: {min_light:.2f} кВт ({time_min_light.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Среднее: {mean_light:.2f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_3', methods=['POST'])
def anal_3():
    data = {}

    # Clean and prepare data
    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if df_clean.empty:
        data['anal'] = "Нет данных для анализа после удаления NaN."
        return data

    # Total energy
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    # Resample to hourly
    hourly_sum = df_clean.resample('h', on='date')['total_energy'].sum().reset_index()
    hourly_appliances = df_clean.resample('h', on='date')['Appliances'].sum().reset_index()
    hourly_lights = df_clean.resample('h', on='date')['lights'].sum().reset_index()

    max_total = hourly_sum['total_energy'].max()
    min_total = hourly_sum['total_energy'].min()
    mean_total = hourly_sum['total_energy'].mean()
    time_max_total = hourly_sum.loc[hourly_sum['total_energy'].idxmax(), 'date']
    time_min_total = hourly_sum.loc[hourly_sum['total_energy'].idxmin(), 'date']

    max_app = hourly_appliances['Appliances'].max()
    min_app = hourly_appliances['Appliances'].min()
    mean_app = hourly_appliances['Appliances'].mean()
    time_max_app = hourly_appliances.loc[hourly_appliances['Appliances'].idxmax(), 'date']
    time_min_app = hourly_appliances.loc[hourly_appliances['Appliances'].idxmin(), 'date']

    max_light = hourly_lights['lights'].max()
    min_light = hourly_lights['lights'].min()
    mean_light = hourly_lights['lights'].mean()
    time_max_light = hourly_lights.loc[hourly_lights['lights'].idxmax(), 'date']
    time_min_light = hourly_lights.loc[hourly_lights['lights'].idxmin(), 'date']

    out = (
        f"📊 Почасовой анализ энергопотребления:\n\n"
        f"🔋 Общее энергопотребление:\n"
        f"• Максимум: {max_total:.2f} кВт ({time_max_total.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Минимум: {min_total:.2f} кВт ({time_min_total.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Среднее: {mean_total:.2f} кВт\n\n"
        f"🔌 Приборы:\n"
        f"• Максимум: {max_app:.2f} кВт ({time_max_app.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Минимум: {min_app:.2f} кВт ({time_min_app.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Среднее: {mean_app:.2f} кВт\n\n"
        f"💡 Освещение:\n"
        f"• Максимум: {max_light:.2f} кВт ({time_max_light.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Минимум: {min_light:.2f} кВт ({time_min_light.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Среднее: {mean_light:.2f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_4', methods=['POST'])
def anal_4():
    data = None
    return jsonify(data)


@app.route('/anal_5', methods=['POST'])
def anal_5():
    data = None
    return jsonify(data)


@app.route('/anal_6', methods=['POST'])
def anal_6():
    data = None
    return jsonify(data)


@app.route('/anal_7', methods=['POST'])
def anal_7():
    data = None
    return jsonify(data)


@app.route('/anal_8', methods=['POST'])
def anal_8():
    data = None
    return jsonify(data)


@app.route('/anal_9', methods=['POST'])
def anal_9():
    data = None
    return jsonify(data)


@app.route('/anal_10', methods=['POST'])
def anal_10():
    data = None
    return jsonify(data)
