## 参考链接

http://www.ibm.com/developerworks/cn/linux/1306_qinzl_squashfs/

## 启动过程

Boot Loader -> kernel -> initd -> rootfs

* Boot Loader: 由 BIOS 加载，用于将后续的 Kernel 和 initrd 的装载到内存中.
* kernel：为 initrd 运行提供基础的运行环境
* initrd：检测并加载各种驱动程序
* rootfs：根文件系统，用户的各种操作都是基于这个被最后加载的文件系统

## vmlinuz

vmlinuz是Linux 内核的镜像文件,可以被引导程序加载,从而启动Linux系统

## initrd
initrd是“initial ramdisk”的简写.initrd一般被用来临时的引导硬件到实际内核vmlinuz能够接管并继续引导的状态.
　　1)在一个RAM disk上建立一个临时的root文件系统,在这个RAM disk上包含着你需要的驱动模块
　　2)载入所需驱动模块,挂载实际的root文件系统 ,启动Linux

## SquashFS

SquashFS 也是一个只读的文件系统，它可以将整个文件系统压缩在一起，存放在某个设备，某个分区或者普通的文件中。如果您将其压缩到一个设备中，那么您可以将其直接 mount 起来使用，而如果它仅仅是个文件的话，您可以将其当为一个 loopback 设备使用。

### 安装

```bash
apt-get -y install squashfs-tools
```


