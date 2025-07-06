import plotly .graph_objs as go
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
                            max(df['Appliances'].tail(145) + df['lights'].tail(145)) + 100])
    fig.add_trace(go.Scatter(x=df['date'], y=(df['Appliances'] + df['lights']), mode='lines+markers', name=''))
    fig.update_layout(title='Энергопотребление приборов',
                      xaxis_title='Дата',
                      yaxis_title='Энергопотребление',
                      margin=dict(l=0, r=0, t=30, b=0))
    fig.update_traces(hoverinfo="all", hovertemplate="Дата: %{x}<br>Потребление: %{y}")