import time
import subprocess
import pty
import os
import pprint
import sys
import select
import fcntl

def receiveData():
    pass

def read_callback(fd):
    data = os.read(fd, 1024) # <-- this doesn't block
    return data 

def _set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

#program = "/home/mango/webhack/nethack-3.6.0/src/nethack"
#pid, master_fd = pty.fork()
#argv=["/home/mango/webhack/nethack-3.6.0/src/nethack"]

#if pid == pty.CHILD:
#    os.execlp(program, *argv)

master, slave = pty.openpty()
#pty.spawn("/bin/sh", read_callback)
#master, slave = pty.spawn("/bin/sh", read_callback)
p = subprocess.Popen("/home/mango/webhack/nethack-3.6.0/src/nethack",
#p = subprocess.Popen("watch ls",
        #stdin=subprocess.PIPE,
        stdin=slave,
        #stdout=slave,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        close_fds=True,)
os.close(slave)
fm = os.fdopen(master, "rw", 1)
_set_nonblocking(master)
#data = os.read(master, 1)
#print(data)
#q = select.poll()
#q.register(slave,select.POLLIN)
#connections = {}; requests = {}; responses = {}
while 1:
#    events=q.poll(1)
    #print(master)
    #data = fm.read(10)
    output = p.stdout.read(100)
    print(output)


    #except (IOError, OSError) as e:
    #    print("error")
    #for fileno, event in events:

    #if pp is None:
    #if not l:
        #data = os.read(master, 512)
        #print(fm.readline)
    """    
    if 1==1:
        pass
        try:
            data = fm.read(10)
        except (IOError, OSError) as e:
            print("error")
            pass 
        os.write(master, "y")
        #print(fm2.read())
        pass
    else:
        data=""
        try:
            data = fm.read(10)
        except (IOError, OSError) as e:
            print("error")
            pass 
        #data = os.read(master, 1)
        print(data)
        sys.stdout.flush()
        pass
    """
# Better: p = subprocess.Popen(["sleep", "30"])

# Wait until process terminates
#while p.poll() is None:
#    time.sleep(0.5)

# It's done
print "Process ended, ret code:", p.returncode

