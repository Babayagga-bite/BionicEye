
import bluetooth
import time
from electrodes_driver import Electrodes
import os
import subprocess

# Configurar los electrodos
electrodes = Electrodes(pin1=2, pin2=3)

def generate_stimulation_from_file(file_content):
    # Interpreta el contenido del archivo y genera estímulos eléctricos
    for line in file_content.splitlines():
        command, duration = line.split(',')
        duration = float(duration)
        if command == 'activate':
            electrodes.activate_stimulus()
        elif command == 'deactivate':
            electrodes.deactivate_stimulus()
        time.sleep(duration)

def receive_file(sock):
    file_data = b''
    while True:
        data = sock.recv(1024)
        if not data:
            break
        file_data += data
    return file_data.decode()

def detect_wifi_signals():
    # Usa la herramienta 'iwlist' para escanear las redes WiFi cercanas
    result = subprocess.run(['iwlist', 'scan'], capture_output=True, text=True)
    return result.stdout

def detect_bluetooth_signals():
    # Usa la herramienta 'hcitool' para escanear dispositivos Bluetooth cercanos
    result = subprocess.run(['hcitool', 'scan'], capture_output=True, text=True)
    return result.stdout

def generate_visual_pattern_from_signals(wifi_data, bluetooth_data):
    # Genera un patrón visual basado en los datos de señales WiFi y Bluetooth
    pattern = f"WiFi Signals: {wifi_data}\nBluetooth Signals: {bluetooth_data}"
    return pattern

def main():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)

    print("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    while True:
        try:
            command = client_sock.recv(1024).decode()
            if command == 'C':
                print("Calibrating system...")
                # Implementar la calibración aquí
            elif command == 'P':
                print("Capturing and processing image...")
                # Implementar la captura y procesamiento de imagen aquí
            elif command == 'F':
                print("Receiving file...")
                file_content = receive_file(client_sock)
                print("File received. Generating stimulation pattern...")
                generate_stimulation_from_file(file_content)
            elif command == 'S':
                print("Scanning for signals...")
                wifi_data = detect_wifi_signals()
                bluetooth_data = detect_bluetooth_signals()
                visual_pattern = generate_visual_pattern_from_signals(wifi_data, bluetooth_data)
                # Enviar el patrón visual al cerebro (electrodos)
                generate_stimulation_from_file(visual_pattern)
        except Exception as e:
            print(f"Error: {e}")
            break

    client_sock.close()
    server_sock.close()

if __name__ == '__main__':
    main()
