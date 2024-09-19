# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

from tkinter import *

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.bind_id_enter = self.widget.bind("<Enter>", self.show_tip)
        self.bind_id_leave = self.widget.bind("<Leave>", self.hide_tip)

    #event=None prevents a TypeError from occurring because the showtip and hidetip methods are bound to a binding that normally always expects an argument to be passed to the method

    def show_tip(self, event=None):  # Agregamos 'event=None' para evitar el error
        # Create window for the Tooltip
        if self.tip_window or not self.text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 25
        self.tip_window = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        
        self.label = Label(tw, text=self.text, justify='left', background="#F2F2F2", relief='solid', borderwidth=1, font=("tahoma", 10, "normal"))
        self.label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
