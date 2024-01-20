# Import Libraries
import pandas as pd, requests as r, tkinter as tk, PySimpleGUI as sg
import sys, bs4, schedule, time, csv, smtplib, ssl, gui, pandas
from threading import Thread
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from datetime import datetime
from email.message import EmailMessage

# Add product ID from the Amazon HTML here
product_list = ['B08H95Y452', 'B0CM9VKQ5N', 'B08H93GKNJ', 'B08GD9MNZB', 'B098TVDYZ3']
base_url = 'https://www.amazon.co.uk'
url = 'https://www.amazon.co.uk/dp/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

base_response = r.get(base_url, headers=headers)
cookies = base_response.cookies

# Load data from source 
gui_df = pd.read_csv("alert_df.csv")
past_results_df = pd.read_csv("alert_df.csv")  # Load past results

def close_application():
    print("Closing App!")
    window.destroy()

def run_app():
    global run_app
    print("App run!")
    bot = price_tracker()

window = tk.Tk()
window.attributes("-fullscreen", False) 
window.title("GeorgeM7784's Console Tracker")
window.rowconfigure(0, weight = 5) 
frame_header = tk.Frame(master = window, borderwidth=2, pady=2)
centre_frame = tk.Frame(window, borderwidth=2, pady=5)
bottom_frame = tk.Frame(window, borderwidth=2, pady=5)
frame_header.grid(row=0, column=0)
centre_frame.grid(row=1, column=0)
bottom_frame.grid(row=2, column=0)

class PriceTrackerApp():
    def __init__(self, window):
        self.window = window
        self.my_price_ps5 = 600
        self.my_price_ps5_digital = 200
        self.my_price_xsx = 250
        self.my_price_xss = 200
        self.my_price_switch = 200

        self.ps5_entry = tk.Entry(bottom_frame)
        self.ps5_entry.grid(row=1, column=0, padx=10, pady=5)
        self.ps5_entry.insert(0, str(self.my_price_ps5))
        self.ps5_digital_entry = tk.Entry(bottom_frame)
        self.ps5_digital_entry.grid(row=1, column=1, padx=10, pady=5)
        self.ps5_digital_entry.insert(0, str(self.my_price_ps5_digital))
        self.xsx_entry= tk.Entry(bottom_frame)
        self.xsx_entry.grid(row=1, column=2, padx=10, pady=5)
        self.xsx_entry.insert(0, str(self.my_price_ps5))
        self.xss_entry= tk.Entry(bottom_frame)
        self.xss_entry.grid(row=1, column=3, padx=10, pady=5)
        self.xss_entry.insert(0, str(self.my_price_ps5))
        self.switch_entry= tk.Entry(bottom_frame)
        self.switch_entry.grid(row=1, column=4, padx=10, pady=5)
        self.switch_entry.insert(0, str(self.my_price_ps5))

        # Buttons to update target prices
        self.update_ps5_button = tk.Button(bottom_frame, text="Update PS5", command=self.update_ps5)
        self.update_ps5_button.grid(row=2, column=0, padx=10, pady=5)
        self.update_ps5_digital_button = tk.Button(bottom_frame, text="Update PS5 Dig", command=self.update_ps5_digital)
        self.update_ps5_digital_button.grid(row=2, column=1, padx=10, pady=5)
        self.update_xsx_button = tk.Button(bottom_frame, text="Update XSX", command=self.update_xsx)
        self.update_xsx_button.grid(row=2, column=2, padx=10, pady=5)
        self.update_xss_button = tk.Button(bottom_frame, text="Update XSS", command=self.update_xss)
        self.update_xss_button.grid(row=2, column=3, padx=10, pady=5)
        self.update_switch_button = tk.Button(bottom_frame, text="Update Switch", command=self.update_switch)
        self.update_switch_button.grid(row=2, column=4, padx=10, pady=5)

    def update_ps5(self):
        new_price = self.ps5_entry.get()
        try:
            self.my_price_ps5 = int(new_price)
            print(f"PS5 price updated to {self.my_price_ps5}")
        except ValueError:
            print("Invalid input for PS5 price")

    def update_ps5_digital(self):
        new_price = self.ps5_digital_entry.get()
        try:
            self.my_price_ps5_digital = int(new_price)
            print(f"PS5 Digital price updated to {self.my_price_ps5_digital}")
        except ValueError:
            print("Invalid input for PS5 Digital price")
        
    def update_xsx(self):
        new_price = self.xsx_entry.get()
        try:
            self.my_price_xsx = int(new_price)
            print(f"XSX price updated to {self.my_price_xsx}")
        except ValueError:
            print("Invalid input for XSX price")

    def update_xss(self):
        new_price = self.xss_entry.get()
        try:
            self.my_price_xss = int(new_price)
            print(f"XSS price updated to {self.my_price_xss}")
        except ValueError:
            print("Invalid input for XSS price")   

    def update_switch(self):
        new_price = self.switch_entry.get()
        try:
            self.my_price_switch = int(new_price)
            print(f"Switch price updated to {self.my_price_switch}")
        except ValueError:
            print("Invalid input for Switch price")

    
