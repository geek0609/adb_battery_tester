import os
import time


def plotGraph(x, y):
    import matplotlib.pyplot as p
    p.plot(x, y)
    p.xlabel("Time")
    p.ylabel("Battery Level in %")
    p.title("Results")
    p.show()

def wait():
    input("Press enter key to continue : ")


# Make sure deps are present
def check_deps():
    try:
        from ppadb.client import Client as AdbClient
        import matplotlib.pyplot as p
        return True
    except ModuleNotFoundError:
        return False


def install_dep():
    if check_deps():
        return True
    else:
        # install deps if not there
        os.system('pip install -U pure-python-adb')
        os.system("pip install matplotlib")
        if check_deps():
            return True
        else:
            print("Unable to install dependencies")
            exit()


# Only works on windows as of now
if os.name != 'nt':
    print("Only Windows is supported in this version")
    exit()

# Kill and start ADB
os.system('adb kill-server')
os.system('adb start-server')

os.system('cls')
print("===============\nWelcome to ADB Battery Tester\nBy github.com/geek0609\n===============")

install_dep()

from ppadb.client import Client as AdbClient

print("\nDoing few checks\n")

# Init AdbClient
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

print("\nLooking for device : ", end="")
# Check if device is connected
if len(devices) == 0:
    print("Device not recognized\nExiting")
    exit()
else:
    print("Device is recognized")

# device refers to the device which we will be tracking now
device = devices[0]

print("Looking for how many devices connected : " + str(len(devices)))

# More than 1 device connected may raise issues
if len(devices) > 1:
    print("Please connect only 1 device")
    exit()

print("Settings up wireless ADB\nMake sure to enable Wireless ADB in Developer Settings on your device\nDO NOT "
      "DISCONNECT UNTIL INSTRUCTED")
wait()
print("Trying to start wireless ADB ")
# ADB on Port 5555
os.system("adb tcpip 5555")
# Wait 3 seconds so device can finish setup properly
time.sleep(3)
# grab local ip address to connect via adb wireless
ifconfig = device.shell("ifconfig wlan0")

# finding IP from that mess
for i in range(len(ifconfig) - 10):
    char = []
    for k in range(10):
        n = ifconfig[i + k]
        char += n
    if char == ['i', 'n', 'e', 't', ' ', 'a', 'd', 'd', 'r', ':']:
        break
ip = ""
i = i + 10
while n != " ":
    n = ifconfig[i]
    ip = ip + n
    i = i + 1

print(ip)
print("Now you can disconnect the cable, ADB will be connected wirelessly")
wait()
# Switch over to wireless ADB
os.system("adb connect " + str(ip))
time.sleep(2)
# Wait for it to connect
devices = client.devices()
# Update devices
device = devices[0]
battery = []
timePeriod = []
mins = 0
# infinite loop with try catch to break it
while True:
    try:
        a = device.shell("dumpsys battery | grep level")
        for i in range(len(a) - 8):
            char = []
            for k in range(8):
                n = a[i + k]
                char += n
            if char == [' ', ' ', 'l', 'e', 'v', 'e', 'l', ':']:
                break
        level = ""
        i = i + 8
        while n != "\n":
            n = a[i]
            level = level + n
            i = i + 1
        level = level.strip(" ")
        level = level.strip("\n")
        print("In " + str(mins) + " minutes, Battery is ", end="")
        print(str(level) + "%")
        battery.append(int(level))
        timePeriod.append(mins)
        mins += 1
        time.sleep(60)
    except:
        break

print(battery)
print(timePeriod)
print("Device Disconneceted")
plotGraph(timePeriod, battery)
