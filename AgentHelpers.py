from collections import OrderedDict
from util import *
import time
import random

agents = OrderedDict()

def update_agents():
    global agents

    agentsinDB = readFromDB(agentsDB)
    agents = OrderedDict()
    for agent in agentsinDB:
        agents[agent.name] = agent

def list_agents():
    update_agents()
    success("Active Agents")
    for i in agents:
        print(f"\\-- {agents[i].name} | {agents[i].remoteip} | {agents[i].hostname}")

def interact_agents(args):
    update_agents()
    if len(args) != 1:
        error("Wrong arguments")
    else:
        name = args[0]
        agents[name].interact()

def clearAgentTasks(name):
    update_agents()
    agents[name].clearTasks()
def clearAgentdownload(name):
    update_agents()
    agents[name].clearDownload()
def clearAgentSecret(name):
    update_agents()
    agents[name].clearSecret()
def clearAgentUpload(name):
    update_agents()
    agents[name].clearUpload()


def displayResults(name,result):
    update_agents()
    if result == "":
        success("Agent {} | Host {} | User completed his task.".format(name, agents[name].hostname))
    else:
        success("Agent {} | Host {} | User returned results : ".format(name, agents[name].hostname))
        print(result)
def displayDownload(name,result):
    update_agents()
    if result == "":
        success("Agent {} | Host {} | User completed his download.".format(name, agents[name].hostname))
    else:
        success("Agent {} | Host {} | User saved this : ".format(name, agents[name].hostname))
        print(result)