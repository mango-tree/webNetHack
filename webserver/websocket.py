import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import subprocess
import select
import pty
import os
import sys
import socket
import colorama

def read_game_data(socketHandler, message):
    data_str = message#str(message, 'UTF-8')
    print(data_str)
    input = os.write(master, bytes(data_str, 'UTF-8'))

    rlist=[1]
    while rlist != []:
        rlist, wlist, xlist = select.select([master], [], [],0.1)
        print(rlist, wlist, xlist)
        for f in rlist:
            output = os.read(f, 1024) # This is used because it doesn't block
            string = bytes(output)
            print(string)
            socketHandler.write_message(string)
            sys.stdout.flush()
    print("**ALL COMPLETED**")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print( 'new connection')
      
    def on_message(self, message):
        print( 'message received:  %s' % message)
        # Reverse Message and send it back
        #print( 'sending back message: %s' % message[::-1])
        #self.write_message(message[::-1])
        if message:
            read_game_data(self, message)
 
    def on_close(self):
        print( 'connection closed')
 
    def check_origin(self, origin):
        return True

    def on_pong(self, data):
        print("qwq")
 
application = tornado.web.Application([
    (r'/', WSHandler),
])
 
 
if __name__ == "__main__":
    master, slave = pty.openpty()


    process = subprocess.Popen('../nethack/src/nethack', 
#process = subprocess.Popen('python3 dummy.py', 
                #stdin=master,#subprocess.PIPE, 
                stdin=slave,
                stdout=slave,
                stderr=slave,
                shell=True,
                close_fds=True,
                cwd=os.path.dirname(os.path.realpath(__file__)))

    process.stdin=os.fdopen(master, 'wb')
    process.stdout=os.fdopen(master, 'rb')
    pin = os.fdopen(master,'w')

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8000)
    myIP = socket.gethostbyname(socket.gethostname())
    print( '*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
