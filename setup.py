#!python
import subprocess
import os
import sys

CONTROLLER_PATH = "./webserver/websocket.py"
WEBSERVER_PATH = "./webserver/mainPage.py"
NETHACK_PATH = "./nethack/"

def start_controller():
    subprocess.run(["python", CONTROLLER_PATH], stdout=subprocess.PIPE)

def start_webserver():
    subprocess.run(["python", WEBSERVER_PATH], stdout=subprocess.PIPE)

def check_nethack_binary():
    pass

def compile_nethack():
    subprocess.run(["make", "install", "-C", NETHACK_PATH], stdout=subprocess.PIPE)
    pass

def delete_save():
    pass

def clean_nethack_binary():
    subprocess.run(["make", "clean", "-C", NETHACK_PATH], stdout=subprocess.PIPE)
    pass

def main(argv):
    commands_list = {
        "start": start,
        "compile": compile_nethack,
        "clean": clean_nethack_binary,
        "run_webserver": start_webserver,
        "run_controller": start_controller,
        "delete_save": delete_save
    }
    if len(sys.argv) == 1:
        print(
'''usage: ./setup.py [Arguments]
Arguments:
    compile: compile Nethack binary
    clean: clean up Nethack path
    run_webserver: run webserver
    run_controller: run game controller
    delete_save: delete save files(Only for dev)''')
        exit(0)
    var = sys.argv[1]
    func = commands_list.get(var)
    func()

if __name__ == "__main__":
    main(sys.argv)
