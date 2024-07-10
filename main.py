import bluetooth
import time
import cv2
import numpy as np
from camera_driver import Camera
from electrodes_driver import Electrodes
from ble_driver import BionicEyeBLE

def find_bionic_eye():
    target_name = "BionicEye"
    nearby_devices = bluetooth.discover_devices()

    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name(bdaddr):
            return bdaddr
    return None

def connect_bionic_eye(address):
    ble = BionicEyeBLE()
    ble.connect(address)
    return ble

def send_command(ble, command):
    ble.send(command.encode())
    time.sleep(1)
    data = ble.receive(1024)
    print(f"Response: {data.decode()}")

def calibrate_system(ble):
    print("Calibrating system...")
    send_command(ble, 'C')

def capture_and_process_image(ble, camera):
    print("Capturing and processing image...")
    send_command(ble, 'P')
    image_data = camera.capture_image()
    display_image(image_data)

def send_file(ble, filename):
    print(f"Sending file '{filename}' to BionicEye...")
    send_command(ble, 'F')  # Indicar al dispositivo que se enviará un archivo
    time.sleep(1)
    with open(filename, 'rb') as f:
        data = f.read()
        ble.send(data)
        time.sleep(1)
    print("File transfer completed.")

def scan_signals(ble):
    print("Scanning for signals...")
    send_command(ble, 'S')
    time.sleep(5)  # Esperar tiempo suficiente para que se completen las exploraciones
    data = ble.receive(4096).decode()
    print("Signals detected:\n", data)

def display_image(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imshow('Captured Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    address = find_bionic_eye()
    if not address:
        print("Could not find BionicEye device")
        return

    ble = connect_bionic_eye(address)
    camera = Camera(i2c_scl=5, i2c_sda=4, spi_sck=18, spi_mosi=19, spi_miso=20)
    electrodes = Electrodes(pin1=2, pin2=3)
    print("Connected to BionicEye")

    while True:
        print("\nOptions:")
        print("1. Calibrate System")
        print("2. Capture and Process Image")
        print("3. Send File to BionicEye")
        print("4. Scan for Signals")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            calibrate_system(ble)
        elif choice == '2':
            capture_and_process_image(ble, camera)
        elif choice == '3':
            filename = input("Enter the filename to send: ")
            send_file(ble, filename)
        elif choice == '4':
            scan_signals(ble)
        elif choice == '5':
            ble.close()
            camera.release()
            print("Connection closed.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
