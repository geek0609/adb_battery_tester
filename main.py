import os


# Make sure deps are present
def check_deps():
    try:
        from ppadb.client import Client as AdbClient
        return True
    except ModuleNotFoundError:
        return False


def install_dep():
    if check_deps():
        return True
    else:
        # install deps if not there
        os.system('pip install -U pure-python-adb')
        if check_deps():
            return True
        else:
            print("Unable to install dependencies")
            exit()


# Only works on windows as of now
if os.name != 'nt':
    print("Only Windows is supported in this version")
    exit()

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
