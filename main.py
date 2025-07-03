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
    df = pd.read_csv(file_path)

    # Ожидаемые столбцы с их типами данных
    expected_columns = {
        'date': 'datetime64[ns]',
        'Appliances': 'int64',
        'lights': 'int64',
        'T1': 'float64',
        'RH_1': 'float64',
        'T2': 'float64',
        'RH_2': 'float64',
        'T3': 'float64',
        'RH_3': 'float64',
        'T4': 'float64',
        'RH_4': 'float64',
        'T5': 'float64',
        'RH_5': 'float64',
        'T6': 'float64',
        'RH_6': 'float64',
        'T7': 'float64',
        'RH_7': 'float64',
        'T8': 'float64',
        'RH_8': 'float64',
        'T9': 'float64',
        'RH_9': 'float64',
        'T_out': 'float64',
        'Press_mm_hg': 'float64',
        'RH_out': 'float64',
        'Windspeed': 'float64',
        'Visibility': 'float64',
        'Tdewpoint': 'float64',
        'rv1': 'float64',
        'rv2': 'float64'
    }

    try:
        # Ищем отсутствующие столбцы
        missing_columns = set(expected_columns.keys()) - set(df.columns())

        # Если есть отсутствующие столбцы, выкидываем ошибку
        if missing_columns:
            raise ValueError(f"Отсутствуют ожидаемые столбцы: {missing_columns}")

        # Ищем лишние столбцы
        extra_columns = set(df.columns()) - set(expected_columns.keys())

        # Если есть лишние столбцы, выкидываем ошибку
        if extra_columns:
            raise ValueError(f"Присутствуют лишние столбцы: {extra_columns}")

        type_errors = []
        # Проверяем каждый столбец на соответствие типов данных
        for col, expected_type in expected_columns.items():
            actual_type = str(df[col].dtype())

            # Особый случай - тип данных datetime
            if expected_type == 'datetime64[ns]':
                # Если тип данных не совпадает с любым возможным представлением даты в pandas/numpy
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    # Добавляем ошибку
                    type_errors.append(f"{col}: ожидается тип - {expected_type}, получен тип - {actual_type}")
            # Для остальных случаев несовпадения типа данных добавляем ошибку
            elif actual_type != expected_type:
                type_errors.append(f"{col}: ожидается тип - {expected_type}, получен тип - {actual_type}")

        # Выкидываем ошибку, если типы данных не совпадают
        if type_errors:
            raise TypeError("Ошибки типов данных:\n" + "\n".join(type_errors))

    except Exception as e:
        print(f"Ошибка при валидации файла: {str(e)}")
        return None


def main():
    # df = pd.read_csv('datasets/energydata_complete.csv')
    # get_data_info(df)

    app.run(debug=True)


if __name__ == '__main__':
    main()