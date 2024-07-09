from machine import Pin

class Electrodes:
    def __init__(self, pin1, pin2):
        self.stim_pin1 = Pin(pin1, Pin.OUT)
        self.stim_pin2 = Pin(pin2, Pin.OUT)

    def activate_stimulus(self):
        self.stim_pin1.on()
        self.stim_pin2.off()

    def deactivate_stimulus(self):
        self.stim_pin1.off()
        self.stim_pin2.off()

