import socket
import sys
import time
import codecs
import tkinter
import tkinter.simpledialog
decode_hex = codecs.getdecoder("hex_codec")

### Change the followings: ###
ip = "192.168.20.243"
need_acknowledgement = True
######

model = ""
MTV_PORT = 23456

def messagecode(hex):
    if need_acknowledgement:
        return  decode_hex('5500004040080004000400d82a'+hex+'aa')[0]
    else:
        return  decode_hex('5500004000080004000400d82a'+hex+'aa')[0]


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
BUTTON_1 = '619e'
BUTTON_2 = '629d'
BUTTON_3 = '639c'
BUTTON_4 = '649b'
BUTTON_5 = '659a'
BUTTON_6 = '6699'
BUTTON_7 = '6798'
BUTTON_8 = '6897'
BUTTON_9 = '6996'
BUTTON_0 = '609f'
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
      

def connect():
    global model,ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)
    server_address = (ip, MTV_PORT)
    try:
        #print("Contacting " + ip + "...")
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
        lbl_model
        lbl_model.configure(text=model, fg='#0000ff')
        lbl_status.configure(text = "MTV connected", fg='#0000ff')
        enable_buttons()
    except TimeoutError:
        lbl_model.configure(text="MTV Not Found", fg='#ff0000')
        lbl_status.configure(text = "MTV connection failed", fg='#ff0000')
        disable_buttons()
    finally:
        sock.close()

def enable_buttons():
    for child in frame_buttons.winfo_children():
        wtype = child.winfo_class()
        if (wtype in ('Button')):
            child.configure(state='normal')
    for child in frame_cbuttons.winfo_children():
        wtype = child.winfo_class()
        if (wtype in ('Button')):
            child.configure(state='normal')

def disable_buttons():
    for child in frame_buttons.winfo_children():
        wtype = child.winfo_class()
        if (wtype in ('Button')):
            child.configure(state='disabled')
    for child in frame_cbuttons.winfo_children():
        wtype = child.winfo_class()
        if (wtype in ('Button')):
            child.configure(state='disabled')

def btn_pressed(button_name):
    global ip
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5.0)
    server_address = (ip, MTV_PORT)
    try:
        message = messagecode(eval(button_name))
        #print("Sending " + button_name + "...")
        sent = sock.sendto(message, server_address)
        if need_acknowledgement:
            reply = sock.recv(128)
            #print("Replay received : " + reply.hex())
            if (reply.hex() == REPLY_OK):
                lbl_status.configure(text = button_name + " : acknowledged", fg='#0000ff')
            else:
                lbl_status.configure(text = button_name + " : unknown reponse", fg='#ff0000')
        else:
            lbl_status.configure(text = button_name + " : sent", fg='#0000ff')            
    except TimeoutError:
        lbel_status.configure(text = button_name + " : no reponse", fg='#ff0000')
    finally:
        sock.close()

root = tkinter.Tk()
root.option_add("*Font", "courier 12")
root.configure(bg="#696969")
root.title("MTV Remote")

frame_device=tkinter.Frame(root)
frame_device.configure(bg="#696969")
frame_device.pack(side="top",fill="x", padx=6, pady=10)
lbl_model = tkinter.Label(frame_device, text="", font=("Arial", 25), fg='#0000ff', anchor="center", bg="#696969")
lbl_model.grid(row=1, column=1, padx = 10, sticky="w")

frame_buttons=tkinter.Frame(root)
frame_buttons.configure(bg="#696969")
frame_buttons.pack(side="top", fill="x", padx=6, pady=5)

frame_cbuttons=tkinter.Frame(root)
frame_cbuttons.configure(bg="#696969")
frame_cbuttons.pack(side="top", fill="x", padx=6, pady=5)

frame_statusbar=tkinter.Frame(root)
frame_statusbar.configure(bg="#696969")
frame_statusbar.pack(side="top", fill="x", padx=6, pady=2)
lbl_status = tkinter.Label(frame_statusbar, text="initializing ...", anchor="e", font="Arial 10", bg="#696969")
lbl_status.grid(row=1, column=1, padx = 10, sticky="e")