def price_tracker():
    global alert_df
    print(datetime.now())
    # Create the Treeview outside the loop
    table = ttk.Treeview(window, columns=('Date', 'URL', 'Title', 'Current_price'))
    table.heading('Date', text='Date')
    table.heading('URL', text='URL')
    table.heading('Title', text='Title')
    table.heading('Current_price', text='Current_price')
    table.grid()

    for prod in product_list:
        product_response = r.get(url+prod, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(product_response.text, features='lxml')
        price_lines = soup.findAll(class_="a-price-whole")
        final_price = str(price_lines[0])
        final_price = final_price.replace('<span class="a-price-whole">', '')
        final_price = final_price.replace('<span class="a-price-decimal">.</span></span>', '')
        title_lines = soup.findAll(class_="a-size-large product-title-word-break")
        prod_title = str(title_lines[0])
        prod_title = prod_title.replace('<span class="a-size-large product-title-word-break" id="productTitle">', '').strip()
        prod_title = prod_title.replace('</span>', '').strip()
        print(url+prod, prod_title, final_price)
        price_tracker = []
        price_tracker = {'URL':[url+prod],
                         'Title':[prod_title], 
                         'Price':[final_price]
                         }
        price_tracker = pd.DataFrame(price_tracker, columns=['URL', 'Title', 'Price'])
        price_tracker.to_csv('price_tracker.csv', index=False, mode='a', sep=' ')
        final_price = int(final_price)



        # EMAIL NOTIFICATONS
        def email_notify():
            port = 465 
            smtp_server = "smtp.gmail.com"
            sender_email = "georgem7784@gmail.com"
            receiver_email = "georgem7784@gmail.com"
            password = 'tunj cszm bvvd emqb'
            subject = 'BUY NOW!'
            message = f"""
            {prod_title} Price has Dropped! Buy your product now!
            Link: {url+prod}"""
            em = EmailMessage()
            em['From'] = sender_email
            em['To'] = receiver_email
            em['Subject'] = subject
            em.set_content(message)
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, em.as_string())
                print("Message Sent")

        # Setting buy_now variable for each product 
                 
        my_price_ps5 = app.my_price_ps5
        my_price_ps5_digital = app.my_price_ps5_digital
        my_price_xsx = app.my_price_xsx
        my_price_xss = app.my_price_xss
        my_price_switch = app.my_price_switch
        alert_df = price_tracker
        alert_df = []
        # Using conditional statements to create a DF that only shows ALERTS
        if final_price <= my_price_ps5 and prod == 'B08H95Y452':
            alert_df = {'Date': [datetime.now()],
                        'URL': [url+prod],
                        'Title': [prod_title],
                        'Current_price': [final_price],
                        'target_price':[my_price_ps5]
            }

            email_notify()

        elif final_price <= my_price_ps5_digital and prod == 'B0CM9VKQ5N':
            alert_df = {'Date': [datetime.now()],
                        'URL': [url+prod],
                        'Title': [prod_title],
                        'Current_price': [final_price],
                        'target_price':[my_price_ps5_digital]
            }

            email_notify()

        elif final_price <= my_price_xsx and prod == 'B08H93GKNJ':
            alert_df = {'Date': [datetime.now()],
                        'URL': [url+prod],
                        'Title': [prod_title],
                        'Current_price': [final_price],
                        'target_price':[my_price_xsx]
            }

            email_notify()

        elif final_price <= my_price_xss and prod == 'B08GD9MNZB':
            alert_df = {'Date': [datetime.now()],
                        'URL': [url+prod],
                        'Title': [prod_title],
                        'Current_price': [final_price],
                        'target_price':[my_price_xss]
            }

            email_notify()

        elif final_price <= my_price_switch and prod == 'B098TVDYZ3':
            alert_df = {'Date': [datetime.now()],
                        'URL': [url+prod],
                        'Title': [prod_title],
                        'Current_price': [final_price],
                        'target_price':[my_price_switch]
            }

            email_notify()
        
        alert_df = pd.DataFrame(alert_df, columns=['Date', 'URL', 'Title', 'Current_price', 'target_price'])
        alert_df.to_csv('alert_df.csv', index=False, mode='a', sep=' ')  



        
        Date = datetime.now()
        URL = url + prod
        Title = prod_title
        Current_price = final_price
        data = (Date, URL, Title, Current_price)
        table.insert(parent='', index=0, values=data)

        def select_items():
            print(table.selection())
            for i in table.selection():
                print(table.item(i)['Current_price'])

        table.bind('<<TreeViewSelect>>', select_items)

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Amazon Price Tracker: Results")
    window.geometry('600x600')
    window.rowconfigure(0, weight=5)
    frame_header = tk.Frame(master=window, borderwidth=2, pady=2)
    centre_frame = tk.Frame(window, borderwidth=2, pady=5)
    bottom_frame = tk.Frame(window, borderwidth=2, pady=5)
    frame_header.grid(row=0, column=0)
    centre_frame.grid(row=1, column=0)
    bottom_frame.grid(row=2, column=0)


header = tk.Label(frame_header, text = "Amazon Price Tracker: Consoles",
                  bg='grey', fg='black', height='3', width='50')
header.grid(row=0, column=0)

button_run = tk.Button(centre_frame, text="Start", command=run_app, bg='green', 
                       fg='white', relief='raised', width=10)
button_run.grid(column=0, row=0, sticky='w', padx=100, pady=2)
button_close = tk.Button(centre_frame, text="Exit", command=close_application, bg='red', 
                       fg='white', relief='raised', width=10)
button_close.grid(column=1, row=0, sticky='e', padx=100, pady=2)

app = PriceTrackerApp(window)
window.mainloop()
# Schedule how often the function will run
schedule.every(1).hours.do(price_tracker)
price_tracker()

while True:
    schedule.run_pending()
    time.sleep(1)

