from camera_driver import Camera
from electrodes_driver import Electrodes
from ble_driver import BionicEyeBLE
import network
import ubluetooth
from time import sleep

# Configurar la cámara
camera = Camera(i2c_scl=5, i2c_sda=4, spi_sck=18, spi_mosi=19, spi_miso=20)

# Configurar los electrodos
electrodes = Electrodes(pin1=2, pin2=3)

# Configurar Bluetooth
ble = BionicEyeBLE()

# Configurar WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Configurar Bluetooth
ble = ubluetooth.BLE()
ble.active(True)

def on_rx(v):
    print("Received via Bluetooth:", v)

ble.irq(handler=lambda e: on_rx(ble.read().decode('utf-8')))

# Funciones de control de electrodos
def activate_stimulus():
    electrodes.activate_stimulus()

def deactivate_stimulus():
    electrodes.deactivate_stimulus()

# Captura y procesamiento de imagen mejorado
def capture_and_process_image():
    # Capturar y procesar la imagen
    camera.capture_image()
    
    # Procesamiento avanzado para determinar la intensidad de luz
    light_intensity = camera.calculate_average_light_intensity()
    
    # Generar patrón de estimulación basado en la intensidad de luz
    generate_stimulation_pattern(light_intensity)

# Generar patrón de estimulación según la intensidad de luz
def generate_stimulation_pattern(intensity):
    # Ajustar los parámetros de estimulación según la intensidad de luz
    if intensity > 128:
        activate_stimulus()
    else:
        deactivate_stimulus()

# Ciclo principal
while True:
    # Capturar señales WiFi y Bluetooth
    wifi_signals, bt_signals = wlan.scan(), ble.gap_scan(1000, 30000, 30000)
    print("WiFi Signals:", wifi_signals)
    print("Bluetooth Signals:", bt_signals)
    
    # Enviar señal Bluetooth de listo
    ble.send(b'Ready')
    
    # Leer comando recibido por Bluetooth
    command = ble.ble.gatts_read(0).decode()
    
    # Procesar comando recibido
    if command == 'C':
        # Activar y desactivar estimulación durante 1 segundo
        for _ in range(10):
            activate_stimulus()
            sleep(0.1)
            deactivate_stimulus()
            sleep(0.1)
    elif command == 'P':
        # Capturar y procesar imagen
        capture_and_process_image()
    
    # Esperar 1 segundo antes de continuar al siguiente ciclo
    sleep(1)
