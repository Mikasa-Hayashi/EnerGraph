import pandas as pd
import numpy as np


def load_data(filepath):
    df = None
    try:
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
    except:
        pass

    return df


def find_sensors_count(df):
    columns = df.columns

    temp_sensors = 0
    humidity_sensors = 0

    for column in columns:
        if column.startswith('T') and column[1:].isdigit():
            temp_sensors += 1
        elif column.startswith('RH_') and column[3:].isdigit():
            humidity_sensors += 1

    return temp_sensors, humidity_sensors


def check_sensor_sequence(df, errors, prefix):
    if prefix == 'T':
        pattern = prefix
        start_idx = 1
    else:
        pattern = prefix + '_'
        start_idx = 1

    sensor_cols = [col for col in df.columns if col.startswith(pattern)]
    sensor_nums = []

    for col in sensor_cols:
        try:
            if prefix == 'T':
                num = int(col[1:])
            else:
                num = int(col[3:])
            sensor_nums.append(num)
        except ValueError:
            continue

    if not sensor_nums:
        return True

    max_num = max(sensor_nums)
    expected_nums = set(range(start_idx, max_num + 1))
    actual_nums = set(sensor_nums)

    missing_nums = expected_nums - actual_nums
    if missing_nums:
        errors.append(f"Для {prefix} отсутствуют сенсоры: {sorted(missing_nums)}")
        return False
    return True


def validate_data(df):
    try:
        errors = []
        df = df.copy()

        mandatory_columns = ['date', 'Appliances', 'lights', 'T_out', 'RH_out']
        for col in mandatory_columns:
            if col not in df.columns:
                errors.append(f"Обязательный столбец '{col}' отсутствует")

        if 'date' in df.columns:
            try:
                df['date'] = pd.to_datetime(df['date'])
            except Exception as e:
                errors.append(f"Не удалось преобразовать столбец 'date' в datetime: {str(e)}")

        check_sensor_sequence(df, errors, 'T')
        check_sensor_sequence(df, errors, 'RH')

        if errors:
            raise ValueError("Обнаружены ошибки:\n" + "\n".join(errors))

        expected_dtypes = {
            'date': 'datetime64[ns]',
            'Appliances': 'int64',
            'lights': 'int64',
            'T_out': 'float64',
            'RH_out': 'float64'
        }

        type_errors = []

        for col in df.columns:
            if col.startswith('T') and col[1:].isdigit():
                expected_dtypes[col] = 'float64'
            elif col.startswith('RH_') and col[3:].isdigit():
                expected_dtypes[col] = 'float64'

        for col, expected_type in expected_dtypes.items():
            if col not in df.columns:
                continue

            actual_type = str(df[col].dtype)
            if actual_type != expected_type:
                type_errors.append(f"Столбец '{col}': ожидаемый тип {expected_type}, получен {actual_type}")

        if type_errors:
            raise TypeError("Ошибки типов данных:\n" + "\n".join(type_errors))

    except Exception as e:
        return False, e

    return True, None