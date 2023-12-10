import clr
import time
import colorama as col
# import os

from gooey import Gooey, GooeyParser
# from message import display_message

from sys import stdout
from os import getcwd, system
from colorama import init
from pygame import mixer

cmd = 'mode 75,30'
system(cmd)

init(autoreset=True)
clear = lambda: system('cls')
clear()
# print(col.Fore.RED + 'some red text')

# import itertools
# import threading

hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']

def initialize_openhardwaremonitor():
    file = rf'{getcwd()}\OpenHardwareMonitorLib.dll'
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle

def fetch_stats(handle):
    stat_list = []
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            if parse_sensor(sensor):
                stat_list.append(parse_sensor(sensor))
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                if parse_sensor(subsensor):
                    stat_list.append(parse_sensor(subsensor))
    return stat_list

def parse_sensor(sensor):
    if sensor.Value:
        if str(sensor.SensorType) == 'Temperature' and hwtypes[sensor.Hardware.HardwareType] != 'SuperIO':
            if + sensor.Value > 70:
                sensor_val = col.Fore.RED + str(sensor.Value) + col.Style.RESET_ALL
            elif sensor.Value > 60:
                sensor_val = col.Fore.YELLOW + str(sensor.Value) + col.Style.RESET_ALL
            elif sensor.Value > 50:
                sensor_val = col.Fore.GREEN + str(sensor.Value) + col.Style.RESET_ALL
            else:
                sensor_val = sensor.Value
            pass
            if hwtypes[sensor.Hardware.HardwareType] == 'CPU':
                result = u'{} {} Temperature Sensor #{} {} - {}\u00B0C'\
                        .format(col.Fore.CYAN + hwtypes[sensor.Hardware.HardwareType] + col.Style.RESET_ALL, 
                                sensor.Hardware.Name, sensor.Index, 
                                sensor.Name, sensor_val
                    )
            if hwtypes[sensor.Hardware.HardwareType] == 'GpuAti':
                result = u'{} {} Temperature Sensor #{} {} - {}\u00B0C'\
                        .format(col.Fore.GREEN + hwtypes[sensor.Hardware.HardwareType] + col.Style.RESET_ALL, 
                                sensor.Hardware.Name, sensor.Index, 
                                sensor.Name, sensor_val
                    )
            if hwtypes[sensor.Hardware.HardwareType] == 'HDD':
                result = u'{} {} Temperature Sensor #{} {} - {}\u00B0C'\
                        .format(hwtypes[sensor.Hardware.HardwareType] + col.Style.RESET_ALL, 
                                sensor.Hardware.Name, sensor.Index, 
                                sensor.Name, sensor_val
                    )
            return result

def slow_prin(str_1):
    for letter in (str_1.split(' ')):
        stdout.write(letter + ' ')
        stdout.flush()
        time.sleep(0.01)


def color_print(text, color_count):
    if color_count % 7 == 0:
        print(col.Fore.GREEN + text)
    elif color_count % 6 == 0:
        print(col.Fore.RED + text)
    elif color_count % 5 == 0:
        print(col.Fore.YELLOW + text)
    elif color_count % 4 == 0:
        print(col.Fore.BLUE + text)
    elif color_count % 3 == 0:
        print(col.Fore.MAGENTA + text)
    elif color_count % 2 == 0:
        print(col.Fore.CYAN + text)
    elif color_count % 1 == 0:
        print(col.Fore.WHITE + text)
    # RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE

if __name__ == "__main__":
    extra_text = '''
    ███████╗██╗  ██╗████████╗██████╗  █████╗ ___________________    
    ██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗___________________    
    █████╗   ╚███╔╝    ██║   ██████╔╝███████║___________________    
    ██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║___________________    
    ███████╗██╔╝ ██╗   ██║   ██║  ██║██║  ██║___________________    
    ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝___________________    

    ██████╗ ██████╗  ██████╗  ██████╗ ██████╗  █████╗ ███╗   ███╗
    ██╔══██╗██╔══██╗██╔═══██╗██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
    ██████╔╝██████╔╝██║   ██║██║  ███╗██████╔╝███████║██╔████╔██║
    ██╔═══╝ ██╔══██╗██║   ██║██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
    ██║     ██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝

    ██████╗ ██████╗  █████╗ ____________________________________
    ╚════██╗╚════██╗██╔══██╗____________________________________
    █████╔╝ █████╔╝╚█████╔╝ ____________________________________
    ██╔═══╝ ██╔═══╝ ██╔══██╗____________________________________
    ███████╗███████╗╚█████╔╝____________________________________
    ╚══════╝╚══════╝ ╚════╝ ____________________________________
    ''' + col.Style.RESET_ALL
    HardwareHandle = initialize_openhardwaremonitor()
    # pygame.init()
    mixer.init()

    sound = mixer.Sound(r'D:\Python\cpu_monitor\bandit_music.mp3')
    

    # time.sleep(5)
    sound_count = -1
    color_count = 0
    while True:
        sound_count += 1
        result_str = ''
        if sound_count == 0:
            sound.play()
            time.sleep(1)
            slow_prin(extra_text)

        for i in fetch_stats(HardwareHandle):
            result_str += i + '\n'
            
        clear()
        # print("OpenHardwareMonitor:")
        color_count += 1
        color_print(extra_text, color_count)
        stdout.write('\r' + result_str)
        stdout.flush()
        time.sleep(1)

#---------------------------------------------------



# import itertools
# import threading
# import time
# import sys

# done = False
# #here is the animation
# def animate():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\rDone!     ')

# t = threading.Thread(target=animate)
# t.start()

# #long process here
# time.sleep(10)
# done = True
