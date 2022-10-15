from tkinter import *
from tkinter import simpledialog
from tkinter import *
import tkinter.messagebox
import customtkinter
import dd_email

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class DailyDigestGui(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    # list_of_emails = DailyDigestEmail()

    def __init__(self):
        super().__init__()

        self.title("Daily Digest User Interface")
        self.geometry(f"{DailyDigestGui.WIDTH}x{DailyDigestGui.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.list_of_emails = dd_email.DailyDigestEmail()
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
    
        """

        The GUI should enable the admin to...
            - configure which content sources to include in email
            - add recipients
            - remove recipients
            - schedule daily time to send email
            - configure sender credential

        """
        #### Checkboxes to activate deactivate the application's functionality ###
        listbox = Listbox(master=self.frame_right)
        for i in self.list_of_emails.recipients_list:
            listbox.insert(END, i)
        listbox.grid(rowspan=10)
        all_iems = listbox.get(0, END)

        b1 = Button(self.frame_right, text="Add to list", font=("purisa", 10, "bold"))
        b1.grid(row=11, column=0, columnspan=1)

        b2 = Button(self.frame_right, text="Remove from list", font=("purisa", 10, "bold"))
        b2.grid(row=11, column=1, columnspan=1)

        def add_item():
            item = simpledialog.askstring("Input", "Enter email recipients:")
            if item is not None:
                listbox.insert('end', item)
        def remove_item():
            index = listbox.curseselection()
            listbox.delete(index)

        # listbox.insert(self.list_of_emails.recipients_list)

        # combobox = customtkinter.CTkComboBox(master=self.frame_right,
        #                                     values=self.list_of_emails.recipients_list)
        # combobox.pack(padx=20, pady=10)
        # combobox.set("option 2")
    
        # check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                             text="Random Quote", onvalue="on", offvalue="off")
        # check_box_1.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        
        # check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                             text="Weather Forecast", onvalue="on", offvalue="off")
        # check_box_2.grid(row=3, column=0, pady=10, padx=20, sticky="w")
        
        # check_box_3 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                             text="Twitter Trends", onvalue="on", offvalue="off")
        # check_box_3.grid(row=4, column=0, pady=10, padx=20, sticky="w")
        
        # check_box_4 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                             text="Wikipedia Article", onvalue="on", offvalue="off")
        # check_box_4.grid(row=5, column=0, pady=10, padx=20, sticky="w")
        
        # check_status = {"check_quote":check_box_1.get(), 
        #                 "check_weather":check_box_2.get(), 
        #                 "check_twitter":check_box_3.get(), 
        #                 "check_wikipedia":check_box_4.get()
        #                 }
       


    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

if __name__=='__main__':
    # root = Tk()
    app = DailyDigestGui()
    # check_box = app.include_content()
    # if check_box:
    #     print(check_box['check_quote'])
    #     print(check_box['check_weather'])
    #     print(check_box['check_twitter'])
    #     print(check_box['check_wikipedia'])
    app.mainloop()