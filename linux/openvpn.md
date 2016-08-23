# 建立 openvpn 证书 client 证书
## 链接服务器
略...
## 制作证书

```bash
# sudo -s
# cd /etc/openvpn
# source vars
# ./build-key sunzhiping
## 一路回车,注意以下两项
Sign the certificate?[y/n]: y
1 out of 1 certificate requests certified, commit? [y/n] y
```

## 拷贝证书
ssh client 环境不同，方法也不同

example：

```bash
# scp ca.crt name.* xxx@xxx.xxx.xxx.xxx:/tmp 
```

## windows 客户端
1. 下载 [windows client](http://swupdate.openvpn.org/community/releases/openvpn-2.2.2-install.exe)
2. 安装
3. 拷贝证书文件到`C:/Program Files/OpenVPN/config`下
4. 在`C:/Program Files/OpenVPN/config`目录下新建client配置文件`suninfo.ovpn`,内容如下：

	```
	client
	dev tun
	proto tcp
	remote xxx.xxx.xxx.xxx 1194
	resolv-retry infinite
	nobind
	persist-key
	persist-tun
	ca ca.crt
	cert NAME.crt
	key NAME.key
	comp-lzo
	```
	
5. 双击桌面openvpn图标，然后右键点击右下角openvpn图标，再点connect

