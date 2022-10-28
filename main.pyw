from src.common import *


APP_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__)) 
SCRIPTS_FOLDER_PATH = os.path.join(APP_FOLDER_PATH, 'local_scripts/')

SHOW_WINDOW = False
MAX_LOG_LENGTH = 10000


os.chdir(APP_FOLDER_PATH)

CLIENT_CONSTANTS_DICT = CLIENT_CONSTANTS.get_dict()

server = Server(CLIENT_CONSTANTS_DICT["SERVER_URL"])


ctypes.windll.kernel32.SetConsoleTitleW("ScriptCaster")


root = tk.Tk()

# Import the tcl file with the tk.call method
root.tk.call('source', 'tkthemes/azure-ttk-theme/azure.tcl')  # Put here the path of your theme file
root.tk.call("set_theme", "dark")
# # Set the theme with the theme_use method
# style.theme_use('azure')  # Theme files create a ttk theme, here you can put its name


class AutoScrollbar(tk.ttk.Scrollbar): # Custom class is used so that scrollbar autohides itself when not needed
       
    # Defining set method with all 
    # its parameter
    def set(self, low, high):
           
        if float(low) <= 0.0 and float(high) >= 1.0:
               
            # Using grid_remove
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.ttk.Scrollbar.set(self, low, high)
       
    # Defining pack method
    def pack(self, **kw):
           
        # If pack is used it throws an error
        raise (tk.TclError,"pack cannot be used with \
        this widget")
       
    # Defining place method
    def place(self, **kw):
           
        # If place is used it throws an error
        raise (tk.TclError, "place cannot be used  with \
        this widget")



root.title(f"ScriptCaster")
root.iconbitmap('favicon.ico')
# root.geometry("680x300")
root.resizable(0,0)

# title_section = tk.ttk.Frame(root)
# title_section.grid(row =1,column=0, columnspan=2)
# title = tk.ttk.Label(title_section, text =  "Log", font = ("Segoe UI bold", 15))
# title.pack()


top_section = tk.ttk.Frame(root)
top_section.grid(row=2,column=0, columnspan=2, sticky="ew", padx=15, pady=15, ipady=10)


# desc_section = tk.ttk.Frame(top_section)
# desc_section.pack(side="left",fill="x", expand = True, padx=15, ipady=10)

desc_section1 = tk.ttk.LabelFrame(top_section)
desc_section1.grid(row=1,column=1, sticky="w")
# desc_section1.grid(row=1,column=0,columnspan=2,sticky="ew")


desc_section2 = tk.ttk.LabelFrame(top_section)
# desc_section2.grid(row=2,column=0,columnspan=2,sticky="ew")
desc_section2.grid(row=2,column=1,columnspan=2, sticky="ew")


desc_text_strvar1 = tk.StringVar()
desc_text1 = tk.Label(desc_section1, textvariable = desc_text_strvar1, justify='left', wraplength=800, padx=5, pady=5, width=105, anchor="w")
desc_text1.pack(anchor="w")
desc_text_strvar2 = tk.StringVar()
desc_text2 = tk.Label(desc_section2, textvariable = desc_text_strvar2, justify='left', wraplength=800, padx=5, pady=5, width=105, anchor="w")
desc_text2.pack(anchor="w")


ops_treeview_section = tk.ttk.Frame(root)
ops_treeview_section.grid(row=3,column=0,sticky="ns", padx=15)

ops_treeview = tk.ttk.Treeview(ops_treeview_section, selectmode = "browse", height=18)
ops_treeview["columns"]=("Scripts")
ops_treeview["show"]="headings"
ops_treeview.heading("Scripts",text = "Scripts")
ops_treeview.tag_configure('Done', background='green')
ops_treeview.tag_configure('Running', background='orange')
ops_treeview.tag_configure('Failed', background='red')
ops_treeview.tag_configure('None', background='')

