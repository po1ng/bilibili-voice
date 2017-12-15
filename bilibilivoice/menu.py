import time
import re
import curses
import webbrowser

from . import logger
from .ui import Ui
from .player import Player
from .api import BiliBiliVoice
from .storage import  Storage

log = logger.getLogger(__name__)


def carousel(left, right, x):
    # carousel x in [left, right]
    if x > right:
        return left
    elif x < left:
        return right
    else:
        return x


class Menu(object):

    def __init__(self):
        self.screen = curses.initscr()
        self.title = 'BiliBili Voice'
        self.play = Player()
        self.bilibilivoice = BiliBiliVoice()
        self.play_song_info = None
        self.generate_obj = None
        self.enter_flag = True
        self.START = time.time()
        self.storage = Storage()
        self.storage.load()
        self.info = self.storage.database['player_info']
        self.songs = self.storage.database['songs']
        self.step = 10
        self.offset = 0
        self.datatype = 'main'
        self.datalist = ['分区', '最近播放', '搜索', '帮助']
        self.channel_list = ['音乐', '舞蹈', '游戏', '科技', '生活', '鬼畜', '时尚', '娱乐', '影视', '放映厅']
        # 用于生成具体栏目下的节目
        self.channel_transform_map = {
            '音乐': 'music',
            '舞蹈': 'dance',
            '游戏': 'game',
            '科技': 'technology',
            '生活': 'life',
            '鬼畜': 'kichiku',
            '时尚': 'fashion',
            '娱乐': 'entertainment',
            '电影': 'movie',
            '放映厅': 'auditorium'
        }
        self.stack = []  # 用一个栈，来模拟点击运行与回退
        self.ui = Ui()
        self.index = 0

    def start(self):
        self.ui.build_header()
        self.ui.build_menu(self.datatype, self.datalist, self.offset, self.step, self.index, self.title, self.START)
        self.ui.build_process_bar(self.play.process_location, self.play.process_length,
                                  self.play.playing_flag, self.play.now_time, self.play.total_time,
                                  self.play.pause_flag, self.START)

        self.stack.append([self.datatype, self.title, self.datalist, self.offset, self.index])
        while True:
            key = self.screen.getch()
            idx = index = self.index
            offset = self.offset
            step = self.step
            datalist = self.datalist
            stack = self.stack
            self.ui.screen.refresh()

            if key == ord('q'):
                break

            elif key == ord('w'):
                if idx == offset:
                    if offset == 0:
                        continue
                    self.offset -= step
                    # 移动光标到最后一列
                    self.index = offset - 1
                else:
                    self.index = carousel(offset, min(
                        len(datalist), offset + step) - 1, idx - 1)

            elif key == ord('s'):
                # turn page if at end
                if idx == min(len(datalist), offset + step) - 1:
                    if offset + step >= len(datalist):
                        # continue
                        try:
                            data = next(self.generate_obj)
                            datalist += data
                            self.datalist += data
                        except Exception as e:
                            continue
                    self.offset += step
                    # 移动光标到第一列
                    self.index = offset + step
                else:
                    self.index = carousel(offset, min(
                        len(datalist), offset + step) - 1, idx + 1)

            elif key == ord('d'):
                self.enter_flag = True
                if len(self.datalist) <= 0:
                    continue
                self.START = time.time()
                self.ui.build_loading()
                self.dispatch_enter(idx)
                if self.enter_flag is True:
                    self.index = 0
                    self.offset = 0

            elif key == ord('a'):
                # if not main menu
                if len(self.stack) == 1:
                    continue
                up = stack.pop()
                self.datatype = up[0]
                self.title = up[1]
                self.datalist = up[2]
                self.offset = up[3]
                self.index = up[4]

            elif key == ord('z'):
                if self.datatype == 'channel_list':
                    song_info = self.datalist[idx]
                    av_number = song_info['aid']
                    self.play.add_music_list(av_number)

            elif key == ord(' '):
                # TODO 播放队列，一个用户定义的播放队列，一个默认当前页面的播放队列
                if self.play.playing_flag is False:
                    if self.datatype == 'channel_list' or self.datatype == 'recently_play':
                        self.play.playing_flag = True
                        self.play.playing_id = self.datalist[idx]['aid']
                        self.play.data_list = self.datalist
                        self.play.playing_index = index
                        self.play_song_info = self.datalist[idx]
                        song_info = self.datalist[idx]
                        av_number = song_info['aid']
                        self.info['player_list'].append(av_number)
                        self.songs[av_number] = song_info
                        self.play.play(av_number)
                else:
                    try:
                        if isinstance(self.datalist[idx], dict) and self.datalist[idx]['aid'] != self.play.playing_id:
                            if self.datatype == 'channel_list':
                                self.play.pause_flag = False
                                self.play_song_info = self.datalist[idx]
                                self.play.playing_id = self.datalist[idx]['aid']
                                self.play.data_list = self.datalist
                                self.play.playing_index = index
                                song_info = self.datalist[idx]
                                av_number = song_info['aid']
                                self.info['player_list'].append(av_number)
                                self.songs[av_number] = song_info
                                time.sleep(0.5)
                                self.play.new_play(av_number)
                        else:
                            self.play.play_and_pause()
                    except Exception as e:
                        log.error(e)

            # TODO 跳转到下一首时，有时可能会跳过几个音乐
            if self.play.change_flag:
                index = self.play.playing_index
                if index + 1 >= len(self.play.data_list):
                    self.play.stop_music()
                av_number = self.play.data_list[index + 1]['aid']
                self.play_song_info = self.play.data_list[index + 1]
                self.play.playing_id = self.play.data_list[index + 1]['aid']
                self.play.playing_index += 1
                self.play.new_play(av_number)
                self.play.change_flag = False
                if self.play.pause_flag:
                    self.play.resume()

            self.ui.build_header()
            self.ui.build_menu(self.datatype, self.datalist, self.offset, self.step, self.index, self.title, self.START)
            self.ui.build_process_bar(self.play.process_location, self.play.process_length,
                                      self.play.playing_flag, self.play.now_time, self.play.total_time,
                                      self.play.pause_flag, self.START, self.play_song_info)
        self.play.quit()
        self.storage.save()
        curses.endwin()

    def dispatch_enter(self, idx):
        datatype = self.datatype
        title = self.title
        datalist = self.datalist
        offset = self.offset
        index = self.index
        self.stack.append([datatype, title, datalist, offset, index])

        if idx > len(self.datalist):
            return False

        if datatype == 'main':
            self.choice_channel(idx)

        elif datatype == 'channel':
            data = self.datalist[idx]
            en_name = self.channel_transform_map[data]
            self.datalist = self.bilibilivoice.get_channel(en_name)
            self.title += ' > ' + data
            self.datatype = en_name + '_channel'
        elif datatype == 'auditorium_channel_detailed':
            data = self.datalist[idx]
            self.datatype = 'channel_list'
            self.generate_obj = self.bilibilivoice.channel_list(data)
            self.datalist = next(self.generate_obj)
            self.title = title + ' > ' + data

        elif re.match('.*_channel', datatype):
            if datatype == 'auditorium_channel':
                data = self.datalist[idx]
                self.datatype = 'auditorium_channel_detailed'
                self.datalist = self.bilibilivoice.get_auditorium_channel_detailed(data)
            else:
                data = self.datalist[idx]
                self.datatype = 'channel_list'
                self.generate_obj = self.bilibilivoice.channel_list(data)
                self.datalist = next(self.generate_obj)
                self.title = title + ' > ' + data

        elif self.datatype == 'search':
            # self.ui.build_search_bar()
            self.generate_obj = self.ui.build_search()
            keyword = self.ui.keyword
            log.debug('ui.keyword' + self.ui.keyword)
            self.datatype = 'channel_list'
            self.datalist = next(self.generate_obj)
            self.title = title + ' > ' + keyword
        else:
            stack = self.stack
            up = stack.pop()
            self.datatype = up[0]
            self.title = up[1]
            self.datalist = up[2]
            self.offset = up[3]
            self.index = idx
            self.enter_flag = False

    def choice_channel(self, idx):
        bilibilivoice = self.bilibilivoice
        if idx == 0:
            self.title += ' > 栏目'
            self.datatype = 'channel'
            self.datalist = self.channel_list

        if idx == 1:
            self.title += ' > 最近播放'
            self.datatype = 'recently_play'
            self.datalist = []
            songs_info = self.songs
            for i in songs_info:
                log.debug(i)
                self.datalist.append(songs_info[i])

        if idx == 2:
            self.title += ' > 搜索'
            self.datatype = 'search'
            # 直接在此处生成用于搜索数据的生成器
            # dispatch_enter中要触发才行，而进入搜索界面以后，是已经不会触发按键事件了
            self.generate_obj = self.ui.build_search()
            self.datatype = 'channel_list'
            self.datalist = next(self.generate_obj)
            keyword = self.ui.keyword
            self.title = self.title + ' > ' + keyword
            log.debug('ui.keyword' + self.ui.keyword)

        if idx == 3:
            self.title += ' > 帮助'
            webbrowser.open_new_tab(
                'https://github.com/gogoforit/bilibili-voice')


        self.offset = 0
        self.index = 0

if __name__ == '__main__':
    try:
        menu = Menu()
        menu.start()
    except Exception as e:
        log.error(e)
        print(e)
        menu.play.quit()
        curses.endwin()
