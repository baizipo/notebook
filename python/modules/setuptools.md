## 参考链接
http://www.voidcn.com/blog/gqtcgq/article/p-4837871.html

http://yansu.org/2013/06/07/learn-python-setuptools-in-detail.html

## 安装与卸载

```bash
$ python setup.py bdist_egg                  # 在dist目录下会生成egg包
$ python setup.py install                    # 将创建的egg包安装到dist-packages目录下
$ python setup.py install --record files.txt # 记录安装文件
$ cat files.txt | xargs rm -rf               # 删除安装文件
```

## setup.py

```python
from setuptools import setup, find_packages
setup(
    name = "HelloWorld",           # 包名
    version = "0.1",               # 版本号
    packages = find_packages(),    # 包含的其它包
    scripts = ['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['docutils>=0.3'],    # 安装依赖

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Me",
    author_email = "me@example.com",
    description = "This is an Example Package",
    license = "PSF",
    keywords = "hello world example examples",
    url = "http://example.com/HelloWorld/",   # project home page, if any
    # could also include long_description, download_url, classifiers, etc.
)
```

### 依赖

setuptools支持在安装发布包时顺带安装它的依赖包，且会在Python Eggs中包含依赖的信息。setuptools和pkg_resources使用一种常见的语法来说明依赖。首先是一个发布包的PyPI名字，后跟一个可选的列表，列表中包含了额外的信息，之后可选的跟一系列逗号分隔的版本说明。版本说明就是由符号<, >, <=, >=, == 或 != 跟一个版本号。

```python
setup(
    install_requires = "foobar",
)
```

如果依赖的模块没有在PyPI中注册，则可以通过setup()的dependency_links参数，提供一个下载该模块的URL。dependency_links选项是一个包含URL字符串的列表，URL可以是直接可下载文件的URL，或者是一个包含下载链接的web页面，还可以是模块库的URL。比如：

```python
setup(
    ...
    dependency_links = [
        "http://peak.telecommunity.com/snapshots/"
    ],
)
```

### find_packages

find_packages参数有: 源码目录、include包名列表、exclude包名列表

1. 默认查找setup.py 同一目录下搜索含有`__init__.py`的包

	```python
	packages = find_packages()
	```

2. 指定源码目录(指定setup.py同级目录下面的src目录)

	```python
	packages = find_packages('src')
	package_dir = {'': 'src'}  # 告诉distutils包都在src下
	```
	
3. include

	```python
	packages = find_packages(include=['wt'])
	```
	
4. exclude

	```python
	packages = find_packages(exclude=['wt'])
	```

5. include_package_data & exclude_package_data

	```python
	setup(
		include_package_data = True,
		exclude_package_data = {'': ['test.py']}
		)
	```

### entry_points

从entry point组名映射到一个表示entry point的字符串或字符串列表。Entry points是用来支持动态发现服务和插件的，一些可扩展的应用和框架可以通过特定的名字找到entry points，也可以通过发布模块的名字来找到，找到之后即可加载使用这些对象了。也用来支持自动生成脚本。

```python
setup(
    entry_points = {
    # console_scripts为entry point组名，一个namespace。同一个entry point组内不能有相同的entry point
        'console_scripts': [
        # 一个entry point就是”name = value”形式的字符串，其中的value就是某个模块中对象的名字
            'foo = demo:test',
            'bar = demo:test',
        ],
        'gui_scripts': [
            'baz = demo:test',
        ]，
        # 使用自定义的”cms.plugin”作为”entry point group”名
        'cms.plugin': [
            'foofun = lib.foo:foofun',
            'barfun = lib.bar.bar:barfun'
        ]
    }
)
```

