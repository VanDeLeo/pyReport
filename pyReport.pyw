from customtkinter import *
from Modules.ui import App
import msvcrt
import sys

LOCKFILE = "tmp/pyreport.lock"

def is_app_running(app_name="pyReport"):
    global lockfile

    lockfile = open(LOCKFILE, "w")

    try:
        msvcrt.locking(lockfile.fileno(), msvcrt.LK_NBLCK,1)
        return False
    except IOError:
        return True

def main():
    if is_app_running():
        sys.exit(0)

    root = CTk()
    root.title("pyReport")
    root.geometry("500x300")
    root.resizable(False,False)
    set_appearance_mode("light")
    Window = App(root)
    root.mainloop()

    msvcrt.locking(lockfile.fileno(), msvcrt.LK_UNLCK,1)
    lockfile.close()
    os.remove(LOCKFILE)

if __name__ == "__main__":
    main()
    