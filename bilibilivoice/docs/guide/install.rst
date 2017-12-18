安装
====

依赖
~~~~

**以下为为必要依赖，需要单独安装。**

**1. mpv**

Mac OS 

..  code-block:: bash

     $ brew install mpv
    
Ubuntu/Debian

..  code-block:: bash 
 
     $ (sudo)apt-get install mpv

..  note:: 提示

     请自行判定是否要加上``sudo``命令
    
**2. youtube-dl**

Mac OS下安装mpv会自动安装youtube-dl

Ubuntu/Debain

.. code-block:: bash

    $ (sudo)apt-get install youtube-dl

**或者**

.. code-block:: bash

    $ (sudo)pip3 install youtube-dl

   
选项1 通过pip安装
~~~~~~~~~~~~~~~~~
 
.. code-block:: bash
 
    $ (sudo)pip3 install bilibili-voice
    
选项2 通过Git Clone安装
~~~~~~~~~~~~~~~~~~~~~~~
 
 
.. code-block:: bash
  
     $ git clone https://github.com/gogoforit/bilibili-voice
    
     
.. code-block:: bash

    $ cd bilibili-voice


.. code-block:: bash

     $ python3 setup.py install
      
.. note:: 注意
 
     如果mpv和youtube-dl安装完毕，还是出现解析错误的话，可以尝试升级mpv和youtube-dl。可能仓库里的软件版本太低，不支持链接解析。

