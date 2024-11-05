import serial
import requests

with serial.Serial('COM6', 9600) as ser:
    while True:
        bytes_serial = ser.inWaiting()

        if bytes_serial > 0:
            message = ser.readline().decode().strip()
            print(f"Received: {message}")

            response = requests.post('http://127.0.0.1:5000/mark_order_completed', json = {"message": message}) 
            
            if response.status_code == 200:
                print(f"Data sent successfully from the client: {message}")
