import pandas as pd
from backend import app, load_data, clear_data


def get_data_info(df: pd.DataFrame):
    print(df.head()) #  first 5 rows
    print('-' * 100)
    print(df.tail()) # last 5 rows
    print('-' * 100)
    print(df.dtypes) # data types
    print('-' * 100)
    print(df.columns) #
    print('-' * 100)
    print(df.shape)
    print('-' * 100)
    print(df.size)
    print('-' * 100)
    print(df.info())
    print('-' * 100)
    print(df.describe())
    print('-' * 100)
    print(df.isnull().sum())


def main():
    # df = pd.read_csv('datasets/energydata_complete.csv')
    # get_data_info(df)
    data = load_data()
    clear_data(data)
    app.run(debug=True)


if __name__ == '__main__':
    main()