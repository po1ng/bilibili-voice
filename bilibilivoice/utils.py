# -*- coding: utf-8 -*-
import time


def str_to_time(time_str):
    """
    字符串到时间的转换，单位：秒

    :param time_str: 时间字符串

    :return: 换算的时间

    """
    time_array = time_str.split(':')
    try:
        total_second = int(time_str[0]) * 3600 + int(time_array[1]) * 60 + int(time_array[2])
        return total_second
    except:
        return ''


def time_to_str(seconds):
    """
    时间（秒）换算成时间字符串

    :param seconds: 时间

    :return: 时间字符串
    """
    m, s = divmod(seconds, 60)
    a = "%02d:%02d" % (m, s)
    return a


def handle_time_stamp():
    """
    获取13位的时间戳
    """
    t = time.time()
    t = str(t).replace('.', '')
    t = t[:13]
    return t

def utf8_data_to_file(f, data):
    """
    数据编码转换
    """
    if hasattr(data, 'decode'):
        f.write(data.decode('utf-8'))
    else:
        f.write(data)


if __name__ == '__main__':
    a = '01'
    b = int(a)
    print(b)
    now_playing = str_to_time('00:12:01')
    total_length = str_to_time('00:20:01')
    pause_flag = False
    process = '['
    for i in range(0, 33):
        if i < now_playing / total_length * 33:
            if (i + 1) > now_playing / total_length * 33:
                if not pause_flag:
                    process += '>'
                    continue
            process += '='
        else:
            process += ' '
    process += '] '
    print(process)