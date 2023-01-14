import requests
import serial
import time
 
api = input("API Linki(örnek: https://api.genelpara.com/embed/doviz.json) :")
 
geridonus = requests.get(api)
 
arduport = input("Arduinonun Bağlı Olduğu Port: ")
maxv = input("bitcoin kaçı geçerse yeşil yansın")
minv = input("bitcoin kaçın altına düşerse kırmızı yansın")
arduino = serial.Serial(arduport, 9600)
while True:
    btc = geridonus.json()["BTC"]["satis"]
    usd = geridonus.json()["USD"]["satis"]
    bitcointl = float(btc) * float(usd)
 
    if bitcointl > float(maxv):
        arduino.write(b"green")
    elif bitcointl < float(minv):
        arduino.write(b"red")
    time.sleep(1)
    print(bitcointl)
