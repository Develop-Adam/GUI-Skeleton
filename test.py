from pyModbusTCP.client import ModbusClient
import time

C = ModbusClient(host='localhost', port=12345, auto_open=True, debug=False)

REGISTER_ADDRESS = 0
REGISER_VALUE = 0

while True:
    if REGISER_VALUE >= 100:
        REGISER_VALUE = 0
    else:
        REGISER_VALUE = REGISER_VALUE + 1
        C.write_single_register(REGISTER_ADDRESS, REGISER_VALUE)
        REG = C.read_holding_registers(REGISTER_ADDRESS, 1)
        print(REG[0])
        time.sleep(1)
