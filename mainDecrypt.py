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
root.title("Ncrypt v1.0 (Decryptor) - Developed by Anurag Chattopadhyay")

fileName = ""
keyList = []
n = 0

# DECRYPTION GUI
def selectFile(*args):
    f1 = askopenfilename(parent=root, title="Select File", filetypes=[("Text files", ".txt")])
    pathName = str(os.path.realpath(f1))
    global fileName
    fileName = pathName
    label1.config(text=f"Selected File: {pathName}")

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

def doDecrypt(*args):
    global n
    try:
        x = keysText.get("1.0", END).strip(" ").strip("\n").split("\n")
        x = [int(i) for i in x]
        if len(x) != n:
            statusLabel.config(text=f"DECRYPTION FAILED! {n} keys expected, {len(keyList)} keys found...")
        else:
            valid = True
            for i in x:
                if not ncryptLib.Ncrypt.D.keyValid(i):
                    statusLabel.config(text="DECRYPTION FAILED! Invalid keys detected...")
                    valid = False
                    break
            if valid:
                keyList.extend(x)
                ncryptLib.Ncrypt.D.decrypt(fileName, n, keyList, "mongodb://localhost:27017")
                statusLabel.config(text="SUCCESSFULLY DECRYPTED!")
    except:
        statusLabel.config(text="DECRYPTION FAILED! Try again...")

def reqKeys(*args):
    global keyList
    global n
    if ncryptLib.Ncrypt.D.keyValid(int(fkey.get())):
        keyList.append(int(fkey.get()))
        n = int(keyCount.get())
        keyCount.config(state="readonly")
        fkey.config(state="readonly")
        submitButton.pack_forget()
        
        keysTextLabel.pack(pady=10)
        keysText.config(height=n)
        keysText.pack(pady=10)
        keysSubmit.pack(pady=10)
        
        statusLabel.config(text="FINAL KEY IS VALID")
        

frame = Frame(root).focus()

label0 = Label(root, text="DECRYPTION TOOL", font="Arial 22")
label0.pack(pady=10)

label1 = Label(root, text="Selected File:", font="Arial 16")
label1.pack(pady=10)


selectButton = Button(root, text="Select File", font="Arial 14", command=selectFile)
selectButton.pack(pady=10)

viewButton = Button(root, text="View File Contents", font="Arial 14", default="disabled", command=viewFile)
viewButton.pack(pady=10)

statusLabel = Label(root, text="", font="Arial 16")
statusLabel.pack(side="bottom", pady=20)

keyLabel = Label(root, text="Enter number of layers of encryption: \n(Within 1 to 20)", font="Arial 16")
keyLabel.pack(pady=10)
keyCount = Entry(root, font="Arial 12", width=2)
keyCount.pack(pady=10)

fKeyLabel = Label(root, text="Enter FINAL KEY:", font="Arial 16")
fKeyLabel.pack(pady=10)
fkey = Entry(root, font="Arial 12", width=9)
fkey.pack(pady=10)

submitButton = Button(root, text="Submit", font="Arial 14", command=reqKeys)
submitButton.pack(pady=10)

keysTextLabel = Label(root, text="Enter all keys in reverse order", font="Arial 16")
keysText = Text(root, font="Arial 16", height=10, width=9)
keysSubmit = Button(root, text="Submit keys", command=doDecrypt, font="Arial 14")

mainloop()