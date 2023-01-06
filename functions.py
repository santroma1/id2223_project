import datetime


def timestamp_2_time(x):
    dt_obj = datetime.datetime.strptime(str(x), '%Y-%m-%d')
    dt_obj = dt_obj.timestamp() * 1000
    return int(dt_obj)