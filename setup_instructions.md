# Setup Instructions

## Hardware Setup

1. **Connect the Camera Module**:
    - Connect the camera module to the Raspberry Pi Pico as per the pin configuration mentioned in `camera_setup.py`.
      
Connections
 Solder I2C:

    SCL (camera) to GP5 (Pin 10) of the Pico.
    SDA (camera) to GP4 (Pin 9) of the Pico.

Solder SPI:

    SCK (camera) to GP18 (Pin 21) of the Pico.
    MOSI (camera) to GP19 (Pin 22) of the Pico.
    MISO (camera) to GP16 (Pin 16) of the Pico.
    CS (camera) to GP17 (Pin 17) of the Pico.

2. **Connect the Electrodes and Driver**:
    - Connect the electrodes to the Raspberry Pi Pico using the L293D driver as per the pin configuration mentioned in `electrodes_setup.py`.
      Conections
      Vcc1 (Pin 8): 3.3V (Pin 36) of Pico W
      Vcc2 (Pin 16): 3.3V (Pin 36) of Pico W
      GND (Pins 5, 12): GND (Pin 38) of the Pico W
      IN1 (Pin 2): GP2 (Pin 4) of the Pico W
      IN2 (Pin 7): GP3 (Pin 5) of the Pico W
      OUT1 (Pin 3): Electrode 1
      OUT2 (Pin 6): Electrode 2
      

3. **Connect the Battery**:
    - Connect the battery to the Raspberry Pi Pico using the charging module. Ensure the battery is properly charged.

4. **3D Print the Case**:
    - Design and print a case to house the components securely. Ensure there are openings for the camera and electrodes.

## Software Setup

1. **Install MicroPython on Raspberry Pi Pico**:
    - Follow the [official guide](https://www.raspberrypi.org/documentation/microcontrollers/micropython.html) to install MicroPython on your Raspberry Pi Pico.

2. **Upload MicroPython Scripts**:
    - Use the Thonny IDE to upload the MicroPython scripts (`camera_setup.py`, `electrodes_setup.py`, `ble_setup.py`, `main.py`) to the Raspberry Pi Pico.

3. **Install Python Dependencies on PC**:
    - Install the necessary Python packages on your PC:
        ```sh
        pip install pybluez opencv-python
        ```

4. **Run the Interface Script**:
    - Run the `interface.py` script on your PC to connect to the bionic eye and control its functionalities.

## Calibration and Usage

1. **Calibrate the System**:
    - Use the interface script to calibrate the system by selecting the "Calibrate System" option.

2. **Capture and Process Image**:
    - Use the interface script to capture and process images by selecting the "Capture and Process Image" option.

3. **View Captured Images**:
    - The captured images will be displayed on your PC screen for analysis and adjustments.
