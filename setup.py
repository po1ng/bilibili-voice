"""
   \ /     ||         ||     ||         ||                                                     
|-------|  ||      \/ || \/  ||      \/ || \/                                        
| /   \ |  ||||||  || || ||  ||||||  || || ||         __   .   __   __ 
|   W   |  ||   || || || ||  ||   || || || ||  \  /  |  |  |  |    |__                         
|-------|  ||||||  || || ||  ||||||  || || ||   \/   |__|  |  |__  |__                                    

"""
from setuptools import setup, find_packages

setup(
    name='bilibili-voice',
    version='0.1.0.1',
    packages=find_packages(),
    install_requires=[
        'future',
        'requests',
        'PyExecJS'
    ],

    entry_points={
        'console_scripts': [
            'bilibilivoice = bilibilivoice:start'
        ],
    },
    license='MIT',
    author='gogoforit',
    author_email='715157026@qq.com',
    description='So nice, BiliBili Voice!',
    url='https://github.com/gogoforit/bilibili-voice',
    keywords=['music', 'bilibili', 'cli', 'voice'],
)