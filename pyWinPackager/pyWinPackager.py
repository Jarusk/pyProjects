# -*- coding: utf-8 -*-
import traceback, re, os, shutil, sys, Tkinter, ttk, tkFileDialog, time, thread, subprocess, glob

#Draws GUI and defines button actions
def graphical():
        global root, status, inFileEntry, begin, options, oneFileVar, noConsoleVar
        root=Tkinter.Tk()
        root.resizable(width=False, height=False)
        root.title("pythonWinPackager")
        oneFileVar = Tkinter.IntVar()
        noConsoleVar = Tkinter.IntVar()
        status = Tkinter.StringVar()
        setStatus("Awaiting User")
        
        content = ttk.Frame(root, padding=(3,3,3,3))
        inFileEntry = ttk.Entry(content, width=30)
        statusLabel = ttk.Label(content, textvariable=status)

        begin = ttk.Button(content, text="Begin", command=beginB)
        selectInFile = ttk.Button(content, text="Add Input File", command=getInFile)
        oneFileBox = ttk.Checkbutton(content, text="oneFile", variable = oneFileVar, onvalue = 1, offvalue = 0)
        noConsoleBox = ttk.Checkbutton(content, text="noConsole", variable = noConsoleVar, onvalue = 1, offvalue = 0)
        
        content.grid(column=0, row=0, sticky="nsew")
        selectInFile.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)
        inFileEntry.grid(column=1, row=0, sticky="nsew", padx=5, pady=5)
        begin.grid(column=1, row=2, sticky="nsew", padx=5, pady=5)
        statusLabel.grid(column=1, row=1, columnspan=2, sticky="nsw", padx=5)
        oneFileBox.grid(column = 0, row=1, sticky="nsw", padx=5)
        noConsoleBox.grid(column = 0, row=2, sticky="nsw", padx=5)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=3)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(2, weight=1)
        content.rowconfigure(3, weight=1)
        
        print "N.B.  Pyinstaller package (2.1 or greater) must be pre-installed if it isn't already"

        root.mainloop()
        

def threadly(routine):
        thread.start_new_thread(routine, ())

def getInFile():
    global inFile
    inFileEntry.delete(0, 100)
    inFile = tkFileDialog.askopenfilename(title = 'Select Input File')
    inFileEntry.insert(0, inFile)

def beginB():
    threadly(controller)
    
def controller():
    global oneFileVar, noConsoleVar, begin
    baseDir = (os.path.split(inFile))[0]
    outFile = (os.path.split(inFile))[1]
    os.chdir(baseDir)
    
    if oneFileVar.get() == 1:
        temp1 = "--onefile"
    else:
        temp1 = ""
        
    if noConsoleVar.get() == 1:
        temp2 = "--noconsole"
    else:
        temp2 = ""
    
    args = "-y --distpath="+baseDir+" "+temp1+" "+temp2+" "+outFile
    begin['state']='disabled'
    setStatus("The Hamster is Running")
    print args
    subprocess.call("C:\Python27\Scripts\pyinstaller.exe " + args, shell=True)
    shutil.rmtree('build')
    for item in glob.glob('*.spec'):
        os.remove(os.path.join(baseDir, item))
    begin['state']='enabled'
    setStatus("Completed")

def setStatus(text):
    status.set("Status: "+text)
        

#End of GUI definitions
#Start of procedural definitions
    


#End of procedural definitions

#Code will execute below when called
if __name__ =='__main__':
        graphical()
