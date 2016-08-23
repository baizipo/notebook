# 模板制作
使用ubuntu14.04桌面版 制作模板！
## 环境准备

1. 安装kvm环境

	```bash
	# apt-get install qemu-kvm libvirt-bin virt-manager bridge-utils
	```
	
2. 使用virt-manager创建虚拟机

	```bash
	# virt-manager
	```
	
3. 编辑虚拟机配置
	1. New VM --> Name --> Local install media (ISO image or CDROM)
	2. Use ISO image --> Browse (选择安装光盘ISO路径)
	3. Choose an operating system type and version --> OS type && Version
	4. Choose Memory and CPU settings 
	5. Create a disk image on the computer's hard drive
	6. Customize configuration before install
	7. VirtIO Disk1 --> Advanced options --> Disk bus: (Virtio)
	8. NIC:xx:xx:xx --> Device model: (virtio)
	8. Display VNC --> Keymap: (en-us)
	9. start install
	
### IFCos

> ##### 注意：编辑虚拟机配置中，选择IFCos ISO


1. 等待图形安装操作系统完成自动关机！
2. 进入磁盘目录

	```bash
	# cd /var/lib/libvirt/images/
	```

3. 挂载虚拟机磁盘到本地

	```bash
	# guestmount -a IFCos.img -m /dev/vda1 --rw /mnt
	```

4. 修改网卡配置文件

	```
	# vim /mnt/etc/sysconfig/network-scripts/ifcfg-eth0
	删除行：
		1. HWADDR
		2. UUID
	修改行：
		1. NM_CONTROLLED=NO
	```
	
5. umount
	
	```bash
	# umount /mnt
	```
	
6. 压缩磁盘

	```bash
	# tar -Jcf IFCos.img.tar.xz IFCos.img
	```

7. 上传到openstack环境中
	
	```bash
	# scp xxx.xxx.xxx.xxx:/tmp
	# ssh xxx.xxx.xxx.xxx
	# tar -Jxf IFCos.img.tar.xz
	# source openrc
	# glance image-create 
	```

### Email Gateway

> ##### 注意：编辑虚拟机配置中，选择Email Gateway ISO

1. 安装操作系统，进入McAfee Email Gateway Installation Menu, 选择 `a`, `y`
2. 操作系统安装结束后，手动关机.
	



