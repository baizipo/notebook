# iptables
## 数据包流
### 以本地为目标的包
步骤 | 表 | 链 | 备注
--- | --- | --- | ---
1 |||	在线路上传输(比如，Internet)
2 |||进入接口 (比如， eth0)
3 |mangle|PREROUTING|这个链用来mangle数据包，比如改变TOS、TTL、MARK
4 |nat|PREROUTING|这个链主要用来做DNAT。不要在这个链做过虑操作，因为某 些情况下包会溜过去。
5 |||路由判断，比如，包是发往本地的，还是要转发的。
6 |mangle|input|在路由之后，被送往本地程序之前，mangle数据包。
7 |filter|INPUT|所有以本地为目的的包都要经过这个链，不管它们从哪儿 来，对这些包的过滤条件就设在这里。
8 |||到达本地程序了(比如，服务程序或客户程序)

## 规则是如何练出来的
规则就是决定如何处理一个包的语句。如果一个包符合所有 的条件（就是符合matche语句），我们就运行target或jump指令。书写规则的语法格式是：
`iptables [-t table] command [match] [target/jump]`


`table`: iptables默认使用filter表来执行所有的命令,可使用`-t table`指定表名。
`command`: 告诉程序该做什么，比如：插入一个规则，还是在链的末尾增加一个规则，还是删除一个规则.
`match`: 细致地描述了包的某个特点，以使这个包区别于其它所有的包。在这里，我们可以指定包的来源IP 地址，网络接口，端口，协议类型，或者其他什么。
`target`: 最后是数据包的目标所在。若数据包符合所有的match，内核就用target来处理它，或者说把包发往 target。

### tables

### commands
command指定iptables 对我们提交的规则要做什么样的操作。这些操作可能是在某个表里增加或删除一些东西，或做点儿其他什么.

Command|example|Explanation
--- | --- | ---
-A --append |iptables -A INPUT |所选的链末加规则
-D --delete |iptables -D INPUT --dport 80 -j DROP 或 iptables -D INPUT 1| 从所选链中删除规则。两种方法：1. 完整规则 2. 使用规则编号
-R --replace | iptables -R INPUT 1 -s 192.168.0.1 -j DROP | 替换指定链的规则
-I --insert | iptables -I INPUT 1 --dport 80 -j ACCEPT | 指定规则之上插入规则
-L --list | iptables -L INPUT| 显示所选链的所有规则。如果没有指定链，则显示指定表中的所有链
-F --flush | iptables -F INPUT | 清空所选的链，如果没有指定链，则清空指定表中的所有链
-Z --zero | iptables -F INPUT | 把指定链(如未指定，则认为是所有链)的所有计数器归零。
-N --new-chain | iptables -N allowed | 根据用户指定的名字建立新的链。注意：所有的名字不能和已有的链、target同名
-X --delete-chain | iptables -X allowed | 删除指定的用户自定义链。
-P --policy | iptables -P INPUT DROP | 为链设置默认的target（可用的是DROP 和ACCEPT，如果还有其它的可用，请告诉我），这个target称作策略。所有不 符合规则的包都被强制使用这个策略。只有内建的链才可以使用规则。但内建的链和用户自定义链都不能被 作为策略使用，也就是说不能象这样使用：iptables -P INPUT allowed（或者是内建的链）。
-E --rename-chain| 	iptables -E allowed disallowed| 对自定义的链进行重命名，原来的名字在前，新名字在后。 如上，就是把allowed改为disallowed。这仅仅是改变 链的名字，对整个表的结构、工作没有任何影响。




## nat
### snat
系统在路由及过虑等处理直到数据包要被送出时才进行SNAT

```
-j SNAT --to IP[-IP][:端口-端口]（nat 表的 POSTROUTING链）

iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j SNAT --to 1.1.1.1
将内网 192.168.0.0/24 的原地址修改为 1.1.1.1，用于 NAT

iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -j SNAT --to 1.1.1.1-1.1.1.10
同上，只不过修改成一个地址池里的 IP
```

### MASQUERADE

```
用于外网口public地址是DHCP动态获取的（如ADSL）
iptables -t nat -A POSTROUTING –o eth1 –s 192.168.1.0/24 –j MASQUERADE
iptables -t nat -A POSTROUTING -o ppp0 -j MASQUERADE

多个内网段SNAT,就是多条SNAT语句即可
iptables -t nat -A POSTROUTING -s 192.168.100.0/24 -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 192.168.0.0/24 -o eth0 -j MASQUERADE
```

### dnat

```
-j DNAT --to IP[-IP][:端口-端口]（nat 表的 PREROUTING 链）
 目的地址转换，DNAT 支持转换为单 IP，也支持转换到 IP 地址池（一组连续的 IP 地址）
例如：
iptables -t nat -A PREROUTING -i ppp0 -p tcp --dport 80 -j DNAT --to 192.168.0.1
把从 ppp0 进来的要访问 TCP/80 的数据包目的地址改为 192.168.0.1

iptables -t nat -A PREROUTING -i ppp0 -p tcp --dport 81 -j DNAT --to 192.168.0.2:80
iptables -t nat -A PREROUTING -i ppp0 -p tcp --dport 80 -j DNAT --to 192.168.0.1-192.168.0.10
```


