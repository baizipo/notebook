## debootstrap_febootstrap

`debootstrap`: debootstrap是debian/ubuntu下的一个工具，用来构建一套基本的系统(根文件系统)。生成的目录符合Linux文件系统标准(FHS)，即包含了/boot、/etc、/bin、/usr等等目录，但它比发行版本的Linux体积小很多，当然功能也没那么强大，因此，只能说是“基本的系统”。

`febootstrap`: fedora下(centos亦可用)相同功能的工具。

> 备注： kernel、grub等需要额外部署配置，debootstrap_febootstrap也可以用来制作docker镜像


### 安装

```bash
# apt-get install debootstrap
```

### 使用

```bash
# debootstrap trusty test_debootstrap/ http://mirrors.aliyun.com/ubuntu
# 详见 debootstrap --help
```

> 备注： 当前debootstrap支持的发行版本可以在/usr/share/debootstrap/scripts查看，而各发行版代号，可以到http://en.wikipedia.org/wiki/List_of_Ubuntu_releases查看。比如gutsy是7.10的代号，precise是12.04的代号，等等。



