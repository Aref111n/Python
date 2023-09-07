import tkinter as tk
from tkinter import messagebox
import time
import imaplib
import email
import smtplib, ssl  
from email import utils
from datetime import datetime, timezone
from Timesplit import *
from New_interface import *
from function import *

class EmailSenderGUI:
    def __init__(self, Self_email):
        self.window = tk.Tk()
        self.window.title("Email Sender")
        self.Self_email = Self_email
        self.time_period = 30
        self.template_messages =  [
            '''<<<REMINDER >>>
Hi,
Good day. Please revert with the price by today.
 
Best Regards,
Shohedullah Sojib''',
            '''<<<REMINDER >>>
 
Hi,
Good day. We are still waiting for your reply.
 
Best Regards,
Shohedullah Sojib'''
        ]
        self.child_window = None
        self.create_widgets()
    

    def create_widgets(self):
        self.to_label = tk.Label(self.window, text="To:")
        self.cc_label = tk.Label(self.window, text="Cc:")
        self.subject_label = tk.Label(self.window, text="Subject:")
        self.message_label = tk.Label(self.window, text="Message:")

        self.to_entry = tk.Entry(self.window, width=50, justify="left")
        self.cc_entry = tk.Entry(self.window, width=50, justify="left")
        self.subject_entry = tk.Entry(self.window, width=50, justify="left")
        self.message_entry = tk.Text(self.window, width=50, height=5, wrap="word", padx=2, pady=2, spacing3=2, relief=tk.SOLID, bd=1)

        self.scrollbar = tk.Scrollbar(self.window)
        self.scrollbar.config(command=self.message_entry.yview)
        self.message_entry.config(yscrollcommand=self.scrollbar.set)

        self.button = tk.Button(self.window, text="Change Automated Mail Settings", command=self.open_another_window)
        self.submit_button = tk.Button(self.window, text="Submit", command=self.send_email)

        self.to_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.to_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.cc_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.cc_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.subject_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.subject_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.message_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.message_entry.grid(row=3, column=1, padx=10, pady=10, rowspan=5, sticky="w")
        self.scrollbar.grid(row=3, column=2, rowspan=5, sticky="ns")
        self.button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
        self.submit_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    def open_another_window(self):
        self.child_window = tk.Toplevel()
        template_interface = TemplateInterface(self.child_window, self.process_input)
        template_interface.run()
        # Send email functionality here
    
    def process_input(self, val1, val2):
        self.template_messages = val1
        self.time_period = val2
        print(self.time_period, self.template_messages)

    def send_email(self):
        print(self.template_messages)
        to_email = self.to_entry.get()
        cc = self.cc_entry.get()
        subject = self.subject_entry.get()
        message = self.message_entry.get("1.0", tk.END)
        # Message = "Subject: " + subject + '\n' + message

        messagebox.showinfo("Confirm", f"Sending message to: {to_email}")
        try:
            Send_Email(to_email, subject, message, cc)   
        except:
            messagebox.showerror("Error", "Message can not be sent!!!")
        else: 
            messagebox.showinfo("Success", f"Message sent successfully")    
            sent_time = time.time()
            dt = datetime.now(timezone.utc).replace(tzinfo=None)
            self.window.destroy()
            ui = InfoInterface(self.Self_email, to_email, sent_time, dt, subject, self.time_period, self.template_messages, cc)
            ui.run()

    def run(self):
        self.window.mainloop()

# Create an instance of the EmailSenderGUI class and run the GUI

