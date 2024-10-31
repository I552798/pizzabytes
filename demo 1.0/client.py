import serial
import requests

with serial.Serial('COM6', 9600, timeout=1) as ser:
    while True:
        # Check how many characters are in the serial buffer
        bytes_serial = ser.inWaiting()

        # Only read if data is available
        if bytes_serial > 0:

            # Read the byte array, decode it to a string, and remove newline characters
            message = ser.readline().decode().strip()
            print(f"Received: {message}") # Debugging

            response = requests.post('http://127.0.0.1:5000/mark_order_completed', json = {"message": message}) # Send a post requst to the "/data" path
            
            if response.status_code == 200: # "200" is the status code for successful requests
                print(f"Data sent successfully from the client: {message}") # Debugging
