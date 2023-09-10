from PyQt5.QtCore import QObject, QThread, pyqtSignal
from data_storage import data as d

#=======================================================================================================#
class ThreadRun(QObject):
    return_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.button_pressed = True
        self.running = True

    def start(self):
        d.battery_level = d.battery_level + 1
        self.return_signal.emit(self.button_pressed)

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