# lbaas v2

http://docs.openstack.org/draft/networking-guide/config-lbaas.html

## 安装

```bash
apt-get -y install neutron-lbaasv2-agent
```

## 配置文件

1. /etc/neutron/lbaas_agent.ini

	```bash
	[DEFAULT]	interface_driver = neutron.agent.linux.interface.OVSInterfaceDriver	debug = true	verbose = true	[haproxy]	user_group = haproxy
	```

2. /etc/neutron/neutron.conf

	> ###### 注意: [existing service plugins]

	```bash
	service_plugins = [existing service plugins],neutron_lbaas.services.loadbalancer.plugin.LoadBalancerPluginv2
	[service_providers]
	service_provider = LOADBALANCERV2:Haproxy:neutron_lbaas.drivers.haproxy.plugin_driver.HaproxyOnHostPluginDriver:default
	```
	
## 数据库

```bash
neutron-db-manage --subproject neutron-lbaas upgrade head
```
	
## 服务

1. 重启所有节点neutron-server
2. 当前节点neutron-lbaasv2-agent
	
	


