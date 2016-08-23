# 制作bootstrap镜像
## 制作bootstrap镜像
1. 修改配置文件

	```bash
	/etc/fuel-bootstrap-cli/fuel_bootstrap_cli.yaml
	```
	
2. 制作镜像

	```bash
	fuel-bootstrap build
	```
	
3. 导入镜像

	```bash
	fuel-bootstrap import /tmp/{uuid}.tar.gz
	```
	
4. 激活镜像

	```bash
	fuel-bootstrap activate {uuid}
	```


