# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

from customtkinter import *
from tkinter import ttk, Text, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import Modules.config_handler
import Modules.read_log
import subprocess
import threading
import os
import Modules.tool_tip
import Modules.config_menu
from tkinter import messagebox
from PIL import Image
import datetime
from Modules.tools import resource_path

projectNameData, stationNameData, sapID, updateRate, logFolder = Modules.config_handler.all_config()

class App():

    def __init__(self, master) -> None:
        self.master = master

        self.tooltips = []
        
        try:
            self.lastModTime = os.path.getmtime(Modules.read_log.getLogPath(logFolder))
        except UnboundLocalError:
            print("No se encontro el log de hoy")

        self.firstUpdate = False
        self.registeredShift = Modules.read_log.getShift(Modules.read_log.getLogPath(logFolder))[0]

        notebook = ttk.Notebook(self.master)
        notebook.pack(expand=True, fill=BOTH)

        main_tab = CTkFrame(notebook, fg_color="#FFFFFF")
        history_tab = CTkFrame(notebook, fg_color="#FFFFFF")
        fails_tab = CTkFrame(notebook, fg_color="#FFFFFF")
        more_tab = CTkFrame(notebook, fg_color="#FFFFFF")
        notebook.add(main_tab, text="FPY")
        notebook.add(history_tab, text="Historial")
        notebook.add(fails_tab, text="Fallas")        
        notebook.add(more_tab, text="Mas...")

        self.widgets_main_tab(main_tab)
        self.widgets_history_tab(history_tab)
        self.widgets_fails_tab(fails_tab)
        self.widgets_more_tab(more_tab)
        
        self.update_plot()
        self.update_history_indicators()
        self.update_last_unit()
        self.update_history_tab()
        self.update_fail_tab()
        
        self.update_all()

        self.master.protocol("WM_DELETE_WINDOW", self.close_master)

    def widgets_main_tab(self, tab):
        #HistoryFrame
        bottomFrame = CTkFrame(tab, width=500, height=50, fg_color="#FFFFFF")
        bottomFrame.pack_propagate(False)
        bottomFrame.pack(side=BOTTOM, expand=False, fill=X)
        historyLabel = CTkLabel(bottomFrame, text="Historial")
        historyLabel.pack(side=LEFT, padx= 10)

        self.historyIndicators = []

        for i in range(30):
            button = CTkButton(bottomFrame, width=10, height=30, text="", corner_radius=1, fg_color="#AAAAAA", hover_color="#505050")
            button.pack(side=LEFT, padx=2)
            self.historyIndicators.append(button)

        #DataFrame
        leftFrame = CTkFrame(tab, width=250, height=250, fg_color="#FFFFFF")
        leftFrame.pack(side=LEFT, expand=False, fill=Y)
        leftFrame.pack_propagate(False)
        projectName = CTkLabel(leftFrame, text=projectNameData, anchor="w", font=("roboto",30,"bold"))
        projectName.pack(side=TOP, anchor="w", padx=10, pady=5)
        dataFrame1 = CTkFrame(leftFrame, fg_color="#FFFFFF")
        dataFrame1.pack(side=TOP, anchor="w", padx=10,pady=5)
        stationName = CTkLabel(dataFrame1, text=stationNameData, anchor="w", font=("roboto",20))
        #stationName.pack(side=TOP, anchor="w", padx=10, pady=5)
        stationName.grid(column=0,row=0)
        sapNumber = CTkLabel(dataFrame1, text=("SAP "+sapID), anchor="w", font=("roboto",20))
        sapNumber.grid(column=1,row=0, padx=10)
        lastUnit = CTkLabel(leftFrame, text="Ultima UUT", anchor="w")
        lastUnit.pack(side=TOP, anchor="w", padx=10, pady=5)
        self.unitSerial = CTkLabel(leftFrame, text="Serial", anchor="w")
        self.unitSerial.pack(side=TOP, anchor="w", padx=10, pady=5)
        self.unitPart = CTkLabel(leftFrame, text="Part Number", anchor="w")
        self.unitPart.pack(side=TOP, anchor="w", padx=10, pady=5)
        self.unitStatus = CTkLabel(leftFrame, text="Status", anchor="w")
        self.unitStatus.pack(side=TOP, anchor="w", padx=10, pady=5)

        #PlotFrame
        rightFrame = CTkFrame(tab, width=250, height=250)
        rightFrame.pack_propagate(False)
        rightFrame.pack(side=RIGHT, expand=False, fill=Y) 
        fig, self.ax = plt.subplots()
        self.ax.pie((70,30), labels=("PASS","FAIL"), autopct="%1.1f%%", startangle=90)
        self.ax.axis('equal')
        self.pieCanvas = FigureCanvasTkAgg(fig,rightFrame)
        self.pieCanvas.draw()
        self.pieCanvas.get_tk_widget().pack()

    def widgets_history_tab(self, tab):
        titleLabel = CTkLabel(tab, text="[SERIAL - PARTNUMBER - TEST STATUS - TEST START - TEST END - FAIL MODE - TEST RESULT - TEST LIMITS]", font=("roboto",10))
        titleLabel.pack(side=TOP)
        textboxFrame = CTkFrame(tab)
        textboxFrame.pack(side=TOP, expand=True, fill=BOTH)
        self.historyBox = Text(textboxFrame, border=0, font=("roboto"))
        self.historyBox.tag_configure("pass", foreground="green")
        self.historyBox.tag_configure("fail", foreground="red")
        self.historyBox.grid(row=0,column=0,sticky=NSEW)
        self.historyBox.configure(state=DISABLED)
        scrollbar = CTkScrollbar(textboxFrame, command=self.historyBox.yview)
        scrollbar.grid(row=0,column=1,sticky=NS)
        self.historyBox.configure(yscrollcommand=scrollbar.set)
        textboxFrame.grid_rowconfigure(0, weight=1)
        textboxFrame.grid_columnconfigure(0, weight=1)
        
    def widgets_fails_tab(self, tab):
        titleLabel = CTkLabel(tab, text="[SERIAL - PARTNUMBER - TEST STATUS - TEST START - TEST END - FAIL MODE - TEST RESULT - TEST LIMITS]", font=("roboto",10))
        titleLabel.pack(side=TOP)
        textboxFrame = CTkFrame(tab)
        textboxFrame.pack(side=TOP, expand=True, fill=BOTH)
        self.failsBox = Text(textboxFrame, border=0, font=("roboto"))
        self.failsBox.tag_configure("fail", foreground="red")
        self.failsBox.grid(row=0,column=0,sticky=NSEW)
        self.failsBox.configure(state=DISABLED)
        scrollbar = CTkScrollbar(textboxFrame, command=self.failsBox.yview)
        scrollbar.grid(row=0,column=1,sticky=NS)
        self.failsBox.configure(yscrollcommand=scrollbar.set)
        textboxFrame.grid_rowconfigure(0, weight=1)
        textboxFrame.grid_columnconfigure(0, weight=1)

    def widgets_more_tab(self, tab):
        logImage = CTkImage(Image.open(resource_path("./Images/log.png")), size=(20,20))
        xlsImage = CTkImage(Image.open(resource_path("./Images/xls.png")), size=(20,20))
        self.openLogButton = CTkButton(tab, text="Abrir .log", width=150, height=50, fg_color="#FFC300", text_color="#000000", hover_color="#EAB300", command=self.open_logfile_thread)
        self.openLogButton.configure(image=logImage)
        self.openLogButton.pack(side=TOP,pady=(40,10))
        generateXlsButton = CTkButton(tab, text="Generar archivo .xls", width=150, height=50, fg_color="#FFC300", text_color="#000000", hover_color="#EAB300")
        generateXlsButton.configure(image=xlsImage)
        generateXlsButton.pack(side=TOP,pady=10)
        settingsButton = CTkButton(tab, text="Configuración", width=150, height=50, fg_color="#FFC300", text_color="#000000", hover_color="#EAB300", command=self.open_config_menu_thread)
        settingsButton.pack(side=TOP, pady=10)

    def update_plot(self):
        fpy = Modules.read_log.calculateFPY(logFolder)
        fail = float(100 - fpy)
        self.ax.clear()
        self.ax.pie((fpy,fail), labels=("PASS","FAIL"), autopct="%1.1f%%", startangle=90, colors=("#28b463","#e74c3c"))
        self.ax.axis('equal')
        self.pieCanvas.draw()

    def update_history_indicators(self):
        last30tests = Modules.read_log.readAll(logFolder)[-28:]
        #print(len(self.tooltips))

        if self.firstUpdate == False or len(self.tooltips) < 28: #If the case is False the objects ToolTips will be created
            for i, indicator in enumerate(self.historyIndicators):
                tooltip = Modules.tool_tip.ToolTip(indicator,"")
