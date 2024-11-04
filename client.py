import serial
import requests

with serial.Serial('COM6', 9600) as ser:
    while True:
        # Check how many characters are in the serial buffer
        bytes_serial = ser.inWaiting()

        # Only read if data is available
        if bytes_serial > 0:
            message = ser.readline().decode().strip()
            print(f"Received: {message}")

            response = requests.post('http://127.0.0.1:5000/mark_order_completed', json = {"message": message}) 
            
            if response.status_code == 200: # "200" is the status code for successful requests
                print(f"Data sent successfully from the client: {message}")
