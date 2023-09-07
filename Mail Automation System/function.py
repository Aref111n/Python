import tkinter as tk
from tkinter import messagebox
import time
import imaplib
import email
import smtplib, ssl  
from email import utils
from Timesplit import *
from New_interface import *
import win32com.client 
import pythoncom
import os
from datetime import datetime, timedelta

def Send_Email(Target_email, Subject, Body, cc=None, bcc=None):
    ol = win32com.client.Dispatch('Outlook.Application', pythoncom.CoInitialize())
    olmailitem = 0x0
    newmail = ol.CreateItem(olmailitem)
    newmail.Subject = Subject
    newmail.To = Target_email
    newmail.CC = cc
    newmail.Body= Body
    #attach = 'C:\\Users\\admin\\Desktop\\Python\\Sample.xlsx'
    #newmail.Attachments.Add(attach)
    #newmail.Display()
    newmail.Send()

def check_reply(Target_email, dttime):
    outlook = win32com.client.Dispatch('outlook.application', pythoncom.CoInitialize())
    mapi = outlook.GetNamespace("MAPI")

    for account in mapi.Accounts:
        print(account.DeliveryStore.DisplayName)

    inbox = mapi.GetDefaultFolder(6)
    latest_message = inbox.Items
    reversed(latest_message)
    msg = latest_message[0]
    if msg:
        received_time = msg.ReceivedTime.replace(tzinfo=None)
        sender = msg.SenderEmailAddress
        if received_time > dttime and sender==Target_email:
            return 1

    return 0





    # Connect to the IMAP server
    # IMAP_SERVER = 'imap.gmail.com'
    # domain = Self_email.split("@")[1].split(".")[0]
    # if domain=="outlook":
    #     IMAP_SERVER = 'outlook.office365.com'
    # IMAP_PORT = 993
    # mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    # mail.login(Self_email, password)
    # mail.select('INBOX')
    # status, email_ids = mail.search(None, 'ALL')
    # email_ids = email_ids[0].split()
    # p=0
    # for email_id in reversed(email_ids):
    #     status, email_data = mail.fetch(email_id, '(RFC822)')

    #     raw_email = email_data[0][1]
    #     msg = email.message_from_bytes(raw_email)

    #     from_address = msg['From']
    #     subject = msg['Subject']
    #     date_string = msg['Date']
        
    #     day, month, year, hour, minute, second = extract_date_components(date_string)
    #     timestamp = get_unix_timestamp(year, month, day)
    #     timestamp += (hour*60*60) + (minute*60) + second
    #     if timestamp > sent_time and Target_email in from_address:
    #         p=1
    #     break

    # mail.logout()
    # return p