btn_power = tkinter.Button(frame_buttons, text="Power", width="10", command= lambda: btn_pressed('BUTTON_POWER'), state="disabled")
btn_power.grid(row=1, column=3, padx=2, sticky="w")

frame_buttons.grid_rowconfigure(2, minsize=10)

btn_guide = tkinter.Button(frame_buttons, text="Guide", width="10", command= lambda: btn_pressed('BUTTON_GUIDE'), state="disabled", bg='#ffffff')
btn_guide.grid(row=3, column=1, padx=2, sticky="w")
btn_menu = tkinter.Button(frame_buttons, text="Menu", width="10", command= lambda: btn_pressed('BUTTON_MENU'), state="disabled", bg='#ffffff')
btn_menu.grid(row=3, column=2, padx=2, sticky="w")
btn_text = tkinter.Button(frame_buttons, text="Text", width="10", command= lambda: btn_pressed('BUTTON_TEXT'), state="disabled", bg='#ffffff')
btn_text.grid(row=3, column=3, padx=2, sticky="w")
btn_aspect = tkinter.Button(frame_buttons, text="Aspect", width="10", command= lambda: btn_pressed('BUTTON_ASPECT'), state="disabled", bg='#ffffff')
btn_aspect.grid(row=4, column=1, padx=2, sticky="w")
btn_audio = tkinter.Button(frame_buttons, text="Audio", width="10", command= lambda: btn_pressed('BUTTON_AUDIO'), state="disabled", bg='#ffffff')
btn_audio.grid(row=4, column=2, padx=2, sticky="w")
btn_subtitle = tkinter.Button(frame_buttons, text="Subtitle", width="10", command= lambda: btn_pressed('BUTTON_SUBTITLE'), state="disabled", bg='#ffffff')
btn_subtitle.grid(row=4, column=3, padx=2, sticky="w")
btn_back = tkinter.Button(frame_buttons, text="🔙", width="10", command= lambda: btn_pressed('BUTTON_BACK'), state="disabled", bg='#000000', fg='#ffffff')
btn_back.grid(row=5, column=1, padx=2, sticky="w")
btn_info = tkinter.Button(frame_buttons, text="ⓘ", width="10", command= lambda: btn_pressed('BUTTON_INFO'), state="disabled", bg='#000000', fg='#ffffff')
btn_info.grid(row=5, column=3, padx=2, sticky="w")

frame_buttons.grid_rowconfigure(6, minsize=10)

btn_up = tkinter.Button(frame_buttons, text="↑", width="10", command= lambda: btn_pressed('BUTTON_UP'), state="disabled", bg='#006400', fg='#ffffff')
btn_up.grid(row=7, column=2, padx=2, sticky="w")
btn_left = tkinter.Button(frame_buttons, text="←", width="10", command= lambda: btn_pressed('BUTTON_LEFT'), state="disabled", bg='#006400', fg='#ffffff')
btn_left.grid(row=8, column=1, padx=2, sticky="w")
btn_ok = tkinter.Button(frame_buttons, text="OK", width="10", command= lambda: btn_pressed('BUTTON_OK'), state="disabled", bg='#006400', fg='#ffffff')
btn_ok.grid(row=8, column=2, padx=2, sticky="w")
btn_right = tkinter.Button(frame_buttons, text="→", width="10", command= lambda: btn_pressed('BUTTON_RIGHT'), state="disabled", bg='#006400', fg='#ffffff')
btn_right.grid(row=8, column=3, padx=2, sticky="w")
btn_down = tkinter.Button(frame_buttons, text="↓", width="10", command= lambda: btn_pressed('BUTTON_DOWN'), state="disabled", bg='#006400', fg='#ffffff')
btn_down.grid(row=9, column=2, padx=2, sticky="w")

frame_buttons.grid_rowconfigure(10, minsize=10)

