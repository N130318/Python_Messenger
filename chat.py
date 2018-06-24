from Tkinter import *
from socket import *

def messageFilter(messageText):
    """
    Filter out all useless white lines at the end of a string,
    returns a new, beautifully filtered string.
    """
    EndFiltered = ''
    for i in range(len(messageText)-1,-1,-1):
        if messageText[i]!='\n':
            EndFiltered = messageText[0:i+1]
            break
    for i in range(0,len(EndFiltered), 1):
            if EndFiltered[i] != "\n":
                    return EndFiltered[i:]+'\n'
    return ''

def displayLocalMessage(chatBox, messageText):
	#if there is no text, do nothing
    if messageText != '':
        chatBox.config(state=NORMAL)
        if chatBox.index('end') != None:
			#adds line of text to the end
            LineNumber = float(chatBox.index('end'))-1.0
			#adds text to chatBox
            chatBox.insert(END, "YOU: " + messageText)
			#tkinter functions to customize aesthetics
            chatBox.tag_add("YOU", LineNumber, LineNumber+0.4)
            chatBox.tag_config("YOU", foreground="#AA3939", font=("Courier", 12, "bold"), justify = "right")
            chatBox.config(state=DISABLED)
            chatBox.yview(END)

def displayRemoteMessage(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=NORMAL)
        if chatBox.index('end') != None:
            try:
                LineNumber = float(chatBox.index('end'))-1.0
            except:
                pass
            chatBox.insert(END, "OTHER: " + messageText)
            chatBox.tag_add("OTHER", LineNumber, LineNumber+0.6)
            chatBox.tag_config("OTHER", foreground="#255E69", font=("Courier", 12, "bold"))
            chatBox.config(state=DISABLED)
            chatBox.yview(END)

def getConnectionInfo(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=NORMAL)
        if chatBox.index('end') != None:
            chatBox.insert(END, messageText+'\n')
            chatBox.config(state=DISABLED)
            chatBox.yview(END)
