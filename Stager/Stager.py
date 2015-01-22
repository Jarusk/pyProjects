# -*- coding: utf-8 -*-
import traceback, re, os, shutil, sys, Tkinter, ttk, tkFileDialog, ScrolledText, time, thread

#Draws GUI and defines button actions
def graphical():
        global root, inputList, progress, status, progVar, outDir, inDir, fileQueue, begin, cancel, selectInFile, selectInFolder, selectOut
        root=Tkinter.Tk()
        root.resizable(width=False, height=False)
        root.title("Scanned Submission Stager")
        fileQueue=[]
        status = Tkinter.StringVar()
        setStatus("Awaiting User")
        
        content = ttk.Frame(root, padding=(3,3,3,3))
        inputList=ScrolledText.ScrolledText(content, borderwidth=5, width =50, height=5)
        outDir = ttk.Entry(content)
        queueLbl = ttk.Label(content, text="Files / Directories in Queue")
        statusLabel = ttk.Label(content, textvariable=status)
        progVar=0
        progress=ttk.Progressbar(content, mode = "determinate", maximum = 100)

        begin = ttk.Button(content, text="Begin", command=beginB)
        cancel=ttk.Button(content, text="Close", command=closeB)
        selectInFile = ttk.Button(content, text="Add Input File(s)", command=getInFile)
        selectInFolder = ttk.Button(content, text="Add Input Folder", command=getInFolder)
        selectOut = ttk.Button(content, text="Select Save Location", command=getOutFolder)

        content.grid(column=0, row=0, sticky="nsew")
        inputList.grid(column=0, row=2, rowspan=3, sticky="nsew", padx=5, pady=5)
        queueLbl.grid(column=0, row=1, sticky="sew", padx=5)
        selectInFile.grid(column=2, row=1, sticky="nsew", padx=5, pady=5)
        selectInFolder.grid(column=1, row=1, sticky="nsew", padx=5, pady=5)
        outDir.grid(column=0, row=0, sticky="nsew", padx=5, pady=5)
        selectOut.grid(column=1, row=0,  columnspan=2,sticky="nsew", padx=5, pady=5)
        begin.grid(column=1, row=4, padx=5)

        cancel.grid(column=2, row=4, padx=5)
        statusLabel.grid(column=1, row=2, columnspan=2, sticky="sw")
        progress.grid(column=1, row=3, columnspan=2, padx=5, pady=5, sticky="new")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=3)
        content.columnconfigure(2, weight=3)
        content.rowconfigure(1, weight=1)

        root.mainloop()
        
def closeB():
        global root
        root.destroy()
        sys.exit()
        return 0

def threadly(routine):
        thread.start_new_thread(routine, ())

def lister():
        global fileQueue
        for root, dirname, filenames in os.walk(tempFolder):
                for item in filenames:
                        fileQueue.append(os.path.join(root,item))

def getOutFolder():
        global outputFolder
        outDir.delete(0,100)
        outDir.insert(0,tkFileDialog.askdirectory(title = 'Select Output Directory'))
        outputFolder = outDir.get()
        
def getInFolder():
        global tempFolder
        tempFolder = tkFileDialog.askdirectory(title = 'Add Input Folder(S)')
        threadly(lister)
        textIn(tempFolder)
        
def getInFile():
        global tempFiles
        tempFiles = root.tk.splitlist(tkFileDialog.askopenfilenames(title = 'Add Input File(s)'))
        for item in tempFiles:
            fileQueue.append(item)
            item = re.sub(".*/","",item)
            textIn(item)

def beginB():
    threadly(controller)
    
def controller():
        global progress, progVar, fileQueue, begin, cancel, selectInFile, selectInFolder, selectOut, homeDir
        begin['state']='disabled'
        selectInFile['state']='disabled'
        selectInFolder['state']='disabled'
        selectOut['state']='disabled'
        cancel['text']='Cancel'
        queueSize = float(len(fileQueue))
        
        #Set default step size incase of zero division error
        if queueSize != 0:
            stepSize = float(100.0/queueSize)
        else:
            stepSize = 100
        
        homeDir = os.getcwd()
        setStatus("The Hamster is Running")
        print queueSize, stepSize
        
        for item in fileQueue:
            print item
            builder(item, outputFolder)
            progVar += stepSize
            progress.configure(value = progVar)
            
        setStatus("Completed")
        progress.configure(value = 0)
        progVar=0
        fileQueue=[]
        inputList.delete(0.0, 500.0)
        begin['state']='enabled'
        selectInFile['state']='enabled'
        selectInFolder['state']='enabled'
        selectOut['state']='enabled'
        cancel['text']='Close'
        os.chdir(homeDir)

def textIn(text):
        global inputList
        inputList.insert(Tkinter.INSERT,str(text)+'\n')

def setStatus(text):
        status.set("Status: "+text)
        

#End of GUI definitions

#Start of procedural definitions
    
def file_copy(path_name, file):
        file = re.sub(r'OF15-59',r'HC6-70',file)
        shutil.copy2(path_name, file)

def builder(path_name, outputFolder):
    try:
        file = os.path.split(path_name)[1]
        sub = pull_sub(file)
        skeleton(sub, outputFolder)
        file = re.sub(r'OF15-59',r'HC6-70',file)
        if not os.path.exists(file):
                file_copy(path_name, file) 
    except:
            traceback.print_exc()
            print("Error: "+path_name)
            print('\n')
            pass

def pull_sub(filename): #Pull submission number from file name
    global log, path_name, name_array
    name_array  = re.findall(r"[\w']+", filename)
    try:
        if len(name_array[4]) == 6:
            sub = name_array[4]
            return sub
        else:
            print("Error: Could not pull sub: "+path_name)
            print('\n')
    except:
        print("Error: Could not pull sub: "+path_name)
        print('\n')
        pass

def skeleton(sub, out_dir):
    global name_array
    path = str(out_dir+'/'+'Scanned Subs for Upload'+'/'+sub[:3]+'000-'+sub[:3]+'999')
    if not os.path.exists(path):
        os.makedirs(path)
    os.chdir(path)
    path = sub[:4]+'00-'+sub[:4]+'99'
    if not os.path.exists(path):
            os.mkdir(path)
    os.chdir(path)
    #Makes main submission directory
    if not os.path.exists(sub[:6]):
            os.mkdir(sub)
    os.chdir(sub)
    #Makes subfolder that is named again by submission/file number
    if not os.path.exists(sub[:6]):
            os.mkdir(sub)
    #Handles the creation of subfolder structure ammendments with correct nomenclature
    if len(name_array[5]) == 6:
        sub = name_array[4]+" - "+name_array[5]
    if not os.path.exists(sub):
        os.mkdir(sub)
    os.chdir(sub)

#End of procedural definitions

#Code will execute below when called
if __name__ =='__main__':
        graphical()
