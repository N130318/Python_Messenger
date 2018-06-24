# -*- coding: utf-8 -*-
from emoji import emojize
from Tkinter import *
from chat import *
import thread
import os
import tkMessageBox
from tkFileDialog import askopenfilename
from tkSimpleDialog import *
import socket

HOST = raw_input("Enter Server IP Address: ")
PORT = 9003
filename=''
extension=''
name=''
filesize=''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	
def onClick():
    messageText = messageFilter(textBox.get("0.0",END)) #filter
    s.send(messageText.encode('utf-8')) #send over socket
    s.send(messageText) #send over socket
    displayLocalMessage(chatBox, messageText.decode('unicode-escape')) #display local
    chatBox.yview(END) #auto-scroll
    textBox.delete("0.0",END) #clear the input box

def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()
    
def onemoji():
    emoji=emojize(" :smiley:", use_aliases=True)
    textBox.insert(END,emoji.encode('unicode-escape'))
    onClick()
    
def getfile():
	global filename
	global extension
	global name
	#global filesize
	filename = askopenfilename()
	(shortname, extension) = os.path.splitext(filename)
	name = os.path.basename(filename)
	filesize = str(os.path.getsize(filename))
	print name
	print extension
	print(filename)
	#print filesize
	w2.config(text=filename)
	
def sendfile():
	global s
	if(tkMessageBox.askyesno("Are you Sure!","Do you want to send "+name) == True):
		s.send('file')
		s.send(str(len(name)))
		s.send(name)
		#s.send(str(len(filesize)))
		#s.send(filesize)
		with open(filename, "rb") as f:
			l = f.read(1024)
			while(l):
				if(s.send(l)):
					#s.send(l)
					l = f.read(1024)
		f.close()
		s.shutdown(socket.SHUT_WR)
		s.close()
		displayRemoteMessage(chatBox, "File Send Suucessfully")
		ReceiveData()
	else:
		print "file transfer cancelled"
		
def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)

def ReceiveData():
	global HOST
	global PORT
	try:
		s.connect((HOST, PORT))
		getConnectionInfo(chatBox, '[ Connected! ]\n-------------------------------------')
	except:
		getConnectionInfo(chatBox, '[ Cannot connect ]')
		return
	while 1:
		try:
			data = s.recv(1024)
		except:
			getConnectionInfo(chatBox, '\n [ Your partner left.] \n')
			break	
		if data != '':
			displayRemoteMessage(chatBox, data.decode('unicode-escape'))
		else:
			getConnectionInfo(chatBox, '\n [ Your partner left. ] \n')
			break
	s.close()
#Base Window
base = Tk()

base.title("Pychat Client")
base.geometry("1000x600+30+30")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#716664")

#Chat
main_body = Frame(base, height=20, width=50)
chatBox = Text(main_body,font="Helvetica",bd=0)
body_text_scroll = Scrollbar(main_body, command=chatBox.yview, bg = "#34495e")
chatBox.focus_set()
body_text_scroll.pack(side=RIGHT, fill=Y)
chatBox.pack(side=LEFT, fill=Y)
body_text_scroll.config(command=chatBox.yview)
chatBox.config(yscrollcommand=body_text_scroll.set,background='grey')
main_body.pack()
chatBox.insert(END, "Welcome to the chat program! \n")
chatBox.insert(END, "Waiting for your partner to connect..\n")
chatBox.config(state=DISABLED)

#Send Button
sendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onClick)

sendEmoji = Button(base, font="Helvetica", text="Send Emoji", width="50", height=5,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onemoji)
                    
#File Share
button = Button(base, text="Choose File", fg="black", command=getfile,width="10", height=5,bd=0, bg="#BDE096",
 activebackground="#BDE096", justify="center",font="Helvetica")
button.pack()
w = Label(text="File Path:")
w.pack()
w2 = Label(text="No File Selected")
w2.pack(side=RIGHT)
button2 = Button(base, text="Send File", fg="black", command=sendfile)
button2.pack()

#Text Input
textBox = Text(base, bd=0, bg="#F8B486",width="29", height="5", font="Helvetica")
textBox.bind("<Return>", removeKeyboardFocus)
textBox.bind("<KeyRelease-Return>", onEnterButtonPressed)

sendButton.place(x=790, y=440, height=40, width=100)
sendEmoji.place(x=300, y=490, height=40, width=100)
textBox.place(x=130, y=440, height=40, width=650)

w.place(x=10, y=540)
w2.place(x=600, y=540)
button.place(x=410, y=490, height=40, width=100)
button2.place(x=520, y=490, height=40, width=100)
#textBox.place(x=15, y=360, height=80, width=250)
thread.start_new_thread(ReceiveData,())
base.mainloop()
