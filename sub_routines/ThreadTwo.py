from PyQt5.QtCore import QObject, QThread, pyqtSignal
from data_storage import data as d
from pyModbusTCP.client import ModbusClient
import time

C = ModbusClient(host='localhost', port=12345, auto_open=True, debug=False)
#=======================================================================================================#
class ThreadRun(QObject):
    return_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.button_pressed = True
        self.running = True

    def start(self):
        while True:
            REGISTER_ADDRESS = 0
            d.battery_level = C.read_holding_registers(REGISTER_ADDRESS, 1)[0]
            self.return_signal.emit(self.button_pressed)
            time.sleep(1)

#=======================================================================================================#
class ThreadStart(QThread):
    return_signal = pyqtSignal(bool)

    def __init__(self, commands_instance):
        super().__init__()
        self.commands_instance = commands_instance
        self.commands_instance.return_signal.connect(self.emit_signal)

    def run(self):
        self.commands_instance.start()

    def emit_signal(self, status):
        self.return_signal.emit(status)