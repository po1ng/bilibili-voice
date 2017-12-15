import time


def str_to_time(time_str):
    time_array = time_str.split(':')
    try:
        total_second = int(time_str[0]) * 3600 + int(time_array[1]) * 60 + int(time_array[2])
        return total_second
    except:
        return ''


def time_to_str(seconds):
    m, s = divmod(seconds, 60)
    a = "%02d:%02d" % (m, s)
    return a


def handle_time_stamp():
    t = time.time()
    t = str(t).replace('.', '')
    t = t[:13]
    return t

def utf8_data_to_file(f, data):
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