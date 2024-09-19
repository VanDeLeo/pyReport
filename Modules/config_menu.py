# made by leo

# Title: pyReport
# Autor: leonardo.avalos.montes@continental-corporation.com
# Position: Test Maintenance Technician
# Location: Continental Periferico - Guadalajara
# Date: 06/09/2024

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import Modules.config_handler
from tkinter import messagebox

class ConfigMenu(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Configuraciones")
        self.geometry("525x340")
        self.resizable(False, False)

        self.grab_set()

        project_name, station_name, sap_id, update_rate, log_folder = Modules.config_handler.all_config()
        
        self.project_name = tk.StringVar(value=project_name)
        self.station_name = tk.StringVar(value=station_name)
        self.sap_id = tk.StringVar(value=sap_id)
        self.update_rate = tk.StringVar(value=update_rate)
        self.log_folder = tk.StringVar(value=log_folder)

        self.create_widgets()

    def create_widgets(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=(10,0), padx=20, fill="both", expand=True)

        labels_frame = ctk.CTkFrame(frame)
        labels_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipadx=10)

        ctk.CTkLabel(labels_frame, text="Nombre del Proyecto:").grid(row=0, column=0, pady=10, sticky="e")
        ctk.CTkLabel(labels_frame, text="Nombre de Estacion:").grid(row=1, column=0, pady=10, sticky="e")
        ctk.CTkLabel(labels_frame, text="SAP ID:").grid(row=2, column=0, pady=10, sticky="e")
        ctk.CTkLabel(labels_frame, text="Rate de actualizacion (ms):").grid(row=3, column=0, pady=10, sticky="e")
        ctk.CTkLabel(labels_frame, text="Carpeta de Logs").grid(row=4, column=0, pady=10, sticky="e")

        entries_frame = ctk.CTkFrame(frame)
        entries_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", ipadx=10)

        ctk.CTkEntry(entries_frame, textvariable=self.project_name, width=250).grid(row=0, column=0, pady=10)
        ctk.CTkEntry(entries_frame, textvariable=self.station_name, width=250).grid(row=1, column=0, pady=10)
        ctk.CTkEntry(entries_frame, textvariable=self.sap_id, width=250).grid(row=2, column=0, pady=10)
        ctk.CTkEntry(entries_frame, textvariable=self.update_rate, width=250).grid(row=3, column=0, pady=10)

        folder_frame = ctk.CTkFrame(entries_frame)
        folder_frame.grid(row=4, column=0, pady=10, sticky="w")

        ctk.CTkEntry(folder_frame, textvariable=self.log_folder, width=170).pack(side="left", padx=(0, 10))
        ctk.CTkButton(folder_frame, fg_color="#FFC300", text_color="#000000", hover_color="#EAB300", text="...", command=self.select_log_folder, width=30).pack(side="left")

        ctk.CTkButton(self, text="Guardar", fg_color="#FFC300", text_color="#000000", hover_color="#EAB300",  command=self.save_config).pack(pady=(10))

    def select_log_folder(self):     
        folder_path = filedialog.askdirectory()
        self.wait_window()
        if folder_path:
            self.log_folder.set(folder_path)

    def save_config(self):

        if Modules.config_handler.save_all(self.project_name.get(), self.station_name.get(), self.sap_id.get(), self.update_rate.get(), self.log_folder.get()):
            messagebox.showinfo("Info", "Es necesario reiniciar la app para aplicar los cambios!")
        else:
            messagebox.showerror("Error", "Los datos no han sido guardados")

        self.destroy()

