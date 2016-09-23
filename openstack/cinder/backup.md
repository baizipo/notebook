## 增量备份 & 全量备份

http://blog.csdn.net/wytdahu/article/details/45246095

## 后端配置

### ceph

```
backup_driver = cinder.backup.drivers.ceph

backup_ceph_conf=/etc/ceph/ceph.conf
backup_ceph_user = cinder
backup_ceph_chunk_size = 134217728
backup_ceph_pool = backups
backup_ceph_stripe_unit = 0
backup_ceph_stripe_count = 0
```

### TSM

```
backup_driver = cinder.backup.drivers.tsm

backup_tsm_compression = True     (BoolOpt) 启用或禁用压缩备份
backup_tsm_password = password     (StrOpt)  运行TSM用户的密码（节点密码）
backup_tsm_volume_prefix = backup     (StrOpt) 当备份到TSM时备份标识id的卷前缀
```

### swift

```
backup_driver = cinder.backup.drivers.swift

backup_swift_url = http://localhost:8080/v1/AUTH
backup_swift_auth = per_user
backup_swift_user = <None>
backup_swift_key = <None>
backup_swift_container = volumebackups
backup_swift_object_size = 52428800
backup_swift_retry_attempts = 3
backup_swift_retry_backoff = 2
backup_compression_algorithm = zlib
```

## 备份

### 全备份
1. 备份

	```bash
	cinder backup-create --name all VOLUME-ID
	```

2. 恢复

	```bash
	cinder backup-restore BACKUP-ID   # 未指定VOLUME-ID 将自动新建一块云硬盘
	cinder backup-restore --volume VOLUME-ID BACKUP-ID
	```
	
3. 删除

	```bash
	cinder backup-delete BACKUP-ID
	```

### 增量备份

1. 备份

	```bash
	cinder backup-create --incremental --name first VOLUME-ID
	```
	
2. 恢复：同上

3. 删除

	> 从备份链顶端开始删除，否则报错
	
#### BUG

BUG: https://bugs.launchpad.net/cinder/+bug/1578036

```bash
$ cd /usr/lib/python2.7/distpackages/
$ patch -p1 < rbd_image.patch
```


## 代码分析

```
backup（/cinder/backup/）
  /cinder/backup/__init__.py：指定并导入cinder-backup的API类；
  /cinder/backup/api.py：处理所有与卷备份服务相关的请求；

class API(base.Base):卷备份管理的接口API,主要定义了卷的备份相关的三个操作的API：
    create：实现卷的备份的建立；
    delete：实现删除卷的备份；
    restore：实现恢复备份；
这三个操作都需要通过backup_rpcapi定义的RPC框架类的远程调用来实现；

/cinder/backup/driver.py:所有备份驱动类的基类；

class BackupDriver(base.Base):所有备份驱动类的基类；

/cinder/backup/manager.py：卷备份的管理操作的实现；

class BackupManager(manager.SchedulerDependentManager):块存储设备的备份管理；继承自类 SchedulerDependentManager；
主要实现的是三个远程调用的方法：
   create_backup：实现卷的备份的建立（对应api.py中的creat方法）；
   restore_backup：实现恢复备份（对应api.py中的restore方法）；
   delete_backup：实现删除卷的备份（对应api.py中的delete方法）；

/cinder/backup/drivers/ceph.py：ceph备份服务实现；
   class CephBackupDriver(BackupDriver):Ceph对象存储的Cinder卷备份类；这个类确认备份Cinder卷到Ceph对象存储系统；

/cinder/backup/drivers/swift.py：用swift作为后端的备份服务的实现；
   class SwiftBackupDriver(BackupDriver):用swift作为后端的备份服务的各种管理操作实现类；

/cinder/backup/drivers/tsm.py：IBM Tivoli存储管理（TSM）的备份驱动类；
   class TSMBackupDriver(BackupDriver):实现了针对TSM驱动的卷备份的备份、恢复和删除等操作；
```

