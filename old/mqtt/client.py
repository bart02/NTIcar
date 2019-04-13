import paho.mqtt.client as mqtt
from graph import find_route
from solve_povor import solve

mapp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
second = False


def on_connect(_client, userdata, flags, rc):
    print ("Connected with result code "+str(rc))

    client.subscribe("/fromserver/car/7")
    client.publish('/toserver/car/7', 'h', 2)


def on_message(_client, userdata, msg):
    global mapp, second
    m = msg.payload
    print(m)
    # if 'l' in m.decode():
    #     print('y')
    if 'l' not in m.decode():
        lastmap = mapp.copy()
        mapp = []
        for e in range(0, len(msg.payload), 2):
            mapp.append([msg.payload[e], msg.payload[e+1]])
        if len(mapp) > len(lastmap):
            mapp = lastmap
    else:
        print(mapp)
        s = m.decode().split('l')
        s, e = list(map(int, s[:2]))
        r = find_route(mapp, s, e)
        t = solve(r)
        print(r, t)
        client.disconnect()


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect('192.168.1.190', 1883, 60)

client.loop_start()

while True:
    pass
