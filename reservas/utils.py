import datetime


def start_of_week(date):
    # Definir o início da semana como segunda-feira
    start = date - datetime.timedelta(days=date.weekday())
    return start


def end_of_week(date):
    # Definir o final da semana como domingo
    end = date + datetime.timedelta(days=(6 - date.weekday()))
    return end
