import bluetooth
from alpha_1s import Command
import time


def main():
    #msg = message(b'\x18', [b'\x00'])
    msg = message(b'\x26', [b'\x01', b'\x20'])
    print(msg)
    bd_addr = discover()
    print(bd_addr)
    #services = bluetooth.find_service(address=bd_addr)
    #if len(services) > 0:
    #    print("Found {} services on {}.".format(len(services), bd_addr))
    #else:
    #    print("No services found.")

    if bd_addr:
        bd_addr_str = str(bd_addr, 'utf-8')
        print(bd_addr_str)
        for services in bluetooth.find_service(address = bd_addr_str):
            print("\t Name:           %s" % (services["name"]))
            print("\t Description:    %s" % (services["description"]))
            print("\t Protocol:       %s" % (services["protocol"]))
            print("\t Provider:       %s" % (services["provider"]))
            print("\t Port:           %s" % (services["port"]))
            print("\t service-classes %s" % (services["service-classes"]))
            print("\t profiles        %s" % (services["profiles"]))
            print("\t Service id:  %s" % (services["service-id"]))
            print("")
        port = 6
        #port = 3
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((bd_addr_str, port))
        # while(True):
        #     try:
        #         sock.connect((bd_addr_str, port))
        #     except:
        #         print("Could not connect; Retrying in 5s...")
        #         time.sleep(5)
        print('Connected')
        sock.settimeout(60.0)
        sock.send(msg)
        print('Sent data')
        response = sock.recv(1024)
        print(Command().get(response))
        sock.close()


def message(command, parameters):
    header = b'\xFB\xBF'
    end = b'\xED'
    parameter = b''.join(parameters)
    # len(header + length + command +parameters + check)
    length = bytes([len(parameters) + 5])
    data = [command, length]
    data.extend(parameters)
    check = bytes([sum(ord(x) for x in data)])
    return header+length+command+parameter+check+end


def discover():
    print("searching ...")
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        print(name)
        if name == "Jimu_3962":
            print("got it")
            return addr


if __name__ == '__main__':
    main()
