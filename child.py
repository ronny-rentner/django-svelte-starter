import os,time,setproctitle
setproctitle.setproctitle('demo-child')
print('child pid', os.getpid())
time.sleep(30)

