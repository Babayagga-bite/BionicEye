import bluetooth

class BionicEyeBLE:
    def __init__(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connect(self, address):
        port = 1
        self.sock.connect((address, port))

    def send(self, data):
        self.sock.send(data)

    def receive(self, buffer_size=1024):
        return self.sock.recv(buffer_size)

    def close(self):
        self.sock.close()
