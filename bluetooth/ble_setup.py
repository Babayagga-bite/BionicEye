import ubluetooth

class BionicEyeBLE:
    def __init__(self):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self.ble_irq)
        self.advertise()
        self.conn_handle = None

    def ble_irq(self, event, data):
        if event == 1:  # Central conectado
            self.conn_handle, _, _ = data
        elif event == 2:  # Central desconectado
            self.conn_handle = None
            self.advertise()

    def advertise(self):
        name = b'BionicEye'
        self.ble.gap_advertise(100, name)

    def send(self, data):
        if self.conn_handle is not None:
            self.ble.gatts_notify(self.conn_handle, 0, data)

ble = BionicEyeBLE()

