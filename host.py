from emoji import emojize
from Tkinter import *
from chat import *
import thread
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = str(socket.gethostbyname(socket.gethostname()))
PORT = 9003
conn = ''
s.bind((HOST, PORT))

def onClick():
    messageText = messageFilter(textBox.get("0.0",END)) #filter
    displayLocalMessage(chatBox, messageText.decode('unicode-escape')) #display local
    chatBox.yview(END) #auto-scroll
    textBox.delete("0.0",END) #clear the input box
    conn.sendall(messageText.encode('utf-8')) #send over socket
    #conn.sendall(messageText) #send over socket
    
def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()

def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)
	
def onemoji():
    emoji=emojize(" :smiley:", use_aliases=True)
    textBox.insert(END,emoji.encode('unicode-escape'))
    onClick()

def openConnection():
    s.listen(2) #Listen for 1 other person
    global conn
    conn, addr = s.accept()
    getConnectionInfo(chatBox, 'Connected with: ' + str(addr) +'\n-------------------------------------')

    while 1:
        try:
            data=conn.recv(1024)
            if(data[0:4]=='file'):
                print data
                recev(conn)
                break
            else:
                data=conn.recv(1024)
                displayRemoteMessage(chatBox, data.decode('unicode-escape')) #Display on Remote Windows
        except:
            #getConnectionInfo(chatBox, '\n [ Your partner has disconnected ]\n [ Waiting for him to connect..] \n  ')
            openConnection()

    conn.close()
    
def recev(conn):
    i=1
    #sc, address = s.accept()
    while True:
        sz=conn.recv(2)
        print sz
        l=conn.recv(int(sz))
        print l

        f = open(l,'wb') 
        l = 1
        while(l):
            l = conn.recv(1024)
            while (l):
		#if (l is not 'end'):
                    f.write(l)
                    l =conn.recv(1024)
                #else:
		    #break
            f.close()
            #print 'File Received'
            displayRemoteMessage(chatBox, "File Rceived Suucessfully")
        #break
        openConnection()
        

#Base Window
base = Tk()
base.title("Pychat Host")
base.geometry("1000x600+30+30")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#716664")

#Chat

main_body = Frame(base, height=20, width=50)
chatBox = Text(main_body,font="Helvetica",bd=0,bg="#689099")
body_text_scroll = Scrollbar(main_body, command=chatBox.yview, bg = "#34495e")
chatBox.focus_set()
body_text_scroll.pack(side=RIGHT, fill=Y)
chatBox.pack(side=LEFT, fill=Y)
body_text_scroll.config(command=chatBox.yview)
chatBox.config(yscrollcommand=body_text_scroll.set,background='grey')
main_body.pack()
chatBox.insert(END, "Welcome to the chat program! \n")
chatBox.insert(END, "Waiting for your partner to connect..\n")
getConnectionInfo(chatBox, 'Server Listening at: ' + HOST +'\n-------------------------------------')
chatBox.config(state=DISABLED)


#Send Button
sendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onClick)
#Send Emoji
sendEmoji = Button(base, font="Helvetica", text="SEND Emoji", width="50", height=8,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onemoji)


#Text Input
textBox = Text(base, bd=0, bg="#F8B486",width="29", height="5", font="Helvetica")
textBox.bind("<Return>", removeKeyboardFocus)
textBox.bind("<KeyRelease-Return>", onEnterButtonPressed)


sendButton.place(x=790, y=440, height=40, width=100)
sendEmoji.place(x=400, y=490, height=40, width=100)
textBox.place(x=130, y=440, height=40, width=650)

thread.start_new_thread(openConnection,()) # try listening again upon fail
base.mainloop() #Start the GUI Thread