ops_treeview_xscrollbar = AutoScrollbar(ops_treeview_section, orient="horizontal", command = ops_treeview.xview)
ops_treeview_yscrollbar = AutoScrollbar(ops_treeview_section, orient="vertical", command = ops_treeview.yview)

ops_treeview.config(xscrollcommand = ops_treeview_xscrollbar.set, yscrollcommand = ops_treeview_yscrollbar.set)

ops_treeview.grid(row=1, column=1,sticky="ns")
ops_treeview_xscrollbar.grid(row=2,column=1,sticky="ew")
ops_treeview_yscrollbar.grid(row=1,column=2,sticky="ns")

ops_log_section = tk.ttk.LabelFrame(root, text = "Choose a script")
ops_log_section.grid(row=3,column=1, sticky='nsew', padx=15)

ops_log = tk.Text(ops_log_section, borderwidth=0)
ops_log.configure(state="disabled")
ops_log_section_xscrollbar = AutoScrollbar(ops_log_section, orient = "horizontal", command=ops_log.xview)
ops_log_section_yscrollbar = AutoScrollbar(ops_log_section, orient = "vertical", command=ops_log.yview)
ops_log.config(xscrollcommand=ops_log_section_xscrollbar.set, yscrollcommand=ops_log_section_yscrollbar.set)

ops_log.grid(row=1,column=1, sticky='nsew')
ops_log_section_xscrollbar.grid(row=2, column=1, sticky='ew')
ops_log_section_yscrollbar.grid(row=1,column=2, sticky='ns')


ops_treeview_section.grid_remove()
ops_log_section.grid_remove()
desc_section2.grid_remove()



def restart_program_fromTkWin():
    root.destroy()
    exit_handler()
    os.execl(sys.executable, sys.executable, *sys.argv)

def quit_window_fromTkWin():
    root.destroy()
    exit_handler() # explicitly calling exit handler due to os._exit not allowing atexit to cleanup 
    os._exit(0)


def restart_program_fromSysTray(icon, item):
    icon.stop()
    root.destroy()
    exit_handler()
    os.execl(sys.executable, sys.executable, *sys.argv)

def quit_window_fromSysTray(icon, item):
    icon.stop()
    root.destroy()
    exit_handler()
    os._exit(0)

def show_window(icon, item):
    icon.stop()
    root.deiconify()


im = PIL.Image.open("favicon.ico")
systrayicon_menu = pystray.Menu(
    pystray.MenuItem(
        'Show log', 
        show_window,
        default=True),
    pystray.MenuItem(
        'Restart', 
        restart_program_fromSysTray),
    pystray.MenuItem(
        'Quit',
        quit_window_fromSysTray))


def withdraw_window():  
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "ScriptCaster - Settings":
            set_defaults_button["state"] = "normal"
            widget.destroy()
            break
    root.withdraw()
    icon = pystray.Icon("script-caster-icon",im,"ScriptCaster", menu=systrayicon_menu)
    icon.run()


final_button_section = tk.Frame(root)
withdraw_button = tk.ttk.Button(final_button_section, text = 'Close', command = withdraw_window)
quit_button = tk.ttk.Button(final_button_section, text = 'Quit', command = quit_window_fromTkWin)
restart_button = tk.ttk.Button(final_button_section, text = 'Restart', command = restart_program_fromTkWin)
final_button_section.grid(row=4, column=1, sticky="e",padx=15,pady=15)
withdraw_button.pack(side="right", padx=5, pady=10)
quit_button.pack(side="right", padx=5, pady=10)
restart_button.pack(side="right", padx=5, pady=10)


footer_section = tk.Frame(root)
threadcount_strvar = tk.StringVar()
footer_name_label = tk.Label(footer_section, text = f"{CLIENT_CONSTANTS_DICT['CLIENT_CODE']}", borderwidth=1, relief="solid", padx=2)
footer_threadcount_label = tk.Label(footer_section, textvariable=threadcount_strvar, borderwidth=1, relief="solid", padx=2)
footer_section.grid(row=5, column=0, columnspan=2, sticky="ew")
footer_threadcount_label.pack(side="right")
footer_name_label.pack(side="right")



