from tkinter import *

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):  # Agregamos 'event=None' para evitar el error
        # Crear la ventana para el tooltip
        if self.tip_window or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 25
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Crear el texto del tooltip
        label = Label(tw, text=self.text, justify='left', background="#AAAAAA", relief='solid', borderwidth=1, font=("tahoma", 10, "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):  # También agregamos 'event=None' aquí
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()

    def destroy(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None