
def get_percent(count_all, count_true):
    percent = 0
    if count_all and count_true:
        percent = (count_true / count_all) * 100
    return f'{count_true} / {round(percent, 2)}%'
