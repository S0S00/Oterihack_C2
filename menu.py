from collections import OrderedDict
import sys
from util import *
from ListenerHelpers import *
from AgentHelpers import *

import readline

class AutoComplete(object):
    
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:

            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]        
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


class Menu:
    def __init__(self,name):
        self.name = name
        self.commands = OrderedDict()
        self.Commands = []
        self.commands["help"] = ["Show help.", ""]
        self.commands["home"] = ["Return home.", ""]
        self.commands["exit"] = ["Exit C2.", ""]
        

    def parse(self):
        
        readline.set_completer(AutoComplete(self.commands).complete)
        readline.parse_and_bind('tab: complete')

        cmd = input(self.name + "> ")

        cmd = cmd.split()
        
        command = cmd[0]
        args = []

        for i in range(1,len(cmd)):
            args.append(cmd[i])
        
        return command, args
    def registerCommand(self, command, description, args):

        self.commands[command] = [description, args]
    
    def showHelp(self):

        success("Available command : ")
        for i in self.commands:
            print(f"{i} - {self.commands[i][0]} - {self.commands[i][1]}")

def evHome(command, args):

    if command == "help":
        MainMenu.showHelp()
    elif command == "home":
        main_menu()
    elif command == "listeners":
        listenersHelper()
    elif command == "agents":
        agentsHelper()
    elif command == "payloads":
        payloadsHelper()
    elif command == "exit":
        Exit()

def evListener(command, args):

    if command == "help":
        ListenerMenu.showHelp()
    elif command == "home":
        main_menu()
    elif command == "start":
        if len(args) != 2:
            error("Invalid usage")
        else:
            listenerStart(args)
    elif command == "list":
        list_listeners()
    elif command == "exit":
        Exit()

def evAgent(command, args):

    if command == "help":
        AgentMenu.showHelp()
    elif command == "home":
        main_menu()
    elif command == "list":
        list_agents()
    elif command == "interact":
        interact_agents(args)
    elif command == "exit":
        Exit()

def main_menu():
    while True:
        try:
            command, args = MainMenu.parse()
        except:
            continue
        if command in MainMenu.commands:
            evHome(command,args)

def main_back():
    while True:
        try:
            command, args = AgentMenu.parse()
        except:
            continue
        if command in AgentMenu.commands:
            evAgent(command,args)

def listenersHelper():
    while True:
        try:
            command, args = ListenerMenu.parse()
        except:
            continue
        if command in ListenerMenu.commands:
            evListener(command,args)

def agentsHelper():
    while True:
        try:
            command, args = AgentMenu.parse()
        except:
            continue
        if command in AgentMenu.commands:
            evAgent(command,args)

def Exit():
    sys.exit()

MainMenu = Menu("Main")
MainMenu.registerCommand("listeners", "Manage listeners.", "")
MainMenu.registerCommand("agents", "Manage agents.", "")

ListenerMenu = Menu("Listener")
ListenerMenu.registerCommand("start", "Start a listener.", "<name> <port>")
ListenerMenu.registerCommand("list", "list running listeners", "")
AgentMenu = Menu("Agents")
AgentMenu.registerCommand("interact","Interact with an agent","<agent_name>")
AgentMenu.registerCommand("list","list agents","")
