from tkinter import *
import os
from threading import Thread as thread
from time import sleep
import subprocess
import shutil

window = Tk()
window.geometry("930x600")
window.resizable(False, False)
window.title("Files++")
window.iconbitmap("icon.ico")

cdir = "C:\\" # cdir is for "Current Directory"

pathbox = Entry(window)
pathbox.insert(0,cdir)
pathbox.place(y=3,x=3,height=26,width=840)

frame = LabelFrame(window, text="Folder")
frame.place(y=35,x=3, width=700, height=540)

toolboxframe = LabelFrame(window,text="Toolbox")
toolboxframe.place(y=35,x=710,width=218,height=160)

itemlist = Listbox(window,activestyle="none")

itemstats = Label(window,fg="blue")
itemstats.place(x=3,y=575)

previewframe = LabelFrame(window,text="Text preview")
previewframe.place(y=195,x=710,width=218,height=380)

filepreview = Text(window, state="disabled")
filepreview.place(y=215,x=715,width=207,height=352)

def shred(file):
    f = open(file, "w")
    for _ in range(100):
        f.write("0000000000000000")
    f.close()
    os.remove(file)
    browse()

def deltarget(target):
    if os.path.isdir(target):
        try:
            os.rmdir(target)
        except:
            shutil.rmtree(target)
    else:
        os.remove(target)
    browse()

# Toolbox Buttons

rmdirbtn = Button(window, text="Delete directory/file", command=lambda:deltarget(cdir))
destroyfile = Button(window,text="Overwrite & Destroy file", command=lambda:shred(cdir))
editfile = Button(window,text="Edit file with Notepad", command=lambda:subprocess.run("notepad.exe "+cdir))
runfile = Button(window,text="Run file (exe only)",command=lambda:subprocess.Popen(cdir))
runfile.place(y=158,x=716, height=30, width=205)
editfile.place(y=124,x=716, height=30, width=205)
destroyfile.place(y=90,x=716, height=30, width=205)
rmdirbtn.place(y=56,x=716, height=30, width=205)

def goback():
    global pathbox
    global cdir
    print("cd into "+cdir)
    if cdir == os.getcwd():
        os.chdir("..")
        cdir = os.getcwd()
    else:
        os.chdir(cdir)
        cdir = os.getcwd()
    pathbox.delete(0,END)
    pathbox.insert(0,cdir)
    browse()

def itemselected(event):
    global selecteditem
    filepreview.delete("1.0",END)
    selecteditem = itemlist.get(itemlist.curselection()[0])
    print(selecteditem)
    global cdir
    cdir = pathbox.get()+selecteditem
    print(cdir)
    print(cdir[-4:])
    if selecteditem == "..":
        itemstats["text"] = "Go back"
    elif os.path.isfile(cdir):
        itemstats["text"] = "\""+selecteditem+"\" - Type: File, Size: "+str(os.stat(cdir).st_size)+" Bytes, Location: "+pathbox.get()
        if os.stat(cdir).st_size < 1048576:
            filepreview["state"] = "normal"
            filepreview.delete("1.0",END)
            f = open(cdir, "r")
            filepreview.insert(END,f.read())
            f.close()
            filepreview["state"] = "normal"
    elif os.path.isdir(cdir):
        itemstats["text"] = "\""+selecteditem+"\" - Type: Folder"

def browseitem(event):
    global selecteditem
    global cdir
    if selecteditem == "..":
        goback()
    elif os.path.isdir(cdir):
        cdir = cdir + "\\"
        pathbox.delete(0,END)
        pathbox.insert(0,cdir)
        browse()
    else:
        print(cdir)
        subprocess.run(cdir)

itemlist.place(y=60,x=12, width=680, height=500)
itemlist.bind('<<ListboxSelect>>', itemselected)
itemlist.bind("<Double-Button>",browseitem)

def browse():
    pathboxold = pathbox.get()
    pathbox.delete(0,END)
    pathbox.insert(0,pathboxold.replace("\\\\","\\"))
    if os.path.isfile(pathbox.get()):
        frame["text"] = "File "+pathbox.get()
    elif os.path.isdir(pathbox.get()):
        os.chdir(pathbox.get())
        global dircontent
        dircontent = []
        frame["text"] = "Folder "+pathbox.get()
        i = 1
        itemlist.delete(0,END)
        itemlist.insert(1,"..")
        for file in os.listdir(pathbox.get()):
            if file != "System Volume Information":
                i += 1
                dircontent.append(file)
                itemlist.insert(i, file)
        if len(dircontent) < 1:
            itemstats["text"] = "Empty directory"
        else:
            itemstats["text"] = "Directory ("+str(len(dircontent))+" items)"

testbtn = Button(window, height=1, text="Enter", width=10, command=browse)
testbtn.place(y=3,x=846)

Button(window,text="Refresh",command=browse).place(x=874,y=577,height=20)

browse()

window.mainloop()