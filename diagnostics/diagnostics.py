#Modules for access the system and view the diagnostics
import psutil
import os
import clr  # package pythonnet, not clr

#List for save the temperature
temp = list()
openhardwaremonitor_sensortypes = [
    "Voltage",
    "Clock",
    "Temperatures",
    "Load",
    "Fan",
    "Flow",
    "Control",
    "Level",
    "Factor",
    "Power",
    "Data",
    "SmallData",
]

#OpenHardwareMonitor Library
def initialize_openhardwaremonitor():
    file = os.path.join(os.path.dirname(__file__),'..','OpenHardwareMonitorLib.dll') #Path of OpenHardwareMonitorLib.dll

    clr.AddReference(file) #Add OpenHardwareMonitorLib.dll

    from OpenHardwareMonitor import Hardware #Import OpenHardwareMonitor

    #Initialize OpenHardwareMonitor
    handle = Hardware.Computer()
    handle.MainboardEnabled = True #Enable Mainboard for get Temperature
    handle.CPUEnabled = True        #Enable CPU for get Temperature
    handle.GPUEnabled = True
    handle.Open()
    return handle

#Fetch data from OpenHardwareMonitor
def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)

        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)

#Parse data for get CPU Core 2 Temperature
def parse_sensor(sensor):
    if sensor.Value is not None:
        if str(sensor.SensorType.Temperature) == "Temperature":
            temp.append(sensor.Value)
        
HardwareHandle = initialize_openhardwaremonitor()

class Diagnostics:
    def __init__(self) -> None:
        pass

    def ram(self) -> int:
        ram = psutil.virtual_memory()
        return round(ram.percent)

    def cpu(self) -> int:
        cpu = psutil.cpu_percent(0)
        return round(cpu)

    def space(self) -> int:
        disk = psutil.disk_usage('/')
        return round(disk.percent)

    def temperature(self) -> any:
        fetch_stats(HardwareHandle)
        return round(temp[0])

if __name__ == '__main__':
    diagnostics = Diagnostics()
    print(f"""RAM: {diagnostics.ram()}
CPU: {diagnostics.cpu()}
Space: {diagnostics.space()}
Temperature: {diagnostics.temperature()}""")