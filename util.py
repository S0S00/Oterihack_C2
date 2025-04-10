import pickle

agentsDB    = "data/databases/agents.db"
listenerDB    = "data/databases/listeners.db"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printBanner():
    print(
    '''
     /$$$$$$    /$$                         /$$ /$$ /$$   /$$                     /$$        /$$$$$$   /$$$$$$ 
    /$$__  $$  | $$                        |__/| $/| $$  | $$                    | $$       /$$__  $$ /$$__  $$
    | $$  \ $$ /$$$$$$    /$$$$$$   /$$$$$$  /$$|_/ | $$  | $$  /$$$$$$   /$$$$$$$| $$   /$$| $$  \__/|__/  \ $$
    | $$  | $$|_  $$_/   /$$__  $$ /$$__  $$| $$    | $$$$$$$$ |____  $$ /$$_____/| $$  /$$/| $$        /$$$$$$/
    | $$  | $$  | $$    | $$$$$$$$| $$  \__/| $$    | $$__  $$  /$$$$$$$| $$      | $$$$$$/ | $$       /$$____/ 
    | $$  | $$  | $$ /$$| $$_____/| $$      | $$    | $$  | $$ /$$__  $$| $$      | $$_  $$ | $$    $$| $$      
    |  $$$$$$/  |  $$$$/|  $$$$$$$| $$      | $$    | $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$/| $$$$$$$$
     \______/    \___/   \_______/|__/      |__/    |__/  |__/ \_______/ \_______/|__/  \__/ \______/ |________/                                                                                                                                                                                              
    ''')


def success(text):
    print(bcolors.OKGREEN + "[+] " + bcolors.ENDC + f"{text}")

def error(text):
    print(bcolors.FAIL + "[-] " + bcolors.ENDC + f"{text}")

def info(text):
    print(bcolors.WARNING + "[i] " + bcolors.ENDC + f"{text}")

def writeToDB(database,data):
    with open(database,"ab") as d:
        pickle.dump(data,d,pickle.HIGHEST_PROTOCOL)

def readFromDB(database):
    data = []
    with open(database,"rb") as d:
        while True:
            try:
                data.append(pickle.load(d))
            except EOFError:
                break
    return data