#####Import packages#####
from email.message import Message
from timeit import repeat
import tkinter
import tkinter.messagebox
import customtkinter
from tkinter import Tk, Frame, Menu, ttk,Toplevel
from PIL import Image,ImageTk
from tkinter.filedialog import askopenfile,asksaveasfilename,asksaveasfile
from openpyxl import load_workbook
import time
from tkinter.ttk import *
import shutil
import os
import pandas as pd
import numpy as np
import shutil
import csv
import urllib.request
import tkinter as tk
import subprocess
import json
import sys
from io import StringIO
from tkinter import Text
from tkinter import PhotoImage
from datetime import datetime, timedelta
import paramiko
from command import excute_remote_command
from tkinter import END, DISABLED
import re
############################
############################
#create the main window

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 980
    HEIGHT = 620

    def __init__(self):
        super().__init__()

        self.title("DeeperInCode -Server Manager")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        vo= str(os.path.abspath(os.getcwd()))+r'.\static\images\logo.ico'
        self.iconbitmap(vo)

        self.services = ["deepertest"]
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        DB_creation_icon=customtkinter.CTkImage(Image.open(r"./static/images/creation_ico.png"), size=(20, 20))
        DB_dumping_icon=customtkinter.CTkImage(Image.open(r"./static/images/dumping_ico_green.png"), size=(20, 20))
        DB_backup_icon=customtkinter.CTkImage(Image.open(r"./static/images/backup_ico_green.png"), size=(20, 20))
        clear_icon=customtkinter.CTkImage(Image.open(r"./static/images/clear_ico.png"), size=(20, 20))
        folders_icon=customtkinter.CTkImage(Image.open(r"./static/images/folders_ico.png"), size=(20, 20))
        
        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="TOOLS",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text ='Restart Server', 
                                                image=DB_creation_icon,
                                                command=self.restart_server)
                                               
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Reload Server",
                                                image=DB_dumping_icon,
                                                command=self.reload_server)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)
        
        self.button_10 = customtkinter.CTkButton(master=self.frame_left,
                                                text ='Stop Server', 
                                                image=DB_backup_icon,
                                                command=self.stop_server)
                                               
        self.button_10.grid(row=4, column=0, pady=10, padx=20)
        
        self.button_6 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Server Status",
                                                image=folders_icon,
                                                command=self.server_status)
        self.button_6.grid(row=5, column=0)


        self.label_choose_server = customtkinter.CTkLabel(master=self.frame_left, text="Choose Service:")
        self.label_choose_server.grid(row=6, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_server = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=self.services,
                                                        command=self.handle_option_selection)
        self.optionmenu_server.grid(row=7, column=0, pady=10, padx=20, sticky="w")

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)
        
        # ============ frame_config ============
        self.label_frame_info = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Configuration",font=("Roboto Medium", -16))
        self.label_frame_info.grid(row=0, column=0, columnspan=1, pady=4, padx=10, sticky="")

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=1, column=0, columnspan=2, rowspan=2, pady=0, padx=20, sticky="nsew")
        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=0)
        self.frame_info.columnconfigure(0, weight=1)
        
        ############## frame terminal ################
        # Label for the terminal-like frame
        self.label_frame_terminal = customtkinter.CTkLabel(master=self.frame_right,
                                                   text="Result",
                                                   font=("Roboto Medium", -16))
        self.label_frame_terminal.grid(row=4, column=0, columnspan=1, pady=4, padx=10, sticky="")

        # Frame to contain the terminal-like Text widget
        self.frame_terminal = customtkinter.CTkFrame(master=self.frame_right, width=800)
        self.frame_terminal.grid(row=5, column=0, columnspan=2, rowspan=3, pady=0, padx=20, sticky="nsew")

        # Configure weight for the terminal-like frame
        self.frame_terminal.grid_rowconfigure(0, weight=1)
        self.frame_terminal.grid_columnconfigure(0, weight=1)
        
        ############## Insert config and settings from json file ################
        self.entry_text = []
        self.entry_text_settings = []
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config_dict = json.load(f)
            
            # Extract config and settings dictionaries
            config = config_dict.get("config", {})
            settings = config_dict.get("settings", {})
            
            # Fill frame_info with config entries
            for i, (key, value) in enumerate(config.items()):
                entry = customtkinter.CTkEntry(master=self.frame_info, width=120, placeholder_text=key)
                if i == 2:
                    entry.configure(show="*")  # Display password entry with stars
                entry.insert(0, value)  # Insert the value from the config file
                entry.grid(row=i, column=0, columnspan=2, pady=5, padx=5, sticky="we")
                self.entry_text.append(entry)
                
            
            
            eye_icon=customtkinter.CTkImage(Image.open(r"./static/images/eye_icon.ico"), size=(10, 10))
            # Create the password entry with toggle button
            
            show_password_button_2 = customtkinter.CTkButton(master=self.frame_info, image= eye_icon, width=1, height=1, text="")
            show_password_button_2.grid(row=2, column=0, pady=10, padx=10, sticky="e")

            # Bind the button click event to toggle password visibility
            show_password_button_2.configure(command=lambda: self.toggle_password_visibility(self.entry_text[2]))
    

        else:
            # Create and add five entry widgets
            list_entry_config=["Enter server hostname",
                    "Enter server port",
                    "Enter server password",
                    "Enter server username"
                    ]
            
            for i in range(4):
                entry = customtkinter.CTkEntry(master=self.frame_info,
                                    width=120,
                                    placeholder_text=list_entry_config[i])
                if i == 2:
                    entry.configure(show="*")  # Display password entry with stars
                entry.grid(row=i, column=0, columnspan=2, pady=5, padx=5, sticky="we")
                self.entry_text.append(entry)
                

            eye_icon=customtkinter.CTkImage(Image.open(r"./static/images/eye_icon.ico"), size=(10, 10))
            # Create the password entry with toggle button
            show_password_button_2 = customtkinter.CTkButton(master=self.frame_info, image= eye_icon, width=1, height=1, text="")
            show_password_button_2.grid(row=2, column=0, pady=10, padx=10, sticky="e")

            # Bind the button click event to toggle password visibility
            show_password_button_2.configure(command=lambda: self.toggle_password_visibility(self.entry_text[2]))

            
        ########## language selection ################
        self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="Turkish")
        self.check_box_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="English")
        self.check_box_2.grid(row=9, column=1, pady=10, padx=20, sticky="w")
        # ============ frame_right ============
        
        self.optionmenu_jornal = customtkinter.CTkOptionMenu(master=self.frame_right,
                                                        values=["1 minute ago", "1 hour ago", "1 day ago", "2 days ago", "1 week ago"],
                                                        command=self.handle_option_selection_jornal)
        self.optionmenu_jornal.grid(row=7, column=2, pady=10, padx=20, sticky="w")
        
        self.sinceentry = customtkinter.CTkEntry(master=self.frame_right,
                                                 width=120,
                                                 placeholder_text="Since*"
                                                 )
        self.sinceentry.grid(row=8, column=2,columnspan=1, pady=10, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Jornal",
                                                border_width=2,  # <- custom border_width
                                                fg_color=None,  # <- no fg_color
                                                command=self.jornal_server)
        self.button_5.grid(row=9, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.optionmenu_1.set("Light")
        self.optionmenu_server.set("deepertest")
        self.check_box_1.configure(state=tkinter.DISABLED, text="Turkish")
        self.check_box_2.select()
        self.selected_server = "deepertest"
        self.selected_jornal = "1 day ago"
        self.services = self.load_service_names()
        self.update_option_menu()  # Call to update the option menu
    ################### frame progress bar for actions ##################
        self.frame_progressbar = customtkinter.CTkFrame(master=self.frame_right,
                                                 width=10,
                                                 corner_radius=0,
                                                 height=30,
                                                 fg_color="transparent")
        self.frame_progressbar.grid(row=0, column=2, columnspan=3, pady=10, padx=10, sticky="we")
        
        self.progressbar = ttk.Progressbar(master=self.frame_progressbar, orient="horizontal", length=200, mode="determinate")
        self.progressbar.pack()

    ################################ app DB manager Functions #########################
    def load_config(self):
            config_list,settings_list=self.display_text()
            config_path = 'config.json'
            global config, settings
            if os.path.exists(config_path):
                # import the json content from the config.json file
                with open(config_path, 'r') as config_file:
                    config_dict = json.load(config_file)
                    config = config_dict['config']
                    settings = config_dict['settings']
            else:
                # Config file doesn't exist, prompt user for input
                config = {
                     'hostname' : config_list[0],
                     'port' : config_list[1],
                     'password' : config_list[2],
                     'username' : config_list[3]
                }

                settings = {
                    'port' : "",
                    'uglifyjs' : "",
                    'minify' :"" ,
                    'backup_lifetime' : "",
                    'email_server' :"" ,
                    'password_email_server' : ""
                }   

                # Create config file
                config_dict= {
                    "config": config,
                    "settings": settings
                }
                with open(config_path, 'w') as config_file:
                    config_file.write(f"{json.dumps(config_dict, indent=2)}\n\n")

            return config, settings
    
    
    def server_status(self):
        # Vérifier si l'utilisateur confirme l'action de dumping
        if tkinter.messagebox.askokcancel("Confirm", "Confirm the report of server status ?"):
            self.progressbar["value"] = 0  # Reset progress bar value
            self.progressbar.update()

            # Charger la configuration depuis les champs de saisie
            config, settings = self.load_config()

            # Rediriger stdout vers un StringIO pour capturer la sortie
            stdout_backup = sys.stdout
            sys.stdout = StringIO()
            cmd = f"systemctl status {self.selected_server}"
            # Exécuter la fonction de dumping de base de données
            excute_remote_command(config,self.update_progress,cmd)
            # Afficher la barre de progression
            #progress_window = self.display_progress_bar()

            # Récupérer la sortie capturée
            output = sys.stdout.getvalue()
            # Rétablir stdout
            #sys.stdout = stdout_backup
                        # Extract information from the output
            extracted_info = self.extract_info(output)

            # Display extracted information
            extracted_info_text = "\n".join([f"{key}: {value}" for key, value in extracted_info.items()])
            self.display_output(extracted_info_text)

            # Attendre 3 secondes avant de fermer la fenêtre de progression et d'afficher la sortie
            #self.after(3000, lambda: self.close_progress_window(progress_window, output))
            success_label=Label(self, text='Server Status reported Successfully!', foreground='green', font=('calibre', 10, 'bold'))
            success_label.grid(row=4, columnspan=3, pady=10)
            self.after(20000, lambda: success_label.destroy())
            
    def display_output_window(self, output):
        output_window = Toplevel(self)
        output_window.title("Terminal Output")
        output_window.geometry("600x400")
        
        text_widget = Text(output_window)
        text_widget.pack(fill="both", expand=True)
        text_widget.insert("1.0", output)
        

    def close_progress_window(self, progress_window, output):
        progress_window.destroy()
        self.display_output_window(output)


    def display_progress_bar(self):
        progress_window = tkinter.Toplevel(self)
        progress_window.title("DB Progress")
        progress_window.geometry("300x100")
        
        progress_bar = ttk.Progressbar(progress_window, orient='horizontal', mode='indeterminate', value=0)
        progress_bar.pack(pady=20)
        progress_bar.start()   

        # Change to determinate mode after 500 ms (0.5 seconds)
        self.after(40000, lambda: self.change_progress_bar_mode(progress_bar))
        
        # Assurez-vous de stocker progress_window dans une variable d'instance si vous avez besoin de référencer la fenêtre plus tard
        self.progress_window = progress_window
        
        return progress_window

    def change_progress_bar_mode(self, progress_bar):
        if progress_bar and progress_bar.winfo_exists():
            progress_bar.stop()
            progress_bar.config(mode='determinate', maximum=100, value=0)
        
    def update_progress(self, completed_tasks, total_tasks):
        progress = int((completed_tasks / total_tasks) * 100)
        self.progressbar["value"] = progress
        self.progressbar.update()
    def reload_server(self):
        # Vérifier si l'utilisateur confirme l'action de dumping
        if tkinter.messagebox.askokcancel("Confirm", "Confirm the reload of server ?"):
            self.progressbar["value"] = 0  # Reset progress bar value
            self.progressbar.update()

            # Charger la configuration depuis les champs de saisie
            config, settings = self.load_config()

            # Rediriger stdout vers un StringIO pour capturer la sortie
            stdout_backup = sys.stdout
            sys.stdout = StringIO()
            cmd = f"systemctl reload {self.selected_server}"
            # Exécuter la fonction de dumping de base de données
            excute_remote_command(config,self.update_progress,cmd)
            # Afficher la barre de progression
            #progress_window = self.display_progress_bar()

            # Récupérer la sortie capturée
            output = sys.stdout.getvalue()
            self.display_output(f"Server {self.selected_server} Reloaded Successfully!")
            # Rétablir stdout
            #sys.stdout = stdout_backup

            # Attendre 3 secondes avant de fermer la fenêtre de progression et d'afficher la sortie
            #self.after(3000, lambda: self.close_progress_window(progress_window, output))
            success_label=Label(self, text='Server Reloaded Successfully!', foreground='green', font=('calibre', 10, 'bold'))
            success_label.grid(row=4, columnspan=3, pady=10)
            self.after(20000, lambda: success_label.destroy())
    
    def stop_server(self):
            # Vérifier si l'utilisateur confirme l'action de dumping
        if tkinter.messagebox.askokcancel("Confirm", "Confirm the stop of server ?"):
            self.progressbar["value"] = 0  # Reset progress bar value
            self.progressbar.update()

            # Charger la configuration depuis les champs de saisie
            config, settings = self.load_config()

            # Rediriger stdout vers un StringIO pour capturer la sortie
            stdout_backup = sys.stdout
            sys.stdout = StringIO()
            cmd = f"systemctl stop {self.selected_server}"
            # Exécuter la fonction de dumping de base de données
            excute_remote_command(config,self.update_progress,cmd)
            # Afficher la barre de progression
            #progress_window = self.display_progress_bar()

            # Récupérer la sortie capturée
            output = sys.stdout.getvalue()
            self.display_output(f"Server {self.selected_server} stopped Successfully!")
            # Rétablir stdout
            #sys.stdout = stdout_backup

            # Attendre 3 secondes avant de fermer la fenêtre de progression et d'afficher la sortie
            #self.after(3000, lambda: self.close_progress_window(progress_window, output))
            success_label=Label(self, text='Server Stopped Successfully!', foreground='green', font=('calibre', 10, 'bold'))
            success_label.grid(row=4, columnspan=3, pady=10)
            self.after(20000, lambda: success_label.destroy())
            
    
    def restart_server(self):
            # Vérifier si l'utilisateur confirme l'action de dumping
        if tkinter.messagebox.askokcancel("Confirm", "Confirm the restart of server ?"):
            self.progressbar["value"] = 0  # Reset progress bar value
            self.progressbar.update()

            # Charger la configuration depuis les champs de saisie
            config, settings = self.load_config()

            # Rediriger stdout vers un StringIO pour capturer la sortie
            stdout_backup = sys.stdout
            sys.stdout = StringIO()
            cmd = f"systemctl restart {self.selected_server}"
            # Exécuter la fonction de dumping de base de données
            excute_remote_command(config,self.update_progress,cmd)
            # Afficher la barre de progression
            #progress_window = self.display_progress_bar()

            # Récupérer la sortie capturée
            output = sys.stdout.getvalue()
            self.display_output(f"Server {self.selected_server} Restarted Successfully!")

            # Rétablir stdout
            #sys.stdout = stdout_backup

            # Attendre 3 secondes avant de fermer la fenêtre de progression et d'afficher la sortie
            #self.after(3000, lambda: self.close_progress_window(progress_window, output))
            success_label=Label(self, text='Server Restarted Successfully!', foreground='green', font=('calibre', 10, 'bold'))
            success_label.grid(row=4, columnspan=3, pady=10)
            self.after(20000, lambda: success_label.destroy())
            
    def jornal_server(self):
            # Vérifier si l'utilisateur confirme l'action de dumping
        if tkinter.messagebox.askokcancel("Confirm", "Confirm the report of jornal ?"):
            self.progressbar["value"] = 0  # Reset progress bar value
            self.progressbar.update()
            # Charger la configuration depuis les champs de saisie
            config, settings = self.load_config()
            since_value = self.sinceentry.get()
            # Rediriger stdout vers un StringIO pour capturer la sortie
            stdout_backup = sys.stdout
            sys.stdout = StringIO()
            if since_value == '' or since_value =='None':
                cmd = f'journalctl --since "{self.selected_jornal}" -u {self.selected_server}'
            else:
                cmd = f'journalctl --since "{since_value}" -u {self.selected_server}'
            print(cmd)
            # Exécuter la fonction de dumping de base de données
            excute_remote_command(config,self.update_progress,cmd)
            # Afficher la barre de progression
            #progress_window = self.display_progress_bar()

            # Récupérer la sortie capturée
            output = sys.stdout.getvalue()
            # Rétablir stdout
            #sys.stdout = stdout_backup
                        # Extract information from the output
            self.display_output_list(output)

            # Attendre 3 secondes avant de fermer la fenêtre de progression et d'afficher la sortie
            #self.after(3000, lambda: self.close_progress_window(progress_window, output))
            success_label=Label(self, text='Jornal reported Successfully!', foreground='green', font=('calibre', 10, 'bold'))
            success_label.grid(row=4, columnspan=3, pady=10)
            self.after(20000, lambda: success_label.destroy())
            
    def default_directory_backup(self):
        backup_directory = 'backup_data'
        max_directory_date = "1970-01-01_00-00-00"
        for directory in os.listdir(backup_directory):
            directory_date = directory.split('_')[1] + '_' + directory.split('_')[2]
            directory_date = datetime.strptime(directory_date, '%Y-%m-%d_%H-%M-%S')
            max_directory_date = datetime.strptime( max_directory_date, '%Y-%m-%d_%H-%M-%S')
            if directory_date > max_directory_date:
                max_directory_date = directory_date
            max_directory_date = max_directory_date.strftime('%Y-%m-%d_%H-%M-%S')
        default_backup_directory = f"backup_{max_directory_date}"
        return default_backup_directory
    
    def display_text(self):
        config_list=[]
        settings_list=[]
        for entry in self.entry_text:
            a=entry.get()
            config_list.append(a)
        for entry in self.entry_text_settings:
            b=entry.get()
            settings_list.append(b)
        print(config_list,settings_list)
        return config_list,settings_list

            
    def list_backup_folders(self):
        backup_data_path = os.path.abspath(os.path.join(os.getcwd(), "backup_data"))
        backup_folders = [folder for folder in os.listdir(backup_data_path) if os.path.isdir(os.path.join(backup_data_path, folder))]
        return backup_folders
    
   # Function to load service names from systemd
    def load_service_names(self):
        import io
        config, settings = self.load_config()
        cmd = "ls /etc/systemd/system/*.service"  # Command to list all service files
        service_names = []
        
        # Create a StringIO object to capture output
        output_capture = io.StringIO()
        original_stdout = sys.stdout  # Save a reference to the original standard output
        sys.stdout = output_capture  # Redirect standard output to the StringIO object

        try:
            # Execute the command to get the service names
            excute_remote_command(config, None, cmd)  # Pass None for progress callback
        finally:
            sys.stdout = original_stdout  # Restore original standard output

        # Get the captured output
        output = output_capture.getvalue().strip().splitlines()  # Capture and split into lines

        if not output:
            print("No output received from the command.")
            return service_names  # Return an empty list if no output

        # Process the output
        for line in output:
            service_name = line.strip()  # Remove any leading/trailing whitespace
            if service_name.endswith(".service"):
                # Extract the service name without the path and extension
                service_name_only = service_name.split('/')[-1][:-8]  # Remove the '.service' extension
                
                # Check conditions based on the service name
                if service_name_only.startswith("dbus"):
                    last_word = service_name_only.split('.')[-1]  # Get the last word after the dot
                    formatted_name = f"{last_word}/dbus"  # Format as required
                    service_names.append(formatted_name)
                elif service_name_only.startswith("snap"):
                    last_word = service_name_only.split('.')[-1]  # Get the last word after the dot
                    formatted_name = f"{last_word}/snap"  # Format as required
                    service_names.append(formatted_name)
                else:
                    service_names.append(service_name_only)  # Append as is for other services

        return service_names


    def update_option_menu(self):
            # Update the option menu with the loaded services
        self.optionmenu_server.configure(values=self.services)

    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self,event=0):
        #delete tmp files if exist
       
   
        # directory
        dir = str(os.path.abspath(os.getcwd()))+r'\tmp'
   
        # path
        try:
            for file in os.scandir(dir):
                os.remove(file.path)
       
        except:
            pass
       
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
    
    li=[]
    
    def open_file(self):
        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="KModes clustering is,\n" +
                                                        "one of the unsupervised Machine Learning algorithms,\n" +
                                                        "that is used to cluster categorical variables" ,
                                                   height=100,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=5, pady=5)
        
        file = askopenfile(mode ='r', filetypes =[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')]) # To open the file that you want. 
    #' mode='r' ' is to tell the filedialog to read the file
    # 'filetypes=[()]' is to filter the files shown as only Excel files

        #wb = load_workbook(filename = file.name) # Load into openpyxl
        
            
        self.li.append(file.name)
            
        print(self.li)
        src_path = file.name
        dst_path =  str(os.path.abspath(os.getcwd()))+r"\tmp"
        shutil.copy(src_path, dst_path)

        pb1 = Progressbar(
        master=self.frame_right,
        orient= 'horizontal', 
        length=300, 
        mode='determinate'
        )
        pb1.grid(row=8, columnspan=2, pady=20)
        for i in range(3):
            self.update_idletasks()
            pb1['value'] += 45
            time.sleep(1)
        pb1.destroy()
        Label(self, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)
        self.button_3.config(state="normal") 


    def uploadFiles(self):
        pb1 = Progressbar(
        master=self.frame_right,
        orient= 'horizontal', 
        length=300, 
        mode='determinate'
        )
        pb1.grid(row=4, columnspan=3, pady=20)
        for i in range(5):
            self.update_idletasks()
            pb1['value'] += 20
            time.sleep(1)
        pb1.destroy()
        Label(self, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)
        
        
    ### fUNCTION TO TREE THE DATA 
    newli=[]
    def lister(self):
        backup_list = self.list_backup_folders()
        self.new_window = tk.Toplevel(self.master)
        self.new_window.geometry("600x400+50+50")
        self.new_window.attributes('-alpha', 0.85)
        self.new_window.title("List of Directories")
        self.new_window.resizable(False, False)
        self.new_window.configure(background='#f5f5f5')
        self.new_window.focus_force()
        self.new_window.grab_set()
        self.new_window.transient(self.master)

        self.tree = ttk.Treeview(self.new_window, columns=("ID", "Directory Name", "Selected"), height=200, show='headings',
                                 style='mystyle.Treeview', selectmode='browse')

        tree_scroll = ttk.Scrollbar(self.new_window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree['columns'] = ('ID', 'name', 'Selected')
        self.tree.column("ID", width=5)
        self.tree.column("name", width=250)
        self.tree.column("Selected", width=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="Directory Name")
        self.tree.heading("Selected", text="Selected")

        for count, directory in enumerate(backup_list):
            self.tree.insert("", "end", values=(count, directory))
        
        self.select_folder_auto()
        # Add a button to select the folder
        select_button = customtkinter.CTkButton(master=self.new_window, text="Select", command=self.select_folder)
        select_button.pack(pady=10)
    
    selected_folder = None
    def select_folder(self):
        selected_item = self.tree.selection()[0]  # Access tree as an instance variable
        self.selected_folder = self.tree.item(selected_item, "values")[1]
        selected_folder=self.selected_folder
        print(self.selected_folder)
        selected_folder_with_flag = "X"
        # Deselect all items in the Treeview
        for item in self.tree.get_children():
            self.tree.set(item, column="Selected", value="")
            self.tree.item(item, tags=()) 
        # Update the 'Selected' column with the selected folder

        self.tree.set(selected_item, column="Selected", value=selected_folder_with_flag)
        self.tree.tag_configure('green', foreground='green')  
        self.tree.item(selected_item, tags=('green',))  
        return selected_folder  
    
    def select_folder_auto(self):
        selected_folder_with_flag = "X"
        selected_directory = self.selected_folder if self.selected_folder is not None else self.default_directory_backup()

        # Iterate over items in the Treeview to find the item with the matching name
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            if values and values[1] == selected_directory:
                selected_directory = item
                break

        # Check if the selected directory is valid
        if selected_directory is not None:
            # Update the 'Selected' column with the selected folder
            self.tree.set(selected_directory, column="Selected", value=selected_folder_with_flag)
            self.tree.tag_configure('green', foreground='green')
            self.tree.item(selected_directory, tags=('green',))
        else:
            print("Error: No selected directory found.")

        
    # Function to toggle password visibility
    def toggle_password_visibility(self, password_entry):
        show_password = password_entry.cget("show")
        if show_password:
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")


    
        
############ FUNCTION TO CLEAN THE DATA ###############
    #create function that reset the app 
    def reset_app(self):
        #delete tmp files if exist
        # directory
        dir = str(os.path.abspath(os.getcwd()))+r'\tmp' 
        # path
        try:
            for file in os.scandir(dir):
                os.remove(file.path)  
                self.button_3.config(state="DISABLED") 
                self.li.clear()
                self.newli.clear()
                self.combobox_1.set("select file")
        except:
            pass
    

    def handle_option_selection(self, selected_value):
        # Update the selected server parameter
        self.selected_server = selected_value   
        print(f"Selected server: {self.selected_server}") 
        
    def handle_option_selection_jornal(self, selected_value):
            # Update the selected server parameter
        self.selected_jornal = selected_value   
        print(f"Selected server: {self.selected_jornal}") 
        
    def display_output(self, output):
        # Create a frame to contain the Text widget and the scrollbar
        frame_output = tk.Frame(self.frame_terminal)  # Place within self.frame_terminal
        frame_output.grid(row=0, column=0, sticky="nsew")  # Adjust row and column

        # Create a Text widget to display the output
        text_output = tk.Text(frame_output, wrap="word", width=60, height=15)  # Increased height
        text_output.insert(tk.END, output)
        text_output.config(state=tk.DISABLED)  # Make the Text widget read-only
        text_output.grid(row=0, column=0, sticky="nsew")

        # Create a Scrollbar and attach it to the Text widget
        scrollbar = tk.Scrollbar(frame_output, command=text_output.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        text_output.config(yscrollcommand=scrollbar.set)
        frame_output.grid_rowconfigure(0, weight=1)
        frame_output.grid_columnconfigure(0, weight=1)
    
    def display_output_list(self, output):
        # Create a frame to contain the Listbox and the scrollbar
        frame_output_list = tk.Frame(self.frame_terminal)  # Place within self.frame_terminal
        frame_output_list.grid(row=0, column=0, sticky="nsew")  # Adjust row and column

        # Split the output into lines
        output_lines = output.split('\n')

        # Create a Listbox to display the output as a list of lines
        list_output = tk.Listbox(frame_output_list, width=80, height=11)  # Increased height
        for line in output_lines:
            list_output.insert(tk.END, line)
        list_output.grid(row=0, column=0, sticky="nsew")

        # Create a Scrollbar and attach it to the Listbox
        scrollbar = tk.Scrollbar(frame_output_list, command=list_output.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        list_output.config(yscrollcommand=scrollbar.set)
        
            # Create a horizontal Scrollbar and attach it to the Listbox
        scrollbar_x = tk.Scrollbar(frame_output_list, orient=tk.HORIZONTAL, command=list_output.xview)
        scrollbar_x.grid(row=1, column=0, sticky="ew")
        list_output.config(xscrollcommand=scrollbar_x.set)
        frame_output_list.grid_rowconfigure(0, weight=1)
        frame_output_list.grid_columnconfigure(0, weight=1)

        
    def extract_info(self, output):
        # Define regular expressions to extract specific information
        regex_patterns = {
            'status': r'Active: (.*?) since',
            'since': r'since (.+)',
            'pid': r'Main PID: (\d+)',
            'memory': r'Memory: (.*?)\n',
            'cpu': r'CPU: (.*?)\n',
            'tasks': r'Tasks: (.*?)\n',
            'CGroup:': r'CGroup: (.*?)\n',
            'Loaded:': r'Loaded: (.*?)\n'
        }

        # Extract information using regex
        extracted_info = {}
        for key, pattern in regex_patterns.items():
            match = re.search(pattern, output)
            if match:
                extracted_info[key] = match.group(1)
            else:
                extracted_info[key] = "N/A"

        # Now extracted_info contains the extracted information
        return extracted_info


        

#create toolbar Menu  and add it to the main window
class Example(Frame):
    
        def __init__(self,app):
            super().__init__()
            self.app_instance=app

            self.initUI()


        def initUI(self):

            self.master.title("DeeperInCode -Server Manager")

            menubar = Menu(self.master)
            self.master.config(menu=menubar)

            fileMenu = Menu(menubar)
            fileMenu.add_command(label="Exit", command=self.onExit)
            menubar.add_cascade(label="File", menu=fileMenu)
            
            editMenu = Menu(menubar)
            editMenu.add_command(label="Undo")
            editMenu.add_separator()
            editMenu.add_command(label="Cut")
            editMenu.add_command(label="Copy")
            editMenu.add_command(label="Paste")
            editMenu.add_separator()
            editMenu.add_command(label="Select All")
            menubar.add_cascade(label="Edit", menu=editMenu)
            helpMenu = Menu(menubar)
            helpMenu.add_command(label="About", command=self.onAbout)
            menubar.add_cascade(label="Help", menu=helpMenu)
            

########################### FUNCTIONS #####################
        def onExit(self):

            self.quit()   
            

        ## FUNCTION TO SHOW ABOUT DIALOG     
        def onAbout(self):
            new_window=Toplevel(self.master)
            new_window.geometry("800x400+50+50")
            new_window.attributes('-alpha', 0.7)
            new_window.title("About")
            new_window.resizable(False,False)
            if self.app_instance.optionmenu_1.get() == "Dark":
                lbl=customtkinter.CTkLabel(master=new_window,
                                                    text=
                                                    '''Auteur : FAHMI DJOBBI \n \n \t'''+
    "Welcome to [DeeperInCode Database Manager], a powerful and user-friendly application designed to streamline your database management journey. \n "
    "Whether you're a database administrator, developer, or business owner, our application provides essential tools for efficiently handling SQL databases.\n"
        "Key Features:\n"
        "1. Database Creation:\n"
        "   Easily create new databases with specific requirements tailored to your needs.\n" 
        "Our intuitive interface guides you through the setup process, \n "
        "ensuring a seamless and error-free database creation experience.\n"
        "2. Migration Capabilities:\n"
        "   Effortlessly migrate data between databases, facilitating smooth transitions or updates.\n " 
        "Whether you're upgrading to a new version or transferring \n "
        "data to a different environment, our application simplifies the migration process.\n"
        "3. Data Duplication:\n"
        "   Duplicate and replicate your data with just a few clicks. Whether you need to create a backup or populate \n "
        "a test environment, our application ensures \n  "
        "accurate and efficient data duplication.\n"
        "4. Backup and Restore:\n"
        "   Secure your data with robust backup and restore functionalities. Schedule automatic backups \n "
        "to prevent data loss, and easily restore databases to previous \n "
        "states whenever needed.\n"
        "5. Auto-Update with Version Control:\n"
        "   Stay up-to-date with our auto-update feature, ensuring you always have access \n "
        "to the latest enhancements and security patches. The application intelligently \n "
        "Support and Feedback:\n"
        "please reach out to our support team at [support@DeeperIncode.com].\n"
        "Thank you for choosing [DeeperInCode Database Manager] for your database management needs.\n  "
        "We are committed to delivering a reliable and efficient solution for \n "
        "your SQL database tasks.\n"
        "Happy managing!\n"
        "[www.deeperincode.com]\n"
        "[djobbioofahmi@gmail.com]",
                                                    
                                                    height=150,
                                                    fg_color=("black"),  #<- custom tuple-color
                                                    justify="left",
                                                    )

                lbl.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="we")
                lbl.configure(font=("Arial", 10, "bold"))

            else:
                lbl=customtkinter.CTkLabel(master=new_window,
                                                    text=
                                                    '''Auteur : FAHMI DJOBBI \n \n \t'''+
    "Welcome to [DeeperInCode Database Manager], a powerful and user-friendly application designed to streamline your database management journey. \n "
    "Whether you're a database administrator, developer, or business owner, our application provides essential tools for efficiently handling SQL databases.\n"
        "Key Features:\n"
        "1. Database Creation:\n"
        "   Easily create new databases with specific requirements tailored to your needs.\n" 
        "Our intuitive interface guides you through the setup process, \n "
        "ensuring a seamless and error-free database creation experience.\n"
        "2. Migration Capabilities:\n"
        "   Effortlessly migrate data between databases, facilitating smooth transitions or updates.\n " 
        "Whether you're upgrading to a new version or transferring \n "
        "data to a different environment, our application simplifies the migration process.\n"
        "3. Data Duplication:\n"
        "   Duplicate and replicate your data with just a few clicks. Whether you need to create a backup or populate \n "
        "a test environment, our application ensures \n  "
        "accurate and efficient data duplication.\n"
        "4. Backup and Restore:\n"
        "   Secure your data with robust backup and restore functionalities. Schedule automatic backups \n "
        "to prevent data loss, and easily restore databases to previous \n "
        "states whenever needed.\n"
        "5. Auto-Update with Version Control:\n"
        "   Stay up-to-date with our auto-update feature, ensuring you always have access \n "
        "to the latest enhancements and security patches. The application intelligently \n "
        "Support and Feedback:\n"
        "please reach out to our support team at [support@DeeperIncode.com].\n"
        "Thank you for choosing [DeeperInCode Database Manager] for your database management needs.\n  "
        "We are committed to delivering a reliable and efficient solution for \n "
        "your SQL database tasks.\n"
        "Happy managing!\n"
        "[www.deeperincode.com]\n"
        "[djobbioofahmi@gmail.com]",
                                                    
                                                    height=150,
                                                    fg_color=("white"),
                                                    bg_color=("black"),
                                                    justify="left",
                                                    )

                lbl.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="we")  
                lbl.configure(font=("Arial", 10, "bold"))



######################### END  APP ###################################               

if __name__ == "__main__":
    app = App()
    app1=Example(app)
    app.mainloop()