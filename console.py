import util
import menu
import os

util.printBanner()


if not os.path.exists("./data"):
    util.info("Database not found, should we create it ?")
    ans = input("[Y/n] ?")
    if ans != "n":
        os.mkdir("./data")
        os.mkdir("./data/listeners/")
        os.mkdir("./data/databases/")
        util.success("Done")
    else:
        util.info("Okay but this will most likely fail")

menu.main_menu()
