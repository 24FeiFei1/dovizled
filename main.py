import tkinter as tk
from tkinter import ttk
import requests
import serial.tools.list_ports
import time

root = tk.Tk()
root.title("Dovizled")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 300
window_height = 300

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

api_url = "https://api.genelpara.com/embed/doviz.json"

currency_combobox = ttk.Combobox(root, state="readonly")
currency_combobox.pack()

port_combobox = ttk.Combobox(root, state="readonly")
port_combobox.pack()

result_label = tk.Label(root, text="")
result_label.configure(bg=root.cget("bg"))
result_label.pack()

last_exchange_rate = 0

def get_exchange_rates():
    response = requests.get(api_url)
    data = response.json()

    currency_data = {}
    for currency, values in data.items():
        currency_data[currency] = f"Alış: {values['alis']} - Satış: {values['satis']}"

    currency_combobox["values"] = list(currency_data.keys())
    currency_combobox.current(0)

    def on_currency_selected(event):
        selected_currency = currency_combobox.get()
        result_label.config(text=currency_data[selected_currency])
        currency_combobox.pack_forget()

    currency_combobox.bind("<<ComboboxSelected>>", on_currency_selected)

def auto_update():
    get_exchange_rates()
    check_exchange_rate()
    root.after(5000, auto_update)

def connect_serial():
    selected_port = port_combobox.get()
    try:
        ser = serial.Serial(selected_port, 9600)
        return ser
    except serial.SerialException:
        error_label.config(text="Porta bağlanılamadı. Lütfen tekrar seçin.")
        return None

def send_message(ser, message):
    ser.write(message.encode())

def check_exchange_rate():
    selected_currency = currency_combobox.get()
    response = requests.get(api_url)
    data = response.json()
    exchange_rate = float(data[selected_currency]["satis"])

    if port_combobox.get():
        ser = connect_serial()

        global last_exchange_rate
        if ser is not None:
            if exchange_rate > last_exchange_rate:
                send_message(ser, "G\n")  # "\n" satır sonu karakterini ekleyin
                root.configure(background="green")
            elif exchange_rate < last_exchange_rate:
                send_message(ser, "R\n")  # "\n" satır sonu karakterini ekleyin
                root.configure(background="red")
            else:
                send_message(ser, "Same\n")  # "\n" satır sonu karakterini ekleyin

        last_exchange_rate = exchange_rate
        if ser is not None:
            ser.close()

def populate_serial_ports():
    available_ports = serial.tools.list_ports.comports()
    connected_ports = [port.device for port in available_ports]
    port_combobox["values"] = connected_ports
    if len(connected_ports) > 0:
        port_combobox.current(0)

def connect_button_clicked():
    check_exchange_rate()
    port_combobox.pack_forget()
    connect_button.pack_forget()

get_exchange_rates()
auto_update()
populate_serial_ports()

connect_button = ttk.Button(root, text="Bağlan", command=connect_button_clicked)
connect_button.pack()

error_label = tk.Label(root, text="", fg="red")
error_label.configure(bg=root.cget("bg"))
error_label.pack()

root.mainloop()
