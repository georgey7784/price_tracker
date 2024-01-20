# Import Libraries
import pandas as pd, tkinter as tk, requests as r, PySimpleGUI as sg
import bs4, schedule, time, csv, smtplib, ssl, os.path
from datetime import datetime
from email.message import EmailMessage
from tracker import price_tracker


def close_application():
    window.destroy()

def caps_to(event):
    buy_price1.set(buy_price1.get().upper())
    if len(buy_price1()) > 3: buy_price1.set(buy_price1.get()[:3])

def caps_from(event):
    tracking_items1.set(tracking_items1.get().upper())
    if len(tracking_items1()) > 3: tracking_items1.set(tracking_items1.get()[:3])

def run_app():
    print("App run!")
    bot = price_tracker()



window =tk.Tk()


window.title("Amazon Price Tracker")
frame_header = tk.Frame(master = window, borderwidth=2, pady=2)
centre_frame = tk.Frame(window, borderwidth=2, pady=5)
bottom_frame = tk.Frame(window, borderwidth=2, pady=5)
frame_header.grid(row=0, column=0)
centre_frame.grid(row=1, column=0)
bottom_frame.grid(row=2, column=0)

header = tk.Label(frame_header, text = "Amazon Price Tracker",
                  bg='grey', fg='black', height='3', width='50')
header.grid(row=0, column=0)

frame_main_1 = tk.Frame(centre_frame, borderwidth=2, relief='sunken')
frame_main_2 = tk.Frame(centre_frame, borderwidth=2, relief='sunken')

tracking_items = tk.Label(frame_main_1, text = "Items: ")
buy_price = tk.Label(frame_main_2, text = "To: ")


tracking_items1 = tk.StringVar()
buy_price1 = tk.StringVar()


tracking_items_entry = tk.Entry(frame_main_1, textvariable = tracking_items1, width=4)
buy_price_entry = tk.Entry(frame_main_2, textvariable = buy_price1, width=4)

button_run = tk.Button(bottom_frame, text="Start", command=run_app, bg='green', 
                       fg='white', relief='raised', width=10)
button_run.grid(column=0, row=0, sticky='w', padx=100, pady=2)

button_close = tk.Button(bottom_frame, text="Exit", command=close_application, bg='red', 
                       fg='white', relief='raised', width=10)
button_close.grid(column=1, row=0, sticky='e', padx=100, pady=2)

frame_main_1.pack(fill='x', pady=2)
frame_main_2.pack(fill='x', pady=2)
tracking_items.pack(side='left')
tracking_items_entry.pack(side='left', padx=1)
buy_price.pack(side='left')
buy_price_entry.pack(side='left', padx=1)

window.mainloop()

