from tkinter import *
from tkinter.ttk import Combobox
from tkinter.font import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from ctypes import windll
import os
import ncryptLib

root = Tk()
windll.shcore.SetProcessDpiAwareness(1)
root.geometry("900x900")
root.title("Ncrypt v1.0 (Encryptor) - Developed by Anurag Chattopadhyay")

fileName = ""
encrypted = False
keys = []

# ENCRYPTION GUI
def selectFile(*args):
    f1 = askopenfilename(parent=root, title="Select File", filetypes=[("Text files", ".txt")])
    pathName = str(os.path.realpath(f1))
    global fileName
    global keys
    global encrypted
    fileName = pathName
    label1.config(text=f"Selected File: {pathName}")
    if encrypted:
        encrypted = False
        keys = []

def viewFile(*args):
    global fileName
    if fileName.strip():
        viewWin = Toplevel(root)
        viewWin.geometry("800x800")
        viewWin.title(fileName)
        data = ""
        with open(fileName) as f:
            data = f.read()
        vText = Text(viewWin, font="Arial 14")
        vText.insert(1.0, data)
        vText.config(state="disabled")
        vText.pack(expand=True, fill=BOTH)
        vText.focus()
    else:
        statusLabel.config(text="Please Select a File to View!")

def doEncrypt(*args):
    x = keyCount.get().strip()
    if x.isdigit():
        k = int(x)
        if (k < 1) or (k > 20):
            statusLabel.config(text="Invalid input!")
        else:
            global keys
            keys = ncryptLib.Ncrypt.E.encrypt(fileName, k, "mongodb://localhost:27017")
            status = f"SUCCESSFULLY ENCRYPTED!\n"
            for i in range(len(keys)-1):
                status += f"Key-{i+1}: {keys[i]}\n"
            status += f"FINAL KEY: {keys[-1]}\n"
            keyCount.config(state="readonly")
            statusLabel.config(text=status)
    elif x.replace("\n", "").strip() == "":
        statusLabel.config(text="Please Enter Number of Layers of Encryption")

def tryEncrypt(*args):
    global fileName
    global encrypted
    if fileName.strip():
        if not encrypted:
            doEncrypt()
            encrypted = True
        else:
            status = f"File already Encrypted!\n"
            global keys
            for i in range(len(keys)-1):
                status += f"Key-{i+1}: {keys[i]}\n"
            status += f"FINAL KEY: {keys[-1]}\n"
            keyCount.config(state="readonly")
            statusLabel.config(text=status)
    else:
        statusLabel.config(text="Please Select a File to Encrypt!")

frame = Frame(root).focus()

label0 = Label(root, text="ENCRYPTION TOOL", font="Arial 22")
label0.pack(pady=10)


label1 = Label(root, text="Selected File:", font="Arial 16")
label1.pack(pady=10)


selectButton = Button(root, text="Select File", font="Arial 14", command=selectFile)
selectButton.pack(pady=10)

viewButton = Button(root, text="View File Contents", font="Arial 14", default="disabled", command=viewFile)
viewButton.pack()

statusLabel = Label(root, text="", font="Arial 16")
statusLabel.pack(side="bottom", pady=20)

keyLabel = Label(root, text="Enter number of layers of encryption: \n(Within 1 to 20)", font="Arial 16")
keyLabel.pack(pady=10)
keyCount = Entry(root, font="Arial 12", width=2)
keyCount.pack(pady=10)
keyCount.focus()

submitButton = Button(root, text="Submit", font="Arial 14", command=tryEncrypt)
submitButton.pack()

mainloop()