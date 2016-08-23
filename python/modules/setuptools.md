# setuptools
## 安装setuptools

```python
apt-get -y install python-setuptools
```

## 创建包流程

1. 创建包目录

	```bash
	$ mkdir /tmp/demo
	$ cd /tmp/demo
	```

2. 编写setup.py文件

	```python
	from setuptools import setup, find_packages
	setup(
		name = 'demo',			            # 包名
		version = '0.1',                # 版本号 
		packages = find_packages(),     # 包含的其它包
		)	
	```
	
3. 打包,安装包

	```bash
	$ python setup.py bdist_egg
	$ python setup.py install
	# 打包后目录结构
	$ tree demo/
	demo/
	├── build
	│   └── bdist.linux-x86_64
	├── demo.egg-info
	│   ├── dependency_links.txt
	│   ├── PKG-INFO
	│   ├── SOURCES.txt
	│   └── top_level.txt
	├── dist
	│   └── demo-0.1-py2.7.egg	         # zip包
	└── setup.py
4 directories, 6 files
	```


