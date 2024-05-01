# boot.py -- run on boot-up
print("\n\n\n\nRunning boot.py...")

def do_connect():
    import network # type: ignore
    import time
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect('Jacopo iPhone', 'hellomads')
        while not sta_if.isconnected():
            print('Connecting...')
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())

do_connect()