# Python3_MagicTV-Remote
Python 3 script for my MTV9600D

test.py is a testing script for you to try sending button message to MagicTV device

mytvremote.pyw is the script to be used as remote
- You need to change the IP address being assigned to the variable "ip"
- Not sure if some models do not support acknowledgement, therefore there is a boolean "need_acknowledgement" for changing. Acknowledgement is a response sent back from MagicTV device after receiving a button message.

Developed based on the followings:
https://github.com/netleave/MagicTV-remote-python
https://github.com/mob41/MagicTVRemote-API

Thanks
