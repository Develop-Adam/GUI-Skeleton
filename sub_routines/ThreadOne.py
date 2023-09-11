from time import sleep
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from pyModbusTCP.server import ModbusServer
from data_storage import registers as r
from data_storage import coils as c
from data_storage import commands as cmd

# Constants
HOST = "127.0.0.1"
PORT = 12345
NUM_REGISTERS = 1000
NUM_COILS = 1000

server = ModbusServer(HOST, PORT, no_block=True)
data_bank = server.data_bank

coil_state = [False] * NUM_COILS
register_state = [0] * NUM_REGISTERS
#=======================================================================================================#
class ThreadRun(QObject):
    return_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.button_pressed = False
        self.running = False

    def start(self):
        if self.button_pressed == False:
            self.button_pressed = True

            print("Start server...")
            server.start()
            print("Server is online")
            while cmd.SERVER_ON == True:
                # Check if any coils have changed state and print the changes
                new_coil_state = data_bank.get_coils(0, NUM_COILS)
                for i in range(NUM_COILS):
                    if coil_state[i] != new_coil_state[i]:
                        coil_state[i] = new_coil_state[i]
                        print(f"Coil {i} has changed to {coil_state[i]}")
                # Check if any registers have changed state and print the changes
                new_register_state = data_bank.get_holding_registers(0, NUM_REGISTERS)
                for i in range(NUM_REGISTERS):
                    if register_state[i] != new_register_state[i]:
                        register_state[i] = new_register_state[i]
                        print(f"Register {i} has changed to {register_state[i]}")
                sleep(1)
                print(cmd.SERVER_ON)
        else:
            self.button_pressed = False
            print("Server is Shutting Down...")
            server.stop()
            print("Server is offline...")

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