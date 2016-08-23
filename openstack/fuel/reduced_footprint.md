# reduced footprint
官方文档：https://docs.mirantis.com/openstack/fuel/fuel-8.0/operations.html#using-the-reduced-footprint-feature

## 部署：

1. 安装Fuel
2. 从PXE启动bare metal machine
3. 打开`Advanced`功能：

   3.1 修改配置文件`/etc/fuel/version.yaml`:
   
   ```bash
   VERSION:
     feature_groups:
       - mirantis
       - advanced
   ```
   
   3.2 重启`nailgun`:
   
   ```bash
   dockerctl shell nailgun
   supervisorctl restart nailgun
   ```
   
4. 修改虚拟机模板文件`/etc/puppet/modules/osnailyfacter/templates/vm_libvirt.erb`：  

   ```xml
    <interface type='bridge'>
      <source bridge='br-prv'/>
      <virtualport type='openvswitch'/>
      <model type='virtio'/>
    </interface>
   ```
   
5. 修改控制节点网络：

	```bash
	# 下载节点配置文件
	fuel deployment --download --env 1
	# 修改network_scheme -> transformations
	- action: add-port
	  bridge: br-ex
	  name: eth1
	# 上传修改后的配置文件
	fuel deployment --update --env 1
	```

6. 创建虚拟机
	
	```bash
	fuel2 node create-vms-conf 2 --conf '{"id":1, "mem":8, "cpu":4}'
	```
	
7. 部署虚拟机

	```bash
	fuel2 env spawn-vms 1
	```
	
8. Fuel UI 配置角色，部署openstack
9. 迁移Fuel

	```bash
	fuel-migrate node-2		# virt节点主机名或IP
	```




