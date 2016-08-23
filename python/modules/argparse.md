# argparse
原文链接：http://python.usyiyi.cn/python_278/library/argparse.html
## argparse 工作流
1. 创建一个解析器

	```python
	>>> parser = argparse.ArgumentParser(description='Process some integers.')
	```
	ArgumentParser对象会保存把命令行解析成Python数据类型所需要的所有信息。
	
2. 添加参数
	通过调用add_argument()方法向ArgumentParser添加程序的参数信息。通常情况下，这些信息告诉ArgumentParser如何接收命令行上的字符串并将它们转换成对象。这些信息被保存下来并在调用parse_args()时用到。例如：
	
	```python
	>>> parser.add_argument('-n', help='username')
	```

3. 解析参数
	ArgumentParser通过parse_args()方法解析参数。它将检查命令行，把每个参数转换成恰当的类型并采取恰当的动作。在大部分情况下，这意味着将从命令行中解析出来的属性建立一个简单的 Namespace对象。
	
	```python
	>>> parser.parse_args(['-n', '1'])
	Namespace(n='1')
	```
	在脚本中，parse_args() 调用一般不带参数，ArgumentParser 将根据sys.argv自动确定命令行参数。
	
## ArgumentParser 对象
__class argparse.ArgumentParser(prog=None, usage=None, description=None, epilog=None, parents=[], formatter_class=argparse.HelpFormatter, prefix_chars='-', fromfile_prefix_chars=None, argument_default=None, conflict_handler='error', add_help=True)__
创建一个新的ArgumentParser对象。所有的参数应该以关键字参数传递。下面有对每个参数各自详细的描述，但是简短地讲它们是：

	* prog - 程序的名字（默认：sys.argv[0]）
	* usage - 描述程序用法的字符串（默认：从解析器的参数生成）
	* description - 参数帮助信息之前的文本（默认：空）
	* epilog - 参数帮助信息之后的文本（默认：空）
	* parents - ArgumentParser 对象的一个列表，这些对象的参数应该包括进去
	* formatter_class - 定制化帮助信息的类
	* prefix_chars - 可选参数的前缀字符集（默认：‘-‘）
	* fromfile_prefix_chars - 额外的参数应该读取的文件的前缀字符集（默认：None）
	* argument_default - 参数的全局默认值（默认：None）
	* conflict_handler - 解决冲突的可选参数的策略（通常没有必要）
	* add_help - 给解析器添加-h/–help 选项（默认：True）

### prog参数
prog参数定义程序的名称，默认使用sys.argv[0].

```python
import argparse
parser = argparse.ArgumentParser(prog='wangtao')
parser.add_argument('-w', help='wangtao')
args = parser.parse_args()
```

```bash
$ python test.py -h
usage: wangtao [-h] [-w W]

optional arguments:
  -h, --help  show this help message and exit
  -w W        wangtao
```

使用`%(prog)s`能快速引用程序的名称

```python
import argparse
parser = argparse.ArgumentParser(prog='wangtao')
parser.add_argument('-w', help='### %(prog)s ###')
args = parser.parse_args()
```

```bash
$ python test.py -h
usage: wangtao [-h] [-w W]

optional arguments:
  -h, --help  show this help message and exit
  -w W        ### wangtao ###
```

### usage 参数
默认情况下，ArgumentParser依据它包含的参数计算出帮助信息，可以通过关键字参数`usage=`覆盖默认的信息

```python
import argparse
parser = argparse.ArgumentParser(usage='python test.py -h')
parser.add_argument('-w', help='### %(prog)s ###')
args = parser.parse_args()
```

```bash
$ python test.py -h
usage: python test.py -h

optional arguments:
  -h, --help  show this help message and exit
  -w W        ### test.py ###
```

### description 参数
程序的简短描述

```python
import argparse
parser = argparse.ArgumentParser(description='test script of argparse')
args = parser.parse_args()
```

```bash
$ python test.py -h
usage: test.py [-h]

test script of argparse

optional arguments:
  -h, --help  show this help message and exit
```

### epilog 参数
帮助信息底部描述

```python
import argparse
parser = argparse.ArgumentParser(description='test script of argparse',
                                 epilog='foot')
args = parser.parse_args()
```

```bash
$ python test.py -h
usage: test.py [-h]

test script of argparse

optional arguments:
  -h, --help  show this help message and exit

foot
```

### parents 参数
设置父参数集，继承父参数

```python
# coding: utf-8
import argparse
# 设置父参数集
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('--parent', type=int)
# 继承父参数集
foo_parser = argparse.ArgumentParser(parents=[parent_parser])
foo_parser.add_argument('foo')
foo_parser.parse_args()
```

```bash
$ python test.py -h
usage: test.py [-h] [--parent PARENT] foo

positional arguments:
  foo

optional arguments:
  -h, --help       show this help message and exit
  --parent PARENT
$ python test.py --parent 2 foo
```

> __注意:__ 大部分父解析器将指定add_help=False。否则，ArgumentParser将看到两个-h/--help 选项（一个在父解析器中，一个在子解析器中）并引发一个错误。
> __注意:__ 在通过parents=传递父解析器之前，你必须完全初始化它们。如果在子解析器之后你改变了父解析器，这些改变不会反映在子解析器中。

### formatter_class 参数



