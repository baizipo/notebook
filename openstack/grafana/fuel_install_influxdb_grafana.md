### 使用fuel安装InfluxDB-Grafana监控openstack组件
----

#### 安装InfluxDB-Grafana和Collector插件

   - InfluxDB-Grafana 服务端安装软件
   - Collector 客户端安装软件

 一.官网下载插件，下载完成后拷贝到fuel节点上

  - [influxdb_grafana](http://plugins.mirantis.com/repository/l/m/lma_collector/lma_collector-0.10-0.10.0-1.noarch.rpm)
  - [Collector](http://plugins.mirantis.com/repository/l/m/lma_collector/lma_collector-0.10-0.10.0-1.noarch.rpm)

 二.安装插件(文档使用rpm包方式安装)    

  1. 安装influxdb_grafana插件
     ```
     [root@fuel ~]# fuel plugins --install influxdb_grafana-0.10-0.10.0-1.noarch.rpm
     ``` 

  2. 安装collector插件
     ```
     [root@fuel ~]# fuel plugins --install lma_collector-0.10-0.10.0-1.noarch.rpm
     ```
     
  3. 确认插件是否安装成功，如下表示安装成功
    ```
     [root@fuel ~]# fuel plugins --list
     id | name             | version | package_version | releases                                     
     ---+------------------+---------+-----------------+----------------------------------------------
     1  | influxdb_grafana | 0.10.0  | 4.0.0         | ubuntu (liberty-8.0, liberty-9.0, mitaka-9.0)
     2  | lma_collector      | 0.10.0  | 4.0.0         | ubuntu (liberty-8.0, liberty-9.0, mitaka-9.0) 
    ```

  4. 登陆fuel节点
       在将插件安装完成过后，选择```环境-我的openstack环境-设置-其他配置```可以看到新安装的两个插件的配置信息，选中
       ```The StackLight InfluxDB-Grafana Server Plugin```和```The StackLight Collector Plugin```前面的复选框。
 
  5. 修改编辑配置文件
       基本上保持默认就可以,当然有些选项可以按需修改   
     
      - 详情可参考[influxdb_grafana官方文档](http://plugins.mirantis.com/docs/i/n/influxdb_grafana/influxdb_grafana-0.10-0.10.0-1.pdf)
      - 详情可参考[Collector官方文档](http://plugins.mirantis.com/docs/l/m/lma_collector/lma_collector-0.10-0.10.0-1.pdf)
 
----

#### 遇到问题
  1. 安装后无法获取数据，原因控制器节点和influxdb节点控制网络不通

  2. 控制节点和计算节点的collectd配置文件不同的地方
      配置文件为```/etc/collectd/conf.d/python-config.conf```
      以下为控制节点的配置内容信息

  3. 控制节点里包含各个节点的api链接，如`openstack_cinder，hypervisor_stats，openstack_glance，openstack_keystone，openstack_neutron，openstack_nova`等模块的api地址和密码等

----
#### 排查方法
   
   <font color=red size=3>influxdb_grafana的servier端:</font>

  1. 确认节点可以访问的influxdb的VIP地址,正常显示如下:
   ```
    #curl -I http://VIP:8086/ping

    The server should return a 204 HTTP status:
    HTTP/1.1 204 No Content
    Request-Id: cdc3c545-d19d-11e5-b457-000000000000
    X-Influxdb-Version: 0.10.0
    Date: Fri, 12 Feb 2016 15:32:19 GMT2.
    ```
    
  2. 确认InfluxDB 集群的VIP地址是up状态
    ```
    #crm resource status vip__influxdb

    resource vip__influxdb is running on: node-1.test.domain.local
    ```

  3. 确认服务是正常运行的
   ```
    #service influxdb status 
    #service grafana-server status
    ```
  4. 查看服务日志

    - InfluxDB – /var/log/influxdb/influxdb.log
    - Grafana – /var/log/grafana/grafana.log

---
  <font color=red size=3>collector客户端:</font> 

  1. 在每个节点上确保服务正常运行

    控制节点:
    ```
    #crm resource status metric_collector
    #crm resource status log_collector
    ``` 

    非控制节点:
    ```
    #status log_collector
    #status metric_collector
    ```

  2. 查看系统日志

    - /var/log/log_collector.log
    - /var/log/metric_collector.log.
    - /var/log/collectd.log

  3. 查看所有节点是否可以连接influxdb VIP的8086端口
    ```
    #telnet VIP 8086
    ```
     
