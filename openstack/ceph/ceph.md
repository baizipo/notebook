## ceph常用命令

```bash
$ ceph osd pool get volumes size      # 查看数据存储多少份
$ ceph osd pool set volumes size 3    # 设置集群保存数据份数
$ ceph osd lspools            
$ ceph osd tree #列出osd        
$ ceph osd pool delete rbd rbd --yes-i-really-really-mean-it  # 删除pool
$ ceph osd pool create volumes 1024 1024  replicated #创建pool
$ ceph osd perf   #查看osd整体性能
$ ceph osd set nobackfill
$ ceph osd unset nobackfill

$ ceph auth list

$ ceph pg dump | grep peering | less  #导出pg信息,主要看unf 和 state_stamp

$ ceph health detail   
```

## rbd 常用命令

```bash
$ rbd create --size 1 volumes/image1  创建卷
$ rbd ls volumes  查看pool中所有卷
$ rbd -p compute info xxxxxxxxxxxxxxx 查看compute池中的xxxxx卷详细信息
$ rbd -p compute ls -l   # 查看详细信息
```

## 查看存储空间

1. 查看磁盘逻辑大小:

	```bash
	$ rbd info -p volumes -i volume-1 | grep size
	```
	
2. 查看磁盘实际占用空间大小:

	```bash
	$ rbd diff -p volumes -i volume-1 2>/dev/null|awk '{SUM += $2} END {print SUM/1024/1024" MB"}'
	```
	
3. 查看快照增量空间:

	```bash
	$ rbd -p volumes -i volume-1 snap ls
	$ rbd -p volumes -i volume-1 --snap 2xxxx.snap --from-snap 1xxxx.snap 2>/dev/null|awk '{SUM += $2} END {print SUM/1024/1024" MB"}'
	```


