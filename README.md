# BiliBili-Voice

[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](LICENSE.txt)
[![platform](https://img.shields.io/badge/python-3.5-green.svg)]()

##  简介
我真是爱死B站这破站了！所以这也算是小小地为B站做点贡献啦~
BiliBili弹幕网命令行版本，提供在命令行下在线收听BiliBili的视频。
哔哩哔哩 - ( ゜- ゜)つロ 乾杯~ - bilibili

## 按键说明
<table>
<tr> <td>S</td> <td>Down</td> <td>下移</td> </tr>
	<tr> <td>W</td> <td>Up</td> <td>上移</td> </tr>
	<tr> <td>A</td> <td>Back</td> <td>后退</td> </tr>
	<tr> <td>D</td> <td>Forword</td> <td>前进</td> </tr>
	<tr> <td>Space</td> <td>Play/Pause</td> <td>播放/暂停</td> </tr>
	<tr> <td>Z</td> <td>Add Song</td> <td>添加音乐</td> </tr>
	<tr> <td>Q</td> <td>Quit</td> <td>退出</td> </tr>
</table>

## 功能简介

### 当前完成的B站解析栏目
* 音乐
  - 原创音乐
  - 翻唱
  - VOCALOID·UTAU
  - 演奏
  - 三次元音乐
  - OP/ED/OST
  - 音乐选集	
* 舞蹈
  - 宅舞
  - 三次元舞蹈
  - 舞蹈教程
* 单机游戏
  - 电子竞技
  - 手机游戏
  - 网络游戏
  - 桌游棋牌
  - GMV
  - 音游
  - Mugen
* 科技
  - 趣味科普人文
  - 野生技术协会
  - 演讲·公开课
  - 星海
  - 数码
  - 机械
  - 汽车
* 生活
  - 搞笑
  - 日常
  - 美食圈
  - 动物园
  - 手工
  - 绘画
  - ASMR
  - 运动
  - 其他
* 鬼畜
  - 鬼畜调教
  - 音MAD
  - 人力VOCALOID
  - 教程演示
* 时尚
  - 美妆
  - 服饰
  - 健身
  - 资讯
* 娱乐
  - 综艺
  - 明星
  - Korea相关
* 影视
  - 影视杂谈
  - 影视剪辑
  - 短片
  - 预告·资讯
  - 特摄
* 放映厅
  - 纪录片
  - 电影
  - 电视剧

### 最近播放
会记录您最近在BiliBili-Voice中的播放记录

### 搜索
提供个性化搜索功能

### 帮助
项目帮助文档

##  安装

### 依赖
以下为必要依赖，需要单独安装。

#### 1. mpv<br>
**Mac OS**
```
$ brew install mpv
```
**Ubuntu/Debian**
```
$ (sudo)apt-get install mpv
```
----------------------------------------
#### 2. youtube-dl<br>

**Mac OS下安装mpv会自动安装youtube-dl**

**Ubuntu/Debian**
```
$ (sudo)apt-get install youtube-dl 
```
或者
```
$ pip3 install youtube-dl
```


### 选项1 通过pip安装
```
$ pip3 install bilibili-voice
```

### 选项2 通过Git Clone安装
```
$ git clone https://github.com/gogoforit/bilibili-voice
```
```
$ cd bilibili-voice
```
```
$ python3 setup.py install
```

**注意：如果mpv和youtube-dl安装完毕，还是出现解析错误的话，可以尝试升级mpv和youtube-dl。可能仓库里的软件版本太低，不支持链接解析。**

## 运行
```
$ bilibilivoice
```
## 使用演示
![](https://storage6.cuntuku.com/2017/12/15/KlmRE.gif)

## 出现问题
`bilibili-vocie`如果出现问题，（其实感觉问题还是很多的样子）
搜索开放[Issues](https://github.com/gogoforit/bilibili-voice/issues)。 如果没人报告，开个新[Issues](https://github.com/gogoforit/bilibili-voice/issues)， 加上详细的命令行输出。

## 文档
开发者[文档](http://bilibili-voice.readthedocs.io/zh/latest/)在这里，内容我还在根据功能的增加不断完善。


## 协助开发
**当然是欢迎各位开发者fork/star啦~，未开发完成功能我将在TODO中完整地列出来，如果大家在使用过程中发现bug或者有什么好的idea都可以给我[Issues](https://github.com/gogoforit/bilibili-voice/issues)或者直接[Pull requests](https://github.com/gogoforit/bilibili-voice/pulls)啦~**

## TODO

+ [ ] 用户可以自定义播放队列
+ [x] 播放过程中如果卡死，或者播放时间超时，直接播放下一首
+ [x] 网络异常的情况下的请求异常
+ [ ] 网络异常的情况下的播放异常
+ [ ] 切换新的歌曲时，处于loading状态时，上一首歌的进度条没有清零
+ [ ] B站用户登录，此处建议从移动端来登录，可以避免验证码
+ [ ] 投硬币功能
+ [ ] 用户收藏喜爱的up到自己的收藏夹
+ [ ] 添加视频播放功能（如果觉得音频还不错，可以选择播放视频）
+ [ ] 缓存歌曲到本地

## 感谢
[Richard Yan](https://github.com/xrichardyan)






   
  
