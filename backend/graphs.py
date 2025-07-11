import plotly .graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import timedelta
from dateutil.parser import parse


def plot_total_energy_consumption(df):
    """
    1. График энергопотребления всех приборов
    :param df: DataFrame с данными
    :return: JSON-представление графика
    """
    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    date_list = [str(d) for d in df_clean['date'].tolist()]
    total_energy_list = (df_clean['Appliances'] + df_clean['lights']).tolist()
    last_n = min(len(date_list), 145)

    last_date = parse(date_list[-1])
    new_end_date = last_date + timedelta(hours=2)
    new_end_date_str = new_end_date.strftime('%Y-%m-%d %H:%M:%S')

    fig = go.Figure()

    fig.update_xaxes(range=[date_list[-last_n], new_end_date_str],
                     autorange=False,
                     type='date')
    fig.update_yaxes(range=[min(total_energy_list[-last_n:]) - 100,
                            max(total_energy_list[-last_n:]) + 100],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     autorange=False)
    fig.add_trace(go.Scatter(x=date_list, y=total_energy_list, mode='lines+markers', name=''))
    fig.update_layout(title=dict(text='Энергопотребление приборов',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      xaxis_title='Дата',
                      yaxis_title='Энергопотребление',
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def plot_appliances_and_lights_energy_consumption(df):
    """
    2. График энергопотребления бытовых приборов и света (раздельно)
    :param df: DataFrame с данными
    :return: JSON-представление графика
    """
    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    date_list = [str(d) for d in df_clean['date'].tolist()]
    appliances_list = df_clean['Appliances'].tolist()
    lights_list = df_clean['lights'].tolist()
    last_n = min(len(date_list), 75)

    last_date = parse(date_list[-1])
    new_end_date = last_date + timedelta(hours=1)
    new_end_date_str = new_end_date.strftime('%Y-%m-%d %H:%M:%S')

    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Энергопотребление бытовых приборов", "Энергопотребление света"))
    fig.update_xaxes(title='Дата', range=[date_list[-last_n], new_end_date_str])
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(appliances_list[-last_n:]) - 50,
                            max(appliances_list[-last_n:]) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(lights_list[-last_n:]) - 20,
                            max(lights_list[-last_n:]) + 20],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     col=2)
    fig.add_trace(go.Scatter(x=date_list, y=appliances_list, mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=date_list, y=lights_list, mode='lines+markers', name=''), 1, 2)
    fig.update_layout(title=dict(text='Энергопотребление приборов (раздельно)',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def plot_hourly_energy_consumption(df):
    """
    3. График почасового энергопотребления
    :param df: DataFrame с данными
    :return: JSON-представление графика
    """
    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    hourly_sum = df_clean.resample('h', on='date')['total_energy'].sum().reset_index()
    hourly_appliances = df_clean.resample('h', on='date')['Appliances'].sum().reset_index()
    hourly_lights = df_clean.resample('h', on='date')['lights'].sum().reset_index()

    date_list = [str(d) for d in hourly_sum['date'].tolist()]

    hourly_sum_list = hourly_sum['total_energy'].tolist()
    hourly_appliances_list = hourly_appliances['Appliances'].tolist()
    hourly_lights_list = hourly_lights['lights'].tolist()
    last_n_sum = min(len(date_list), 75)
    last_n_other = min(len(date_list), 50)

    last_date = parse(date_list[-1])
    new_end_date = last_date + timedelta(hours=4)
    new_end_date_str = new_end_date.strftime('%Y-%m-%d %H:%M:%S')

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Дата',
                     range=[date_list[-last_n_sum],
                            new_end_date_str],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Дата',
                     range=[date_list[-last_n_other],
                            new_end_date_str],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Дата',
                     range=[date_list[-last_n_other],
                            new_end_date_str],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(hourly_sum_list[-last_n_sum:]) - 300,
                            max(hourly_sum_list[-last_n_sum:]) + 300],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(hourly_appliances_list[-last_n_other:]) - 300,
                            max(hourly_appliances_list[-last_n_other:]) + 300],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(hourly_lights_list[-last_n_other:]) - 30,
                            max(hourly_lights_list[-last_n_other:]) + 30],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=date_list,
                             y=hourly_sum_list,
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=date_list,
                             y=hourly_appliances_list,
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=date_list,
                             y=hourly_lights_list,
                             mode='lines+markers', name=''), 2, 2)
    fig.update_layout(title=dict(text='Почасовое энергопотребление приборов',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def plot_daily_energy_consumption(df):
    """
    4. График дневного энергопотребления
    :param df: DataFrame с данными
    :return: JSON-представление графика
    """
    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    daily_sum = df_clean.resample('d', on='date')['total_energy'].sum().reset_index()
    daily_appliances = df_clean.resample('d', on='date')['Appliances'].sum().reset_index()
    daily_lights = df_clean.resample('d', on='date')['lights'].sum().reset_index()

    date_list = [str(d) for d in daily_sum['date'].tolist()]

    daily_sum_list = daily_sum['total_energy'].tolist()
    daily_appliances_list = daily_appliances['Appliances'].tolist()
    daily_lights_list = daily_lights['lights'].tolist()
    last_n_sum = min(len(date_list), 75)
    last_n_other = min(len(date_list), 50)

    last_date = parse(date_list[-1])
    new_end_date = last_date + timedelta(days=4)
    new_end_date_str = new_end_date.strftime('%Y-%m-%d %H:%M:%S')

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Дата',
                     range=[date_list[-last_n_sum],
                            new_end_date_str],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Дата',
                     range=[date_list[-last_n_other],
                            new_end_date_str],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Дата',
                     range=[date_list[-last_n_other],
                            new_end_date_str],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(daily_sum_list[-last_n_sum:]) - 5000,
                            max(daily_sum_list[-last_n_sum:]) + 5000],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(daily_appliances_list[-last_n_other:]) - 5000,
                            max(daily_appliances_list[-last_n_other:]) + 5000],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(daily_lights_list[-last_n_other:]) - 300,
                            max(daily_lights_list[-last_n_other:]) + 300],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=date_list,
                             y=daily_sum_list,
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=date_list,
                             y=daily_appliances_list,
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=date_list,
                             y=daily_lights_list,
                             mode='lines+markers', name=''), 2, 2)
    fig.update_layout(title=dict(text='Почасовое энергопотребление приборов',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def plot_temperature_energy_consumption(df, temperature_count):
    """
    5. График зависимости энергопотребления от средней температуры в доме
    :param df: DataFrame с данными
    :param temperature_count: кол-во датчиков температуры в доме
    :return: JSON-представление графика
    """
    temperature_columns = [f'T{i}' for i in range(1, temperature_count + 1)]

    all_columns = temperature_columns + ['Appliances', 'lights']
    df_clean = df.dropna(subset=all_columns).copy()

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['avg_temp'] = df_clean[temperature_columns].mean(axis=1).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    last_n_sum = min(len(df_clean), 100)
    last_n_other = min(len(df_clean), 75)

    grouped = df_clean.groupby('avg_temp')

    mean_total = grouped['total_energy'].mean().round(0)
    mean_appliances = grouped['Appliances'].mean().round(0)
    mean_lights = grouped['lights'].mean().round(0)

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Температура',
                     range=[mean_total.index[-last_n_sum], mean_total.index[-1] + 1],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Температура',
                     range=[mean_appliances.index[-last_n_other], mean_total.index[-1] + 1],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Температура',
                     range=[mean_lights.index[-last_n_other], mean_total.index[-1] + 1],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_total.tail(last_n_sum).values) - 50,
                            max(mean_total.tail(last_n_sum).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_appliances.tail(last_n_other).values) - 50,
                            max(mean_appliances.tail(last_n_other).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_lights.tail(last_n_other).values) - 10,
                            max(mean_lights.tail(last_n_other).values) + 10],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=mean_total.index.tolist(),
                             y=mean_total.values.tolist(),
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=mean_appliances.index.tolist(),
                             y=mean_appliances.values.tolist(),
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=mean_lights.index.tolist(),
                             y=mean_lights.values.tolist(),
                             mode='lines+markers', name=''), 2, 2)
    fig.update_layout(title=dict(text='Зависимость энергопотребления от температуры',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Температура: %{x}<br>"
                                                     "Потребление: %{y}")
    return fig.to_plotly_json()


def plot_humidity_energy_consumption(df, humidity_count):
    """
    6. График зависимости энергопотребления от средней влажности в доме
    :param df: DataFrame с данными
    :param humidity_count: кол-во датчиков влажности в доме
    :return: JSON-представление графика
    """
    humidity_columns = [f'RH_{i}' for i in range(1, humidity_count + 1)]

    all_columns = humidity_columns + ['Appliances', 'lights']
    df_clean = df.dropna(subset=all_columns).copy()

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['avg_humidity'] = df_clean[humidity_columns].mean(axis=1).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('avg_humidity')

    mean_total = grouped['total_energy'].mean().round(0)
    mean_appliances = grouped['Appliances'].mean().round(0)
    mean_lights = grouped['lights'].mean().round(0)

    last_n_sum = min(len(df_clean), 100)
    last_n_other = min(len(df_clean), 75)

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Влажность',
                     range=[mean_total.index[-last_n_sum], mean_total.index[-1] + 1],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Влажность',
                     range=[mean_appliances.index[-last_n_other], mean_total.index[-1] + 1],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Влажность',
                     range=[mean_lights.index[-last_n_other], mean_total.index[-1] + 1],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_total.tail(last_n_sum).values) - 50,
                            max(mean_total.tail(last_n_sum).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_appliances.tail(last_n_other).values) - 50,
                            max(mean_appliances.tail(last_n_other).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_lights.tail(last_n_other).values) - 10,
                            max(mean_lights.tail(last_n_other).values) + 10],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=mean_total.index.tolist(),
                             y=mean_total.values.tolist(),
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=mean_appliances.index.tolist(),
                             y=mean_appliances.values.tolist(),
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=mean_lights.index.tolist(),
                             y=mean_lights.values.tolist(),
                             mode='lines+markers', name=''), 2, 2)
    fig.update_layout(title=dict(text='Зависимость энергопотребления от влажности',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Влажность: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def plot_temperature_diff_energy_consumption(df, temperature_count):
    """
    7. График зависимости энергопотребления от разности температуры снаружи и внутри дома
    :param df: DataFrame с данными
    :param temperature_count: кол-во датчиков температуры в доме
    :return: JSON-представление графика
    """
    temperature_columns = [f'T{i}' for i in range(1, temperature_count + 1)]

    all_columns = temperature_columns + ['Appliances', 'lights', 'T_out']
    df_clean = df.dropna(subset=all_columns).copy()

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['temperature_diff'] = (df_clean['T_out'] - df_clean[temperature_columns].mean(axis=1)).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('temperature_diff')

    mean_total = grouped['total_energy'].mean().round(0)
    mean_appliances = grouped['Appliances'].mean().round(0)
    mean_lights = grouped['lights'].mean().round(0)

    last_n_sum = min(len(df_clean), 100)
    last_n_other = min(len(df_clean), 75)

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Разность температур',
                     range=[mean_total.index[-last_n_sum], mean_total.index[-1] + 1],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Разность температур',
                     range=[mean_appliances.index[-last_n_other], mean_total.index[-1] + 1],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Разность температур',
                     range=[mean_lights.index[-last_n_other], mean_total.index[-1] + 1],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_total.tail(last_n_sum).values) - 50,
                            max(mean_total.tail(last_n_sum).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_appliances.tail(last_n_other).values) - 50,
                            max(mean_appliances.tail(last_n_other).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_lights.tail(last_n_other).values) - 10,
                            max(mean_lights.tail(last_n_other).values) + 10],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=mean_total.index.tolist(),
                             y=mean_total.values.tolist(),
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=mean_appliances.index.tolist(),
                             y=mean_appliances.values.tolist(),
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=mean_lights.index.tolist(),
                             y=mean_lights.values.tolist(),
                             mode='lines+markers', name=''), 2, 2)
    fig.update_layout(title=dict(text='Зависимость энергопотребления от разности температуры снаружи и внутри дома',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Разность температур: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def plot_humidity_diff_energy_consumption(df, humidity_count):
    """
    8. График зависимости энергопотребления от разности влажности снаружи и внутри дома
    :param df: DataFrame с данными
    :param humidity_count: кол-во датчиков влажности в доме
    :return: JSON-представление графика
    """
    humidity_columns = [f'RH_{i}' for i in range(1, humidity_count + 1)]

    all_columns = humidity_columns + ['Appliances', 'lights', 'RH_out']
    df_clean = df.dropna(subset=all_columns).copy()

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['humidity_diff'] = (df_clean['RH_out'] - df_clean[humidity_columns].mean(axis=1)).round(1)
    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']

    grouped = df_clean.groupby('humidity_diff')

    mean_total = grouped['total_energy'].mean().round(0)
    mean_appliances = grouped['Appliances'].mean().round(0)
    mean_lights = grouped['lights'].mean().round(0)

    last_n_sum = min(len(df_clean), 100)
    last_n_other = min(len(df_clean), 75)

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Разность влажности',
                     range=[mean_total.index[-last_n_sum], mean_total.index[-1] + 1],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Разность влажности',
                     range=[mean_appliances.index[-last_n_other], mean_total.index[-1] + 1],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Разность влажности',
                     range=[mean_lights.index[-last_n_other], mean_total.index[-1] + 1],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_total.tail(last_n_sum).values) - 50,
                            max(mean_total.tail(last_n_sum).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_appliances.tail(last_n_other).values) - 50,
                            max(mean_appliances.tail(last_n_other).values) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(mean_lights.tail(last_n_other).values) - 10,
                            max(mean_lights.tail(last_n_other).values) + 10],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=mean_total.index.tolist(),
                             y=mean_total.values.tolist(),
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=mean_appliances.index.tolist(),
                             y=mean_appliances.values.tolist(),
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=mean_lights.index.tolist(),
                             y=mean_lights.values.tolist(),
                             mode='lines+markers', name=''), 2, 2)
    fig.update_layout(title=dict(text='Зависимость энергопотребления от разности влажности снаружи и внутри дома',
                                 x=0.5,
                                 xanchor='center',
                                 yanchor='top',
                                 font=dict(size=20)),
                      legend_orientation="h",
                      legend=dict(x=0.5, xanchor='center'),
                      margin=dict(l=0, r=0, t=105, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Разность влажности: %{x}<br>"
                                                     "Потребление: %{y}")

    return fig.to_plotly_json()


def histogram_average_hourly_consumption(df):
    """
    9. Гистограмма среднего энергопотребления по часам дня
    :param df: DataFrame с данными
    :return: JSON-представление графика
    """
    df_clean = df.dropna(subset=['date', 'Appliances', 'lights']).copy()
    df_clean['date'] = pd.to_datetime(df_clean['date'])

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']
    df_clean['hour'] = df_clean['date'].dt.hour

    avg_energy = df_clean.groupby('hour')[['total_energy', 'Appliances', 'lights']].mean().reset_index().round(2)

    hours_list = avg_energy['hour'].tolist()
    mean_total_list = avg_energy['total_energy'].tolist()
    mean_appliances_list = avg_energy['Appliances'].tolist()
    mean_lights_list = avg_energy['lights'].tolist()


    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=hours_list,
        y=mean_total_list,
        name='Общее потребление',
        marker_color='#1f77b4'
    ))

    fig.add_trace(go.Bar(
        x=hours_list,
        y=mean_appliances_list,
        name='Бытовая техника',
        marker_color='#ff7f0e'
    ))

    fig.add_trace(go.Bar(
        x=hours_list,
        y=mean_lights_list,
        name='Освещение',
        marker_color='#2ca02c'
    ))

    fig.update_xaxes(
        title_text='Час дня',
        tickvals=list(range(24)),
        range=[-0.5, 23.5]
    )

    fig.update_yaxes(
        title_text='Энергопотребление',
        rangemode='tozero'
    )

    fig.update_layout(
        title=dict(text='Среднее энергопотребление по часам дня',
                   x=0.5,
                   xanchor='center',
                   yanchor='top',
                   font=dict(size=20)),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=0.5, xanchor='center'),
        margin=dict(l=0, r=0, t=65, b=0)
    )

    return fig.to_plotly_json()


