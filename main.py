import pandas as pd
from backend import app

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

    app.run(debug=True)


if __name__ == '__main__':
    main()