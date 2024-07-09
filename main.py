from camera_driver import Camera
from electrodes_driver import Electrodes
from ble_driver import BionicEyeBLE
from time import sleep

# Configurar la cámara
camera = Camera(i2c_scl=5, i2c_sda=4, spi_sck=18, spi_mosi=19, spi_miso=20)

# Configurar los electrodos
electrodes = Electrodes(pin1=2, pin2=3)

# Configurar Bluetooth
ble = BionicEyeBLE()

def capture_and_process_image():
    # Capturar y procesar la imagen
    camera.capture_image()
    light_intensity = 0
    pixel_count = 0
    for i in range(1000):  # Ejemplo simple de procesamiento
        pixel = camera.spi.read(1)[0]
        light_intensity += pixel
        pixel_count += 1
    light_intensity //= pixel_count
    generate_stimulation_pattern(light_intensity)

def generate_stimulation_pattern(intensity):
    if intensity > 128:
        electrodes.activate_stimulus()
    else:
        electrodes.deactivate_stimulus()

# Ciclo principal
while True:
    ble.send(b'Ready')
    command = ble.ble.gatts_read(0).decode()
    if command == 'C':
        for _ in range(10):
            electrodes.activate_stimulus()
            sleep(0.1)
            electrodes.deactivate_stimulus()
            sleep(0.1)
    elif command == 'P':
        capture_and_process_image()
    sleep(1)