class TemplateInterface():
    def __init__(self, parent, callback):
        self.callback = callback
        self.window = parent
        self.window.title("Template Interface")
        self.minutes = 30
        self.template_lines = [
            '''<<<REMINDER >>>
Hi,
Good day. Please revert with the price by today.
 
Best Regards,
Shohedullah Sojib''',
            '''<<<REMINDER >>>
 
Hi,
Good day. We are still waiting for your reply.
 
Best Regards,
Shohedullah Sojib'''
        ]

        self.create_widgets()

    def create_widgets(self):
        self.minutes_label = tk.Label(self.window, text="Automated templates will be sent after ")
        self.minutes_entry = tk.Entry(self.window, width=5)
        self.minutes_entry.insert(tk.END, self.minutes)
        self.minutes_label2 = tk.Label(self.window, text=" seconds")

        self.template_label = tk.Label(self.window, text="Template Lines:")
        self.template_listbox = tk.Listbox(self.window, width=50)
        for line in self.template_lines:
            self.template_listbox.insert(tk.END, line)

        self.up_button = tk.Button(self.window, text="Move Up", command=self.move_up)
        self.down_button = tk.Button(self.window, text="Move Down", command=self.move_down)
        self.edit_button = tk.Button(self.window, text="Edit", command=self.edit_line)
        self.delete_button = tk.Button(self.window, text="Delete", command=self.delete_line)
        self.add_button = tk.Button(self.window, text="Add Line", command=self.add_line)
        self.save_button = tk.Button(self.window, text="Save", command=self.save_lines)

        self.minutes_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.minutes_entry.grid(row=0, column=1, padx=5, pady=10)
        self.minutes_label2.grid(row=0, column=2, sticky="w", pady=10)
        self.template_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.template_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        self.up_button.grid(row=2, column=3, padx=5, pady=5, sticky="n")
        self.down_button.grid(row=2, column=3, padx=5, pady=5, sticky="s")
        self.edit_button.grid(row=3, column=0, padx=10, pady=5)
        self.delete_button.grid(row=3, column=1, padx=5, pady=5)
        self.add_button.grid(row=3, column=2, padx=5, pady=5)
        self.save_button.grid(row=4, column=1, padx=5, pady=5)

    def save_lines(self):
        val1 = self.template_lines
        val2 = self.minutes_entry.get()
        self.callback(val1, val2)
        self.window.destroy()

    def move_up(self):
        selected_index = self.template_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index > 0:
                line = self.template_lines.pop(index)
                self.template_lines.insert(index - 1, line)
                self.update_template_listbox()

    def move_down(self):
        selected_index = self.template_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            if index < len(self.template_lines) - 1:
                line = self.template_lines.pop(index)
                self.template_lines.insert(index + 1, line)
                self.update_template_listbox()

    def edit_line(self):
        selected_index = self.template_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            line = self.template_lines[index]
            edit_window = tk.Toplevel(self.window)
            edit_window.title("Edit Line")
            edit_label = tk.Label(edit_window, text="Enter the new line:")
            edit_entry = tk.Entry(edit_window, width=50)
            edit_entry.insert(tk.END, line)
            update_button = tk.Button(edit_window, text="Update", command=lambda: self.update_line(index, edit_entry.get(), edit_window))

            edit_label.pack(padx=10, pady=10)
            edit_entry.pack(padx=10, pady=5)
            update_button.pack(padx=10, pady=10)

    def update_line(self, index, line, edit_window):
        self.template_lines[index] = line
        self.update_template_listbox()
        edit_window.destroy()

    def delete_line(self):
        selected_index = self.template_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            self.template_lines.pop(index)
            self.update_template_listbox()

    def add_line(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Add Line")
        add_label = tk.Label(add_window, text="Enter the new line:")
        add_entry = tk.Entry(add_window, width=50)
        add_button = tk.Button(add_window, text="Add", command=lambda: self.add_new_line(add_entry.get(), add_window))

        add_label.pack(padx=10, pady=10)
        add_entry.pack(padx=10, pady=5)
        add_button.pack(padx=10, pady=10)

    def add_new_line(self, line, add_window):
        self.template_lines.append(line)
        self.update_template_listbox()
        add_window.destroy()

    def update_template_listbox(self):
        self.template_listbox.delete(0, tk.END)
        for line in self.template_lines:
            self.template_listbox.insert(tk.END, line)

    def run(self):
        self.window.mainloop()
