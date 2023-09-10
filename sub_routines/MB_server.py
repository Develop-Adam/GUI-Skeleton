from time import sleep
from pyModbusTCP.server import ModbusServer
from data_storage import registers as r
from data_storage import coils as c
from data_storage import commands as cmd

# Constants
HOST = "127.0.0.1"
PORT = 12345
NUM_REGISTERS = 1000
NUM_COILS = 1000

# Create an instance of ModbusServer
server = ModbusServer(HOST, PORT, no_block=True)
data_bank = server.data_bank

# Initialize the initial states for coils and registers
coil_state = [False] * NUM_COILS
register_state = [0] * NUM_REGISTERS

def start_server():
    if cmd.SERVER_ON == True:
        # Associate DataBank with the server instance to access the coils and registers
        print("Start server...")
        server.start()
        print("Server is online")
        while True:
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
                    r.registers[i] = register_state[i]
            sleep(1)
            print(cmd.SERVER_ON)
    else:
        print("Server is offline")
        server.stop()
        print("Server is offline")