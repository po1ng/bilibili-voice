import requests
import re
import execjs
import json
from . import logger
import time

from .utils import handle_time_stamp

log = logger.getLogger(__name__)
default_timeout = 10

# 每个栏目的频道下包含的子栏目
channel_map = {
    'music_channel_list': ['原创音乐', '翻唱', 'VOCALOID·UTAU', '演奏', '三次元音乐',
                           'OP/ED/OST', '音乐选集'],

    'dance_channel_list': ['宅舞', '三次元舞蹈', '舞蹈教程'],

    'game_channel_list': ['单机游戏', '电子竞技', '手机游戏', '网络游戏',
                          '桌游棋牌', 'GMV', '音游', 'Mugen'],

    'technology_channel_list': ['趣味科普人文', '野生技术协会', '演讲·公开课',
                                '星海', '数码', '机械', '汽车'],


    'life_channel_list': ['搞笑', '日常', '美食圈', '动物园', '手工',
                          '绘画', 'ASMR', '运动', '其他'],

    'kichiku_channel_list': ['鬼畜调教', '音MAD', '人力VOCALOID', '教程演示'],

    'fashion_channel_list': ['美妆', '服饰', '健身', '资讯'],

    'entertainment_channel_list': ['综艺', '明星', 'Korea相关'],

    'movie_channel_list': ['影视杂谈', '影视剪辑', '短片', '预告·资讯', '特摄'],

    'auditorium_channel_list': ['纪录片', '电影', '电视剧']
}

# 放映室的二级目录
auditorium_channel_detailed_map = {
    '纪录片': ['人文历史', '科学探索', '热血军事', '舌尖上的旅行'],
    '电影': ['华语电影', '欧美电影', '日本电影', '其他国家'],
    '电视剧': ['国产剧', '海外剧']
}

# 每个子栏目对应的api请求id
channel_rid_map = {

    # 音乐
    '原创音乐': '28',
    '翻唱': '31',
    'VOCALOID·UTAU': '30',
    '演奏': '59',
    '三次元音乐': '29',
    'OP/ED/OST': '54',

    # 舞蹈
    '宅舞': '20',
    '三次元舞蹈': '154',
    '舞蹈教程': '156',

    # 游戏
    '单机游戏': '17',
    '电子竞技': '171',
    '手机游戏': '172',
    '网络游戏': '65',
    '桌游棋牌': '173',
    'GMV': '121',
    '音游': '136',
    'Mugen': '19',

    # 科技
    '趣味科普人文': '124',
    '野生技术协会': '122',
    '演讲• 公开课': '39',
    '星海': '96',
    '数码': '95',
    '机械': '98',
    '汽车': '176',

    # 生活
    '搞笑': '138',
    '日常': '21',
    '美食圈': '76',
    '动物圈': '75',
    '手工': '161',
    '绘画': '162',
    'ASMR': '175',
    '运动': '163',
    '其他': '174',

    # 鬼畜
    '鬼畜调教': '22',
    '音MAD': '26',
    '人力VOCALOID': '126',
    '教程演示': '127',

    # 时尚
    '美妆': '157',
    '服饰': '158',
    '健身': '164',
    '资讯': '159',

    # 娱乐
    '综艺': '71',
    '明星': '137',
    'Korea相关': '131',

    # 电影
    '影视杂谈': '182',
    '影视剪辑': '183',
    '短片': '85',
    '预告 资讯': '184',
    '特摄': '86',

    # 放映厅->纪录片
    '人文历史': '37',
    '科学探索': '178',
    '热血军事': '179',
    '舌尖上的旅行': '180',

    # 放映厅->电影
    '华语电影': '147',
    '欧美电影': '145',
    '日本电影': '146',
    '其他国家': '83',

    # 放映厅->电视剧
    '国产剧': '185',
    '海外剧': '187'

}