##                if i < len(last30tests):
##                    if "PASS" in last30tests[i]:
##                        indicator.configure(fg_color="#28b463")
##                        tooltip = Modules.tool_tip.ToolTip(indicator,last30tests[i])
##                    elif "FAIL" in last30tests[i]:
##                        indicator.configure(fg_color="#e74c3c")
##                        tooltip = Modules.tool_tip.ToolTip(indicator,last30tests[i])
##                    self.tooltips.append(tooltip)
                self.tooltips.append(tooltip)
            self.firstUpdate = True
        
        else: #On the other hand only the ToolTip text will be edited
            for i, indicator in enumerate(self.historyIndicators):
                if i < len(last30tests):
                    if "PASS" in last30tests[i]:
                        indicator.configure(fg_color="#28b463")
                        #self.tooltips[i].text = last30tests[i]                    
                    elif "FAIL" in last30tests[i]:
                        indicator.configure(fg_color="#e74c3c")
                        #self.tooltips[i].text = last30tests[i]
                    if i < len(self.tooltips):
                        self.tooltips[i].text = last30tests[i]
        

    def update_last_unit(self):
        serial,partNumber,testStatus,testStart,testEnd,failMode,testResult,testLimits = Modules.read_log.lastUnit(logFolder)

        self.unitSerial.configure(text=("Serial: "+serial))
        self.unitPart.configure(text=("Numero de parte: "+partNumber))
        
        if testStatus == "FAIL":
            self.unitStatus.configure(text=("Estatus: "+testStatus+" "+failMode+" "+testResult))
        else:
            self.unitStatus.configure(text=("Estatus: "+testStatus))

    def update_history_tab(self):
        logData = Modules.read_log.readAll(logFolder)
        logData = logData[::-1] 
        self.historyBox.configure(state=NORMAL)
        self.historyBox.delete(1.0,END)
        for item in logData:
            if "PASS" in item:
                self.historyBox.insert(END, item, "pass")
            elif "FAIL" in item:
                self.historyBox.insert(END, item, "fail")
        self.historyBox.configure(state=DISABLED)

    def update_fail_tab(self):
        logData = Modules.read_log.readFails(logFolder)
        logData = logData[::-1]
        self.failsBox.configure(state=NORMAL)
        self.failsBox.delete(1.0,END)
        for item in logData:
            self.failsBox.insert(END, item, "fail")
        self.failsBox.configure(state=DISABLED)

    def update_all(self): #This method update all the ui calling the other update methods

        currentModTime = os.path.getmtime(Modules.read_log.getLogPath(logFolder))
        currentShift = Modules.read_log.getShift(Modules.read_log.getLogPath(logFolder))[0]

        if currentShift != self.registeredShift: #End program if the shift changes
            self.close_master()

        if currentModTime != self.lastModTime: #If the file was modified the data will be updated
            self.lastModTime = currentModTime
            self.update_plot()
            self.update_history_indicators()
            self.update_last_unit()
            self.update_fail_tab()
            self.update_history_tab()

        try:
            self.master.after(int(updateRate), self.update_all) #Start a cycle to update the ui with the new data from the log file
        except ValueError:
            messagebox.showerror("Error", ("El rate de actualización debe ser de tipo int por lo que: " + str(updateRate) + " no es valido, revise el dato manualmente desde el archivo de configuraciones"))
            sys.exit(0)


    def open_logfile_thread(self):
        threading.Thread(target=self.open_logfile).start()

    def open_logfile(self):
        logPath = Modules.read_log.getLogPath(logFolder)

        self.openLogButton.configure(state=DISABLED)
        process = subprocess.Popen(["notepad",logPath])        
        process.wait()
        self.openLogButton.configure(state=NORMAL)

    def open_config_menu_thread(self):
        threading.Thread(target=self.open_config_menu).start()

    def open_config_menu(self):
        Modules.config_menu.ConfigMenu(self.master)

    def close_master(self):
        sys.exit(0)