def exit_handler():

    for process in list(ClientScripts.ActiveSubprocesses.processes.keys()): 
        ClientScripts.ActiveSubprocesses.processes[process].terminate() 

    folder = SCRIPTS_FOLDER_PATH
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    # for filename in os.listdir(folder):
    #     file_path = os.path.join(folder, filename)
    #     try:
    #         if os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))


atexit.register(exit_handler)


class Auth:
    id = None
    client_code = CLIENT_CONSTANTS_DICT["CLIENT_CODE"]
    token = None

class Exterior:
    records = dict()
    # processes = dict()
    # process_loggers = dict()
    all_sheet_values = list()


class ClientScripts:
    contents = dict()
    statuses = dict()
    class ActiveSubprocesses:
        processes = dict()
        loggers = dict() 



class Logger:

    def __init__(self, log = ''):
        self.log=[]
        self.log.append(log)


    def updatelog(self, text, end=None):
        max_len = MAX_LOG_LENGTH
        if max_len != None:
            if len(self.log)==max_len:
                self.log.pop(0)
            elif len(self.log)>max_len:
                self.log = self.log[len(self.log)-max_len+1:]
        if end=='\r' and len(self.log)>0:
            self.log.pop()
        self.log.append(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+" -"+"\n\n"+text)

    def deletelog(self):
        self.log.clear()

    def getlog(self):
        totalLog=""""""
        for element in self.log:
            totalLog+=element+"\n\n\n"
        return totalLog



mainlogger1 = Logger()
mainlogger2 = Logger()




def countdown(t, message, logger=None):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        if logger==None:
            print(f"{message} {timeformat}", end='\r')
        else:
            # exec(f"logger.updatelog('{message} {timeformat}', '\\r')")
            logger.updatelog(message +' '+ timeformat, end='\r')
        time.sleep(1)
        t -= 1


def convert_col_index(column_int):
    start_index = 1   #  it can start either at 0 or at 1
    letter = ''
    while column_int > 25 + start_index:   
        letter += chr(65 + int((column_int-start_index)/26) - 1)
        column_int = column_int - (int((column_int-start_index)/26))*26
    letter += chr(65 - start_index + (int(column_int)))
    return letter


REMOTE_SERVER = "one.one.one.one"
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
     pass # we ignore any errors, returning False
  return False


def protect_connection(codetext):
    global mainlogger1
    global mainlogger2
    while True:
        try:
            exec(codetext)
            mainlogger1.deletelog()
            mainlogger1.updatelog(f"{CLIENT_CONSTANTS_DICT['CLIENT_CODE']} is currently connected to Exterior/{CLIENT_CONSTANTS_DICT['CLIENT_CODE']}")
            break
        except Exception as e:
            print(e)
            mainlogger1.deletelog()
            mainlogger2.deletelog()
            mainlogger2.updatelog(f'An error occurred.')
            while True:
                if is_connected(REMOTE_SERVER):
                    break
                else:
                    mainlogger1.updatelog("Internet connection lost.")
                    countdown(60, "Next attempt to connect: ", logger = mainlogger2)




def update_local_client_scripts():
    for process in list(ClientScripts.ActiveSubprocesses.processes.keys()): 
        ClientScripts.ActiveSubprocesses.processes[process].terminate() 
    if os.path.isdir(SCRIPTS_FOLDER_PATH):
        shutil.rmtree(SCRIPTS_FOLDER_PATH)
    os.mkdir(SCRIPTS_FOLDER_PATH) 
    
    def update_scripts(path, user_scripts_dict):

        for user_script_path in user_scripts_dict.keys():
            filepath = os.path.join(path, user_script_path)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            with open(filepath, 'w') as f:
                f.write(user_scripts_dict[user_script_path])
            
        return user_scripts_dict.keys()

    client_scripts_names = update_scripts(SCRIPTS_FOLDER_PATH, ClientScripts.contents)

    client_scripts_statuses = dict()
    for client_script_name in client_scripts_names:
        client_scripts_statuses[client_script_name] = 'None'
    return client_scripts_statuses



