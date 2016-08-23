# cliff

`cliff`使用4个对象组合在一起，创建一个有用的命令行程序。

## Application

`cliff.app.App`命令行程序的入口，负责总体运行！

## CommandManager

`cliff.commandmanager.CommandManager` 默认实现使用`setuptools entry points`加载命令插件！

## Command

`cliff.command.Command`是真正工作的地方。`get_parser`配置参数，`take_action`执行动作。

## Interactive Application

`cliff.interactive.InteractiveApp`提供交互模式。

# Demo App
## 安装
1. 安装虚拟环境

	```python
	$ pip install virtualenv
	$ virtualenv .venv
	$ . .venv/bin/activate
	```
	
2. 安装cliff

	```python
	(.venv)$ python setup.py install
	```

3. 安装Demo App

	```python
	(.venv)$ cd demoapp
	(.venv)$ python setup.py install
	```

## 使用
1. 获取帮助

	```python
	$ cliffdemo -h  
	```
	
2. 执行二级命令

	```python
	$ cliffdemo simple
	```
	
3. 二级命令获取帮助

	```python
	$ cliffdemo help simple
	$ cliffdemo simple --help
	```
	
## `cliffdemo` 源码

cliffdemo包含几个模块

### main.py

```python
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class DemoApp(App):

    def __init__(self):
        super(DemoApp, self).__init__(
            description='cliff demo app',                  # 命令描述信息
            version='0.1',                                 # 命令版本
            command_manager=CommandManager('cliff.demo'),  # 配置查找子命令的namespace
            deferred_help=True,
            )

    def initialize_app(self, argv):                        # 主程序解析后，子命令运行前，进入交互模式前，将被回调
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):                 # 子命令执行前，被回调
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):                  # 子命令执行后，将被回调。如果子命令抛出异常，将覆盖err的值。
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = DemoApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```

### simple.py

```python
import logging

from cliff.command import Command


class Simple(Command):
    "A simple command that prints a message."              # 命令行显示的帮助信息

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):                    # 执行子命令回调take_action
        self.log.info('sending greeting')
        self.log.debug('debugging')
        self.app.stdout.write('hi!\n')


class Error(Command):
    "Always raises an error"

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('causing error')
        raise RuntimeError('this is the expected exception')
```

### list.py

```python
import logging
import os

from cliff.lister import Lister                       # Lister 格式化输出


class Files(Lister):
    """Show a list of files in the current directory.

    The file name and size are printed by default.
    """

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        return (('Name', 'Size'),
                ((n, os.stat(n).st_size) for n in os.listdir('.'))
                )                                     # 返回需要输出的内容
```

### show.py

```python
import logging
import os

from cliff.show import ShowOne                        # 格式输出


class File(ShowOne):
    "Show details about a file"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(File, self).get_parser(prog_name)
        parser.add_argument('filename', nargs='?', default='.')
        return parser

    def take_action(self, parsed_args):
        stat_data = os.stat(parsed_args.filename)
        columns = ('Name',
                   'Size',
                   'UID',
                   'GID',
                   'Modified Time',
                   )
        data = (parsed_args.filename,
                stat_data.st_size,
                stat_data.st_uid,
                stat_data.st_gid,
                stat_data.st_mtime,
                )
        return (columns, data)                     # 返回需要输出的内容
```

### setup.py

```python
#!/usr/bin/env python

PROJECT = 'cliffdemo'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,			                 # 项目名称
    version=VERSION,                    # 项目版本

    description='Demo app for cliff',   # 项目描述
    long_description=long_description,

    author='Doug Hellmann',                  # 项目作者
    author_email='doug.hellmann@gmail.com',  # 项目email

    url='https://github.com/openstack/cliff',
    download_url='https://github.com/openstack/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],   # 适用于任何操作系统平台

    scripts=[],

    provides=[],
    install_requires=['cliff'],   # 安装需要的模块

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [           # 主入口
            'cliffdemo = cliffdemo.main:main'
        ],
        'cliff.demo': [              # 所有子命令定义在这儿
            'simple = cliffdemo.simple:Simple',
            'two_part = cliffdemo.simple:Simple',
            'error = cliffdemo.simple:Error',
            'list files = cliffdemo.list:Files',
            'files = cliffdemo.list:Files',
            'file = cliffdemo.show:File',
            'show file = cliffdemo.show:File',
            'unicode = cliffdemo.encoding:Encoding',
        ],
    },

    zip_safe=False,
)
```

