#### 下载grafana安装包
[下载链接](http://grafana.org/download/)，找到对应的版本，我们这里使用的是Grafana v3.0.4 这里下载的为deb包

#### 安装grafana包
已经grafana和必要的依赖关系包打好tar包，目录在本地电脑/home/deploy/grafana_install.tar.gz文件
```
tar zxvf grafana_install.tar.gz
dpkg -i install xxx.deb

```

#### 修改配置文件
详细可参考以下[文档](http://my.oschina.net/guol/blog/515126)
```
$vim /etc/grafana/grafana.ini

[analytics]
reporting_enabled = false　　　　　　　　＃是否发送分析信息到stats.grafana.org

[auth.ldap]
config_file = /etc/grafana/ldap.toml
enabled = false                   　　　#是否启用ldap


#[database]
#host = 192.168.112.2:3306       　　#指定存储数据库
#name = grafana
#password = password
#type = mysql　　　　　　　　　　　　　　＃类型，可以是mysql、postgres、sqlite3，默认是sqlite3
#user = grafana

[security] 
admin_user = grafana                 #默认的admin用户，默认是admin 
admin_password = grafana             #admin的默认密码，默认是admin 
login_remember_days = 5              #多少天内保持登录状态 
secret_key：                         #保持登录状态的签名 
disable_gravatar：                   #


[server]
http_addr：监听的ip地址，默认是0.0.0.0 
http_port：监听的端口，默认是3000 
protocol：http或者https，，默认是http 
domain：这个设置是root_url的一部分，当你通过浏览器访问grafana时的公开的domian名称，默认是localhost 
enforce_domain：如果主机的header不匹配domian，则跳转到一个正确的domain上，默认是false 
root_url：这是一个web上访问grafana的全路径url，默认是%(protocol)s://%(domain)s:%(http_port)s/ 
router_logging：是否记录web请求日志，默认是false
cert_file：如果使用https则需要设置 
cert_key：如果使用https则需要设置



[log] 
mode：可以是console、file，默认是console、file，也可以设置多个，用逗号隔开
buffer_len：channel的buffer长度，默认是10000 
level：可以是"Trace", "Debug", "Info", "Warn", "Error", "Critical"，默认是info
 
[log.console] 
level：设置级别 

[log.file] 
level：设置级别 
log_rotate：是否开启自动轮转 
max_lines：单个日志文件的最大行数，默认是1000000 
max_lines_shift：单个日志文件的最大大小，默认是28，表示256MB 
daily_rotate：每天是否进行日志轮转，默认是true 
max_days：日志过期时间，默认是7,7天后删除
```

##### 配置实例:
```
[analytics]
reporting_enabled = false

[auth.ldap]
config_file = /etc/grafana/ldap.toml
enabled = false

#[database]
#host = 192.168.112.2:3306
#name = grafana
#password = password
#type = mysql
#user = grafana

[security]
admin_password = password
admin_user = lma

[server]
domain = 192.168.112.4
http_address =
http_port = 8000

```

#### grafana配置数据源
１. 安装完grafa后登陆页面配置grafana,页面默认用户名和密码均为admin
>  访问方式 http://granafa配置ip:端口       配置端口为8000

２. 添加数据源
> 左上角选择data source,然后添加信息，如果一个源数据的话需要选择默认，否则会有问题

３. 导入已有template模板，在导入之前需要修改模板里面对应的设备信息
>  如替换主机名字`node-3.domain.tld`和数据库查询字段里的对应的host `dev1`为实际的信息
node-3.domain.tld为控制节点的主机名,dev1为计算节点里的一台主机名

４.　设置登陆用户后默认访问的界面
> 左上角选择用户，然后选择Preference选项,选择home dashaboard为要显示的界面，update即可,

#### 附录
influxdb 　　
> 访问方式 http://ip:8083







