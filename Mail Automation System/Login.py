import sys
import tkinter as tk
import os
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from app import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoginInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login System")
        
        self.create_widgets()

    def create_widgets(self):
        image = Image.open(resource_path('H&M.png'))
        image = image.resize((200, 150))
        self.tk_image = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self.window, image=self.tk_image)
        self.email_label = tk.Label(self.window, text="Email:")
        self.text_label = tk.Label(self.window, text="This is a Demo Version")
        self.security_code_label = tk.Label(self.window, text="Security Code:")

        self.email_entry = tk.Entry(self.window, width=50, justify="left")
        self.security_code_entry = tk.Entry(self.window, width=50, justify="left", show="*")

        self.security_code_visibility = tk.BooleanVar(value=False)

        self.security_code_eye_icon = ttk.Button(
            self.window, 
            text="👁", 
            command=self.toggle_security_code_visibility
        )

        self.login_button = tk.Button(self.window, text="Login", command=self.login)
        self.image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.text_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.email_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        self.security_code_label.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.security_code_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.security_code_eye_icon.grid(row=4, column=2, padx=(0, 10), pady=10, sticky="e")
        self.login_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def toggle_security_code_visibility(self):
        if self.security_code_visibility.get():
            self.security_code_entry.config(show="*")
        else:
            self.security_code_entry.config(show="")
        self.security_code_visibility.set(not self.security_code_visibility.get())

    def login(self):
        email = self.email_entry.get()
        security_code = self.security_code_entry.get()

        # Replace with your predetermined security code
        predetermined_security_code = "123456"

        if security_code == predetermined_security_code:
            messagebox.showinfo("Success", "Login Successful!")
            self.window.destroy()
            email_sender = EmailSenderGUI(email)
            email_sender.run()
        else:
            messagebox.showerror("Error", "Login Failed. Incorrect Security Code.")

    def run(self):
        self.window.mainloop()

# Create an instance of the LoginInterface class and run the GUI
app_pass = "tpolcgctgispolqd" #hbdaqgcmqwgzejxj
login_interface = LoginInterface()
login_interface.run()
