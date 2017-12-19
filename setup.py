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
    version='0.2.0.3',
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
    description='bilibili-voice is a native audio player for BiliBili video in command line mode',
    long_description=open('README.rst').read(),
    url='https://github.com/gogoforit/bilibili-voice',
    keywords=['music', 'bilibili', 'cli', 'voice'],
    platforms=['Ubuntu', 'Mac OS']
)