from customtkinter import *
from tkinter import ttk, Text, Scrollbar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import Modules.config_handler
import Modules.read_log
import subprocess
import threading

import Modules.tool_tip

projectNameData, stationNameData, updateRate, logFolder = Modules.config_handler.all_config()

class App():

    def __init__(self, master) -> None:
        self.master = master

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

        self.update_all()

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
        stationName = CTkLabel(leftFrame, text=stationNameData, anchor="w", font=("roboto",20))
        stationName.pack(side=TOP, anchor="w", padx=10, pady=5)
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
        failsBox = CTkTextbox(tab)
        failsBox.configure(state=DISABLED)
        failsBox.pack(side=TOP, expand=TRUE, fill=BOTH)

    def widgets_more_tab(self, tab):
        self.openLogButton = CTkButton(tab, text="Abrir .log",command=self.open_logfile_thread)
        self.openLogButton.pack(side=TOP,pady=10)
        generateXlsButton = CTkButton(tab, text="Generar archivo .xls")
        generateXlsButton.pack(side=TOP,pady=10)
        settingsButton = CTkButton(tab, text="Configuración")
        settingsButton.pack(side=TOP, pady=10)

    def update_plot(self):
        fpy = Modules.read_log.calculateFPY(logFolder)
        fail = float(100 - fpy)
        self.ax.clear()
        self.ax.pie((fpy,fail), labels=("PASS","FAIL"), autopct="%1.1f%%", startangle=90, colors=("#28b463","#e74c3c"))
        self.ax.axis('equal')
        self.pieCanvas.draw()

    def update_history_indicators(self):
        last30tests = Modules.read_log.readAll(logFolder)[-30:]
        i=0
        
        for indicator in self.historyIndicators:
            if "PASS" in last30tests[i]:
                indicator.configure(fg_color="#28b463")
                tooltip = Modules.tool_tip.ToolTip(indicator,last30tests[i])
            elif "FAIL" in last30tests[i]:
                indicator.configure(fg_color="#e74c3c")
                tooltip = Modules.tool_tip.ToolTip(indicator,last30tests[i])
                
            i+=1

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

    def update_all(self):
        self.update_plot()
        self.update_history_indicators()
        self.update_last_unit()
        self.update_history_tab()

        self.master.after(int(updateRate), self.update_all)


    def open_logfile_thread(self):
        threading.Thread(target=self.open_logfile).start()

    def open_logfile(self):
        logPath = Modules.read_log.getLogPath(logFolder)

        self.openLogButton.configure(state=DISABLED)
        process = subprocess.Popen(["notepad",logPath])        
        process.wait()
        self.openLogButton.configure(state=NORMAL)