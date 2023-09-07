import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter.font as tkFont
import time
import imaplib
import email
import smtplib, ssl  
from email import utils
from datetime import datetime, timezone
from Timesplit import *
from function import *
import threading

class InfoInterface:
    def __init__(self, Self_email, to_email, sent_time, dt, subject, time_period, template_message, cc):
        self.current_status = 0
        self.self_email = Self_email
        self.to_email = to_email
        self.sent_time = sent_time
        self.current_status = "Waiting for Reply"
        self.subject = subject
        self.time_period = time_period
        self.process_terminated = False
        self.repeat_messages = template_message
        self.cc = cc
        self.dttime = dt

        self.window = tk.Tk()
        self.window.title("Status")
        bold_font = tkFont.Font(weight="bold")
        header_text = "Status: " + self.to_email
        self.title_label = tk.Label(self.window, text=header_text, font=bold_font)
        self.title_label.grid(row=0, column=0, padx=10, pady=10)

        self.info_text = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, height=10)
        self.info_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.stop_button = tk.Button(self.window, text="Stop Process", command=self.stop_process)
        self.stop_button.grid(row=2, column=0, padx=10, pady=10)

        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        self.thread = threading.Thread(target=self.CheckforReply)
        self.thread.start()
    
    def CheckforReply(self):
        t = 0
        tt = 0
        show_text = "mail sent, Waiting for reply"
        dtime = datetime.now()
        dtime = dtime.strftime("%Y-%m-%d %H:%M:%S")
        self.add_info(dtime + " " + show_text)
        while not self.process_terminated:
            if check_reply(self.to_email, self.dttime) == 0:
                curr_time = time.time()
                dtime = datetime.now()
                dtime = dtime.strftime("%Y-%m-%d %H:%M:%S")
                tp = int(self.time_period)
                if int((curr_time - self.sent_time) // tp) != tt:
                    tt += 1
                    if tt==1:
                        show_text = "1st follow up message sent"
                    elif tt==2:
                        show_text = "2nd follow up message sent"
                    elif tt==3:
                        show_text = "3rd follow up message sent"
                    else:
                        show_text = f"{tt}th follow up message sent"
                    # message = "Subject: " + self.subject + "\n" + self.repeat_messages[t]
                    # Send_Email(self.self_email, self.to_email, self.app_pass, message)
                    # send_email(self.subject, self.repeat_messages[t], self.self_email, self.to_email, self.app_pass, self.cc, self.bcc)
                    Send_Email(self.to_email, self.subject, self.repeat_messages[t], self.cc)
                    self.add_info(dtime + " " + show_text)
                    print(f"sent at {curr_time - self.sent_time} seconds")
                    t += 1
                    if t == len(self.repeat_messages):
                        t = 0
            else:
                break
        self.window.update_idletasks()

        if self.process_terminated:
            self.add_info(dtime + " Process Terminated")
        else:
            messagebox.showinfo("Success", f"New message from {self.to_email}")
            print(self.dttime)
            self.add_info(dtime + " New Message Arrived")

        self.stop_process()
    
    def stop_process(self):
        self.process_terminated = True

    def add_info(self, msg):
        line = msg
        self.info_text.insert(tk.END, line + "\n")
        self.info_text.see(tk.END)  # Scroll to the bottom to display the new line

    def run(self):
        self.window.mainloop()

# Create an instance of the InfoInterface class and run the GUI

