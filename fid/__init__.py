import cv2
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pathlib import Path
from datetime import datetime

APP_PATH = Path(__file__).parent.parent.absolute()

class System:
    camera = None
    modbus = None
    url = None

    def set_modbus_client(self, host: str = '127.0.0.1', port: int = 502):
        self.modbus = ModbusClient(host=host, port=port)
        self.modbus.connect()

    def connect_camera(self, url):
        self.url = url
        self.camera = cv2.VideoCapture(url, cv2.CAP_DSHOW)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 5472)  # 5472
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 3648)  # 3648

    def send_signal_to_controller(self, address: int, value: int, unit: int):
        self.modbus.write_coil(address, value, unit=unit)

    def save_image(self, image, start_time: datetime, defect: bool):
        start_time = start_time.strftime('%Y-%m-%d %H-%M-%S.%f')
        start_time = start_time.split(' ')
        folder = start_time[0]
        filename = start_time[1]
        Path(f'{APP_PATH}/images package').mkdir(parents=True, exist_ok=True)
        Path(f'{APP_PATH}/images package/normal/{folder}').mkdir(parents=True, exist_ok=True)
        Path(f'{APP_PATH}/images package/defect/{folder}').mkdir(parents=True, exist_ok=True)
        if defect:
            cv2.imwrite(f'{APP_PATH}/images package/defect/{folder}/{filename}.jpg', image)
            return f'images package/defect/{folder}/{filename}.jpg'
        else:
            cv2.imwrite(f'{APP_PATH}/images package/normal/{folder}/{filename}.jpg', image)
            return f'images package/normal/{folder}/{filename}.jpg'

    def get_image(self):
        ret, image = self.camera.read()
        if ret:
            return image
        else:
            self.connect_camera(self.url)
