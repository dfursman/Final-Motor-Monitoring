#!/usr/bin/env python3

import asyncio
from pymodbus.client import AsyncModbusSerialClient, ModbusSerialClient
import time

# Creates a global client that all of the aysnchronous functions are run on
client = None
async def create_client():
    global client 
    client = AsyncModbusSerialClient(
        port='/dev/ttyUSB0',
        baudrate=9600,
        timeout = 1
        )
    connected = await client.connect()

    if not connected:
        raise Exception("Modbus connection failed")


async def async_rtu_air():
    """Async RTU client test, airflow sensor."""

    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet
    result = await client.read_holding_registers(address=61,count=2,slave=1) 

    if not result.isError():
        flowvalue = result.registers[0] << 16 | result.registers[1] # Combining the high and low bits of the flowvalue
        return flowvalue / 90
    else:
        print("Error:", result)


async def async_rtu_powerA():
    """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
    result =  await client.read_holding_registers(address=278,count=2,slave=127)

    if not result.isError():
        power = result.registers[0]
        return power
    else:
        print("Error:", result)

async def async_rtu_powerB():
    """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
    result =  await client.read_holding_registers(address=280,count=2,slave=127)

    if not result.isError():
        power = result.registers[0]
        return power
    else:
        print("Error:", result)

async def async_rtu_powerC():
    """Async RTU client test, airflow sensor."""
        
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
    result =  await client.read_holding_registers(address=282,count=2,slave=127)

    if not result.isError():
        power = result.registers[0]
        return power
    else:
        print("Error:", result)

async def async_rtu_voltageA():
     """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
     result =  await client.read_holding_registers(address=256,count=2,slave=127)

     if not result.isError():
         voltage = result.registers[0]
         return voltage * .1
     else:
         print("Error:", result)

async def async_rtu_voltageB():
     """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
     result =  await client.read_holding_registers(address=258,count=2,slave=127)

     if not result.isError():
         voltage = result.registers[0]
         return voltage * .1
     else:
         print("Error:", result)


async def async_rtu_voltageC():
     """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
     result =  await client.read_holding_registers(address=260,count=2,slave=127)

     if not result.isError():
         voltage = result.registers[0]
         return voltage * .1
     else:
         print("Error:", result)



async def async_rtu_currentA():
     """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
     result =  await client.read_holding_registers(address=272,count=2,slave=127)

     if not result.isError():
         current = result.registers[0]
         return current / 1000
     else:
         print("Error:", result)


async def async_rtu_currentB():
     """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
     result =  await client.read_holding_registers(address=274,count=2,slave=127)

     if not result.isError():
         current = result.registers[0]
         return current/ 1000
     else:
         print("Error:", result)

async def async_rtu_currentC():
     """Async RTU client test, airflow sensor."""
    
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
     result =  await client.read_holding_registers(address=276,count=2,slave=127)

     if not result.isError():
         current = result.registers[0]
         return current/ 1000
     else:
         print("Error:", result)

async def powerFactor():
    """Async RTU client test, airflow sensor."""
        
    # The address is given in the data sheet
    # The count refers to the number of registers that needs to be read, usually it is 2
    # The slave id is specified in the data sheet, default it is the last two of the serial number, but it can be set to whatever you want
    # For sensors reading from the same sensor, the slave id must be the same
    result =  await client.read_holding_registers(address=315,count=2,slave=127)

    if not result.isError():
        powFac = result.registers[0]
        powerF = powFac * 0.001
        return powerF
    else:
        print("Error:", result)

# Sets the dimensions of the theoretical tube
# Specifies length, width, shape, flow units, radius, and and length units (Metric or Imperial)
def setTube():
    client = ModbusSerialClient(
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout = 1
    )
    client.connect()
    client.write_register(address = 57, value = 152, slave = 1)
    time.sleep(1)
    client.write_register(address = 58, value = 61, slave = 1)
    time.sleep(1)
    client.write_register(address = 93, value = 0, slave = 1)
    time.sleep(1)
    client.write_register(address = 59, value = 1, slave = 1)

    client.write_register(address = 63, value = 1, slave = 1)
    time.sleep(1)
    client.write_register(address = 92, value = 1, slave = 1)
   
    client.close()

setTube()
time.sleep(2)

