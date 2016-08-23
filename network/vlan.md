# 配置vlan
工作笔记，备忘！


## 使用ip命令配置vlan
```bash
ip link add link eth0 name eth0.8 type vlan id 8
ip address add 192.168.1.2/24 dev eth0.8
ip -d link show eth0.8
# ip link delete eth0.8
```
## ubuntu 配置vlan
1. 安装vlan包:

	```bash
	apt-get -y install vlan
	```

2. 加载vlan模块:

	```bash
	modprobe 8021q
	```

3. 修改配置文件`/etc/network/interfaces`:

	```bash
	# 引入子配置文件
	source /etc/network/interfaces.d/*
	# 配置eth0物理网卡
	auto eth0
	iface eth0 inet manual
	# 配置vlan子网卡
	auto eth0.32
	iface eth0.32 inet manual
	vlan-raw-device eth0
	# 添加桥接使用
	auto br-ex
	iface br-ex inet static
	bridge_ports eth0.32 p_ff798dba-0
	address 192.168.32.4/24
	gateway 192.168.32.254
	```


## centos 配置vlan
1. 加载模块:

	```bash
	modprobe --first-time 8021q
	```

2. 修改配置文件`/etc/sysconfig/network-scripts/ifcfg-eth0`:

	```bash
	DEVICE=eth0
	TYPE=Ethernet
	BOOTPROTO=none
	ONBOOT=yes
	```

3.  修改配置文件`/etc/sysconfig/network-scripts/ifcfg-eth0.192`:

	```bash
	DEVICE=eth0.192
	BOOTPROTO=none
	ONBOOT=yes
	IPADDR=192.168.1.1
	PREFIX=24
	NETWORK=192.168.1.0
	VLAN=yes
	```
