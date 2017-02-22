import time
import subprocess
import select
import pty
import os
import sys
import socket


ip = '0.0.0.0'
port = 8080
size = 1024
 
# 소켓생성
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 바인드
server.bind((ip, port))
# 리슨, 여기까지는 기본적인 서버 소켓 세팅
server.listen(1)
# select 함수에서 관찰될 소켓 리스트 설정
input_list = [server]


master, slave = pty.openpty()

process = subprocess.Popen('/home/mango/webhack/nethack-3.6.0/src/nethack', 
#process = subprocess.Popen('python3 dummy.py', 
            #stdin=master,#subprocess.PIPE, 
            stdin=slave,
            stdout=slave,
            stderr=slave,
            shell=True,
            close_fds=True)

process.stdin=os.fdopen(master, 'wb')
process.stdout=os.fdopen(master, 'rb')
flag=1
pin = os.fdopen(master,'w')
#check packet from server
while 1:
    input_ready, write_ready, except_ready = select.select(input_list, [], [],0.1)



    rlist, wlist, xlist = select.select([master], [], [],0.1)

    if rlist != []:
        for f in rlist:
            output = os.read(f, 1024) # This is used because it doesn't block
            print(bytes(output))
            #sys.stdout.write(str(output))
            sys.stdout.flush()



    for ir in input_ready:
        if ir == sys.stdin:
            pass
        elif ir == server:
            client, address = server.accept()
            print(address, 'is connected', flush=True)
            input_list.append(client)
        else:
            data = ir.recv(size)
            if data:
                print(ir.getpeername(), 'send :', data, flush=True)
                data_str = str(data, 'UTF-8')
                print(data_str)
                input = os.write(master, bytes(data_str, 'UTF-8'))
                #input = os.write(master, bytes('y\n', 'UTF-8'))
                #pin.write(str(data))

                #while process.poll() is None:
                rlist, wlist, xlist = select.select([master], [], [],0.1)
                print(rlist, wlist, xlist)

                for f in rlist:
                    output = os.read(f, 1024) # This is used because it doesn't block
                    print(bytes(output))
                    #sys.stdout.write(str(output))
                    sys.stdout.flush()
                print("**ALL COMPLETED**")
                ir.send(data)
            else:
                print(ir.getpeername(), 'close', flush=True)
                ir.close()
                input_list.remove(ir)

"""
#process.stdin=os.fdopen(master, 'wb')
#process.stdout=os.fdopen(master, 'rb')


print(process.poll())
while process.poll() is None:
    input = os.write(slave, bytes('y', 'UTF-8'))
    rlist, wlist, xlist = select.select([master], [], [])

    for f in rlist:
        input = os.write(master, bytes('y\n', 'UTF-8'))
        output = os.read(f, 1000) # This is used because it doesn't block
        print(output)
        #sys.stdout.write(str(output))
        sys.stdout.flush()
        #if flag==1:
            #flag=0
        time.sleep(5)
    print("**ALL COMPLETED**")
"""