def histogram_average_weekly_consumption(df):
    """
    10. Гистограмма среднего энергопотребления по дням недели
    :param df: DataFrame с данными
    :return: JSON-представление графика
    """
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

    if len(df_clean) == 0:
        raise ValueError("Нет данных для построения графика после удаления NaN.")

    df_clean['total_energy'] = df_clean['Appliances'] + df_clean['lights']
    df_clean['day_of_week'] = df_clean['date'].dt.day_name()
    df_clean['day_num'] = df_clean['date'].dt.dayofweek

    weekly_avg = df_clean.groupby(['day_num', 'day_of_week'], as_index=False)[
        ['total_energy', 'Appliances', 'lights']].mean().round(2)

    weekly_avg = weekly_avg.sort_values('day_num')
    weekly_avg['day_of_week_ru'] = weekly_avg['day_of_week'].map(days_ru)

    days_list = weekly_avg['day_of_week_ru'].tolist()
    mean_total_list = weekly_avg['total_energy'].tolist()
    mean_appliances_list = weekly_avg['Appliances'].tolist()
    mean_lights_list = weekly_avg['lights'].tolist()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=days_list,
        y=mean_total_list,
        name='Общее потребление',
        marker_color='#1f77b4'
    ))

    fig.add_trace(go.Bar(
        x=days_list,
        y=mean_appliances_list,
        name='Бытовая техника',
        marker_color='#ff7f0e'
    ))

    fig.add_trace(go.Bar(
        x=days_list,
        y=mean_lights_list,
        name='Освещение',
        marker_color='#2ca02c'
    ))

    fig.update_xaxes(
        title_text='День недели',
        categoryorder='array',
        categoryarray=days_list
    )

    fig.update_yaxes(
        title_text='Энергопотребление',
        rangemode='tozero'
    )

    fig.update_layout(
        title=dict(text='Среднее энергопотребление по дням недели',
                   x=0.5,
                   xanchor='center',
                   yanchor='top',
                   font=dict(size=20)),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1,
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=0.5, xanchor='center'),
        margin=dict(l=0, r=0, t=65, b=0)
    )

    return fig.to_plotly_json()


def plot_weekday_hourly_consumption(df):
    pass