# k8s
## 常用命令
1. 列出集群中的节点

	```bash
	$ kubectl get nodes
	NAME             STATUS    AGE
	192.168.30.231   Ready     3d
	192.168.30.232   Ready     3d
	192.168.30.233   Ready     3d
	```


```
export nodes="root@192.168.220.101 root@192.168.220.102 root@192.168.220.103"
export role="ai i i"
export NUM_NODES=${NUM_NODES:-3}
export SERVICE_CLUSTER_IP_RANGE=10.10.3.0/24
```


