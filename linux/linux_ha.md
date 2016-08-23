## pacemaker

### debug

1. 常用debug命令

	```bash
	pcs resource show vip__public                    # 查看指定资源信息信息
	pcs resource debug-start vip__public             # debug 启动资源
	pcs resource debug-start --full vip__public      # 特详细debug
	pcs resource vip__public other_networks=undef    # 更改资源属性
	```

2. osf文件路径

	```bash
	/usr/lib/ocf/resource.d/
	```


