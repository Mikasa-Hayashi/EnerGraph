import os
import pandas as pd

from Scripts.bottle import redirect
from flask import Flask, render_template, jsonify, flash, request
from werkzeug.utils import secure_filename
from .data_handler import validate_data, load_data



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

        if validate_data(df):
            return render_template('graphs.html')

        return render_template('load_error.html')

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
def analysisEnergyСonsumptionOfAllDevices():
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
        f"📈 Анализ энергопотребления всех приборов:\n\n"
        f"• Максимум: {max_val:.2f} кВт ({max_time.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Минимум: {min_val:.2f} кВт ({min_time.strftime('%d.%m.%Y %H:%M')})\n"
        f"• Среднее значение за период: {mean_val:.2f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_2', methods=['POST'])
def analysisEnergyConsumptionHouseholdAppliancesAndLight():
    data = {}

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

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
        f"🔦 Анализ энергопотребления бытовых приборов и света:\n\n"
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
def analysisEnergyConsumptionHourly():
    data = {}

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

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
def analysisEnergyConsumptionDaily():
    data = {}

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    daily_sum = df_clean.resample('d', on='date')['total_energy'].sum().reset_index()
    daily_appliances = df_clean.resample('d', on='date')['Appliances'].sum().reset_index()
    daily_lights = df_clean.resample('d', on='date')['lights'].sum().reset_index()

    max_total = daily_sum['total_energy'].max()
    min_total = daily_sum['total_energy'].min()
    mean_total = daily_sum['total_energy'].mean()
    time_max_total = daily_sum.loc[daily_sum['total_energy'].idxmax(), 'date']
    time_min_total = daily_sum.loc[daily_sum['total_energy'].idxmin(), 'date']

    max_app = daily_appliances['Appliances'].max()
    min_app = daily_appliances['Appliances'].min()
    mean_app = daily_appliances['Appliances'].mean()
    time_max_app = daily_appliances.loc[daily_appliances['Appliances'].idxmax(), 'date']
    time_min_app = daily_appliances.loc[daily_appliances['Appliances'].idxmin(), 'date']

    max_light = daily_lights['lights'].max()
    min_light = daily_lights['lights'].min()
    mean_light = daily_lights['lights'].mean()
    time_max_light = daily_lights.loc[daily_lights['lights'].idxmax(), 'date']
    time_min_light = daily_lights.loc[daily_lights['lights'].idxmin(), 'date']

    out = (
        f"📅 Дневной анализ энергопотребления:\n\n"
        f"🔋 Общее потребление:\n"
        f"• Максимум: {max_total:.2f} кВт ({time_max_total.strftime('%d.%m.%Y')})\n"
        f"• Минимум: {min_total:.2f} кВт ({time_min_total.strftime('%d.%m.%Y')})\n"
        f"• Среднее: {mean_total:.2f} кВт\n\n"
        f"🔌 Приборы:\n"
        f"• Максимум: {max_app:.2f} кВт ({time_max_app.strftime('%d.%m.%Y')})\n"
        f"• Минимум: {min_app:.2f} кВт ({time_min_app.strftime('%d.%m.%Y')})\n"
        f"• Среднее: {mean_app:.2f} кВт\n\n"
        f"💡 Освещение:\n"
        f"• Максимум: {max_light:.2f} кВт ({time_max_light.strftime('%d.%m.%Y')})\n"
        f"• Минимум: {min_light:.2f} кВт ({time_min_light.strftime('%d.%m.%Y')})\n"
        f"• Среднее: {mean_light:.2f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_5', methods=['POST'])
def analysisDependenceEnergyConsumptionAverageTemperatureHouse():
    data = {}
    temperature_count = 9 # число комнат

    temperature_columns = [f'T{i}' for i in range(1, temperature_count + 1)]
    all_columns = temperature_columns + ['Appliances', 'lights']
    df_clean = df.dropna(subset=all_columns).copy()

    df_clean['avg_temp'] = df_clean[temperature_columns].mean(axis=1).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('avg_temp')
    mean_total = grouped['total_energy'].mean().round(0)

    temp_max_energy = mean_total.idxmax()
    max_energy = mean_total.max()

    temp_min_energy = mean_total.idxmin()
    min_energy = mean_total.min()

    avg_energy = mean_total.mean()

    out = (
        f"🌡️ Зависимость энергопотребления от средней температуры в доме:\n\n"
        f"• 🔥 Максимальное среднее потребление: {max_energy:.0f} кВт при {temp_max_energy}°C\n"
        f"• ❄️ Минимальное среднее потребление: {min_energy:.0f} кВт при {temp_min_energy}°C\n"
        f"• 📊 Среднее по всем температурам: {avg_energy:.0f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_6', methods=['POST'])
def analysisDependenceEnergyConsumptionAverageHumidityHouse():
    data = {}
    humidity_count = 9 # число комнат

    humidity_columns = [f'RH_{i}' for i in range(1, humidity_count + 1)]
    all_columns = humidity_columns + ['Appliances', 'lights']
    df_clean = df.dropna(subset=all_columns).copy()

    df_clean['avg_humidity'] = df_clean[humidity_columns].mean(axis=1).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('avg_humidity')
    mean_total = grouped['total_energy'].mean().round(0)

    hum_max_energy = mean_total.idxmax()
    max_energy = mean_total.max()

    hum_min_energy = mean_total.idxmin()
    min_energy = mean_total.min()

    avg_energy = mean_total.mean()

    out = (
        f"💧 Зависимость энергопотребления от средней влажности в доме:\n\n"
        f"• 📈 Максимальное среднее потребление: {max_energy:.0f} кВт при {hum_max_energy}% влажности\n"
        f"• 📉 Минимальное среднее потребление: {min_energy:.0f} кВт при {hum_min_energy}% влажности\n"
        f"• 📊 Среднее по всем уровням влажности: {avg_energy:.0f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_7', methods=['POST'])
def analysisDependenceEnergyConsumptionTemperatureDifference():
    data = {}
    temperature_count = 9

    temperature_columns = [f'T{i}' for i in range(1, temperature_count + 1)]
    all_columns = temperature_columns + ['Appliances', 'lights', 'T_out']
    df_clean = df.dropna(subset=all_columns).copy()

    df_clean['temperature_diff'] = (df_clean['T_out'] - df_clean[temperature_columns].mean(axis=1)).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('temperature_diff')
    mean_total = grouped['total_energy'].mean().round(0)

    diff_max_energy = mean_total.idxmax()
    max_energy = mean_total.max()

    diff_min_energy = mean_total.idxmin()
    min_energy = mean_total.min()

    avg_energy = mean_total.mean()

    out = (
        f"🌡️ Зависимость энергопотребления от разности температур (улица - дом):\n\n"
        f"• 📈 Максимальное среднее потребление: {max_energy:.0f} кВт при разности {diff_max_energy}°C\n"
        f"• 📉 Минимальное среднее потребление: {min_energy:.0f} кВт при разности {diff_min_energy}°C\n"
        f"• 📊 Среднее по всем значениям разности температур: {avg_energy:.0f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_8', methods=['POST'])
def analysisDependenceEnergyConsumptionHumidityDifference():
    data = {}
    humidity_count = 9

    humidity_columns = [f'RH_{i}' for i in range(1, humidity_count + 1)]
    all_columns = humidity_columns + ['Appliances', 'lights', 'RH_out']
    df_clean = df.dropna(subset=all_columns).copy()

    df_clean['humidity_diff'] = (df_clean['RH_out'] - df_clean[humidity_columns].mean(axis=1)).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('humidity_diff')
    mean_total = grouped['total_energy'].mean().round(0)

    diff_max_energy = mean_total.idxmax()
    max_energy = mean_total.max()

    diff_min_energy = mean_total.idxmin()
    min_energy = mean_total.min()

    avg_energy = mean_total.mean()

    out = (
        f"💧 Зависимость энергопотребления от разности влажности (улица - дом):\n\n"
        f"• 📈 Максимальное среднее потребление: {max_energy:.0f} кВт при разности {diff_max_energy}%\n"
        f"• 📉 Минимальное среднее потребление: {min_energy:.0f} кВт при разности {diff_min_energy}%\n"
        f"• 📊 Среднее по всем значениям разности влажности: {avg_energy:.0f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_9', methods=['POST'])
def analysisAverageEnergyConsumptionHour():
    data = {}

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']
    df_clean['hour'] = df_clean['date'].dt.hour

    avg_energy = df_clean.groupby('hour')[['total_energy', 'Appliances', 'lights']].mean().reset_index().round(2)

    max_hour = avg_energy.loc[avg_energy['total_energy'].idxmax(), 'hour']
    max_val = avg_energy['total_energy'].max()

    min_hour = avg_energy.loc[avg_energy['total_energy'].idxmin(), 'hour']
    min_val = avg_energy['total_energy'].min()

    avg_val = avg_energy['total_energy'].mean()

    out = (
        f"🕒 Анализ среднего энергопотребления по часам:\n\n"
        f"• ⏰ Максимальное потребление в {max_hour}:00 — {max_val:.2f} кВт\n"
        f"• 💤 Минимальное потребление в {min_hour}:00 — {min_val:.2f} кВт\n"
        f"• 📊 Среднее потребление за сутки: {avg_val:.2f} кВт"
    )

    data['anal'] = out
    return data


@app.route('/anal_10', methods=['POST'])
def analysisAverageEnergyConsumptionDaysWeek():
    data = {}

    days_ru = {
        'Monday': 'Понедельник',
        'Tuesday': 'Вторник',
        'Wednesday': 'Среда',
        'Thursday': 'Четверг',
        'Friday': 'Пятница',
        'Saturday': 'Суббота',
        'Sunday': 'Воскресенье'
    }

    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']
    df_clean['day_of_week'] = df_clean['date'].dt.day_name()
    df_clean['day_num'] = df_clean['date'].dt.dayofweek

    weekly_avg = df_clean.groupby(['day_num', 'day_of_week'], as_index=False)[
        ['total_energy', 'Appliances', 'lights']].mean().round(2)

    weekly_avg = weekly_avg.sort_values('day_num')
    weekly_avg['day_of_week_ru'] = weekly_avg['day_of_week'].map(days_ru)

    max_day = weekly_avg.loc[weekly_avg['total_energy'].idxmax(), 'day_of_week_ru']
    max_val = weekly_avg['total_energy'].max()

    min_day = weekly_avg.loc[weekly_avg['total_energy'].idxmin(), 'day_of_week_ru']
    min_val = weekly_avg['total_energy'].min()

    avg_val = weekly_avg['total_energy'].mean()

    out = (
        f"📅 Анализ среднего энергопотребления по дням недели:\n\n"
        f"• 🔝 Максимальное потребление в {max_day} — {max_val:.2f} кВт\n"
        f"• 🔻 Минимальное потребление в {min_day} — {min_val:.2f} кВт\n"
        f"• 📊 Среднее потребление за неделю: {avg_val:.2f} кВт"
    )

    data['anal'] = out
    return data
