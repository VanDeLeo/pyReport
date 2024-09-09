from customtkinter import *
from Modules.ui import App

def main():
    root = CTk()
    root.title("pyReport")
    root.geometry("500x300")
    root.resizable(False,False)
    set_appearance_mode("light")
    Window = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    