from listeners import Listener
from collections import OrderedDict
from util import *
import time
import random

listeners = OrderedDict()

def list_listeners():
    success("Active listeners")
    for i in listeners:
        print(f"\\-- {i} - {listeners[i].host}:{listeners[i].port}")

def generate_id():
        animals = random.choice(open("animals.txt").readlines()).strip()
        adj = random.choice(open("adjectives.txt").readlines()).strip()
        return f"{adj}_{animals}"

def listenerStart(args):
    name = generate_id()
    listeners[name] = Listener(args[0],args[1],name)
    listeners[name].start()
    time.sleep(1)