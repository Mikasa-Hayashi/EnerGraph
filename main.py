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


def validate_data(file_path):
    try:
        df = pd.read_csv(file_path)

        required_columns = ['date', 'Appliances', 'lights', 'T1', 'RH_1', 'T2', 'RH_2', 'T3',
           'RH_3', 'T4', 'RH_4', 'T5', 'RH_5', 'T6', 'RH_6', 'T7', 'RH_7', 'T8',
           'RH_8', 'T9', 'RH_9', 'T_out', 'Press_mm_hg', 'RH_out', 'Windspeed',
           'Visibility', 'Tdewpoint', 'rv1', 'rv2']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"Отсутствуют столбцы: {missing_columns}")

    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return None


def main():
    # df = pd.read_csv('datasets/energydata_complete.csv')
    # get_data_info(df)

    app.run(debug=True)


if __name__ == '__main__':
    main()