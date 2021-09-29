from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from system import System

if __name__ == '__main__':
    # system = System()
    # system.set_modbus_client(host='10.162.0.224', port=502)
    # system.send_signal_to_controller(6, True, 1)
    modbus = ModbusClient(host='10.162.0.224', port=502)
    print(modbus.state)
    print(modbus.is_socket_open())
    modbus.connect()
    modbus.write_coil(6, True)
    # system.modbus.connect()
    # system.connect_camera(url='rtsp://univer:Univer123@192.168.48.248:554/Streaming/Channels/201',
    #                       url2='rtsp://univer:Univer123@192.168.48.248:554/Streaming/Channels/101')
    # while True:
    #     system.identify_ice_cream_defect()