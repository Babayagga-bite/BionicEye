import cv2

class Camera:
    def __init__(self, i2c_scl, i2c_sda, spi_sck, spi_mosi, spi_miso):
        self.cap = cv2.VideoCapture(0)  # Abre la cámara predeterminada

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        else:
            raise RuntimeError("Failed to capture image")

    def release(self):
        self.cap.release()
