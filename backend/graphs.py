import plotly .graph_objs as go
from plotly.subplots import make_subplots
import plotly
import pandas as pd



def power_consumation_over_time():
    pass


def energy_dependence_from_temperature():
    pass


def energy_dependence_from_humidity():
    pass


def graph_4():
    pass


def graph_5():
    pass


def graph_6():
    pass


def graph_7():
    pass


def graph_8():
    pass


def graph_9():
    pass


def plot_total_energy_consumption(df):
    fig = go.Figure()
    fig.update_xaxes(range=[df['date'].iloc[-145], df['date'].iloc[-1] + pd.Timedelta(hours=2)])
    fig.update_yaxes(range=[min(df['Appliances'].tail(145) + df['lights'].tail(145)) - 100,
                            max(df['Appliances'].tail(145) + df['lights'].tail(145)) + 100],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537')
    fig.add_trace(go.Scatter(x=df['date'], y=(df['Appliances'] + df['lights']), mode='lines+markers', name=''))
    fig.update_layout(title='Энергопотребление приборов',
                      xaxis_title='Дата',
                      yaxis_title='Энергопотребление',
                      margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>"
                                                     "Потребление: %{y}")


def plot_appliances_and_lights_energy_consumption(df):
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Энергопотребление бытовых приборов", "Энергопотребление света"))
    fig.update_xaxes(title='Дата', range=[df['date'].iloc[-75], df['date'].iloc[-1] + pd.Timedelta(hours=1)])
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(df['Appliances'].tail(75)) - 50,
                            max(df['Appliances'].tail(75)) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(df['lights'].tail(75)) - 50,
                            max(df['lights'].tail(75)) + 50],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     col=2)
    fig.add_trace(go.Scatter(x=df['date'], y=df['Appliances'], mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=df['date'], y=df['lights'], mode='lines+markers', name=''), 1, 2)
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


def plot_hourly_energy_consumption(df):
    df['total_energy'] = df['Appliances'] + df['lights']

    hourly_sum = df.resample('h', on='date')['total_energy'].sum().reset_index()
    hourly_appliances = df.resample('h', on='date')['Appliances'].sum().reset_index()
    hourly_lights = df.resample('h', on='date')['lights'].sum().reset_index()

    fig = make_subplots(rows=2, cols=2,
                        specs=[[{"rowspan": 2}, {}], [None, {}]],
                        subplot_titles=("Общее энергопотребление", "Энергопотребление бытовых приборов",
                                        "Энергопотребление света"))

    fig.update_xaxes(title='Дата',
                     range=[hourly_sum['date'].iloc[-75],
                            hourly_sum['date'].iloc[-1] + pd.Timedelta(hours=4)],
                     row=1,
                     col=1)
    fig.update_xaxes(title='Дата',
                     range=[hourly_appliances['date'].iloc[-50],
                            hourly_appliances['date'].iloc[-1] + pd.Timedelta(hours=4)],
                     row=1,
                     col=2)
    fig.update_xaxes(title='Дата',
                     range=[hourly_lights['date'].iloc[-50],
                            hourly_lights['date'].iloc[-1] + pd.Timedelta(hours=4)],
                     row=2,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(hourly_sum['total_energy'].tail(75)) - 300,
                            max(hourly_sum['total_energy'].tail(75)) + 300],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=1)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(hourly_appliances['Appliances'].tail(50)) - 300,
                            max(hourly_appliances['Appliances'].tail(50)) + 300],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=1,
                     col=2)
    fig.update_yaxes(title='Энергопотребление',
                     range=[min(hourly_lights['lights'].tail(50)) - 30,
                            max(hourly_lights['lights'].tail(50)) + 30],
                     zeroline=True,
                     zerolinewidth=2,
                     zerolinecolor='#902537',
                     row=2,
                     col=2)
    fig.add_trace(go.Scatter(x=hourly_sum['date'],
                             y=hourly_sum['total_energy'],
                             mode='lines+markers', name=''), 1, 1)
    fig.add_trace(go.Scatter(x=hourly_appliances['date'],
                             y=hourly_appliances['Appliances'],
                             mode='lines+markers', name=''), 1, 2)
    fig.add_trace(go.Scatter(x=hourly_lights['date'],
                             y=hourly_lights['lights'],
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