def main():
    
    main.initialized = False

    global mainlogger1
    global mainlogger2
    
    global sheet
    
    global process_log_extractor_thread

    mainlogger1.updatelog(f"Welcome {CLIENT_CONSTANTS_DICT['CLIENT_CODE']} !")

    def local_auth_client():
        while True:
            try:
                mainlogger1.updatelog(f"Authenticating with server...")
                Auth.id = server.auth_client(Auth.client_code)
                mainlogger1.updatelog(f"Done.")
                break
            except Exception as e:
                print(e)
                countdown(60, f"Authentication failed. Next attempt: ", logger = mainlogger1)

    def local_get_token():
        while True:
            try:
                countdown(20, f"Awaiting approval... Next attempt: ", logger = mainlogger1)
                Auth.token = server.get_token(Auth.id, Auth.client_code)
                if Auth.token == "Denied":
                    mainlogger1.updatelog(f"Token denied.")
                    local_auth_client()
                elif Auth.token == "Pending":
                    continue
                else:
                    mainlogger1.updatelog(f"Done.")
                    break
            except Exception as e:
                print(e)
                countdown(60, f"An error occurred. Awaiting approval... Next attempt: ", logger = mainlogger1)

    local_auth_client()
    local_get_token()

    server.save_auth(AUTH_ID = Auth.id, CLIENT_CODE = Auth.client_code, AUTH_TOKEN = Auth.token)

    while True:
        try:
            mainlogger1.updatelog(f"Fetching scripts...")
            Exterior.records, Exterior.all_sheet_values, ClientScripts.contents = server.get_tasks(1)
            ClientScripts.statuses = update_local_client_scripts()
            mainlogger1.updatelog(f"Done.")
            break
        except Exception as e:
            print(e)
            countdown(60, f"Failed to fetch scripts. Next attempt:", logger = mainlogger1)

    for key in ClientScripts.statuses.keys():
        ClientScripts.ActiveSubprocesses.loggers[key] = Logger()

    
    main.initialized = True
    main.first_iter = True


    while True:                

        if not main.first_iter:
            protect_connection(f'Exterior.records, Exterior.all_sheet_values, x = server.get_tasks(0)')

        if Exterior.records["UPDATE_LOCAL_CLIENT_SCRIPTS"] == "ON":
            
            mainlogger2.updatelog(f"Updating scripts...", end='\r')
            
            try:
                protect_connection(f'Exterior.records, Exterior.all_sheet_values, x = server.get_tasks(1)')
                ClientScripts.statuses = update_local_client_scripts()
                mainlogger2.updatelog(f"Scripts updated.", end='\r')
                protect_connection("server.send_data('UPDATE_LOCAL_CLIENT_SCRIPTS', {'STATUS': 'Done ("+datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')+")'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
            except Exception as e:
                print(e)
                mainlogger2.updatelog("Could not update client-scripts.", end='\r')
                protect_connection("server.send_data('UPDATE_LOCAL_CLIENT_SCRIPTS', {'STATUS': 'Failed ("+datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')+")'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
            
            protect_connection("server.send_data('UPDATE_LOCAL_CLIENT_SCRIPTS', {'UPDATE_LOCAL_CLIENT_SCRIPTS': 'OFF'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
        
        for key in list(ClientScripts.statuses.keys()):
            
            if key in Exterior.records:
                
                if Exterior.records[key] == 'ON':
                    
                    if key in list(ClientScripts.ActiveSubprocesses.processes.keys()):  #Element exists 
                        
                        if ClientScripts.ActiveSubprocesses.processes[key].poll() != None: #Subprocess is not running

                            protect_connection(f"server.send_data('{key}'"+", {'"+key+"': 'OFF'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
                          
                            if ClientScripts.ActiveSubprocesses.processes[key].poll() == 0:

                                protect_connection(f"server.send_data('{key}'"+", {'STATUS': 'Done ("+datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')+")'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
                                ClientScripts.statuses[key]="Done"
                            else:
                                protect_connection(f"server.send_data('{key}'"+", {'STATUS': 'Failed ("+datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')+")'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
                                # protect_connection(f"exterior_connection.update_parameter_status(sheet, '{key}', 'Failed ({datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')})', Exterior.all_sheet_values)")
                                ClientScripts.statuses[key]="Failed"
                            del ClientScripts.ActiveSubprocesses.processes[key]

                    else: # Element doesnt exist
            
                        new_env = os.environ.copy()

                        row, col = exterior_connection.find_parameter_cells(None, key, sheet_values = Exterior.all_sheet_values)
                        print(row, col)
                        col = convert_col_index(col)
                        row_parameters = Exterior.all_sheet_values[row-1]
                        row_values = Exterior.all_sheet_values[row]
                        row_dict = dict(zip(row_parameters, row_values))
                        row_json = json.dumps(row_dict)
                        new_env["SC_PARAMETERS"] = row_json

                        new_env["SC_CLIENT_CODE"] = CLIENT_CONSTANTS_DICT["CLIENT_CODE"]
                        new_env["SC_SERVER_URL"] = CLIENT_CONSTANTS_DICT["SERVER_URL"]

                        new_env["SC_AUTH"] = json.dumps({"AUTH_ID": Auth.id, "CLIENT_CODE": Auth.client_code, "AUTH_TOKEN": Auth.token})

                        new_env["SC_SCRIPTS_FOLDER_PATH"] = SCRIPTS_FOLDER_PATH

                        script_path = os.path.join(SCRIPTS_FOLDER_PATH, key)
                        script_parent_dir_path = os.path.dirname(os.path.abspath(script_path))
                
                        # new_env["PYTHONPATH"]=CONSTANT_CLIENT_VARIABLES["APP_FOLDER_PATH"]
                        # new_env["PYTHONPATH"] = script_parent_dir_path 
                        new_env["PYTHONPATH"] = script_parent_dir_path
                        new_env["PYTHONUNBUFFERED"] = "1"
                        
                        extension = os.path.splitext(key)[1]
                        
                        if extension == '.py':
                            script_command = "python"
                        elif extension == '.pyw':
                            script_command = "pythonw"

                        ClientScripts.ActiveSubprocesses.processes[key] = subprocess.Popen([script_command, script_path], cwd = script_parent_dir_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, env=new_env)
                        print(key)
                        protect_connection(f"server.send_data('{key}'"+", {'STATUS': 'Running ("+datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')+")'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
                        # protect_connection(f"exterior_connection.update_parameter_status(sheet, '{key}', 'Running ({datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')})', Exterior.all_sheet_values)")
                        ClientScripts.statuses[key]="Running"
                
                elif Exterior.records[key]=='OFF':
            
                    if key in ClientScripts.ActiveSubprocesses.processes.keys():
                        if ClientScripts.ActiveSubprocesses.processes[key].poll() == None: #Subprocess is running

                            protect_connection(f"server.send_data('{key}'"+", {'STATUS': 'Done ("+datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')+")'}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
                            # protect_connection(f"exterior_connection.update_parameter_status(sheet, '{key}', 'Done ({datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')})', Exterior.all_sheet_values)")
                            ClientScripts.statuses[key]="Done"
                            #Kill process
                            ClientScripts.ActiveSubprocesses.processes[key].terminate()
                        del ClientScripts.ActiveSubprocesses.processes[key]                    
                    else:
                        if exterior_connection.get_parameter_status(sheet=None, parameter_name=key, sheet_values=Exterior.all_sheet_values)[0:7] == "Running": # Status may be stuck at running if program was shut abruptly before. Removing the status now -
                            protect_connection(f"server.send_data('{key}'"+", {'STATUS': ''}, ALL_SHEET_VALUES = Exterior.all_sheet_values)")
                            # protect_connection("server.update_parameter_status(sheet, '"+key+"', '' , Exterior.all_sheet_values)")
                        ClientScripts.statuses[key]="None"

                else:
                    pass

        if ClientScripts.ActiveSubprocesses.processes:
            if not process_log_extractor_thread.is_alive():
                process_log_extractor_thread = threading.Thread(target = process_log_extractor)
                process_log_extractor_thread.start()

        
        countdown(int(Exterior.records["REQUEST_INTERVAL"]), f"Next request in:", logger=mainlogger2)

        main.first_iter = False




def process_log_extractor():
    while ClientScripts.ActiveSubprocesses.processes:
        for key in ClientScripts.statuses.keys():
            if key in list(ClientScripts.ActiveSubprocesses.processes.keys()):
                if ClientScripts.ActiveSubprocesses.processes[key].poll() == None: #process is running
                    output = ClientScripts.ActiveSubprocesses.processes[key].stdout.readline()
                    if not output:
                        continue
                    else:
                        ClientScripts.ActiveSubprocesses.loggers[key].updatelog(str(output))




def show_selected_log():

    if main.initialized == True:
        ops_treeview_section.grid()
        ops_log_section.grid()
        desc_section2.grid()
        main.initialized = None
    elif main.initialized == False:
        ops_treeview_section.grid_remove()
        ops_log_section.grid_remove()
        desc_section2.pack_forget()
        main.initialized = None


    threadcount_strvar.set(f"Threads: {threading.active_count()}")

    if len(mainlogger1.log)>0:
        desc_text_strvar1.set(mainlogger1.log[-1])
    else: 
        desc_text_strvar1.set('')
  
  
    if len(mainlogger2.log)>0:
        desc_text_strvar2.set(mainlogger2.log[-1])
    else:
        desc_text_strvar2.set('')
  
  

    selection_list = ops_treeview.item(ops_treeview.focus())['values']
    

    if len(selection_list)>0:
        selection = selection_list[0] 
        
        if selection in list(ClientScripts.ActiveSubprocesses.loggers.keys()):
            
            ops_log_section.configure(text = selection)
            
            yscrollbar_posn = ops_log.yview()
            xscrollbar_posn = ops_log.xview()
            
            ops_log.configure(state="normal")
            ops_log.delete("1.0","end")   
            ops_log.insert("1.0", ClientScripts.ActiveSubprocesses.loggers[selection].getlog())
            ops_log.configure(state="disabled")
            
            if float(yscrollbar_posn[1]) == 1.0:
                # So that client can control scrollbar without its position resetting repeatedly        
                ops_log.yview_moveto(yscrollbar_posn[1]) 
            else:
                # So that scrollbar appears at bottom if not in use
                ops_log.yview_moveto(yscrollbar_posn[0])

            ops_log.xview_moveto(xscrollbar_posn[0])

    else:

        ops_log_section.configure(text = "Choose a script")


    common = [script for script in list(ClientScripts.statuses.keys()) if script in list(Exterior.records.keys())]
    if list(ops_treeview.get_children()) != common:
        for item in ops_treeview.get_children():
            ops_treeview.delete(item)
        for client_script_name in common:
            ops_treeview.insert('', index = "end",iid=client_script_name, values=(client_script_name))
    else:
        # Settings colours to scripts based on status
        for client_script_name in common:
            ops_treeview.item(client_script_name, tags = ClientScripts.statuses[client_script_name])


    root.after(200, show_selected_log)




main_thread = threading.Thread(target = main)

process_log_extractor_thread = threading.Thread(target = process_log_extractor)

main_thread.start()




def mainloop_callback():
    if SHOW_WINDOW is False:
        root.after(10, withdraw_window)
    root.after(500, show_selected_log)


root.protocol('WM_DELETE_WINDOW', withdraw_window)
root.after(10, mainloop_callback)
root.mainloop()
