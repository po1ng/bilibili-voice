import curses
import random
import time
from . import terminalsize

from .api import BiliBiliVoice
from .cache import Cache
from . import logger

log = logger.getLogger(__name__)

from .scrollstring import truelen, scrollstring


class Ui(object):
    def __init__(self):
        self.screen = curses.initscr()
        self.screen.timeout(100)  # the screen refresh every 100ms
        # charactor break buffer
        curses.cbreak()
        self.screen.keypad(1)
        self.screen.move(1, 2)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        size = terminalsize.get_terminal_size()
        self.x = max(size[0], 10)
        self.y = max(size[1], 25)

        self.startcol = int(float(self.x) / 5)
        self.headercol = int(float(self.x) / 12)

        self.bilibilivoice = BiliBiliVoice()
        self.wave = ''
        self.indented_startcol = max(self.startcol - 3, 0)
        self.wave_list = ['▁', '▂', '▃', '▅', '▆', '▇']
        self.keyword = ''

    def addstr(self, *args):
        if len(args) == 1:
            self.screen.addstr(args[0])
        else:
            self.screen.addstr(args[0], args[1], args[2].encode('utf-8'), *args[3:])

    def build_loading(self):
        self.addstr(7, self.startcol, '哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili，loading...',
                    curses.color_pair(1))
        self.screen.refresh()

    def build_loading_process(self):
        """
        播放进度条缓冲
        """
        self.addstr(20, self.startcol, '哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili，loading...',
                    curses.color_pair(1))
        self.screen.refresh()

    def build_header(self):
        self.addstr(1, self.headercol, '   \ /     ||         ||     ||         ||')
        self.addstr(2, self.headercol, '|-------|  ||      \/ || \/  ||      \/ || \/')
        self.addstr(3, self.headercol, '| /   \ |  ||||||  || || ||  ||||||  || || ||         __   .   __   __')
        self.addstr(4, self.headercol, '|   W   |  ||   || || || ||  ||   || || || ||  \  /  |  |  |  |    |__')
        self.addstr(5, self.headercol, '|-------|  ||||||  || || ||  ||||||  || || ||   \/   |__|  |  |__  |__')
        self.screen.refresh()

    def build_menu(self, datatype, datalist, offset, step, index, title, start):
        """
        菜单栏UI构造
        :param datatype: 菜单类型
        :param datalist: 菜单列表
        :param offset: 该页面起始位置
        :param step: 该页面包括的菜单数
        :param index: 光标所处位置
        :param title: 进度菜单
        BiliBili Voice > 栏目 > 音乐
        :param start: 时间
        """
        curses.noecho()
        self.screen.move(7, 1)
        self.screen.clrtobot()  # 从光标以下全被刷新
        self.addstr(7, self.startcol, title, curses.color_pair(1))

        if datatype == 'channel_list' or datatype == 'recently_play':
            songs_list = []
            for i in datalist:
                songs_list.append(i['title'])

            iter_range = min(len(datalist), offset + step)
            for i in range(offset, iter_range):
                # this item is focus
                name = songs_list[i]
                if i == index:
                    self.addstr(i - offset + 9, 0,
                                ' ' * self.startcol)
                    lead = '-> ' + str(i) + '. '
                    self.addstr(i - offset + 9,
                                self.indented_startcol, lead,
                                curses.color_pair(2))


                    # the length decides whether to scoll
                    if truelen(name) < self.x - self.startcol - 1:
                        self.addstr(
                            i - offset + 9,
                            self.indented_startcol + len(lead), name,
                            curses.color_pair(2))
                    else:
                        name = scrollstring(name + '  ', start)
                        self.addstr(
                            i - offset + 9,
                            self.indented_startcol + len(lead), str(name),
                            curses.color_pair(2))
                else:
                    self.addstr(i - offset + 9, 0,
                                ' ' * self.startcol)
                    self.addstr(
                        i - offset + 9, self.startcol,
                        str(i) + '. ' + name)

            self.addstr(iter_range - offset + 9, 0, ' ' * self.x)

        elif datatype == 'search':
            self.build_search_bar()

        else:
            # main, music_channel, channel等目录的刷新
            for i in range(offset, min(len(datalist), offset + step)):
                if i == index:
                    self.addstr(i - offset + 9,
                                self.indented_startcol,
                                '-> ' + str(i) + '. ' + datalist[i],
                                curses.color_pair(2))
                else:
                    self.addstr(i - offset + 9, self.startcol,
                                str(i) + '. ' + datalist[i])

        self.screen.refresh()

    def build_add_av(self):
        self.build_add_av_bar()
        av_number = self.get_av_number()
        cache = Cache()
        bilibili = BiliBiliVoice()
        mp3_down_url = bilibili.handle_mp3_url(str(av_number))
        cache.downloading.append([mp3_down_url])
        cache.start_download()

    def build_add_av_bar(self):
        curses.noecho()
        self.addstr(10, self.startcol, '请添加要播放的av号',
                    curses.color_pair(1))
        self.addstr(11, self.startcol, 'av:', curses.color_pair(1))
        # self.addstr(12, self.startcol, '密码:', curses.color_pair(1))
        self.screen.move(11, 24)

    def build_process_bar(self, now_playing, total_length, playing_flag,
                           now_time, total_time, pause_flag,  start, song_info=None):
        curses.noecho()
        self.screen.move(20, 1)
        self.screen.clrtoeol()
        self.screen.move(21, 1)
        self.screen.clrtoeol()
        self.screen.move(22, 1)
        self.screen.clrtoeol()
        if not playing_flag:
            return
        if now_playing is 0 and total_length is 0:
            self.build_loading_process()
            return
        process = ''
        if not pause_flag:
            process += 'o(*≧▽≦) '
        else:
            process += '(≖ ‿ ≖) '
        process += now_time + '['
        for i in range(0, 33):
            if total_length is 0:
                process += ' '
            elif i < now_playing / total_length * 33:
                if (i + 1) > now_playing / total_length * 33:
                    if not pause_flag:
                        process += '>'
                        continue
                process += '='
            else:
                process += ' '
        process += ']' + total_time
        if not pause_flag:
            self.wave = ''
            for i in range(0, 10):
                a = random.choice(self.wave_list)
                self.wave += a
        process += '  ' + self.wave
        process_title = '[' + song_info['up_name'] + ']' + ' [' + song_info['title'] + '] ' + '[' + 'av' + str(song_info['aid']) + ']'

        if truelen(process_title) < self.x - self.startcol - 1:
            self.addstr(
                20,
                self.startcol - 8, process_title,
                curses.color_pair(2))
        else:
            name = scrollstring(process_title + '  ', start)
            self.addstr(
                20,
                self.startcol - 8, str(name),
                curses.color_pair(2))

        # 把滚动轴多余的刷新到下一行的，刷新掉
        self.addstr(21, 0, ' ' * self.x)
        self.addstr(21, self.startcol - 8, process, curses.color_pair(1))

        self.screen.refresh()

    def build_search_bar(self):
        curses.noecho()
        self.screen.move(6, 1)
        self.screen.clrtobot()
        self.addstr(10, self.startcol, '请输入要搜索的内容：',curses.color_pair(1))
        self.screen.move(12, 24)
        self.screen.refresh()

    def build_search(self):
        self.build_search_bar()
        keyword = self.get_search_keyword()
        self.keyword = keyword
        bilibilibvoice = self.bilibilivoice
        generate_search = bilibilibvoice.get_search(keyword)
        return generate_search

    def get_search_keyword(self):
        self.screen.timeout(-1)  # disable the screen timeout
        curses.echo()
        keyword = self.screen.getstr(10, self.startcol + 20, 60)
        self.screen.timeout(100)  # restore the screen timeout
        return keyword.decode('utf-8')

    def get_av_number(self):
        self.screen.timeout(-1)  # disable the screen timeout
        curses.echo()
        account = self.screen.getstr(11, self.startcol + 6, 60)
        self.screen.timeout(100)  # restore the screen timeout
        return account.decode('utf-8')
