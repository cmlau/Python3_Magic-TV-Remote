import socket
import sys
import time
import codecs
decode_hex = codecs.getdecoder("hex_codec")

ip = "192.168.20.243"


def messagecode(hex):
    # return  decode_hex('5500004000080004000400d82a'+hex+'aa')[0]
    return  decode_hex('5500004040080004000400d82a'+hex+'aa')[0]


REPLY_OK = '55000080400600011002000400aa'

GET_INFO = decode_hex('5500004040040001000000aa')[0]

BUTTON_POWER = '11ee'
BUTTON_MENU = '0ff0'
BUTTON_GUIDE = '32cd'
BUTTON_ASPECT = '34cb'
BUTTON_AUDIO = '4eb1'
BUTTON_SUBTITLE = '4fb0'
BUTTON_BACK = '35ca'
BUTTON_UP = '0af5'
BUTTON_DOWN = '0bf4'
BUTTON_LEFT = '0cf3'
BUTTON_RIGHT = '0df2'
BUTTON_INFO = '36c9'
BUTTON_OK = '0ef1'
BUTTON_VOLUP = '14eb'
BUTTON_VOLDOWN = '15ea'
BUTTON_MUTE = '18e7'
BUTTON_CHUP = '16e9'
BUTTON_CHDOWN = '17e8'
BUTTON_REC = '24db'
BUTTON_PAUSE = '22dd'
BUTTON_STOP = '23dc'
BUTTON_PLAY = '21de'
BUTTON_REVERSE = '25da'
BUTTON_FORWARD = '26d9'
BUTTON_REPLAY = '27d8'
BUTTON_SKIP = '28d7'
BUTTON_LIVESRC = '37c8'
BUTTON_1 = '619e' # number 1
BUTTON_2 = '629d' # number 2
BUTTON_3 = '639c' # number 3
BUTTON_4 = '649b' # number 4
BUTTON_5 = '659a' # number 5
BUTTON_6 = '6699' # number 6
BUTTON_7 = '6798' # number 7
BUTTON_8 = '6897' # number 8
BUTTON_9 = '6996' # number 9
BUTTON_0 = '609f' # number 0
BUTTON_CLEAR = '38c7'
BUTTON_ENTER = '39c6'
BUTTON_RED = '48b7'
BUTTON_GREEN = '4bb4'
BUTTON_YELLOW = '4cb3'
BUTTON_BLUE = '4db2'

def verifybuttoncode():
    for k, v in list(globals().items()):
        if k[0:6] == "BUTTON":
            print(k, "OK" if int(v[0:2],16) + int(v[2:4],16) == 255 else "ERROR")
      

def getinfo():
    model = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)
    server_address = (ip, 23456)
    try:
        print("Contacting " + ip)
        sent = sock.sendto(GET_INFO, server_address)
        reply = sock.recv(128)
        notstarted = True
        for b in reply:
            if notstarted:
                if b != 90:
                    continue
                else:
                    notstarted = False
                    continue
            if (model == "" and b == 0):
                continue
            if (b == 0):
                break
            model += chr(b)
        return model
    except TimeoutError:
        return "MTV Not Found"
    finally:
        sock.close()

def sendmessage(button):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)
    server_address = (ip, 23456)
    try:
        message = messagecode(eval(button))
        print("Sending " + button)
        sent = sock.sendto(message, server_address)
        reply = sock.recv(128)
        if (reply.hex() == REPLY_OK):
            return button + " : received"
        else:
            return button + " : unknown"
    except TimeoutError:
        return button + " : no response"
        pass
    finally:
        sock.close()

print(getinfo())
print(sendmessage('BUTTON_STOP'))
