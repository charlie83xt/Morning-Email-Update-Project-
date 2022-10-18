from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import dd_email
from dd_scheduler import DailyDigestScheduler

"""

    The GUI should enable the admin to...
        - configure which content sources to include in email
        - add recipients
        - remove recipients
        - schedule daily time to send email
        - configure sender credential

"""

# customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
# customtkinter.CTk

class DailyDigestGui():

    WIDTH = 420
    HEIGHT = 680

    # list_of_emails = DailyDigestEmail()

    def __init__(self, root):
        # Build the GUI
        self.__root = root
        self.__root.title("Daily Digest User Interface")
        title_label = ttk.Label(self.__root, text= '**Daily Digest User Interface**', 
                                font= 'HelvLight', justify="center")
        title_label.pack(padx=5, pady=5)
        self.__style = ttk.Style()
        self.__style.configure('TButton', font = ('HelvLight', 12, 'bold'))
        self.__style.configure('Header.TLabel', font = ('HelvLight', 18, 'bold'))
        # ============ create frame ============
        recipients_frame = ttk.Frame(self.__root)
        recipients_frame.pack(padx=5, pady=5)
        self.__add_recipient_var = StringVar()
        self.__recipient_list_var = Variable()
        self.__build_gui_recipients(recipients_frame,
                                    self.__add_recipient_var,
                                    self.__recipient_list_var)
    
        # ============ create schedule frame ============
        schedule_frame = ttk.Frame(self.__root)
        schedule_frame.pack(padx=5, pady=5)
        self.__hour_var = StringVar()
        self.__minute_var = StringVar()
        self.__build_gui_schedule(schedule_frame,
                                    self.__hour_var,
                                    self.__minute_var)

        # ============ GUI checkboxes to select content that its included ============            
        contents_frame = ttk.Frame(self.__root)
        contents_frame.pack(padx=5, pady=5)
        self.__quote_var = IntVar()
        self.__weather_var = IntVar()
        self.__twitter_var = IntVar()
        self.__wikipedia_var = IntVar()
        self.__build_gui_contents(contents_frame,
                                    self.__quote_var,
                                    self.__weather_var,
                                    self.__twitter_var,
                                    self.__wikipedia_var)
        
        # GUI fields for sender email/password credentials
        credential_frame = ttk.Frame(self.__root)
        credential_frame.pack(padx=5, pady=5)
        self.__username_var = StringVar()
        self.__password_var = StringVar()
        self.__build_gui_sender(credential_frame,
                                    self.__username_var,
                                    self.__password_var)
        

        # GUI field for controls
        controls_frame = ttk.Frame(self.__root)
        controls_frame.pack(padx=5, pady=5)
        self.__build_gui_controls(controls_frame)

        # set initial values for variables
        self.__list_of_emails = dd_email.DailyDigestEmail()

        self.__add_recipient_var.set('')
        self.__recipient_list_var.set(self.__list_of_emails.recipients_list)

        self.__hour_var.set('07') # defaul send time
        self.__minute_var.set('30')

        self.__quote_var.set(self.__list_of_emails.content['quote']['include'])
        self.__weather_var.set(self.__list_of_emails.content['weather']['include'])
        self.__twitter_var.set(self.__list_of_emails.content['twitter']['include'])
        self.__wikipedia_var.set(self.__list_of_emails.content['wikipedia']['include'])

        self.__username_var.set(self.__list_of_emails.sender_credentials['email'])
        self.__password_var.set(self.__list_of_emails.sender_credentials['password'])

        # Initialize scheduler
        self.__scheduler = DailyDigestScheduler()
        self.__scheduler.start()
        self.__root.protocol("VM_DELETE_WINDOW", self.__shutdown_self)

    """
    Build GUI elements to add/remove recipients 
    """
    def __build_gui_recipients(self, master, add_recipient_var, recipient_list_var):

        header = ttk.Label(master, text='Recipients', style='Header.TLabel')
        spacer_frame = ttk.Frame(master) # Use Gui as spacer

        recipients_entry = ttk.Entry(master, width=40, textvariable=add_recipient_var)
        recipients_scrollbar = ttk.Scrollbar(master, orient=VERTICAL)
        recipients_scrollbar.grid(row=4, column=1, sticky= N+S+W+E)
        recipients_listbox = Listbox(master, listvariable=recipient_list_var,
                                     selectmode= 'multiple', width= 40, height= 5)
        recipients_listbox.configure(yscrollcommand=recipients_scrollbar.set)
        recipients_scrollbar.config(command=recipients_listbox.yview)
        
        add_button = Button(master, text="Add to list", command=self.__add_recipients, font=("HelvLight", 10, "bold"), fg= 'green')
        remove_button = Button(master, text="Remove from list", 
                               command= lambda: self.__remove_selected_recipients(recipients_listbox.curselection()), font=("HelvLight", 10, "bold"), fg= 'green')

        # Place gui widgets using grid geometry manager
        header.grid(row=0, column=0)
        recipients_entry.grid(row=1, column=0)
        add_button.grid(row=2, column=0)
        spacer_frame.grid(row=3, column=0, pady=5)
        recipients_listbox.grid(row=4, column=0)
        remove_button.grid(row=5, column=0)

    """
    Build GUI elements to schedule send time
    """
    def __build_gui_schedule(self, master, hour_var, minute_var):
        # create widgest
        header = ttk.Label(master, text='Scheduled Time (24hr):' , style='Header.TLabel')
        hour_spinbox = ttk.Spinbox(master, from_ = 0, to = 23, textvariable= hour_var,
                                    wrap=True, width=3, justify = CENTER, font="HelvLight 12")
        minute_spinbox = ttk.Spinbox(master, from_ = 0, to = 59, textvariable= minute_var,
                                    wrap=True, width=3, justify = CENTER, font="HelvLight 12")
        
        # Place gui widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        hour_spinbox.grid(row=1, column=0, sticky= E, padx=2, pady=5)
        minute_spinbox.grid(row=1, column=1, sticky= W, padx=2, pady=5)
    
    """
    Build GUI elements to select content to include
    """
    def __build_gui_contents(self, master, quote_var, weather_var, twitter_var, wikipedia_var):
        # create widgest
        header = ttk.Label(master, text='Digest Contents', style='Header.TLabel')
        quote_checkbox = customtkinter.CTkCheckBox(master, text="Random Quote", 
                                                   onvalue=True, offvalue=False)
        weather_checkbox = customtkinter.CTkCheckBox(master, text="Weather Forecast", 
                                                    onvalue=True, offvalue=False)
        twitter_checkbox = customtkinter.CTkCheckBox(master, text="Twitter Trends", 
                                                    onvalue=True, offvalue=False)
        wikipedia_checkbox = customtkinter.CTkCheckBox(master, text="Wikipedia Article", 
                                                      onvalue=True, offvalue=False)

        # Place gui widgets using grid geometry manager
        header.grid(row=0, column=0, columnspan=2)
        quote_checkbox.grid(row=1, column=0, sticky= W)
        weather_checkbox.grid(row=2, column=0, sticky= W)
        twitter_checkbox.grid(row=1, column=1, sticky= W)
        wikipedia_checkbox.grid(row=2, column=1, sticky= W)

    """
    Build GUI elements to configure sender credentials
    """
    def __build_gui_sender(self, master, sender_email_var, sender_password_var):
        # create widgest
        header = ttk.Label(master, text='Sender Credentials', style='Header.TLabel')
        email_label = ttk.Label(master, text= 'Email')
        email_entry = ttk.Entry(master, width = 40, 
                                textvariable= sender_email_var)
        password_label = ttk.Label(master, text= 'Password')
        password_entry = ttk.Entry(master, width = 40, show='*',
                                textvariable= sender_password_var)
        
        # place GUI widgets using grid geometry manager
        header.grid(row=0, column=0)
        email_label.grid(row=1, column=0, pady = 2, sticky= E)
        email_entry.grid(row=1, column=1, pady = 2, sticky= W)
        password_label.grid(row=2, column=0, pady = 2, sticky= E)
        password_entry.grid(row=2, column=1, pady = 2, sticky= W)

    """
    Build GUI elements to update settings & manually send digest email
    """
    def __build_gui_controls(self, master):
        # create widgest
        update_button = Button(master, text='Update Settings', command = self.__update_settings, fg='green')
        send_button = Button(master, text='Send Manually', command = self.__manual_send, fg='green')

        # place GUI widgets using grid geometry manager
        update_button.grid(row=0, column=0, padx=5, pady=5)
        send_button.grid(row=0, column=1, padx=5, pady=5)
    
    """
    Callback function to add recipient
    """
    def __add_recipients(self):
        new_recipient = self.__add_recipient_var.get()
        if new_recipient != '':
            recipient_list = self.__recipient_list_var.get()
            if recipient_list != '':
                self.__recipient_list_var.set(recipient_list + (new_recipient,)) 
            else:
                self.__recipient_list_var.set([new_recipient])
            self.__add_recipient_var.set('')
    
    """
    Callback function to remove selected recipient(s)
    """
    def __remove_selected_recipients(self, selection):

        recipient_list = list(self.__recipient_list_var.get())
        for index in reversed(selection):
            recipient_list.pop(index)
        self.__recipient_list_var.set(recipient_list)

    """
    Callback function to update settings
    """ 
    def __update_settings(self):
        print('Updating settings...')
        self.__list_of_emails.recipients_list = list(self.__recipient_list_var.get())

        self.__list_of_emails.content['quote']['include'] = self.__quote_var.get()
        self.__list_of_emails.content['weather']['include'] = self.__weather_var.get()
        self.__list_of_emails.content['twitter']['include'] = self.__twitter_var.get()
        self.__list_of_emails.content['wikipedia']['include'] = self.__wikipedia_var.get()

        self.__list_of_emails.sender_credentials = {'email': self.__username_var.get(),
                                                    'password': self.__password_var.get()}
        
        self.__scheduler.schedule_daily(int(self.__hour_var.get()),
                                        int(self.__minute_var.get()),
                                        self.__list_of_emails.send_email)
        
    """
    Callback function to manually send digest email
    """ 
    def __manual_send(self):
        # note: settings are not updated before manual send
        print('Sending..')
        self.__list_of_emails.send_email()
    
    """
    Shutdown the scheduler before closing the GUI window
    """

    def __shutdown_self(self):
        print('Shutting down the scheduler...')
        self.__scheduler.stop()
        self.__scheduler.join()
        self.__root.destroy() # close the gui
        
        
if __name__=='__main__':
    root = Tk()
    app = DailyDigestGui(root)
    root.mainloop()
    