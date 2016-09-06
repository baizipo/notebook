## 组件

### wheel

#### rest_cherrypy keys

 参考链接: https://docs.saltstack.com/en/latest/ref/netapi/all/salt.netapi.rest_cherrypy.html#keys

#### local api
参考链接: https://docs.saltstack.com/en/latest/ref/wheel/all/salt.wheel.key.html#module-salt.wheel.key

#### command

```bash
saltutil.wheel:

    Execute a wheel module and function. This function must be run against a
    minion that is local to the master.

    New in version 2014.7.0

    name
        The name of the function to run

    args
        Any positional arguments to pass to the wheel function. A common example
        of this would be the ``match`` arg needed for key functions.

        New in version v2015.8.11

    kwargs
        Any keyword arguments to pass to the wheel function

    CLI Example:

        salt my-local-minion saltutil.wheel key.accept jerry
        salt my-local-minion saltutil.wheel minions.connected

    Note:

        Since this function must be run against a minion that is running locally
        on the master in order to get accurate returns, if this function is run
        against minions that are not local to the master, "empty" returns are
        expected. The remote minion does not have access to wheel functions and
        their return data.
```

### async
saltstack 支持异步执行的功能，发出命令后返回JID.

1. 命令行

	```bash
	$ salt node-1 --async cmd.run 'sleep 1000'    # --async 发布异步命令
	$ salt-run jobs.lookup_jid $JID               # 查看结果
	```
	
2. api

	```bash
	result = {'client':'local_async', 'fun':'cmd.run', 'tgt':'node-1', 'arg1':'sleep 1000'}
	```



