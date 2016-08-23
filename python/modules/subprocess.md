# subprocess
subprocess的目的就是启动一个新的进程并且与之通信。
## subprocess常用方法
### subprocess.call
subprocess.call 返回命令执行的状态码

```python
import subprocess
subprocess.call('ls')		             # 执行ls命令
subprocess.call('ls -l', shell=True)   # args为字符串且命令带参数，必须设置shell=True
subprocess.call(['ls', '-l'])          # args为list，可以不用打开shell=True
```

### subprocess.check_call()
命令执行后，返回值为非零抛出异常`CalledProcessError`

```python
subprocess.check_call('exit 1', shell=True)
```

```bash
Traceback (most recent call last):
  File "/Users/wangtao/PycharmProjects/sub_pro/sub_pro1.py", line 6, in <module>
    print subprocess.check_call('exit 1', shell=True)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 540, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1
```

### subprocess.check_output()
返回命令执行的结果。如果返回码非零，它将引发CalledProcessError。CalledProcessError将返回码保存在returncode属性中并把任何输出都保存在output属性中。

```python
subprocess.check_output('ls')
```

### subprocess.PIPE
可以作为Popen的stdin、stdout 或者stderr参数使用的特殊值，指示应该打开一个管道至标准流。

### subprocess.STDOUT
可以作为Popen的stderr 参数使用的特殊值，指示标准错误应该和标准输出得到相同的处理。

### exception subprocess.CalledProcessError
check_call()或者check_output()运行的进程在返回非零的退出状态时所抛出的异常。

### returncode
子进程的退出状态。

### cmd
用于产生子进程的命令。

### output
子进程的输出，如果异常是由check_output()引发。Otherwise, None.

### Popen对象
class subprocess.Popen(args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0)

```python
subprocess.Popen('ls')
```

#### Popen类的实例具有以下方法：
1. `Popen.poll()`: 检查子进程是否已经终止。设置并返回returncode属性。

	```python
	import subprocess
	pyth = subprocess.Popen(['sleep', '3'])
	print pyth.poll()			# 子进程执行中，返回None
	import time
	time.sleep(4)
	print pyth.poll()			# 子进程执行结束后，返回 returncode 属性。
	```

2. `Popen.wait()`: 等待子进程终止。设置并返回returncode属性。

	```python
	pyth = subprocess.Popen(['sleep', '3'])
	print pyth.wait()			# 等待进程执行结束
	print 'Done'
	```
3. `Popen.communicate(input=None)`: 与进程交互：将数据发送到标准输出。从标准输出和标准错误读取数据，直至到达文件末尾。等待进程终止。可选的input 参数应该是一个要发送给子进程的字符串，如果没有数据要发送给子进程则应该为None。communicate()返回一个元组(stdoutdata, stderrdata)。

	```python
	import subprocess
	pyth = subprocess.Popen(['python'],
	                        stdin=subprocess.PIPE,
	                        stdout=subprocess.PIPE,
	                        stderr=subprocess.PIPE)
	pyth.stdin.write('print "Hello world."')
	stdout_stderr = pyth.communicate()
	print stdout_stderr
	```

4. `Popen.send_signal(signal)`: 发送信号signal 给子进程。
5. `Popen.terminate()`: 终止子进程。在Posix操作系统上，该方法发送SIGTERM给子进程。在Windows上，调用Win32 API 函数TerminateProcess()来终止子进程。
6. `Popen.kill()`: 杀死子进程。在Posix操作系统上，该函数发送SIGKILL给子进程。在Windows上，kill()是terminate()的别名。
7. `Popen.stdin`: 如果stdin 参数为PIPE，则该属性为一个文件对象，它提供子进程的输入。否则，为None。
8. `Popen.stdout`: 如果stdout 参数为PIPE，则该属性是一个文件对象，它提供子进程中的输出。否则，为None。
9. `Popen.stderr`: 如果stderr 参数为PIPE，则该属性是一个文件对象，它提供子进程中的错误输出。否则，为None。

	```python
	p1 = subprocess.Popen('echo test',
                         shell=True,
                         stdout=subprocess.PIPE,)

	p2 = subprocess.Popen(['grep','test'],
                         stdin=p1.stdout,
                         stdout=subprocess.PIPE)

	print p2.stdout.read()
	```
	
10. `Popen.pid`: 子进程的进程ID。注意如果你设置shell 参数为True，那么它是产生的shell的进程ID。
11. `Popen.returncode`: 子进程的返回码，由poll() 和wait()设置（communicate()是间接设置）。None值表示子进程还没有终止。一个负的值-N表示子进程被信号N终止（只在Unix上）。


## 异常
在子进程中引发的异常，在新程序开始执行之前将在父进程中被重新引发。另外，该异常对象将包含一个额外的属性叫做child_traceback，它是一个包含子进程回溯信息的字符串。

1. `OSError`: 执行不存在的命令抛出此异常

2. `ValueError`: 如果Popen 的调用带有非法的参数将引发ValueError 。

3. `CalledProcessError`: 如果调用的进程返回非零的返回码，check_call() 和check_output() 将引发CalledProcessError异常。



