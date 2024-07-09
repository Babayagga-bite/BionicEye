import bluetooth
import time
import cv2
import numpy as np

def find_bionic_eye():
    target_name = "BionicEye"
    nearby_devices = bluetooth.discover_devices()

    for bdaddr in nearby_devices:
        if target_name == bluetooth.lookup_name(bdaddr):
            return bdaddr
    return None

def connect_bionic_eye(address):
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((address, port))
    return sock

def send_command(sock, command):
    sock.send(command)
    time.sleep(1)
    data = sock.recv(1024)
    print(f"Response: {data.decode()}")

def calibrate_system(sock):
    print("Calibrating system...")
    send_command(sock, 'C')

def capture_and_process_image(sock):
    print("Capturing and processing image...")
    send_command(sock, 'P')
    time.sleep(2)  # Esperar tiempo suficiente para que se procese la imagen en el dispositivo

def send_file(sock, filename):
    print(f"Sending file '{filename}' to BionicEye...")
    with open(filename, 'rb') as f:
        data = f.read()
        sock.send(data)
        time.sleep(1)
    print("File transfer completed.")

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

    sock = connect_bionic_eye(address)
    print("Connected to BionicEye")

    while True:
        print("\nOptions:")
        print("1. Calibrate System")
        print("2. Capture and Process Image")
        print("3. Send File to BionicEye")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            calibrate_system(sock)
        elif choice == '2':
            capture_and_process_image(sock)
            image_data = b''
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                image_data += chunk
            display_image(image_data)
        elif choice == '3':
            filename = input("Enter the filename to send: ")
            send_file(sock, filename)
        elif choice == '4':
            sock.close()
            print("Connection closed.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