btn_volup = tkinter.Button(frame_buttons, text="Vol ↑", width="10", command= lambda: btn_pressed('BUTTON_VOLUP'), state="disabled", bg='#ffffff')
btn_volup.grid(row=11, column=1, padx=2, sticky="w")
btn_mute = tkinter.Button(frame_buttons, text="Mute 🔇", width="10", command= lambda: btn_pressed('BUTTON_MUTE'), state="disabled", bg='#ffffff')
btn_mute.grid(row=11, column=2, padx=2, sticky="w")
btn_chup = tkinter.Button(frame_buttons, text="Ch/Pg ↑", width="10", command= lambda: btn_pressed('BUTTON_VOLDOWN'), state="disabled", bg='#ffffff')
btn_chup.grid(row=11, column=3, padx=2, sticky="w")
btn_voldown = tkinter.Button(frame_buttons, text="Vol ↓", width="10", command= lambda: btn_pressed('BUTTON_VOLDOWN'), state="disabled", bg='#ffffff')
btn_voldown.grid(row=12, column=1, padx=2, sticky="w")
btn_chdown = tkinter.Button(frame_buttons, text="Ch/Pg ↓", width="10", command= lambda: btn_pressed('BUTTON_CHDOWN'), state="disabled", bg='#ffffff')
btn_chdown.grid(row=12, column=3, padx=2, sticky="w")

frame_buttons.grid_rowconfigure(13, minsize=10)

btn_record = tkinter.Button(frame_buttons, text="⏺", width="10", command= lambda: btn_pressed('BUTTON_RECORD'), state="disabled", bg='#ff0000', fg='#ffffff')
btn_record.grid(row=14, column=1, padx=2, sticky="w")
btn_pause = tkinter.Button(frame_buttons, text="⏸", width="10", command= lambda: btn_pressed('BUTTON_PAUSE'), state="disabled", bg='#ffff00')
btn_pause.grid(row=14, column=2, padx=2, sticky="w")
btn_stop = tkinter.Button(frame_buttons, text="⏹", width="10", command= lambda: btn_pressed('BUTTON_STOP'), state="disabled", bg='#000000', fg='#ffffff')
btn_stop.grid(row=14, column=3, padx=2, sticky="w")
btn_reverse = tkinter.Button(frame_buttons, text="⏪", width="10", command= lambda: btn_pressed('BUTTON_REVERSE'), state="disabled", bg='#000000', fg='#ffffff')
btn_reverse.grid(row=15, column=1, padx=2, sticky="w")
btn_play = tkinter.Button(frame_buttons, text="▶", width="10", command= lambda: btn_pressed('BUTTON_PLAY'), state="disabled", bg='#ffff00')
btn_play.grid(row=15, column=2, padx=2, sticky="w")
btn_forward = tkinter.Button(frame_buttons, text="⏩", width="10", command= lambda: btn_pressed('BUTTON_FORWARD'), state="disabled", bg='#000000', fg='#ffffff')
btn_forward.grid(row=15, column=3, padx=2, sticky="w")
btn_replay = tkinter.Button(frame_buttons, text="⏮", width="10", command= lambda: btn_pressed('BUTTON_REPLAY'), state="disabled", bg='#000000', fg='#ffffff')
btn_replay.grid(row=16, column=1, padx=2, sticky="w")
btn_livesrc = tkinter.Button(frame_buttons, text="Live Src", width="10", command= lambda: btn_pressed('BUTTON_LIVESRC'), state="disabled", bg='#ffffff', fg='#000000')
btn_livesrc.grid(row=16, column=2, padx=2, sticky="w")
btn_skip = tkinter.Button(frame_buttons, text="⏭", width="10", command= lambda: btn_pressed('BUTTON_SKIP'), state="disabled", bg='#000000', fg='#ffffff')
btn_skip.grid(row=16, column=3, padx=2, sticky="w")

frame_buttons.grid_rowconfigure(17, minsize=10)

