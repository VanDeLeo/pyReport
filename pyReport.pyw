# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

from customtkinter import *
from Modules.ui import App
import msvcrt
import sys

LOCKFILE = "tmp/pyreport.locks"

#This function verify if the process already running with a special file that block if the case is true
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
    root.iconbitmap("Images/icon.ico")
    set_appearance_mode("light")
    Window = App(root)
    root.mainloop()

    #Unlock the file when the process ends
    msvcrt.locking(lockfile.fileno(), msvcrt.LK_UNLCK,1)
    lockfile.close()
    os.remove(LOCKFILE)

if __name__ == "__main__":
    main()


#            *
#           *
#          *
#         ****
#           *
#          *
#         *     
  
