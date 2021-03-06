import os
import time


def saveCSV(result, resultTime):
    import pandas as pd
    f = open("results/" + str(resultTime) + "/file.csv", "w+")
    f.close()
    df = pd.DataFrame(result)
    df.to_csv("results/" + str(resultTime) + "/file.csv")


def plotGraph(x, y, resultTime):
    import matplotlib.pyplot as p
    p.plot(x, y)
    p.xlabel("Time in Min")
    p.ylabel("Battery Level in %")
    p.title("Results")
    p.savefig("results/" + str(resultTime) + '/result.jpg')


def wait():
    input("Press enter key to continue : ")


# Make sure deps are present
def check_deps():
    try:
        from ppadb.client import Client as AdbClient
        import matplotlib.pyplot as p
        import pandas as pd
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
        os.system("pip install pandas")
        if check_deps():
            return True
        else:
            print("Unable to install dependencies")
            return False


os.system('cls')
print("===============\nWelcome to ADB Battery Tester\nBy github.com/geek0609\n===============\n\nDoing a few "
      "stuff to make sure we are good to go\n\nRestarting ADB \n")

# Kill and start ADB
os.system('adb kill-server')
os.system('adb start-server')
time.sleep(2)

# Only works on windows as of now
print ("\nDone..\n\nYour Operating System is identified to be: " + str(os.name))

if os.name != 'nt':
    print("Only Windows is supported in this version")
    exit()

print("Checking if you have deps: ", end="")
if install_dep():
    print ("OK")
else:
    print("Issues installing deps")
    exit()

from ppadb.client import Client as AdbClient

# Init AdbClient
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

print("Looking for device : ", end="")
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

print("\n\nChecks passed\n\n\nSettings up wireless ADB\nMake sure to enable Wireless ADB in Developer Settings "
      "on your device, make sure you"
      " are not using any VPN as it can affect connection, both this PC and the device is in same network"
      "and finally make sure both are connected at all times"
      "\nDO NOT DISCONNECT UNTIL INSTRUCTED")
wait()
print("\n\nTrying to start wireless ADB now\n\n")
# ADB on Port 5555
os.system("adb tcpip 5555")
# Wait 3 seconds so device can finish setup properly
time.sleep(3)
# grab local ip address to connect via adb wireless
print("\nGetting local IP so we can connect to it .....")
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

print("Local IP is found to be " + str(ip))
print("Now you can disconnect the cable, ADB will be connected via wireless ADB ")
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
results = [["Battery Level", "Time (Minutes)"]]
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
        results.append([int(level),int(mins)])
        mins += 1
        time.sleep(60)
    except:
        break

print(battery)
print(timePeriod)
print(results)
print("Device Disconneceted")
TimeNow = int(time.time())
os.mkdir("results/" + str(TimeNow))
saveCSV(results, TimeNow)
plotGraph(timePeriod, battery, TimeNow)
