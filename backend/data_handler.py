import pandas as pd



def load_data():
    try:
        df = pd.read_csv('datasets/energydata_complete.csv')
    except:
        pass


def validate_data(df):
    pass


def clear_data(df):
    pass