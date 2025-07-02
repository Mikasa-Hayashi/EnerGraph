import pandas as pd



def get_data_info(df: pd.DataFrame):
    print(df.head())
    print('-' * 100)
    print(df.tail())
    print('-' * 100)
    print(df.dtypes)
    print('-' * 100)
    print(df.columns)
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
    df = pd.read_csv('datasets/energydata_complete.csv')
    get_data_info(df)


if __name__ == '__main__':
    main()