class BiliBiliVoice(object):
    """
    解析BiliBili的接口类
    """
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0)'
                          ' Gecko/20100101 Firefox/57.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.session()

    def http_request(self,
            method,
            url,
            query=None,
            urlencoded=None,
            callback=None,
            timeout=None):
        connection = self.raw_http_request(method, url, query, urlencoded, callback, timeout)
        # print(connection)
        return connection

    def raw_http_request(self,
            method,
            url,
            query=None,
            urlencoded=None,
            callback=None,
            timeout=None):
        if method == 'GET':
            # url = action if query is None else action + '?' + query
            connection = self.session.get(url, params=query,
                                          headers=self.header,
                                          timeout=default_timeout)

        elif method == 'POST':
            connection = self.session.post(url,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)

        elif method == 'Login_POST':
            connection = self.session.post(url,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)
            self.session.cookies.save()

        connection.encoding = 'UTF-8'
        return connection.text

    def handle_mp3_url(self, av_number):
        """
        处理出唧唧上的mp3的下载地址，其中有两次重定向，然后要通过ref中的一个加密字符串来解析出最终
        的下载地址，通过直接执行js代码，来获取出最红mp3的下载地址
        :param av_number: 想要下载的av号
        :return: av_number对应的mp3下载地址
        """
        url = 'http://www.jijidown.com/video/{av_number}/'
        av_number = av_number.replace(' ', '')
        url = url.format(av_number=av_number)
        html = requests.get(url=url).text

        down_number = re.findall("mp4.*href='/Files/DownLoad/(.*?).mp3", html)[0]
        down_url = 'http://www.jijidown.com/FreeDown/{down_number}.jsp'
        down_url = down_url.format(down_number=down_number)

        html = requests.get(url=down_url).text
        redirect_url = re.findall('"mp3" != "mp3".*if \("(.*?)".indexOf', html, re.S)[0]
        redirect_url = ''.join(['http://www.jijidown.com', redirect_url]).replace('CDN', '')  # CDN路线的 加载特别慢, 用去掉CDN路线的

        headers = self.header
        ref_response = requests.get(url=redirect_url, headers=headers)
        ref_url = ref_response.url.split('=')[1]
        mp3_down_url = self._decrypt_js(ref_url)
        return mp3_down_url

    def _decrypt_js(self, ref_url):
        """
        解析哔哩哔哩唧唧上的mp3下载地址
        :param ref_url: 中间跳转的地址
        :return: mp3下载地址
        """
        mp3_down_url = execjs.compile(open(r"asset/analyze-url.js").read()).call('test', ref_url)
        return mp3_down_url

    def get_channel(self, name):
        """
        获取每个频道下具体的子栏目
        :param name: 频道名
        :return: 子栏目列表
        """
        name = name + '_channel_list'
        return channel_map[name]

    def get_auditorium_channel_detailed(self, name):
        """
        获取"放映厅"二级目录下的子栏目
        :param name: 二级下的目录频道名
        :return: 二级目录下的子栏目列表
        """
        return auditorium_channel_detailed_map[name]

    def channel_list(self, channel):
        """
        用于获取各种子栏目信息的生成器
        :param channel: 各种子栏目名
        :return: 信息列表
        """
        page_number = 1
        rid = channel_rid_map[channel]
        while True:
            time_stamp = handle_time_stamp()
            data = {
                'callback': 'jQuery17208755520020902555_' + time_stamp,
                'rid': rid,
                'type': '0',
                'pn': str(page_number),
                'ps': '20',
                'jsonp': 'jsonp',
                '_': time_stamp
            }
            url = 'https://api.bilibili.com/x/web-interface/newlist'
            response_text = self.http_request('GET', url, data)
            songs_info_str = re.findall('.*("archives":.*?]),"page".*', response_text, re.S)[0]
            songs_info_str = ''.join(['{', songs_info_str, '}'])
            songs_info_json = json.loads(songs_info_str)
            songs_info_list = songs_info_json['archives']
            songs_list = []
            for i in songs_info_list:
                aid = i['aid']
                title = i['title']
                tname = i['tname']
                up_name = i['owner']['name']
                up = {}
                up['aid'] = aid
                up['title'] = title
                up['tname'] = tname
                up['up_name'] = up_name
                songs_list.append(up)
            yield songs_list
            page_number += 1

    def get_play_total_time(self, av_number):
        """
        获取播放的总时间
        :param av_number: 播放id号
        :return: 总共的播放时间
        >>> bilibili = BiliBiliVoice()
        >>> a = bilibili.get_play_total_time('17100583')
        210
        """
        data = {
            'aid': av_number,
            'jsonp': 'jsonp'
        }
        url = 'https://api.bilibili.com/x/player/pagelist'
        try:
            response_json = self.http_request('GET', url, data)
            json_data = json.loads(response_json)
            total_time = json_data['data'][0]['duration']
        except Exception as e:
            log.error('json解析错误' + e)
            total_time = 0
        return total_time

    def get_search(self, keyword):
        page_number = 1
        while True:
            time_stamp = handle_time_stamp()
            data = {
                'keyword': keyword,
                'page': page_number,
                'order': 'totalrank',
                '_': time_stamp
            }
            url = 'https://search.bilibili.com/ajax_api/video'
            response_text = self.http_request('GET', url, data)
            response_json = json.loads(response_text)
            html = response_json['html']
            try:
                li_list = re.findall('<li(.*?)</li>', html, re.S)
            except Exception as e:
                log.error(e)
            info_list = []
            try:
                for i in li_list:
                    info_dict = {}
                    aid = re.findall('data-aid="(.*?)"', i, re.S)[0]
                    title = re.findall('title="(.*?)"', i, re.S)[0]
                    up_name = re.findall('up主.*<a.*>(.*?)</a>', i, re.S)[0]
                    info_dict['aid'] = aid
                    info_dict['title'] = title
                    info_dict['up_name'] = up_name
                    info_dict['tname'] = '搜索'
                    info_list.append(info_dict)
            except Exception as e:
                log.error(e)
            yield info_list
            page_number += 1

if __name__ == '__main__':
    bilibili = BiliBiliVoice()
    a = bilibili.get_search('神奇女侠')
    print(a)
    # bilibili.get_play_total_time('17210906')
    while True:
        c = input()
        print(next(a))