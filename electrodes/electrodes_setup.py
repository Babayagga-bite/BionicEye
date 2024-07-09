from machine import Pin

# Configuración de pines para los electrodos
stim_pin1 = Pin(2, Pin.OUT)
stim_pin2 = Pin(3, Pin.OUT)

def activate_stimulus():
    stim_pin1.on()
    stim_pin2.off()

def deactivate_stimulus():
    stim_pin1.off()
    stim_pin2.off()