btn_1 = tkinter.Button(frame_buttons, text="1", width="10", command= lambda: btn_pressed('BUTTON_1'), state="disabled", bg='#ffffff', fg='#000000')
btn_1.grid(row=18, column=1, padx=2)
btn_2 = tkinter.Button(frame_buttons, text="2", width="10", command= lambda: btn_pressed('BUTTON_2'), state="disabled", bg='#ffffff', fg='#000000')
btn_2.grid(row=18, column=2, padx=2)
btn_3 = tkinter.Button(frame_buttons, text="3", width="10", command= lambda: btn_pressed('BUTTON_3'), state="disabled", bg='#ffffff', fg='#000000')
btn_3.grid(row=18, column=3, padx=2)
btn_4 = tkinter.Button(frame_buttons, text="4", width="10", command= lambda: btn_pressed('BUTTON_4'), state="disabled", bg='#ffffff', fg='#000000')
btn_4.grid(row=19, column=1, padx=2)
btn_5 = tkinter.Button(frame_buttons, text="5", width="10", command= lambda: btn_pressed('BUTTON_5'), state="disabled", bg='#ffffff', fg='#000000')
btn_5.grid(row=19, column=2, padx=2)
btn_6 = tkinter.Button(frame_buttons, text="6", width="10", command= lambda: btn_pressed('BUTTON_6'), state="disabled", bg='#ffffff', fg='#000000')
btn_6.grid(row=19, column=3, padx=2)
btn_7 = tkinter.Button(frame_buttons, text="7", width="10", command= lambda: btn_pressed('BUTTON_7'), state="disabled", bg='#ffffff', fg='#000000')
btn_7.grid(row=20, column=1, padx=2)
btn_8 = tkinter.Button(frame_buttons, text="8", width="10", command= lambda: btn_pressed('BUTTON_8'), state="disabled", bg='#ffffff', fg='#000000')
btn_8.grid(row=20, column=2, padx=2)
btn_9 = tkinter.Button(frame_buttons, text="9", width="10", command= lambda: btn_pressed('BUTTON_9'), state="disabled", bg='#ffffff', fg='#000000')
btn_9.grid(row=20, column=3, padx=2)
btn_clear = tkinter.Button(frame_buttons, text="✖", width="10", command= lambda: btn_pressed('BUTTON_CLEAR'), state="disabled", bg='#000000', fg='#ffffff')
btn_clear.grid(row=21, column=1, padx=2)
btn_0 = tkinter.Button(frame_buttons, text="0", width="10", command= lambda: btn_pressed('BUTTON_0'), state="disabled", bg='#ffffff', fg='#000000')
btn_0.grid(row=21, column=2, padx=2)
btn_enter = tkinter.Button(frame_buttons, text="✔", width="10", command= lambda: btn_pressed('BUTTON_ENTER'), state="disabled", bg='#000000', fg='#ffffff')
btn_enter.grid(row=21, column=3, padx=2)

btn_red = tkinter.Button(frame_cbuttons, text="", width="5", command= lambda: btn_pressed('BUTTON_RED'), state="disabled", bg='#ff0000')
btn_red.grid(row=1, column=1, padx=2)
spacer1 = tkinter.Label(frame_cbuttons, text="", width="2", bg="#696969")
spacer1.grid(row=1, column=2)
btn_green = tkinter.Button(frame_cbuttons, text="", width="5", command= lambda: btn_pressed('BUTTON_GREEN'), state="disabled", bg='#006400')
btn_green.grid(row=1, column=3, padx=2)
spacer2 = tkinter.Label(frame_cbuttons, text="", width="2", bg="#696969")
spacer2.grid(row=1, column=4)
btn_yellow = tkinter.Button(frame_cbuttons, text="", width="5", command= lambda: btn_pressed('BUTTON_YELLOW'), state="disabled", bg='#ffff00')
btn_yellow.grid(row=1, column=5, padx=2)
spacer3 = tkinter.Label(frame_cbuttons, text="", width="2", bg="#696969")
spacer3.grid(row=1, column=6)
btn_blue = tkinter.Button(frame_cbuttons, text="", width="5", command= lambda: btn_pressed('BUTTON_BLUE'), state="disabled", bg='#0000ff')
btn_blue.grid(row=1, column=7, padx=2)

connect()

root.mainloop()














