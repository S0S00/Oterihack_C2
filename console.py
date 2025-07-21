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
        
if not os.path.exists("./C2_download"):
    util.info("Download Folder not found, should we create it ?")
    ans = input("[Y/n] ?")
    if ans != "n":
        os.mkdir("./C2_download")
        util.success("Done")
    else:
        util.info("Okay but this will most likely fail")

if not os.path.exists("./C2_uploads"):
    util.info("Upload Folder not found, should we create it ?")
    ans = input("[Y/n] ?")
    if ans != "n":
        os.mkdir("./C2_uploads")
        util.success("Done")
    else:
        util.info("Okay but this will most likely fail")

menu.main_menu()
