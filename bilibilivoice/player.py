import subprocess
import re
import time
import threading


from .utils import str_to_time, time_to_str
from .api import BiliBiliVoice
from .storage import Storage
from .ui import Ui
from .mpv import MPV
from . import logger

log = logger.getLogger(__name__)


class MyMPV(MPV):
    #-------------------------------------------------------------------------
    # Initialization.
    #-------------------------------------------------------------------------

    # The mpv process and the communication code run in their own thread
    # context. This results in the callback methods below being run in that
    # thread as well.

    def __init__(self, path):
        # Pass a window id to embed mpv into that window. Change debug to True
        # to see the json communication.
        super().__init__(window_id=None, debug=False)

        self.process_location = 0
        self.remaining = 0
        self.command("loadfile", path, "append")
        self.set_property("playlist-pos", 0)
        self.loaded = threading.Event()
        self.loaded.wait()

    #-------------------------------------------------------------------------
    # Callbacks
    #-------------------------------------------------------------------------

    # The MPV base class automagically registers event callback methods
    # if they are specially named: "file-loaded" -> on_file_loaded().
    def on_file_loaded(self):
        self.loaded.set()

    # The same applies to property change events:
    # "time-pos" -> on_property_time_pos().
    def on_property_time_pos(self, position=None):
        if position is None:
            return
        self.process_location = int(position)
        return

    def on_property_length(self, length=None):
        if length is None:
            return

    def on_property_time_remaining(self, remaining=None):
        if remaining is None:
            return
        self.remaining = int(remaining)
        return remaining

    #-------------------------------------------------------------------------
    # Commands
    #-------------------------------------------------------------------------
    # Many commands must be implemented by changing properties.
    def new_play(self, url):
            self.command("loadfile", url, "replace")
            self.set_property("playlist-pos", 0)

    def add_music_list(self, url):
        self.command("loadfile", url, 'append-play')

    def play(self):
        self.set_property("pause", False)

    def pause(self):
        self.set_property("pause", True)

    def seek(self, position):
        self.command("seek", position, "absolute")

    def resume(self):
        self.set_property("pause", False)

    def stop(self):
        self.command("stop")


class Player(object):

    def __init__(self):
        self.ui = Ui()
        self.bilibilivoice = BiliBiliVoice()
        self.playing_flag = False
        self.pause_flag = False
        self.player = None
        self.total_flag = False  # 进度条是否可以判定为结束的标志
        self.change_flag = False  # 切歌标志
        self.now_time = ''
        self.total_time = ''
        self.play_thread = None
        self.data_list = None
        self.playing_index = 0  # 正在播放的音乐在播放池中的位置
        self.process_length = 0  # 总的播放时间
        self.process_location = 0  # 当前播放进度
        self.playing_id = 0  # 正在播放的音乐的av号

        self.storage = Storage()
        self.info = self.storage.database['player_info']
        self.songs = self.storage.database['songs']

    def play(self, av_number):
        self.playing_flag = True
        self.playing_id = av_number
        play_url = 'https://www.bilibili.com/video/av{av_number}'.format(av_number=av_number)

        # TODO 播放卡死后，或者播放超时之后，直接播放下一首
        def runInThread():
            self.player = MyMPV(play_url)
            self.player.play()
            while True:
                if self.playing_flag is False:
                    break
                self.process_location = int(self.player.process_location)
                self.remaining = int(self.player.remaining)
                self.now_time = time_to_str(self.process_location)
                if not self.total_flag:
                    self.process_length = self.bilibilivoice.get_play_total_time(self.playing_id)
                    if self.process_length is not 0:
                        self.total_flag = True
                # 此时判定为该音乐播放完成
                if abs(self.process_length - self.process_location) < 2:
                    self.total_flag = False
                    self.change_flag = True
                self.total_time = time_to_str(self.process_length)
                if self.process_location == self.process_length and self.process_length is not 0:
                    self.playing_flag = False

        self.play_thread = threading.Thread(target=runInThread, args=())
        self.play_thread.setDaemon(True)
        self.play_thread.start()
        self.ui.build_loading()

    # TODO 切换新的歌曲时，location进度条临时性没有归零
    def new_play(self, av_number):
        self.playing_id = av_number
        self.process_location = 0
        self.now_time = time_to_str(self.process_location)
        play_url = 'https://www.bilibili.com/video/av{av_number}'.format(av_number=av_number)
        self.total_flag = False
        self.player.new_play(play_url)

    def add_music_list(self, av_number):
        play_url = 'https://www.bilibili.com/video/av{av_number}'.format(av_number=av_number)
        self.player.add_music_list(play_url)

    def play_and_pause(self):
        if not self.pause_flag:
            self.pause()
        else:
            self.resume()

    def stop_music(self):
        if self.playing_flag and self.player:
            self.playing_flag = False
            try:
                self.player.close()
            except IOError as e:
                log.error(e)

    def quit(self):
        if self.playing_flag and self.player:
            self.playing_flag = False
            try:
                self.player.close()
            except IOError as e:
                log.error(e)

    def pause(self):
        if not self.playing_flag and not self.player:
            return
        self.pause_flag = True
        try:
            self.player.pause()
        except IOError as e:
            log.error(e)
            return

    def resume(self):
        self.pause_flag = False
        try:
            self.player.resume()
        except IOError as e:
            log.error(e)
            return

if __name__ == '__main__':
    player = Player()
    player.play('https://www.bilibili.com/video/av16860566/')
    time.sleep(10)
    player.stop()

