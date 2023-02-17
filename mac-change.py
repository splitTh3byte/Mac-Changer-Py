import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", '--interface', dest="interface", help="Interface to change MAC Adress")
    parser.add_option("-m", '--mac', dest="new_mac", help="New Mac")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] PLease specify an interface , use --help for more info")
    elif not options.new_mac:
        parser.error("[-] PLease specify a  new mac , use --help for more info")

    return options


def get_currentMac(interface):
    output = subprocess.check_output(["ifconfig", interface])

    matchObj = re.search(r"\w+\:\w+\:\w+\:\w+\:\w+\:\w+", str(output))
    if matchObj:
        return matchObj.group(0)
    else:
        return "[-] I can`t read the mac adress"


def change_mac(interface, new_mac):
    print("[+] Changing the mac for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

options = get_arguments()
current_mac = get_currentMac(options.interface)
print("Current MAC is " + current_mac)
change_mac(options.interface,options.new_mac)
current_mac = get_currentMac(options.interface)
if current_mac == options.new_mac:
    print("[i] The MAC Adress was succesfully changed !")
else:
    print("[i] I can`t change the MAC Adress !")

