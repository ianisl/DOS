# -*- coding: utf-8 -*-
import pypot.dynamixel
from OSC import OSCServer, OSCClient, OSCMessage
from time import sleep
import types

def app():
    global dxlIO, server, client
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        raise IOError('No port available.')
    dxlIO = pypot.dynamixel.DxlIO(ports[0])
    availableIDs = dxlIO.scan()
    server = OSCServer(('0.0.0.0', 8000))
    for motorID in availableIDs:
        server.addMsgHandler('/motor/' + str(motorID), motorHandler) # Register OSC handlers for each found ID
    client = OSCClient()
    client.connect(('localhost', 8001))
    print 'Ready. Found ' + str(availableIDs) + ' ID(s)'
    while True:
        server.handle_request()
        sleep(0.01)

def motorHandler(addr, tags, data, source):
    # Ranges are given for AX-18 motors. For other models, see:
    # https://github.com/poppy-project/pypot/blob/master/pypot/dynamixel/conversion.py
    global dxlIO, client
    motorID = int(addr.split('/')[2])
    if (data[0] == 'factory_reset'):
       dxlIO.factory_reset()
    elif (data[0] == 'get_control_mode'):
        sendResponse(motorID, dxlIO.get_control_mode([motorID])[0])
    elif (data[0] == 'get_alarm_led'):
        sendResponse(motorID, dxlIO.get_alarm_LED([motorID])[0])
    elif (data[0] == 'get_alarm_shutdown'):
        sendResponse(motorID, dxlIO.get_alarm_shutdown([motorID])[0])
    elif (data[0] == 'get_angle_limit'):
        sendResponse(motorID, dxlIO.get_angle_limit([motorID])[0])
    elif (data[0] == 'get_compliance_margin'):
        sendResponse(motorID, dxlIO.get_compliance_margin([motorID])[0])
    elif (data[0] == 'get_compliance_slope'):
        sendResponse(motorID, dxlIO.get_compliance_slope([motorID])[0])
    elif (data[0] == 'get_drive_mode'):
        sendResponse(motorID, dxlIO.get_drive_mode([motorID])[0])
    elif (data[0] == 'get_firmware'):
        sendResponse(motorID, dxlIO.get_firmware([motorID])[0])
    elif (data[0] == 'get_goal_position'):
        sendResponse(motorID, dxlIO.get_goal_position([motorID])[0])
    elif (data[0] == 'get_goal_position_speed_load'):
        sendResponse(motorID, dxlIO.get_goal_position_speed_load([motorID])[0])
    elif (data[0] == 'get_highest_temperature_limit'):
        sendResponse(motorID, dxlIO.get_highest_temperature_limit([motorID])[0])
    elif (data[0] == 'get_max_torque'):
        sendResponse(motorID, dxlIO.get_max_torque([motorID])[0])
    elif (data[0] == 'get_moving_speed'):
        sendResponse(motorID, dxlIO.get_moving_speed([motorID])[0])
    elif (data[0] == 'get_present_load'):
        sendResponse(motorID, dxlIO.get_present_load([motorID])[0])
    elif (data[0] == 'get_present_position'):
        sendResponse(motorID, dxlIO.get_present_position([motorID])[0])
    elif (data[0] == 'get_present_position_speed_load'):
        sendResponse(motorID, dxlIO.get_present_position_speed_load([motorID])[0])
    elif (data[0] == 'get_present_speed'):
        sendResponse(motorID, dxlIO.get_present_speed([motorID])[0])
    elif (data[0] == 'get_present_temperature'):
        sendResponse(motorID, dxlIO.get_present_temperature([motorID])[0])
    elif (data[0] == 'get_present_voltage'):
        sendResponse(motorID, dxlIO.get_present_voltage([motorID])[0])
    elif (data[0] == 'get_return_delay_time'):
        sendResponse(motorID, dxlIO.get_return_delay_time([motorID])[0])
    elif (data[0] == 'get_torque_limit'):
        sendResponse(motorID, dxlIO.get_torque_limit([motorID])[0])
    elif (data[0] == 'get_voltage_limit'):
        sendResponse(motorID, dxlIO.get_voltage_limit([motorID])[0])
    elif (data[0] == 'is_led_on'):
        sendResponse(motorID, str(dxlIO.is_led_on([motorID])[0]))
    elif (data[0] == 'is_moving'):
        sendResponse(motorID, str(dxlIO.is_moving([motorID])[0]))
    elif (data[0] == 'is_torque_enabled'):
        sendResponse(motorID, str(dxlIO.is_torque_enabled([motorID])[0]))
    elif (data[0] == 'set_wheel_mode'):
        dxlIO.set_wheel_mode([motorID])
    elif (data[0] == 'set_joint_mode'):
        dxlIO.set_joint_mode([motorID])
    elif (data[0] == 'set_control_mode'):
        dxlIO.set_control_mode({motorID: data[1]}) # Range: {'wheel', 'joint'}.
    elif (data[0] == 'set_angle_limit'):
        dxlIO.set_angle_limit({motorID: [float(i) for i in data[1:]]}) # Range: [-150.0 ; 150.0]° (2 values)
    elif (data[0] == 'set_alarm_led'):
        dxlIO.set_alarm_LED({motorID: data[1:]}) # Range: {'None Error', 'Instruction Error', 'Overload Error', 'Checksum Error', 'Range Error', 'Overheating Error', 'Angle Limit Error', 'Input Voltage Error'} (up to 8 values)
    elif (data[0] == 'set_alarm_shutdown'):
        dxlIO.set_alarm_shutdown({motorID: data[1]}) # Range: {'None Error', 'Instruction Error', 'Overload Error', 'Checksum Error', 'Range Error', 'Overheating Error', 'Angle Limit Error', 'Input Voltage Error'} (up to 8 values)
    elif (data[0] == 'set_compliance_margin'):
        dxlIO.set_compliance_margin({motorID: [int(float(i)) for i in data[1:]]}) # Range [0, 254] (2 values)
    elif (data[0] == 'set_compliance_slope'):
        dxlIO.set_compliance_slope({motorID: [int(float(i)) for i in data[1:]]}) # Range [1, 254] (2 values)
    elif (data[0] == 'set_drive_mode'):
        dxlIO.set_drive_mode({motorID: data[1]}) # Doesn't seem to be working (at least for AX-18 motors)
    elif (data[0] == 'set_goal_position'):
        dxlIO.set_goal_position({motorID: float(data[1])}) # Range: [-150.0 ; 150.0]°
    elif (data[0] == 'set_goal_position_speed_load'):
        dxlIO.set_goal_position_speed_load({motorID: [float(i) for i in data[1:]]}) # Range: [-150.0 ; 150.0]° x [-681.984 ; 681.984] x [0.0 ; 100.0] (3 values)
    elif (data[0] == 'set_highest_temperature_limit'):
        dxlIO.set_highest_temperature_limit({motorID: int(float(data[1]))}) # Do not touch (as advised by the official doc)
    elif (data[0] == 'set_max_torque'):
        dxlIO.set_max_torque({motorID: float(data[1])}) # Range: [0.0 ; 100.0] where maximum corresponds to 1.8 N.m
    elif (data[0] == 'set_moving_speed'):
        dxlIO.set_moving_speed({motorID: float(data[1])}) # Range [-681.984 ; 681.984] where maximum corresponds to 582°/s (negative values only make sense in wheel mode)
    elif (data[0] == 'set_return_delay_time'):
        dxlIO.set_return_delay_time({motorID: int(float(data[1]))}) # Range [0 ; 500] microseconds
    elif (data[0] == 'set_torque_limit'):
        dxlIO.set_torque_limit({motorID: float(data[1])}) # Range [0.0 ; 100.0] where maximum corresponds to 1.8 N.m
    elif (data[0] == 'set_voltage_limit'):
        dxlIO.set_voltage_limit({motorID: [float(i) for i in data[1:]]}) # Range: [5.0 ; 25.0]V

def sendResponse(motorID, response):
    global client
    m = OSCMessage('/motor/' + str(motorID))
    m.append(response)
    client.send(m)

if __name__ == '__main__': app()