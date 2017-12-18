# encoding: UTF-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
import os


class Constant(object):
    """
    常量使用地址

    :param conf_dir: 整个文件目录地址

    :param download_dir: 缓存文件夹地址

    :param config_path: 配置文件地址

    :param storage_path: 播放信息等存储地址

    :param cookie_path: cookie存储地址

    :param log_path: 日志存储地址
    """
    conf_dir = os.path.join(os.path.expanduser('~'), '.bilibili-voice')
    download_dir = os.path.join(conf_dir, 'cached')
    config_path = os.path.join(conf_dir, 'config.json')
    storage_path = os.path.join(conf_dir, 'database.json')
    cookie_path = os.path.join(conf_dir, 'cookie')
    log_path = os.path.join(conf_dir, 'bilibili-voice.log')
