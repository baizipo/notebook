# windows模板制作
## 安装前准备


1. 创建磁盘：

	```bash
	qemu-img create -f qcow2 -o size=40G /var/lib/libvirt/images/template-2008R2.qcow2
	```

2. 使用virt-manager配置虚拟机:
	1. New VM --> Name --> import existing disk image
	2. Provide the existing storage path --> OS type (windows) --> Version (Microsoft Windows Server 2008)
	3. Customize configuration before install
	4. Add Hardware --> Storage --> Select managed or other existing storage (选择系统盘路径) --> Device type (IDE CDROM) --> Finish
	5. Add Hardware --> Storage --> Select managed or other existing storage (选择virtio驱动盘路径) --> Device type (IDE CDROM) --> Finish
	6. VirtIO Disk1 --> Advanced options --> Disk bus: (Virtio)
	7. NIC:xx:xx:xx --> Device model: (virtio)
	8. Display VNC --> Keymap: (en-us)
	9. start install


## 安装操作系统
1. 加载驱动驱动程序： 选择virtio光盘目录


## 配置操作系统
1. 以administrator用户登录并开启命令行窗口

2. 安装VirtIO驱动：

	```bash
	pnputil -i -a d:\Balloon\2k8R2\amd64\*.INF
	pnputil -i -a d:\NetKVM\2k8R2\amd64\*.INF
	pnputil -i -a d:\qemupciserial\2k8R2\amd64\*.INF
	pnputil -i -a d:\viorng\2k8R2\amd64\*.INF
	pnputil -i -a d:\vioscsi\2k8R2\amd64\*.INF
	pnputil -i -a d:\vioserial\2k8R2\amd64\*.INF
	pnputil -i -a d:\viostor\2k8R2\amd64\*.INF
	```
3. 我的电脑 --> 属性 --> 高级系统设置 --> 远程 --> 允许运行任意版本远程桌面的计算机连接
4. 开始 --> 控制面板 --> Windows 防火墙 --> 高级设置 --> Windows 防火墙属性 --> 域配置文件 & 专用配置文件 & 公用配置文件 --> 防火墙状态 --> 关闭 
5. 控制面板--->windows update--->检查更新--->立即更新
6. 安装python
7. 重启虚拟机
8. 添加修改密码脚本
	1. 开始 --> 运行 --> mmc 
	2. 文件 --> 添加/删除管理单元
	3. 组策略对象编辑器 --> 添加 --> 确定
	4. 本地计算机 策略 --> 计算机配置 --> Windows 设置 --> 脚本(启动/关机) --> 启动
	5. 添加 --> 脚本路径 --> 确定 
	6. 保存控制台
9. run sysperp
	1. Untitled.xml拷贝到c:\Windows\System32\sysprep
	2. sysprep /generalize /oobe /shutdown /unattend:C:\Windows\System32\sysprep\Untitled.xml
	
10. 补充`balloon`：

	1. 拷贝`Balloon/2K8R2/amd64/`目录下所有文件到`c:/Program files/Balloon/`目录下
	2. 使用管理员权限打开`cmd`
	3. 进入目录`c:/Program files/Balloon/`
	4. 安装服务:`BLNSVR.exe -i`
	
	> ##### 重要：
	> ###### 运行sysperp后会自动关机，需要手动开机，开机后加载驱动后会自动重启，在硬盘引导之前强制关机，准备上传到openstack

## 上传镜像
1. 转换格式：qcow2-->raw

  ```bash
  qemu-img convert -f qcow2 -O raw template-2008R2.qcow2 template-2008R2.raw
  ```
  
2. 查看镜像信息

  ```bash
   [root@node-3 ~]# qemu-img info template-2008R2.raw 
	image: template-2008R2.raw
	file format: raw
	virtual size: 40G (42949672960 bytes)
	disk size: 19G

  ```
3. 上传模板  

  ```bash
  glance image-create --name=Windows2008R2mb --disk-format=raw --container-format=bare --min-disk 40 --os-distro windows --property login_name=administrator --visibility=public < /root/template-2008R2.raw
  ```
  
  1. `--min-disk`: 设置最小磁盘
  2. `login_name`: 设置登录虚拟机的用户名
  3. `os-distro`: 设置系统类型(可选：windows,centos,ubuntu,other)
  

## 测试虚拟机
1. 创建虚拟机：

  ```bash 
	nova boot --image 29d3e55b-b5ef-417b-ba06-2d2aa3dd99a6 --flavor 3 --nic 	net-id=71d18020-9ffd-4ead-9707-c6b549f61663  --meta admin_pass=wangtao_789 windows-test
  ```
2. 查看启动日志：

	```bash 
	nova console-log windows-test
	```


